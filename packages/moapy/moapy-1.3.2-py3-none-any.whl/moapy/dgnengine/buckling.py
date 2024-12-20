import base64
from pydantic import Field, ConfigDict
from moapy.auto_convert import auto_schema, MBaseModel
from moapy.data_pre import SectionForce, EffectiveLengthFactor
from moapy.steel_pre import SteelSection_AISC05_US, SteelLength
from moapy.alu_pre import AluMaterial, AluMomentModificationFactor
from moapy.dgnengine.base import call_func, load_dll, read_file_as_binary
from moapy.data_post import ResultBytes, print_result_data
from typing import List
from moapy.designers_guide.resource.report_form import ReportForm
from moapy.designers_guide.func_general import DG_Result_Reports
import numpy as np
from scipy.optimize import fsolve
import math


class Frame_Select(MBaseModel):
    data_frame: str = Field(default="UnBraced Frame", title="Frame Type", description="Determine the calculation formula applied",enum=["UnBraced Frame","Braced Frame"])

class SectProp_C(MBaseModel):
    length: float = Field(default_factory=float, title="Lc", description="Upper Column Length")
    inertia: float = Field(default_factory=float, title="Ic", description="Moment of Inertia")
    elastic: float = Field(default_factory=float, title="Ec", description="Modulus of Elasticity of the Column")

    model_config = ConfigDict(
        title="Calc Column",
        description = "This is the information of the column you want to obtain the K value.")

class SectProp_Ct(MBaseModel):
    length: float = Field(default_factory=float, title="Lc", description="Upper Column Length")
    inertia: float = Field(default_factory=float, title="Ic", description="Moment of Inertia")
    elastic: float = Field(default_factory=float, title="Ec", description="Modulus of Elasticity of the Column")

    model_config = ConfigDict(
        title="Upper Column",
        description = "The upper column of the reference column.")

class SectProp_Cb(MBaseModel):
    type : str = Field(default="Bot Column", title="Fixity", description="Bot Column= Calculation , Settled on bedrock = 1.5  , UnSettled on bedrock = 3.0 , Settled on Soil = 5.0 , Setteld on End Support Piles = 1.0 ",enum=["Bot Column","Settled on bedrock","UnSettled on bedrock","Settled on Soil","Setteld on End Support Piles"])
    length: float = Field(default_factory=float, title="Lc", description="Upper Column Length")
    inertia: float = Field(default_factory=float, title="Ic", description="Moment of Inertia")
    elastic: float = Field(default_factory=float, title="Ec", description="Modulus of Elasticity of the Column")

    model_config = ConfigDict(
        title="Above Column",
        description = "The above column of the reference column.")

class SectProp_Ga(MBaseModel):
    length: float = Field(default_factory=float, title="Lg", description="Girder Length")
    inertia: float = Field(default_factory=float, title="Ig", description="Moment of Inertia")
    elastic: float = Field(default_factory=float, title="Eg", description="Modulus of Elasticity of the Girder")
    model_config = ConfigDict(
        title="Girder",
        description = "Information on the beam on the top of the column.")
    
class SectProp_Gb(MBaseModel):
    length: float = Field(default_factory=float, title="Lg", description="Girder Length")
    inertia: float = Field(default_factory=float, title="Ig", description="Moment of Inertia")
    elastic: float = Field(default_factory=float, title="Eg", description="Modulus of Elasticity of the Girder")
    model_config = ConfigDict(
        title="Girder",
        description = "Information on the beam on the bottom of the column.")
    
class Factor(MBaseModel):
    factor : str = Field(default="Not Used", title="Factor", description="Fixability with substructure",enum=["Not Used","Bolt Connection","Weld Connection","Pin Connection"])

class InputData(MBaseModel):
    frame_type: Frame_Select = Field(default=Frame_Select(), title="TYPE")
    column: SectProp_C = Field(default=SectProp_C(length=3.0, inertia=7.20E-03, elastic=2.1E+08), title="Column 1", description="Column to calculate K value")
    topcolumn: SectProp_Ct = Field(default=SectProp_Ct(length=3.0, inertia=7.20E-03, elastic=2.1E+08), title="Column 2", description="The upper member of a column 1")
    botcolumn: SectProp_Cb = Field(default=SectProp_Cb(length=3.0, inertia=7.20E-03, elastic=2.1E+08), title="Column 3", description="The above member of a column 1")
    topGirder: list[SectProp_Ga] = Field(default=[SectProp_Ga(length=8.0, inertia=7.20E-03, elastic=2.1E+08), SectProp_Ga(length=5.0, inertia=7.20E-03, elastic=2.1E+08)], title="Top", description="")
    botGirder: list[SectProp_Gb] = Field(default=[SectProp_Gb(length=8.0, inertia=7.20E-03, elastic=2.1E+08), SectProp_Gb(length=5.0, inertia=7.20E-03, elastic=2.1E+08)], title="Bottom", description="")

    model_config = ConfigDict(title="",description = "Please use a unified unit system. Ex:Length=m, Inertia = m⁴, Elastic = kN/m²")


@auto_schema(title="The effective buckling length coefficient calculator", description="The effective buckling length coefficient of [KDS 14 31 15] is calculated by an approximate formula.                                                                                                                                                          Please use a unified unit system. Ex:Length=m, Inertia = m⁴, Elastic = kN/m²")
def calculator_buckling_length_coeff(input: InputData) -> DG_Result_Reports:
    ga = calculator_Ga(input)
    gb_c = calculator_Gb(input)
    gb = replace_Gb(gb_c, input.botcolumn.type)
    k = calculate_final_K(input.frame_type, ga, gb)

    if input.botcolumn.type == "Bot Column" :
        res_gb = ReportForm(title='Gb', description="Ratio of the sum of the properties of the member strongly bound to the bottom of the column in the plane where the bending occurs , Max Ga = 50(Braced Frame), 100(UnBraced Frame)", result=gb, symbol="G_{b}",formula="\\frac{\\sum \\left( {E_c I_c}/{L_c} \\right)}{\\sum \\left({E_g I_g}/{L_g} \\right)} ",decimal=3)
    else :
        res_gb = ReportForm(title='Gb', description="Calculation of effective length coefficient of columns integrated with foundation Max Gb = 50(Braced Frame), 100(UnBraced Frame)", result=gb,formula="User\\:Input",symbol="G_{b}",decimal=1)

    if input.frame_type.data_frame == "UnBraced Frame" :
        res_k = ReportForm(title='UnBraced K', description="The effective buckling length coefficient of UnBraced Type", result=k, symbol="K",formula="(Ga * Gb / (4 * (\\pi / K)^2) - 36) / (6 * (Ga + Gb)) = (\\pi / K) / tan(\\pi / K) = 1",decimal=3)
    else :
        res_k = ReportForm(title='Braced K', description="The effective buckling length coefficient of Braced Type", result=k, symbol="K",formula="Ga * Gb / (4 * (\\pi / K)^2) + (Ga + Gb) / 2 * (1 - ((\\pi / K) / \\tan(\\pi / K))) + 2 * \\tan(0.5 * \\pi / K) / (\\pi / K) = 1",decimal=3)
    
    res_ga = ReportForm(title='Ga', description="Ratio of the sum of the properties of the member strongly bound to the top of the column in the plane where the bending occurs , Max Ga = 50(Braced Frame), 100(UnBraced Frame) ", result=ga, symbol="G_{a}",formula="\\frac{\\sum \\left( {E_c I_c}/{L_c} \\right)}{\\sum \\left({E_g I_g}/{L_g} \\right)}",decimal=3)
    results = {
        "result": [
            [
                res_ga.to_dict(),
                res_gb.to_dict(),
                res_k.to_dict()
            ]
        ]
    }
    return DG_Result_Reports(res_report=results)


def calculator_Ga(input: InputData) -> float:
    Stiffness_C = (input.column.elastic * input.column.inertia) / input.column.length
    if input.topcolumn.length == 0:
        Stiffness_Ct = 0
    else:
        Stiffness_Ct = (input.topcolumn.elastic * input.topcolumn.inertia) / input.topcolumn.length

    Stiffness_Ca = Stiffness_C + Stiffness_Ct

    Stiffenss_Ga = 0.0
    for girder in input.topGirder:
        if girder.length == 0:
            Stiffenss_Ga = 100
        else :
            Stiffenss_Ga += ((girder.elastic * girder.inertia) / girder.length)

    Ga = Stiffness_Ca/Stiffenss_Ga
    
    # Apply limits based on frame type
    if input.frame_type.data_frame == "Braced Frame":
        Ga = min(Ga, 50)
    else:
        Ga = min(Ga, 100)

    return Ga

def calculator_Gb(input: InputData) -> float:
    Stiffness_C = (input.column.elastic * input.column.inertia) / input.column.length
    if input.botcolumn.length == 0:
        Stiffness_Cb = 0
    else:
        Stiffness_Cb = (input.botcolumn.elastic * input.botcolumn.inertia) / input.botcolumn.length

    Stiffness_Cb = Stiffness_C + Stiffness_Cb

    Stiffenss_Gb = 0.0
    for girder in input.botGirder:
        if girder.length == 0:
            Stiffenss_Gb = 100
        else :
            Stiffenss_Gb += ((girder.elastic * girder.inertia) / girder.length)

    Gb_c=Stiffness_Cb/Stiffenss_Gb
    
        # Apply limits based on frame type
    if input.frame_type.data_frame == "Braced Frame":
        Gb_c = min(Gb_c, 50)
    else:
        Gb_c = min(Gb_c, 100)

    return Gb_c

def replace_Gb(Gb_c: float, input: InputData) -> float:

    Gb_mapping = {"Settled on bedrock": 1.5 ,"UnSettled on bedrock" : 3.0 ,"Settled on Soil" : 5.0 ,"Setteld on End Support Piles" : 1.0}
    if input == "Bot Column":
        Gb = Gb_c
    else:
        Gb = Gb_mapping.get(input)  # 기본값은 1.0으로 설정

    return Gb

def Braced_K(Ga: float, Gb: float) -> float:
    def left(K):
        return (Ga * Gb / 4 * (math.pi / K) ** 2 + (Ga+Gb)/2*(1-((math.pi / K)/math.tan(math.pi / K))+2*math.tan(0.5*math.pi / K)/(math.pi / K)))
    right = 1

    k = [0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0]
    dif = []
    for i in k:
        left_i = left(i)
        right_i = right
        dif_i = (left_i - right_i)
        dif.append(dif_i)

    for dif_i in dif:
        if dif_i < 0:
            key_index_j = dif.index(dif_i)
            key_index_i = key_index_j - 1
            print("K = ", k[dif.index(dif_i)])
            break
    tolerance = 10
    ki = k[key_index_i]
    kj = k[key_index_j]
    while tolerance > 0.001:
        km = (ki + kj) / 2
        left_m = left(km)
        right_m = right
        dif_m = (left_m - right_m)
        if dif_m > 0:
            ki = km
        else:
            kj = km
        tolerance = abs(dif_m)
    return km

def Unbraced_K(Ga: float, Gb: float) -> float:
    def left(K):
        return (Ga * Gb * (math.pi / K) ** 2 - 36) / (6 * (Ga + Gb))

    def right(K):
        return math.pi / K / math.tan(math.pi / K)

    k = [1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.2, 2.4, 2.6, 2.8, 3, 3.5, 4, 4.5, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20]
    dif = []
    for i in k:
        left_i = left(i)
        right_i = right(i)
        dif_i = (left_i - right_i)
        dif.append(dif_i)

    for dif_i in dif:
        if dif_i < 0:
            key_index_j = dif.index(dif_i)
            key_index_i = key_index_j - 1
            print("K = ", k[dif.index(dif_i)])
            break

    tolerance = 10
    ki = k[key_index_i]
    kj = k[key_index_j]
    while tolerance > 0.001:
        km = (ki + kj) / 2
        left_m = left(km)
        right_m = right(km)
        dif_m = (left_m - right_m)
        if dif_m > 0:
            ki = km
        else:
            kj = km
        tolerance = abs(dif_m)
    return km

def calculate_final_K(frame: Frame_Select, Ga: float, Gb: float) -> float:
    """
    Calculate final_K based on frame type.
    """
    if frame.data_frame == "UnBraced Frame":
        final_K = Unbraced_K(Ga, Gb)
    elif frame.data_frame == "Braced Frame":
        final_K = Braced_K(Ga, Gb)
    else:
        raise ValueError("Invalid frame type provided.")

    return final_K

if __name__ == "__main__":
    res = calculator_buckling_length_coeff(**{"input":{"frameType":{"dataFrame":"Braced Frame"},"column":{"length":3,"inertia":0.0072,"elastic":210000000},"topcolumn":{"length":0,"inertia":0,"elastic":0},"botcolumn":{"type":"Bot Column","length":3,"inertia":0.0072,"elastic":210000000},"topGirder":[{"length":0,"inertia":0,"elastic":0},{"length":0,"inertia":0,"elastic":0}],"botGirder":[{"length":5,"inertia":0.01,"elastic":210000000},{"length":5,"inertia":0.01,"elastic":210000000}]}})
    print_result_data(res)