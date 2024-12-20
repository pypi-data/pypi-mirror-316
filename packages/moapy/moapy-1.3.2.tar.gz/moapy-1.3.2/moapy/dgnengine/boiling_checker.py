import re
from enum import Enum
import pandas as pd
from pydantic import Field, ConfigDict
from moapy.auto_convert import auto_schema, MBaseModel
from moapy.enum_pre import enum_to_list
from moapy.designers_guide.resource.report_form import ReportForm
from moapy.designers_guide.func_general import DG_Result_Reports
from moapy.data_post import print_result_data, ResultMD

# 입력구조체
class InputData(MBaseModel):    
    d2: float = Field(default="4", title="근입길이 ", description="굴착저면에서 흙막이벽 근입길이 (m)")
    gamma_w: float = Field(default="10", title="물의 단위중량 (kN/m^3)", description="물의 단위중량 (kN/m^3)")
    gamma_prime: float = Field(default="11.35", title="수중 단위중량 (kN/m^3)", description="수중 단위중량 (kN/m^3)")
    Ha: float = Field(default="4.535", title="평균 과잉수두 (m)", description="평균 과잉수두 (m)")
    Fs_target: float = Field(default="1.5", title="허용 안전율", description="허용 안전율")
    Cave: float = Field(default="50", title="근입 지반의 평균 점착력 (kN/m^2)", description="근입 지반의 평균 점착력 (kN/m^2)")
    Lh: float = Field(default="1", title="점착저항이 발생하는 길이 (m)", description="점착저항이 발생하는 길이 (m)")


    model_config = ConfigDict(
        title="Boiling Assessment in Viscous Soils",
        description="This tool enables the calculation of a boiling review method proposed by Davidenkoff (1970), which incorporates additional consideration of cohesion in viscous soils."
    )


# Terzaghi 보일링 검토를 위한 계산 코드
@auto_schema(title="점성토 지반의 보일링 조건 평가 도구: Davidenkoff 이론 기반", description="본 도구는 주어진 입력 파라미터와 계산 결과를 바탕으로 점성토에서 발생하는 보일링 조건에 대한 상세한 평가를 제공합니다. 평가 방법은 점성토의 점착력(cohesion)을 고려하는 Davidenkoff(1970)의 접근법을 기반으로 하고 있습니다.")
def boiling_checker(inp: InputData) -> ResultMD:
    # 각 계산식에 LaTeX 표현식 추가

    # 과잉간극수압 (U)
    U = (inp.gamma_w * inp.Ha * inp.d2) / 2
    U_formula = f"$$U = \\frac{{\\gamma_w \\cdot H_a \\cdot d_2}}{{2}} = \\frac{{{inp.gamma_w} \\cdot {inp.Ha} \\cdot {inp.d2}}}{{2}} = {U:.2f} \\text{{ kN/m}}$$"

    # 흙의 중량 (W)
    W = inp.gamma_prime * (inp.d2**2) / 2
    W_formula = f"$$W = \\frac{{\\gamma' \\cdot d_2^2}}{{2}} = \\frac{{{inp.gamma_prime} \\cdot {inp.d2}^2}}{{2}} = {W:.2f} \\text{{ kN/m}}$$"

    # 점착 저항력 (Fc)
    Fc = 2 * inp.Cave * inp.Lh
    Fc_formula = f"$$F_c = 2 \\cdot C_{{ave}} \\cdot L_h = 2 \\cdot {inp.Cave} \\cdot {inp.Lh} = {Fc:.2f} \\text{{ kN/m}}$$"

    # 총 저항력
    total_resistance = W + Fc
    total_resistance_formula = f"$$\\text{{Total Resistance}} = W + F_c = {W:.2f} + {Fc:.2f} = {total_resistance:.2f} \\text{{ kN/m}}$$"

    # 안전율 계산
    Fs = total_resistance / U
    Fs_formula = f"$$F_s = \\frac{{\\text{{Total Resistance}}}}{{U}} = \\frac{{{total_resistance:.2f}}}{{{U:.2f}}} = {Fs:.2f}$$"

    # 결과 판단
    result = "O.K" if Fs >= inp.Fs_target else "N.G (Not Safe)"

    # 마크다운 형태로 변환
    md_result = f"""
<style>
    .katex {{
        font-size: 20px; /* 전체 수식의 글자 크기 */
      }}
    .katex .mord {{
        color: #333; /* 일반 문자 색상 */
      }}
    .katex .mrel {{
        color: #555; /* 연산자 색상 */
      }}
    .katex .mfrac {{
        font-size: 30px; /* 전체 분수 크기 */
        }}
    .katex .mfrac .vlist .sizing.size3:first-child {{
        font-size: 18px; /* 분자 크기 */
        color: blue; /* 분자 색상 */
        }}
    .katex .mfrac .vlist .sizing.size3:last-child {{
        font-size: 16px; /* 분모 크기 */
        color: red; /* 분모 색상 */
        }}
    .katex .mfrac .frac-line {{
        border-bottom-width: 2px; /* 분수선 두께 */
        border-bottom-color: black; /* 분수선 색상 */
        }}
    body {{
        font-family: 'Arial', sans-serif;
        line-height: 1.6;
        background-color: #f9f9f9;
        color: #333;
        padding: 20px;
    }}
    h1, h2, h3 {{
        color: #2c3e50;
    }}
    table {{
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
    }}
    table, th, td {{
        border: 1px solid #ddd;
        padding: 8px;
    }}
    th {{
        background-color: #f4f4f4;
        font-size: 14px; /* 헤더 글자 크기 */
    }}
    td {{
        font-size: 13px; /* 본문 셀 글자 크기 */
    }}
    th, td {{
        text-align: left;
    }}
</style>


# 점성토 지반의 보일링 조건 평가 도구: Davidenkoff 이론 기반

## 개요
본 보고서는 주어진 입력 파라미터와 계산 결과를 바탕으로 점성토에서 발생하는 보일링 조건에 대한 상세한 평가를 제공합니다.  
본 평가 방법은 점성토의 점착력(cohesion)을 고려하는 Davidenkoff(1970)의 접근법을 기반으로 하고 있습니다.

---

## Input Parameters
| Parameter                          | Value    | Unit         | Description                             |
|:-----------------------------------|:---------|:-------------|:----------------------------------------|
| 근입길이 (d2)                      | {inp.d2:<8} | m            | 굴착저면에서 흙막이벽 근입길이            |
| 물의 단위중량 (gamma_w)           | {inp.gamma_w:<8} | kN/m³       | 물의 단위중량                           |
| 수중 단위중량 (gamma_prime)       | {inp.gamma_prime:<8} | kN/m³       | 수중 단위중량                           |
| 평균 과잉수두 (Ha)                 | {inp.Ha:<8} | m            | 평균 과잉수두                           |
| 허용 안전율 (Fs_target)           | {inp.Fs_target:<8} | -            | 허용 안전율                             |
| 근입 지반의 평균 점착력 (Cave)     | {inp.Cave:<8} | kN/m²       | 근입 지반의 평균 점착력                   |
| 점착저항이 발생하는 길이 (Lh)     | {inp.Lh:<8} | m            | 점착저항이 발생하는 길이                 |

---

## Results
| Metric                            | Value       | Unit         | Description                             |
|:----------------------------------|:------------|:-------------|:----------------------------------------|
| 과잉간극수압 (U)                 | {U:<11.2f} | kN/m         | 과잉간극수압                            |
| 흙의 중량 (W)                    | {W:<11.2f} | kN/m         | 흙의 중량                               |
| 점착 저항력 (Fc)                 | {Fc:<11.2f} | kN/m         | 점착 저항력                             |
| 안전율 (Fs)                      | {Fs:<11.2f} | -            | 안전율                                  |

---

## Calculations
- 과잉간극수압 (U):  
{U_formula}  
- 흙의 중량 (W):  
{W_formula}  
- 점착 저항력 (Fc):  
{Fc_formula}  
- 총 저항력:  
{total_resistance_formula}  
- 안전율 (Fs):  
{Fs_formula}

---
## 주의사항
> * *점착력 고려의 일반성 제한: 보일링(Boiling) 검토 시 점착력을 직접 고려하는 방법(예: Davidenkoff 이론 적용)은 일반적으로 통용되는 표준 접근법이 아닙니다. 이는 본래 점성토(cohesive soil) 지반을 전제로 개발된 개념으로, 풍화암(Weathered rock)과 같이 비전형적 토질 특성을 가진 재료에 동일하게 적용하기 위해서는 신중한 엔지니어링 판단이 필요합니다. 즉, 단순히 표준 공식 대입이 아닌, 지반특성(풍화 정도, 불균질성, 인장강도 산정 난이도)을 종합적으로 고려해야 합니다.  
> * *Cave, Lh 파라미터 적용: 파라미터 중 Cave, Lh는 점착력 고려 대상 지층 특성값으로, 이 값들 역시 단순치환이 아닌 엔지니어의 경험과 실내시험, 문헌값 등을 통한 검증 과정이 수반되어야 합니다. 특히 Cave(점착력)와 Lh(수직 방향 길이)는 지반 특성에 따라 매우 민감하게 변동할 수 있으므로, 이러한 파라미터 선정 시에는 지반조사 결과, 실험치 및 기존 문헌자료를 충분히 검토해야 합니다.  
> * *실무적 활용과 한계 인식: 실무에서는 풍화암 근입부 안정성 검토 시 Davidenkoff 이론을 응용하는 사례가 있으나, 이는 일반화된 검토법이 아니라 특정 조건(풍화암 지층 특성, 시공 경험)에 근거한 응용적 접근입니다. 따라서 이 방법을 사용할 때에는, 이론적 배경 및 적용 한계를 충분히 이해하고, 필요하다면 수치해석이나 추가 보수계수 적용 등을 통해 불확실성을 감소시키는 것이 바람직합니다. 또한, 가이드 이미지나 문헌 자료를 통해 Davidenkoff 이론의 전제 및 결과 해석 방법을 숙지하는 것이 중요합니다.  

"""

    return ResultMD(md=md_result)

if __name__ == "__main__":
    # res = boiling_checker(InputData())
    # print(res)
    input_data = InputData(d2=4, gamma_w=10, gamma_prime=11.35, Ha=4.535, Fs_target=1.5, Cave=50, Lh=1)
    res = boiling_checker(input_data)
    result_md = print_result_data(res)
    # # 마크다운 결과를 파일로 저장
    # with open("boiling_assessment_result.md", "w", encoding="utf-8") as f:
    #     f.write(result_md.md)
    # print_result_data(result_md)