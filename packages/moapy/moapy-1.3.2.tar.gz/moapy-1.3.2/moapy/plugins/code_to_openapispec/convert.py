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
    script_code: str = Field(default="""from fastapi import APIRouter

router = APIRouter()
@auto_schema(title="python to openapi spec", description="This tool generates OpenAPI spec from Python code")
def hello_world():
    return {"message": "Hello, World!"}
""", title="Python Script Code", description="Python script code to generate OpenAPI spec")

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
    inp = """import ctypes
import json
import base64
from pydantic import Field
from moapy.auto_convert import auto_schema, MBaseModel
from moapy.data_pre import UnitLoads, SectionRectangle, SectionForce, Moment, enUnitMoment, enUnitLength, Length
from moapy.rc_pre import SlabMember_EC, GirderLength, BeamRebarPattern, MaterialNative
from moapy.dgnengine.base import load_dll, call_func, read_file_as_binary
from moapy.data_post import ResultBytes
from moapy.enum_pre import enUnitSystem

@auto_schema(
    title="Eurocode 2 Beam Design",
    description="Eurocode 2 provides a comprehensive review of reinforced concrete (RC) beam design with a focus on strength assessment, available in Excel format."
)
def report_ec2_beam(matl: MaterialNative = MaterialNative.create_default(enUnitSystem.SI),
                    sect: SectionRectangle = SectionRectangle.create_default(enUnitSystem.SI),
                    rebar: BeamRebarPattern = BeamRebarPattern.create_default(enUnitSystem.SI),
                    force: SectionForce = SectionForce.create_default(enUnitSystem.SI)) -> ResultBytes:
    dll = load_dll()
    json_data_list = [matl.json(), sect.json(), rebar.json(), force.json()]
    file_path = call_func(dll, 'Report_EC2_Beam', json_data_list)
    if file_path is None:
        return ResultBytes(type="md", result="Error: Failed to generate report.")
    return ResultBytes(type="xlsx", result=base64.b64encode(read_file_as_binary(file_path)).decode('utf-8'))

def calc_ec2_beam(matl: MaterialNative = MaterialNative.create_default(enUnitSystem.SI),
                  sect: SectionRectangle = SectionRectangle.create_default(enUnitSystem.SI),
                  rebar: BeamRebarPattern = BeamRebarPattern.create_default(enUnitSystem.SI),
                  force: SectionForce = SectionForce.create_default(enUnitSystem.SI)) -> dict:
    dll = load_dll()
    json_data_list = [matl.json(), sect.json(), rebar.json(), force.json(), ctypes.c_void_p(0), ctypes.c_void_p(0)]
    jsondata = call_func(dll, 'Calc_EC2_Beam', json_data_list)
    dict = json.loads(jsondata)
    print(dict)


if __name__ == "__main__":
    force = SectionForce.create_default(enUnitSystem.SI)
    force.Mx.value = 50
    force.Vy.value = 100
    res = report_ec2_beam(matl = MaterialNative.create_default(enUnitSystem.SI),
                          sect = SectionRectangle.create_default(enUnitSystem.SI),
                          rebar = BeamRebarPattern.create_default(enUnitSystem.SI),
                          force = force)
    print(res)"""
    
    data = {"inp": {"script_code": inp}}
    
    print(str(generate_openapi_spec_from_code(**data)))
