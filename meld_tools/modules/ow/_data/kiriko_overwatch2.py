from ....shared.utils.singleton import singleton


@singleton
def all_bones() -> dict:
    return extra_bones()


@singleton
def extra_bones() -> dict:
    return {
        "bone_05D9": "OW-DEF-Hair8_1",
        "bone_0083": "OW-DEF-Hair8_2",
        "bone_3480": "OW-DEF-Hairband",
        "bone_07A9": "OW-DEF-Hair7_1",
        "bone_07B3": "OW-DEF-Hair2_1",
        "bone_07AA": "OW-DEF-Hair6_1",
        "bone_07B4": "OW-DEF-Hair3_1",
        "bone_07AB": "OW-DEF-Hair5_1",
        "bone_0084": "OW-DEF-Hair1_1",
        "bone_07B5": "OW-DEF-Hair4_1",
        "bone_2B12": "OW-DEF-Eyelid_Top4.L",
        "bone_2B15": "OW-DEF-Eyelid_Top4.R",
        "bone_2AC9": "OW-DEF-Orbit1.L",
        "bone_2ACA": "OW-DEF-Orbit1.R",
        "bone_2B10": "OW-DEF-Eyelid_Top2.L",
        "bone_2B11": "OW-DEF-Eyelid_Top3.L",
        "bone_2B13": "OW-DEF-Eyelid_Top2.R",
        "bone_2B14": "OW-DEF-Eyelid_Top3.R",
        "bone_2ACB": "OW-DEF-Orbit2.L",
        "bone_2ACC": "OW-DEF-Orbit2.R",
    }


@singleton
def vertex_group() -> set:
    """返回英雄皮肤特有的 Deform 顶点组，方便后续添加英雄皮肤特有骨骼"""
    return {
        "OW-DEF-Hair8_1",
        "OW-DEF-Hair8_2",
        "OW-DEF-Hairband",
        "OW-DEF-Hair7_1",
        "OW-DEF-Hair2_1",
        "OW-DEF-Hair6_1",
        "OW-DEF-Hair3_1",
        "OW-DEF-Hair5_1",
        "OW-DEF-Hair1_1",
        "OW-DEF-Hair4_1",
        "OW-DEF-Eyelid_Top4.L",
        "OW-DEF-Eyelid_Top4.R",
        "OW-DEF-Orbit1.L",
        "OW-DEF-Orbit1.R",
        "OW-DEF-Eyelid_Top2.L",
        "OW-DEF-Eyelid_Top3.L",
        "OW-DEF-Eyelid_Top2.R",
        "OW-DEF-Eyelid_Top3.R",
        "OW-DEF-Orbit2.L",
        "OW-DEF-Orbit2.R",
    }
