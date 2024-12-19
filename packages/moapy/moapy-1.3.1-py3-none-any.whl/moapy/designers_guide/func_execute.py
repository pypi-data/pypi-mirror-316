from moapy.designers_guide.func_general import execute_calc_content, DG_Result_Reports

def calc_content_1(G4_COMP_1: str) -> DG_Result_Reports:
    target_components = ['G4_COMP_4', 'G4_COMP_5', 'G4_COMP_6', 'G4_COMP_7', 'G4_COMP_8', 'G4_COMP_9']
    inputs = {"G4_COMP_1": G4_COMP_1}
    return execute_calc_content(target_components, inputs)

def calc_content_10(G3_COMP_2: float, G3_COMP_6: float, G3_COMP_10: float, G3_COMP_15: str, G10_COMP_3: float, G10_COMP_4: float, G10_COMP_5: float, G10_COMP_6: float) -> DG_Result_Reports:
    target_components = ['G10_COMP_1']
    inputs = {"G3_COMP_2": G3_COMP_2, "G3_COMP_6": G3_COMP_6, "G3_COMP_10": G3_COMP_10, "G3_COMP_15": G3_COMP_15, "G10_COMP_3": G10_COMP_3, "G10_COMP_4": G10_COMP_4, "G10_COMP_5": G10_COMP_5, "G10_COMP_6": G10_COMP_6}
    return execute_calc_content(target_components, inputs)

def calc_content_11(G11_COMP_1: str, G11_COMP_4: str, G11_COMP_5: float, G11_COMP_11: str, G11_COMP_14: str, G11_COMP_18: float, G11_COMP_19: float, G11_COMP_25: float, G11_COMP_26: float, G11_COMP_30: str, G11_COMP_33: float, G11_COMP_34: float) -> DG_Result_Reports:
    target_components = ['G11_COMP_2', 'G11_COMP_3']
    inputs = {"G11_COMP_1": G11_COMP_1, "G11_COMP_4": G11_COMP_4, "G11_COMP_5": G11_COMP_5, "G11_COMP_11": G11_COMP_11, "G11_COMP_14": G11_COMP_14, "G11_COMP_18": G11_COMP_18, "G11_COMP_19": G11_COMP_19, "G11_COMP_25": G11_COMP_25, "G11_COMP_26": G11_COMP_26, "G11_COMP_30": G11_COMP_30, "G11_COMP_33": G11_COMP_33, "G11_COMP_34": G11_COMP_34}
    return execute_calc_content(target_components, inputs)

def calc_content_12(G12_COMP_1: str, G12_COMP_2: str, G12_COMP_4: str, G12_COMP_5: float, G12_COMP_6: float) -> DG_Result_Reports:
    target_components = ['G12_COMP_15', 'G12_COMP_16', 'G12_COMP_17']
    inputs = {"G12_COMP_1": G12_COMP_1, "G12_COMP_2": G12_COMP_2, "G12_COMP_4": G12_COMP_4, "G12_COMP_5": G12_COMP_5, "G12_COMP_6": G12_COMP_6}
    return execute_calc_content(target_components, inputs)

def calc_content_13(G3_COMP_2: float, G3_COMP_6: float, G3_COMP_10: float, G3_COMP_15: str, G13_COMP_2: float, G13_COMP_3: float, G13_COMP_8: str) -> DG_Result_Reports:
    target_components = ['G13_COMP_16']
    inputs = {"G3_COMP_2": G3_COMP_2, "G3_COMP_6": G3_COMP_6, "G3_COMP_10": G3_COMP_10, "G3_COMP_15": G3_COMP_15, "G13_COMP_2": G13_COMP_2, "G13_COMP_3": G13_COMP_3, "G13_COMP_8": G13_COMP_8}
    return execute_calc_content(target_components, inputs)

def calc_content_14(G14_COMP_1: float, G14_COMP_2: str, G14_COMP_3: str, G14_COMP_4: str) -> DG_Result_Reports:
    target_components = ['G14_COMP_15', 'G14_COMP_16', 'G14_COMP_17', 'G14_COMP_18', 'G14_COMP_19']
    inputs = {"G14_COMP_1": G14_COMP_1, "G14_COMP_2": G14_COMP_2, "G14_COMP_3": G14_COMP_3, "G14_COMP_4": G14_COMP_4}
    return execute_calc_content(target_components, inputs)

def calc_content_15(G14_COMP_4: str, G15_COMP_1: float, G15_COMP_2: str) -> DG_Result_Reports:
    target_components = ['G15_COMP_6', 'G15_COMP_8', 'G15_COMP_9']
    inputs = {"G14_COMP_4": G14_COMP_4, "G15_COMP_1": G15_COMP_1, "G15_COMP_2": G15_COMP_2}
    return execute_calc_content(target_components, inputs)

def calc_content_16(G14_COMP_4: str, G15_COMP_2: str, G16_COMP_5: float, G16_COMP_6: float, G16_COMP_11: float, G16_COMP_12: float, G16_COMP_14: str, G16_COMP_23: float) -> DG_Result_Reports:
    target_components = ['G16_COMP_17', 'G16_COMP_19']
    inputs = {"G14_COMP_4": G14_COMP_4, "G15_COMP_2": G15_COMP_2, "G16_COMP_5": G16_COMP_5, "G16_COMP_6": G16_COMP_6, "G16_COMP_11": G16_COMP_11, "G16_COMP_12": G16_COMP_12, "G16_COMP_14": G16_COMP_14, "G16_COMP_23": G16_COMP_23}
    return execute_calc_content(target_components, inputs)

def calc_content_17(G14_COMP_4: str, G15_COMP_2: str, G16_COMP_11: float, G16_COMP_12: float, G16_COMP_14: str, G16_COMP_23: float, G17_COMP_11: float) -> DG_Result_Reports:
    target_components = ['G17_COMP_10', 'G17_COMP_16']
    inputs = {"G14_COMP_4": G14_COMP_4, "G15_COMP_2": G15_COMP_2, "G16_COMP_11": G16_COMP_11, "G16_COMP_12": G16_COMP_12, "G16_COMP_14": G16_COMP_14, "G16_COMP_23": G16_COMP_23, "G17_COMP_11": G17_COMP_11}
    return execute_calc_content(target_components, inputs)

def calc_content_18(G14_COMP_3: str, G18_COMP_1: float, G18_COMP_7: str) -> DG_Result_Reports:
    target_components = ['G18_COMP_3', 'G18_COMP_6', 'G18_COMP_10']
    inputs = {"G14_COMP_3": G14_COMP_3, "G18_COMP_1": G18_COMP_1, "G18_COMP_7": G18_COMP_7}
    return execute_calc_content(target_components, inputs)

def calc_content_19(G14_COMP_4: str, G19_COMP_1: str, G19_COMP_2: str, G19_COMP_8: str, G19_COMP_10: str, G19_COMP_15: str, G19_COMP_16: str, G19_COMP_17: str, G19_COMP_19: str, G19_COMP_23: str, G19_COMP_26: str, G19_COMP_28: str) -> DG_Result_Reports:
    target_components = ['G19_COMP_3', 'G19_COMP_7']
    inputs = {"G14_COMP_4": G14_COMP_4, "G19_COMP_1": G19_COMP_1, "G19_COMP_2": G19_COMP_2, "G19_COMP_8": G19_COMP_8, "G19_COMP_10": G19_COMP_10, "G19_COMP_15": G19_COMP_15, "G19_COMP_16": G19_COMP_16, "G19_COMP_17": G19_COMP_17, "G19_COMP_19": G19_COMP_19, "G19_COMP_23": G19_COMP_23, "G19_COMP_26": G19_COMP_26, "G19_COMP_28": G19_COMP_28}
    return execute_calc_content(target_components, inputs)

def calc_content_2(G3_COMP_2: float, G3_COMP_6: float, G3_COMP_10: float, G3_COMP_15: str) -> DG_Result_Reports:
    target_components = ['G3_COMP_24']
    inputs = {"G3_COMP_2": G3_COMP_2, "G3_COMP_6": G3_COMP_6, "G3_COMP_10": G3_COMP_10, "G3_COMP_15": G3_COMP_15}
    return execute_calc_content(target_components, inputs)

def calc_content_20(G20_COMP_12: str, G20_COMP_14: str) -> DG_Result_Reports:
    target_components = ['G20_COMP_1', 'G20_COMP_8', 'G20_COMP_13', 'G20_COMP_15', 'G20_COMP_18']
    inputs = {"G20_COMP_12": G20_COMP_12, "G20_COMP_14": G20_COMP_14}
    return execute_calc_content(target_components, inputs)

def calc_content_3(G1_COMP_1: str, G1_COMP_3: float, G1_COMP_4: float, G1_COMP_6: float, G1_COMP_7: float) -> DG_Result_Reports:
    target_components = ['G1_COMP_16', 'G1_COMP_17']
    inputs = {"G1_COMP_1": G1_COMP_1, "G1_COMP_3": G1_COMP_3, "G1_COMP_4": G1_COMP_4, "G1_COMP_6": G1_COMP_6, "G1_COMP_7": G1_COMP_7}
    return execute_calc_content(target_components, inputs)

def calc_content_4(G2_COMP_4: float, G2_COMP_7: float, G6_COMP_2: str) -> DG_Result_Reports:
    target_components = ['G2_COMP_1', 'G2_COMP_5', 'G2_COMP_6']
    inputs = {"G2_COMP_4": G2_COMP_4, "G2_COMP_7": G2_COMP_7, "G6_COMP_2": G6_COMP_2}
    return execute_calc_content(target_components, inputs)

def calc_content_5(G3_COMP_2: float, G3_COMP_6: float, G3_COMP_10: float, G3_COMP_15: str, G5_COMP_6: float, G5_COMP_7: float, G5_COMP_8: str, G5_COMP_9: str, G5_COMP_11: float, G5_COMP_12: str, G5_COMP_17: float) -> DG_Result_Reports:
    target_components = ['G5_COMP_1', 'G5_COMP_13', 'G5_COMP_16']
    inputs = {"G3_COMP_2": G3_COMP_2, "G3_COMP_6": G3_COMP_6, "G3_COMP_10": G3_COMP_10, "G3_COMP_15": G3_COMP_15, "G5_COMP_6": G5_COMP_6, "G5_COMP_7": G5_COMP_7, "G5_COMP_8": G5_COMP_8, "G5_COMP_9": G5_COMP_9, "G5_COMP_11": G5_COMP_11, "G5_COMP_12": G5_COMP_12, "G5_COMP_17": G5_COMP_17}
    return execute_calc_content(target_components, inputs)

def calc_content_6(G6_COMP_2: str, G6_COMP_4: float, G6_COMP_6: str, G6_COMP_9: float, G6_COMP_10: float, G6_COMP_11: float) -> DG_Result_Reports:
    target_components = ['G6_COMP_1']
    inputs = {"G6_COMP_2": G6_COMP_2, "G6_COMP_4": G6_COMP_4, "G6_COMP_6": G6_COMP_6, "G6_COMP_9": G6_COMP_9, "G6_COMP_10": G6_COMP_10, "G6_COMP_11": G6_COMP_11}
    return execute_calc_content(target_components, inputs)

def calc_content_7(G7_COMP_3: float, G7_COMP_4: float, G7_COMP_8: float) -> DG_Result_Reports:
    target_components = ['G7_COMP_1', 'G7_COMP_2', 'G7_COMP_7', 'G7_COMP_9']
    inputs = {"G7_COMP_3": G7_COMP_3, "G7_COMP_4": G7_COMP_4, "G7_COMP_8": G7_COMP_8}
    return execute_calc_content(target_components, inputs)

def calc_content_8(G8_COMP_3: float, G8_COMP_4: float, G8_COMP_8: float) -> DG_Result_Reports:
    target_components = ['G8_COMP_1', 'G8_COMP_2', 'G8_COMP_10', 'G8_COMP_11', 'G8_COMP_12', 'G8_COMP_13']
    inputs = {"G8_COMP_3": G8_COMP_3, "G8_COMP_4": G8_COMP_4, "G8_COMP_8": G8_COMP_8}
    return execute_calc_content(target_components, inputs)

def calc_content_9(G8_COMP_8: float, G9_COMP_4: float, G9_COMP_5: str, G9_COMP_8: float, G9_COMP_17: float) -> DG_Result_Reports:
    target_components = ['G9_COMP_1', 'G9_COMP_2', 'G9_COMP_11', 'G9_COMP_13', 'G9_COMP_14']
    inputs = {"G8_COMP_8": G8_COMP_8, "G9_COMP_4": G9_COMP_4, "G9_COMP_5": G9_COMP_5, "G9_COMP_8": G9_COMP_8, "G9_COMP_17": G9_COMP_17}
    return execute_calc_content(target_components, inputs)
