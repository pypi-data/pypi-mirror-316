import moapy.auto_convert as auto_convert
import json
import sys
import ast
import jsonref
import copy
import types
import importlib
from pydantic import Field
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from version import moapy_version
from moapy.api_url import API_PYTHON_EXECUTOR
from moapy.auto_convert import auto_schema, MBaseModel, ConfigDict

class AutoConvertFinder(ast.NodeVisitor):
    def __init__(self):
        self.auto_convert_funcs = []

    def visit_FunctionDef(self, node):
        # 데코레이터가 auto_schema인지 확인
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == "auto_schema":
                self.auto_convert_funcs.append(node.name)
            elif (
                isinstance(decorator, ast.Call)
                and isinstance(decorator.func, ast.Name)
                and decorator.func.id == "auto_schema"
            ):
                # auto_schema가 호출된 경우도 확인
                self.auto_convert_funcs.append(node.name)
        self.generic_visit(node)

def resolve_refs_and_merge(json_data):
    # 원본 데이터를 깊은 복사하여 변경되지 않도록 함
    resolved_json = copy.deepcopy(json_data)

    # jsonref로 참조를 해소함
    resolved_json = jsonref.JsonRef.replace_refs(resolved_json)

    # 원본 데이터를 순회하면서 $ref가 있던 곳의 추가 정보를 복사하여 병합
    def merge_refs(original, resolved):
        if isinstance(original, dict):
            for key, value in original.items():
                if isinstance(value, dict):
                    # $ref가 있는 경우
                    if "$ref" in value:
                        # resolved에서 병합
                        resolved_value = resolved.get(key, {})
                        # 모든 key-value 쌍을 병합
                        resolved[key] = {**resolved_value, **value}
                        # original에서 키를 가져와 병합
                        for k, v in original[key].items():
                            if k != "$ref":  # $ref는 제외
                                resolved[key][k] = v

                        # default가 있는 경우 특별 처리
                        if "default" in original[key] and isinstance(
                            original[key]["default"], dict
                        ):
                            # original의 default에서 value와 unit을 가져와 병합
                            default_value = original[key]["default"].get("value")
                            default_unit = original[key]["default"].get("unit")

                            if default_value is not None:
                                # value를 properties에 추가
                                resolved[key]["properties"]["value"]["default"] = (
                                    default_value
                                )

                            if default_unit is not None:
                                # unit을 properties에 추가
                                resolved[key]["properties"]["unit"]["default"] = (
                                    default_unit
                                )

                        resolved[key].pop("$ref", None)  # $ref 제거
                    else:
                        merge_refs(value, resolved.get(key, {}))
        elif isinstance(original, list):
            for index, item in enumerate(original):
                merge_refs(item, resolved[index])

    merge_refs(json_data, resolved_json)
    return resolved_json

def extract_auto_schema_functions(code: str):
    """주어진 코드에서 auto_schema 데코레이터가 붙은 함수 이름을 추출합니다."""
    try:
        parsed_code = ast.parse(code)  # 코드 파싱
        finder = AutoConvertFinder()  # 탐색기 인스턴스 생성
        finder.visit(parsed_code)  # AST 방문
        return finder.auto_convert_funcs  # 찾은 함수 이름 반환
    except Exception as e:
        print(f"Error parsing code: {e}")
        return []

def generate_openapi_spec(router, resolve_refs=True):
    temp_app = FastAPI(
        title="moapy", description="Schema for moapy", version=moapy_version
    )
    temp_app.include_router(router)
    openapi_spec = get_openapi(
        title=temp_app.title,
        version=temp_app.version,
        openapi_version=temp_app.openapi_version,
        description=temp_app.description,
        routes=temp_app.routes,
        servers=[
            {"url": API_PYTHON_EXECUTOR},
        ],
    )

    def handle_composite_keys(schema, key):
        if key in schema:
            for item in schema[key]:
                if "$ref" in item:
                    schema.update(item)
            del schema[key]

    def apply_camel_case_to_schema_keys(schema):
        if isinstance(schema, dict):
            return {auto_convert.to_camel(k): v for k, v in schema.items()}
        return schema

    def process_schema(schema):
        if isinstance(schema, dict):
            for key, value in list(schema.items()):
                if key == "schema":  # "schema" 키 내부의 Key만 변환
                    schema[key] = apply_camel_case_to_schema_keys(value)
                elif key in {"allOf"}:
                    handle_composite_keys(schema, key)
                else:
                    process_schema(value)
        elif isinstance(schema, list):
            for item in schema:
                process_schema(item)

    process_schema(openapi_spec)
    openapi_spec_ref = resolve_refs_and_merge(openapi_spec) if resolve_refs else openapi_spec

    return openapi_spec_ref

class InputCode(MBaseModel):
    script_code: str = Field(default_factory=str, title="Python Script Code", description="Python script code to generate OpenAPI spec")

    model_config = ConfigDict(title="Python Script Code Input")

@auto_schema(title="python to openapi spec", description="This tool generates OpenAPI spec from Python code")
def generate_openapi_spec_from_code(inp: InputCode) -> str:
    """
    Python 코드 문자열에서 정의된 함수들에 대해 OpenAPI 스펙을 생성합니다.

    매개변수:
        script_code (str): Python 코드 문자열
        app (FastAPI): FastAPI 애플리케이션 인스턴스
        resolve_refs (bool): 스키마에서 참조를 해석할지 여부
    """
    if not inp.script_code:
        raise ValueError("입력된 코드가 비어 있습니다.")
    app = FastAPI()

    module_name = "dynamic_module"
    dynamic_module = types.ModuleType(module_name)
    # 동적 모듈을 sys.modules에 등록
    sys.modules[module_name] = dynamic_module
    # 이제 importlib.import_module 사용 가능
    module = importlib.import_module(module_name)
    # 코드 실행 후 동적 모듈에 추가
    exec(inp.script_code, dynamic_module.__dict__)
    # 코드에서 함수들 추출
    functions = extract_auto_schema_functions(inp.script_code)

    if not functions:
        raise ValueError("입력된 코드에서 호출 가능한 함수가 없습니다.")

    # 각 함수에 대해 OpenAPI 스펙 생성
    for func in functions:
        # auto_convert.get_router_for_module()가 동적으로 불러온 함수에도 작동한다고 가정
        full_function_name = module_name + func
        router = auto_convert.get_router_for_module(full_function_name)
        app.include_router(router)

        return generate_openapi_spec(router)

if __name__ == "__main__":
    # 예시로 사용할 코드 (스크립트 코드 자체를 문자열로 입력)
    script_code = """
from pydantic import Field, ConfigDict
from moapy.auto_convert import auto_schema, MBaseModel
from moapy.designers_guide.resource.report_form import ReportForm
from moapy.designers_guide.func_general import DG_Result_Reports

class Inputdata(MBaseModel):
    wind_speed: float = Field(default=70, title="Wind Speed", description="Wind speed in ft/s")
    kd: str = Field(default="Buildings-Main wind force resisting system",
                    title="Wind Directionality Factor,Kd",
                    description="Wind Directionality Factor,Kd",
                    enum=["Buildings-Main wind force resisting system", "Buildings-Components and Cladding", "Arched roofs", "Circle dones", "Chimneys,tanks, and similar Structures-Square","Chimneys,tanks, and similar Structures-Hexagonal","Chimneys,tanks, and similar Structures-Octagonal","Chimneys,tanks, and similar Structures-Round",
                        "Solid freestanding walls, roof top equipment, and solid freestanding and attached signs", "Open Signs and single-plane open frames", "Open signs and single-plane open frames", "Trussed towers - Triangular, square, or rectangular", "Trussed towers - All other cross sections"])

    exposure: str = Field(default="C", title="Exposure", description="Exposure", enum=["C", "B", "D"])
    topo_K1_HLh: str = Field(default="0.3", title="Topographic Factor K1 Multiplier", description="Topographic Factor K1 Multiplier", enum=["0.20", "0.25", "0.30", "0.35", "0.40", "0.45", "0.50"])
    topo_K1_multi: str = Field(default="2D Ridge", title="Topographic Factor K1 Multiplier", description="Topographic Factor K1 Multiplier", enum=["2D Ridge", "2D Escarpment", "3D Axisymmetrical Hill"])

    topo_K2_xLh: str = Field(default="0.0", title="Topographic Factor K2 Multiplier", description="Topographic Factor K2 Multiplier", enum=["0.00", "0.50", "1.00", "1.50", "2.00", "2.50", "3.00", "3.50", "4.00"])
    topo_K2_multi: str = Field(default="2D Escarpment", title="Topographic Factor K2 Multiplier", description="Topographic Factor K2 Multiplier", enum=["2D Escarpment", "All Other Cases"])

    topo_K3_xLh: str = Field(default="1.00", title="Topographic Factor K3 Multiplier", description="Topographic Factor K3 Multiplier", enum=["0.00", "0.10", "0.20", "0.30", "0.40", "0.50", "0.60", "0.70", "0.80", "0.90", "1.00", "1.50", "2.00"])
    topo_K3_multi: str = Field(default="2D Ridge", title="Topographic Factor K3 Multiplier", description="Topographic Factor K3 Multiplier", enum=["2D Escarpment", "All Other Cases"])

    sea_level: float = Field(default=1, title="Sea Level", description="Sea Level in ft", enum=["<0", "0", "1000", "2000", "3000", "4000", "5000", "6000", ">6000"])

    velocity_pressure: float = Field(default=0, title="Velocity Pressure", description="Velocity Pressure in Pa")

    model_config = ConfigDict(
        title="Model Configuration",
        description="Configuration for the model analysis"
    )

class OutputData(MBaseModel):
    result: str = Field(default="TGC", title="result_title", description="result_description")

    model_config = ConfigDict(title="TGC 2024 Output Data Test")

def calculate_topo_K1(topo_K1_HLh: str, topo_K1_multi: str) -> float:
    if topo_K1_HLh == "0.20":
        if topo_K1_multi == "2D Ridge":
            return 0.29
        elif topo_K1_multi == "2D Escarpment":
            return 0.17
        else:
            return 0.21
    elif topo_K1_HLh == "0.25":
        if topo_K1_multi == "2D Ridge":
            return 0.36
        elif topo_K1_multi == "2D Escarpment":
            return 0.21
        else:
            return 0.26
    elif topo_K1_HLh == "0.30":
        if topo_K1_multi == "2D Ridge":
            return 0.43
        elif topo_K1_multi == "2D Escarpment":
            return 0.26
        else:
            return 0.32
    elif topo_K1_HLh == "0.35":
        if topo_K1_multi == "2D Ridge":
            return 0.51
        elif topo_K1_multi == "2D Escarpment":
            return 0.30
        else:
            return 0.37
    elif topo_K1_HLh == "0.40":
        if topo_K1_multi == "2D Ridge":
            return 0.58
        elif topo_K1_multi == "2D Escarpment":
            return 0.34
        else:
            return 0.42
    elif topo_K1_HLh == "0.45":
        if topo_K1_multi == "2D Ridge":
            return 0.65
        elif topo_K1_multi == "2D Escarpment":
            return 0.38
        else:
            return 0.47
    elif topo_K1_HLh == "0.50":
        if topo_K1_multi == "2D Ridge":
            return 0.72
        elif topo_K1_multi == "2D Escarpment":
            return 0.43
        else:
            return 0.53
    return None

def calculate_topo_K2(topo_K2_xLh: str, topo_K2_multi: str) -> float:
    if topo_K2_xLh == "0.00":
        if topo_K2_multi == "2D Escarpment":
            return 1.00
        else:
            return 1.00
    elif topo_K2_xLh == "0.50":
        if topo_K2_multi == "2D Escarpment":
            return 0.88
        else:
            return 0.67
    elif topo_K2_xLh == "1.00":
        if topo_K2_multi == "2D Escarpment":
            return 0.75
        else:
            return 0.33
    elif topo_K2_xLh == "1.50":
        if topo_K2_multi == "2D Escarpment":
            return 0.63
        else:
            return 0.00
    elif topo_K2_xLh == "2.00":
        if topo_K2_multi == "2D Escarpment":
            return 0.50
        else:
            return 0.00
    elif topo_K2_xLh == "2.50":
        if topo_K2_multi == "2D Escarpment":
            return 0.38
        else:
            return 0.00
    elif topo_K2_xLh == "3.00":
        if topo_K2_multi == "2D Escarpment":
            return 0.25
        else:
            return 0.00
    elif topo_K2_xLh == "3.50":
        if topo_K2_multi == "2D Escarpment":
            return 0.13
        else:
            return 0.00
    elif topo_K2_xLh == "4.00":
        if topo_K2_multi == "2D Escarpment":
            return 0.00
        else:
            return 0.00
    return None

@auto_schema(
    title="Wind load pressure calculation",
    description=(
        "This tool calculates the wind load pressure on a structure"
    )
)
def wind_load_pressure_calculator(input_data: Inputdata) -> DG_Result_Reports:
    k1 = calculate_topo_K1(input_data.topo_K1_HLh, input_data.topo_K1_multi)
    k2 = calculate_topo_K2(input_data.topo_K2_xLh, input_data.topo_K2_multi)
    value = 5.0
    result = ReportForm(result=value)
    results = {
        "result": [
            [
                result.to_dict()
            ]
        ]
    }
    return DG_Result_Reports(res_report=results)


if __name__ == "__main__":
    res = wind_load_pressure_calculator(Inputdata())
    print(res)
    """

    print(generate_openapi_spec_from_code(script_code))
    
    # # Example usage
    # app = FastAPI()
    # directory = "./moapy/wgsd"
    # # directory = "./moapy/dgnengine"
    # # directory = "./moapy/plugins"
    # # directory = "./moapy/project/"
    # # auto_convert_functions = find_all_auto_convert_funcs(directory)
    # auto_convert_functions = {".\\moapy\\dgnengine\\eurocode2_beam.py": ["report_ec2_beam"]} #개별 테스트용
    # for file, funcs in auto_convert_functions.items():
    #     module_name = path_to_module(file)
    #     module = importlib.import_module(module_name) 
    #     resolve_refs = False if directory == "./moapy/plugins" else True

    #     for func in funcs:
    #         router = auto_convert.get_router_for_module(module_name + func)
    #         app.include_router(router)
    #         save_openapi_spec(
    #             router, path_to_schema(file) + f"{func}.json", resolve_refs=resolve_refs
    #         )

    # make_init_py_in_subfolders("schemas")
