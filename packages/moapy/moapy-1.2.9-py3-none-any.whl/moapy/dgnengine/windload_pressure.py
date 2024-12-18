from pydantic import Field, ConfigDict
from moapy.auto_convert import auto_schema, MBaseModel
from moapy.designers_guide.resource.report_form import ReportForm
from moapy.designers_guide.func_general import DG_Result_Reports
from moapy.data_post import print_result_data
from typing import List, Dict, Optional
from pydantic import Field, BaseModel, field_validator
import math

# Enum Field for exposure
class ExposureCategory(str):
    B = "B"
    C = "C"
    D = "D"

# kd_mapping을 반영한 함수
def get_kd_value(selection: str) -> float:
    if selection == "Buildings-Main wind force resisting system":
        return 0.85
    elif selection == "Buildings-Components and Cladding":
        return 0.85
    elif selection == "Arched roofs":
        return 0.85
    elif selection == "Circle domes":
        return 1.0
    elif selection == "Chimneys, tanks, and similar Structures-Square":
        return 0.9
    elif selection == "Chimneys, tanks, and similar Structures-Hexagonal":
        return 0.95
    elif selection == "Chimneys, tanks, and similar Structures-Octagonal":
        return 1.0
    elif selection == "Chimneys, tanks, and similar Structures-Round":
        return 1.0
    elif selection == "Solid freestanding walls, roof top equipment, and solid freestanding and attached signs":
        return 0.85
    elif selection == "Open Signs and single-plane open frames":
        return 0.85
    elif selection == "Trussed towers - Triangular, square, or rectangular":
        return 0.95
    elif selection == "Trussed towers - All other cross sections":
        return 0.95
    else:
        raise ValueError(f"Invalid kd selection: {selection}")

class Inputdata(MBaseModel):
    wind_speed: float = Field(default=120, title="Wind Speed", description="Basic wind speed obtained from ASCE7-22  [ft/s]")
    Height_ft: float = Field(default=120, title="Mean roof height", description="Mean roof height of a building or height of other structure [ft]")
    
    'Exposure Category'
    exposure: str = Field(default="C", title="Exposure", description="Exposure", enum=["B", "C", "D"])
  
    'Topographic_factor, Kzt = (1+K1*K2*K3)^2'
    Lh: float = Field(default=60, title="Distandce upwind, Lh", description="Distance upwind of crest of hill, ridge, or escarpment to where the difference in ground elevation is half the height of the hill, ridge, or escarpment, ft")
    topo_K1_multi: str = Field(default="2D Ridge", title="Topographic Factor K1 Multiplier", description="Topographic Factor K1 Multiplier", enum=["2D Ridge", "2D Escarpment", "3D Axisymmetrical Hill"])
    topo_K2_x: float = Field(default=30, title="Topographic K2 Multiplier x", description="Topographic K2 Multiplier x value to obtain Kzt")
    topo_K2_multi: str = Field(default="All Other Cases", title="Topographic Factor K2 Multiplier", description="Topographic Factor K2 Multiplier", enum=["2D Escarpment", "All Other Cases"])
    topo_K3_z: float = Field(default=30, title="Topographic K3 Multiplie z", description="Topographic K3 Multiplier z value to obtain Kzt")
    topo_K3_multi: str = Field(default="2D Ridge", title="Topographic Factor K3 Multiplier", description="Topographic Factor K3", enum=["2D Ridge", "2D Escarpment", "3D Axisymmetrical Hill"])

    'sea_level, ke'
    ke: float = Field(default="0", title="Sea Level, Ke", description="Ground elevation factor", enum=["<0", "0", "1000", "2000", "3000", "4000", "5000", "6000", ">6000"])

    kd: str = Field(
        default="Buildings-Main wind force resisting system",
        title="Wind Directionality Factor, Kd",
        description="Wind Directionality Factor",
        enum=[
            "Buildings-Main wind force resisting system",
            "Buildings-Components and Cladding",
            "Arched roofs",
            "Circle domes",
            "Chimneys, tanks, and similar Structures-Square",
            "Chimneys, tanks, and similar Structures-Hexagonal",
            "Chimneys, tanks, and similar Structures-Octagonal",
            "Chimneys, tanks, and similar Structures-Round",
            "Solid freestanding walls, roof top equipment, and solid freestanding and attached signs",
            "Open Signs and single-plane open frames",
            "Trussed towers - Triangular, square, or rectangular",
            "Trussed towers - All other cross sections"
        ]
    )

    'Velocity Pressure Exposure coefficients, kh and kz'
    kz: float = Field(default=0.85, title="Velocity Pressure Exposure Coefficient, kz(kh)", description="Velocity pressure exposure coefficient evaluated at height z = h")

    model_config = ConfigDict(
        title="ASCE 7-22 Wind Velocity Pressure Calculation Input",
        description="Standard for wind Velocity Pressure on buildings and structures"
    )

    # 동적으로 kd 값을 얻는 메서드
    def get_kd_value(self) -> float:
        return get_kd_value(self.kd)


# 26.8.2 Topographic Factor
""" The values for
K2 and K3 shall not be less than 0. The equations for K1, K2, and K3 may be used instead of using the tabular values
when increased accuracy in determining Kzt is required. For H/Lh > 0.5, assume that H/Lh = 0.5 for evaluating K1 and
substitute 2H for Lh for evaluating K2 and K3."""

#Speed-up effects
""" Wind speed-up effects at isolated hills, ridges, and escarpments constituting abrupt changes in the general topography, located in any exposure category, shall be
included in the determination of the wind loads when site conditions and locations of buildings and other structures meet all the following conditions:
1. The building or other structure is located as shown in Figure 26.8-1 in the upper one-half of a hill or ridge or near the crest of an escarpment.
2. H∕Lh ≥ 0.2.
3. H is greater than or equal to 15 ft (4.5 m) for Exposures C and D and 60 ft (18 m) for Exposures B."""

def calculate_topo_K1(Height_ft: float, Lh: float, topo_K1_multi: str) -> float:
    """
    Calculate Topo K1 based on H / Lh and multi type.
    """
    x_values = [0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]
    ridge_values = [0.29, 0.36, 0.43, 0.51, 0.58, 0.65, 0.72]
    escarpment_values = [0.17, 0.21, 0.26, 0.30, 0.34, 0.38, 0.43]
    axisymmetrical_values = [0.21, 0.26, 0.32, 0.37, 0.42, 0.47, 0.53]

    H_Lh = min(Height_ft / Lh, 0.5)  # H/Lh > 0.5인 경우 H/Lh = 0.5로 제한

    if H_Lh < 0.2:  # 조건 1: H / Lh >= 0.2 확인
        return 0

    if topo_K1_multi == "2D Ridge":
        return max(0, linear_interpolate(H_Lh, x_values, ridge_values))  # K1 >= 0
    elif topo_K1_multi == "2D Escarpment":
        return max(0, linear_interpolate(H_Lh, x_values, escarpment_values))  # K1 >= 0
    else:
        return max(0, linear_interpolate(H_Lh, x_values, axisymmetrical_values))  # K1 >= 0

def calculate_topo_K2(topo_K2_x: float, Lh: float, topo_K2_multi: str, exposure: str, Height_ft: float) -> float:
    """
    Calculate Topo K2 using provided formula and additional constraints.
    """
    x_values = [0.00, 0.50, 1.00, 1.50, 2.00, 2.50, 3.00, 3.50, 4.00]
    escarpment_values = [1.0, 0.88, 0.75, 0.63, 0.50, 0.38, 0.25, 0.13, 0.00]
    all_other_values = [1.0, 0.67, 0.33, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]

    if not validate_H_condition(exposure, Height_ft):  # 조건 2: H 조건 확인
        return 0

    x_Lh = topo_K2_x / Lh
    
    if topo_K2_multi == "2D Escarpment":
        return max(0, linear_interpolate(x_Lh, x_values, escarpment_values))
    else:
        return max(0, linear_interpolate(x_Lh, x_values, all_other_values))

def calculate_topo_K3(topo_K3_z: float, Lh: float, topo_K3_multi: str) -> float:
    """
    Calculate Topo K3 using provided formula.
    """
    z_values = [0.00, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00, 1.50, 2.00]
    ridge_values = [1.0, 0.74, 0.55, 0.41, 0.30, 0.22, 0.17, 0.12, 0.09, 0.07, 0.05, 0.01, 0.00]
    escarpment_values = [1.0, 0.78, 0.61, 0.47, 0.37, 0.29, 0.22, 0.17, 0.14, 0.11, 0.08, 0.02, 0.00]
    axisymmetrical_values = [1.0, 0.67, 0.45, 0.30, 0.20, 0.14, 0.09, 0.06, 0.04, 0.03, 0.02, 0.00, 0.00]

    z_Lh = topo_K3_z / Lh

    if topo_K3_multi == "2D Escarpment":
        return max(0, linear_interpolate(z_Lh, z_values, escarpment_values))
    elif topo_K3_multi == "2D Ridge":
        return max(0, linear_interpolate(z_Lh, z_values, ridge_values))
    else:
        return max(0, linear_interpolate(z_Lh, z_values, axisymmetrical_values))

def validate_H_condition(exposure: str, Height_ft: float) -> bool:
    """
    Validate if H satisfies the conditions for a given exposure.
    """
    if exposure in ["C", "D"]:
        return Height_ft >= 15  # H >= 15 ft for Exposures C and D
    elif exposure == "B":
        return Height_ft >= 60  # H >= 60 ft for Exposure B

    return False

def linear_interpolate(x: float, x_values: list, y_values: list) -> float:
    """
    Perform linear interpolation for a given x based on x_values and y_values.
    """
    for i in range(len(x_values) - 1):
        if x_values[i] <= x <= x_values[i + 1]:
            x0, x1 = x_values[i], x_values[i + 1]
            y0, y1 = y_values[i], y_values[i + 1]
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)

    return y_values[-1] if x > x_values[-1] else y_values[0]  # Extrapolate if out of bounds

#print(calculate_topo_K1(120, 60, "2D Ridge"))
#print(calculate_topo_K2(30, 60, "All Other Cases", 0.5, "C", 120))
#print(calculate_topo_K3(30, 60, "2D Ridge"))

# Ke 계산 값
def linear_interpolate(x, x_values, y_values):
    """1차원 선형 보간 함수"""
    for i in range(len(x_values) - 1):
        if x_values[i] <= x <= x_values[i + 1]:
            # 보간 계산
            y = y_values[i] + (y_values[i + 1] - y_values[i]) * (x - x_values[i]) / (x_values[i + 1] - x_values[i])
 #           print(f"Interpolating: x={x}, x_range=({x_values[i]}, {x_values[i + 1]}), y_range=({y_values[i]}, {y_values[i + 1]}), result={y}")
            return y
    raise ValueError("Value out of range for interpolation")

def calculate_ke(sea_level: str) -> float:
    """Ze 값을 계산"""
    # enum 기준 값 설정
    sea_level_enum = ["<0", "0", "1000", "2000", "3000", "4000", "5000", "6000", ">6000"]
    ke = [1.00, 0.96, 0.93, 0.90, 0.86, 0.83, 0.80]  # 보간용 값
    
 #   print(f"Input sea_level: {sea_level}")
    
    # Ze 값 변환
    if sea_level == "<0":
        Ze = -1  # "<0"을 -1로 처리 (음수로 간주)
    elif sea_level == ">6000":
        Ze = 6001  # ">6000"을 초과 값으로 처리
    else:
        Ze = float(sea_level)  # 나머지 경우는 숫자로 변환

 #   print(f"Converted Ze: {Ze}")

    # "<0" 또는 ">6000"일 때 특수 처리
    if Ze < 0:
        result = math.exp(-0.0000362 * Ze)
        print(f"Ze < 0 special case: Ze={Ze}, result={result}")
        return result
    elif Ze > 6000:
        result = math.exp(-0.0000362 * Ze)
 #       print(f"Ze > 6000 special case: Ze={Ze}, result={result}")
        return result

    # 그 외의 경우 보간
    x_values = [0, 1000, 2000, 3000, 4000, 5000, 6000]
    result = linear_interpolate(Ze, x_values, ke)
#    print(f"Interpolated result: Ze={Ze}, result={result}")
    return result

# # 예제 실행
# print("Result:", calculate_ke("0"))
# print("Result:", calculate_ke("<0"))
# print("Result:", calculate_ke(">6000"))



# Kz 값
# Velocity pressure exposure coefficient calculation function
def calculate_kz(height_ft, exposure):
    if height_ft < 15:
        # Exposure constants for height < 15 ft
        exposure_constants = {
            "B": {"a": 7.5, "zg": 3280},
            "C": {"a": 9.8, "zg": 2460},
            "D": {"a": 11.5, "zg": 1935},
        }
        constants = exposure_constants[exposure]
        a = constants["a"]
        zg = constants["zg"]

        # Calculate kz based on height
        if height_ft < 15:
            kz = 2.41 * (15 / height_ft) ** (2 / a)
        elif 15 <= height_ft < zg:
            kz = 2.41 * (height_ft / zg) ** (2 / a)
        elif zg <= height_ft <= 3280:
            kz = 2.41
        else:
            raise ValueError("Height exceeds maximum limit of 3280 ft.")

    elif 15 <= height_ft < 30:
        # Data points for each exposure category for height 15 <= height_ft < 30
        data = {
            'B': [(0, 0.70), (15, 0.70), (20, 0.70), (25, 0.70), (30, 0.70), (40, 0.74), (50, 0.79), (60, 0.83), 
                  (70, 0.86), (80, 0.90), (90, 0.92), (100, 0.95), (120, 1.00), (140, 1.04), (160, 1.08), 
                  (180, 1.11), (200, 1.14), (250, 1.21), (300, 1.27), (350, 1.33), (400, 1.50), (450, 1.42), (500, 1.46)],
            'C': [(0, 0.85), (15, 0.85), (20, 0.90), (25, 0.94), (30, 0.98), (40, 1.04), (50, 1.09), (60, 1.13), 
                  (70, 1.17), (80, 1.21), (90, 1.24), (100, 1.26), (120, 1.31), (140, 1.34), (160, 1.39), 
                  (180, 1.41), (200, 1.44), (250, 1.51), (300, 1.57), (350, 1.62), (400, 1.66), (450, 1.70), (500, 1.74)],
            'D': [(0, 1.03), (15, 1.03), (20, 1.08), (25, 1.12), (30, 1.16), (40, 1.22), (50, 1.27), (60, 1.31), 
                  (70, 1.34), (80, 1.38), (90, 1.40), (100, 1.43), (120, 1.48), (140, 1.52), (160, 1.55), 
                  (180, 1.58), (200, 1.61), (250, 1.68), (300, 1.73), (350, 1.78), (400, 1.82), (450, 1.86), (500, 1.89)],
        }
    elif height_ft >= 30:
        # Data points for each exposure category for height >= 30
        data = {
            'B': [(0, 0.57), (15, 0.57), (20, 0.62), (25, 0.66), (30, 0.70), (40, 0.74), (50, 0.79), (60, 0.83), 
                  (70, 0.86), (80, 0.90), (90, 0.92), (100, 0.95), (120, 1.00), (140, 1.04), (160, 1.08), 
                  (180, 1.11), (200, 1.14), (250, 1.21), (300, 1.27), (350, 1.33), (400, 1.50), (450, 1.42), (500, 1.46)],
            'C': [(0, 0.85), (15, 0.85), (20, 0.90), (25, 0.94), (30, 0.98), (40, 1.04), (50, 1.09), (60, 1.13), 
                  (70, 1.17), (80, 1.21), (90, 1.24), (100, 1.26), (120, 1.31), (140, 1.34), (160, 1.39), 
                  (180, 1.41), (200, 1.44), (250, 1.51), (300, 1.57), (350, 1.62), (400, 1.66), (450, 1.70), (500, 1.74)],
            'D': [(0, 1.03), (15, 1.03), (20, 1.08), (25, 1.12), (30, 1.16), (40, 1.22), (50, 1.27), (60, 1.31), 
                  (70, 1.34), (80, 1.38), (90, 1.40), (100, 1.43), (120, 1.48), (140, 1.52), (160, 1.55), 
                  (180, 1.58), (200, 1.61), (250, 1.68), (300, 1.73), (350, 1.78), (400, 1.82), (450, 1.86), (500, 1.89)],
        }
    else:
        raise ValueError("Invalid height_ft value.")

    # Check if the exposure is valid
    if exposure not in data:
        raise ValueError(f"Invalid exposure category: {exposure}. Valid categories are 'B', 'C', or 'D'.")
    
    # Get the data points for the selected exposure category
    exposure_data = data[exposure]
    
    # If the height is below the first data point, return the first value
    if height_ft <= exposure_data[0][0]:
        return exposure_data[0][1]
    
    # If the height is above the last data point, return the last value
    if height_ft >= exposure_data[-1][0]:
        return exposure_data[-1][1]
    
    # Perform linear interpolation for heights between two data points
    for i in range(1, len(exposure_data)):
        x1, y1 = exposure_data[i - 1]
        x2, y2 = exposure_data[i]
        
        if height_ft >= x1 and height_ft <= x2:
            # Linear interpolation formula
            return y1 + (height_ft - x1) * (y2 - y1) / (x2 - x1)

#print(calculate_kz(120, "C"))

# Wind load pressure 계산 함수
@auto_schema(
    title="Wind load pressure calculation",
    description=(
        "This tool calculates the wind load pressure on a structure according to the ASCE 7-22 standard."
    )
)
def wind_load_pressure_calculator(input_data: Inputdata) -> DG_Result_Reports:
    """
    Calculate wind load pressure and return results.
    """
    print("Starting wind load pressure calculation...")

    # Calculate topographic factors
    k1 = calculate_topo_K1(input_data.Height_ft, input_data.Lh, input_data.topo_K1_multi)
    print(f"Calculated k1: {k1}")

    k2 = calculate_topo_K2(
    topo_K2_x=input_data.topo_K2_x, Lh=input_data.Lh, topo_K2_multi=input_data.topo_K2_multi, exposure=input_data.exposure, Height_ft=input_data.Height_ft)
    print(f"Calculated k2: {k2}")

    k3 = calculate_topo_K3(input_data.topo_K3_z, input_data.Lh, input_data.topo_K3_multi)
    print(f"Calculated k3: {k3}")

    # Calculate Kzt
    kzt = (1 + k1 * k2 * k3) ** 2
    print(f"Calculated Kzt: {kzt}")

    # Retrieve kd value
    kd = input_data.get_kd_value()
    print(f"Selected kd value: {kd}")

    # Calculate ke
    ke = calculate_ke(input_data.ke)
    print(f"Calculated ke: {ke}")

    # Calculate kz
    kz = calculate_kz(input_data.Height_ft, input_data.exposure)
    print(f"Calculated kz: {kz}")

    # Calculate wind speed
    V = input_data.wind_speed
    print(f"Wind speed (V): {V}")

    # Calculate wind load pressure (q)
    q = 0.00256 * kz * kzt * ke * (V ** 2)
    print(f"Calculated velocity pressure (q): {q}")

    # Create report forms
    res_k1 = ReportForm(title='k1', description="K1 Multipliers from ASCE7-22 Figure 26.8-1 to obtain Kzt", result=k1, symbol="K_{1}", decimal=2)
    res_k2 = ReportForm(title='k2', description="K2 Multipliers from ASCE7-22 Figure 26.8-1 to obtain Kzt", result=k2, symbol="K_{2}", decimal=2)
    res_k3 = ReportForm(title='k3', description="K3 Multipliers from ASCE7-22 Figure 26.8-1 to obtain Kzt", result=k3, symbol="K_{3}", decimal=2)
    res_kzt = ReportForm(title='kzt', description="Topographic Factor", formula=["(1+ k_{1} \\times k_{2} \\times k_{3})^2 ", f"(1 + {k1} \\times {k2} \\times {k3})^2"], result=kzt, symbol="K_{zt}", decimal=2)
    res_kd = ReportForm(title='kd', description="Wind Directionality Factor from ASCE7-22 Table 26.6-1", result=kd, symbol="K_{d}", decimal=2)
    res_ke = ReportForm(title='ke', description="Ground Elevation Factor from ASCE7-22 Table 26.9-1", result=ke, symbol="K_{e}", decimal=2)
    res_kz = ReportForm(title='kz', description="Velocity Pressure Exposure Coefficient from Table 26.10-1", result=kz, symbol="K_{z}", decimal=2)
    res_q = ReportForm(title='qz', description="Velocity pressure at height z", formula=["0.00256 \\times k_{z} \\times k_{zt} \\times k_{e}\\times V^2 ", f"0.00256 \\times {kz} \\times {kzt} \\times {ke}\\times {V}^2"], result=q, symbol="q_{z}", unit="psi", decimal=5)

    # Organize results
    results = {
        "result": [
            [
                res_k1.to_dict(),
                res_k2.to_dict(),
                res_k3.to_dict(),
                res_kzt.to_dict(),
                res_kd.to_dict(),
                res_ke.to_dict(),
                res_kz.to_dict(),
                res_q.to_dict()
            ]
        ]
    }
    print("Calculation results organized into reports.")

    return DG_Result_Reports(res_report=results)

if __name__ == "__main__":
    res = wind_load_pressure_calculator(Inputdata())
    print_result_data(res)

    
class OutputData(MBaseModel):
    result: str = Field(default="ASCE 7-22 standard Wind Pressure calculation", title="Wind Pressure", description="result")

    model_config = ConfigDict(title="Wind Pressure")