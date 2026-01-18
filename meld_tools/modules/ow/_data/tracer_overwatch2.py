from ....shared.utils.singleton import singleton


@singleton
def all_bones() -> dict:
    return point_bones() | extra_bones()


@singleton
def point_bones() -> dict:
    return {
        "bone_03BD": "OW-UpperArm_Point.L",  # 不明上臂定位骨骼.L
        "bone_0180": "OW-Carpals_Point.L",  # 不明腕部定位骨骼.L
        "bone_03BE": "OW-UpperArm_Point.R",  # 不明上臂定位骨骼.R
        "bone_0181": "OW-Carpals_Point.R",  # 不明腕部定位骨骼.R
        "bone_007D": "OW-Head_Point1",  # 不明头部定位骨骼1
        "bone_05F0": "OW-Head_Point2",  # 不明头部定位骨骼2
        "bone_097F": "OW-Hips_Point2",
        "bone_0984": "OW-Hips_Point3",
        "bone_0985": "OW-Hips_Point4",
        "bone_002C": "OW-Palm_Point1.L",  # 定位手心1.L
        "bone_004A": "OW-Palm_Point1.R",  # 定位手心1.R
    }


@singleton
def extra_bones() -> dict:
    return {
        "bone_2AC9": "OW-DEF-Orbit1.L",
        "bone_2ACA": "OW-DEF-Orbit1.R",
        "bone_2ACB": "OW-DEF-Orbit2.L",
        "bone_2ACC": "OW-DEF-Orbit2.R",
        "bone_008B": "OW-Glasses",
        "bone_0069": "OW-DEF-Glasses_Brow",
        "bone_0090": "OW-DEF-Glasses_Brow1.L",
        "bone_0092": "OW-DEF-Glasses_Brow2.L",
        "bone_0091": "OW-DEF-Glasses_Brow1.R",
        "bone_0093": "OW-DEF-Glasses_Brow2.R",
        "bone_0083": "OW-DEF-Hair1_1",
        "bone_0084": "OW-DEF-Hair1_2",
        "bone_0085": "OW-DEF-Hair1_3",
        "bone_0086": "OW-DEF-Hair2_1",
        "bone_0087": "OW-DEF-Hair2_2",
        "bone_0088": "OW-DEF-Hair2_3",
        "bone_012F": "OW-DEF-Hair3_1",
        "bone_00A1": "OW-DEF-Forearm_Wrist.L",
        "bone_00A2": "OW-DEF-Forearm_Wrist.R",
        "bone_011C": "OW-Weapon_Point.L",
        "bone_011D": "OW-Weapon_Point.R",
        "bone_00EC": "OW-DEF-Collar",
        "bone_0F94": "OW-DEF-Shoulder_Ribbon.L",
        "bone_0F93": "OW-DEF-Shoulder_Ribbon.R",
        "bone_0109": "OW-Bomb_Point",
        "bone_1CCD": "OW-DEF-Back_Ribbon",
        "bone_1CCF": "OW-DEF-Back_Ribbon1_1.L",
        "bone_1CD1": "OW-DEF-Back_Ribbon1_2.L",
        "bone_1CD3": "OW-DEF-Back_Ribbon1_3.L",
        "bone_1CD0": "OW-DEF-Back_Ribbon1_1.R",
        "bone_1CD2": "OW-DEF-Back_Ribbon1_2.R",
        "bone_1CD5": "OW-DEF-Back_Ribbon1_3.R",
        "bone_00ED": "OW-DEF-Collar.L",
        "bone_00EE": "OW-DEF-Collar.R",
        "bone_1CCE": "OW-DEF-Neck_Armor",
        "bone_0237": "OW-DEF-Shoulder.R",
        "bone_041E": "OW-DEF-Waist_Ribbon1_1.L",
        "bone_0421": "OW-DEF-Waist_Ribbon1_2.L",
        "bone_1471": "OW-DEF-Waist_Ribbon1_3.L",
        "bone_041D": "OW-DEF-Waist_Ribbon1_1.R",
        "bone_0422": "OW-DEF-Waist_Ribbon1_2.R",
        "bone_192B": "OW-DEF-Waist_Ribbon1_3.R",
    }


@singleton
def vertex_group() -> set:
    """返回英雄皮肤特有的 Deform 顶点组，方便后续添加英雄皮肤特有骨骼"""
    return {
        "OW-DEF-Orbit1.L",
        "OW-DEF-Orbit1.R",
        "OW-DEF-Orbit2.L",
        "OW-DEF-Orbit2.R",
        "OW-DEF-Glasses_Brow",
        "OW-DEF-Glasses_Brow1.L",
        "OW-DEF-Glasses_Brow2.L",
        "OW-DEF-Glasses_Brow1.R",
        "OW-DEF-Glasses_Brow2.R",
        "OW-DEF-Hair1_1",
        "OW-DEF-Hair1_2",
        "OW-DEF-Hair1_3",
        "OW-DEF-Hair2_1",
        "OW-DEF-Hair2_2",
        "OW-DEF-Hair2_3",
        "OW-DEF-Hair3_1",
        "OW-DEF-Forearm_Wrist.L",
        "OW-DEF-Forearm_Wrist.R",
        "OW-DEF-Collar",
        "OW-DEF-Shoulder_Ribbon.L",
        "OW-DEF-Shoulder_Ribbon.R",
        "OW-DEF-Back_Ribbon",
        "OW-DEF-Back_Ribbon1_1.L",
        "OW-DEF-Back_Ribbon1_2.L",
        "OW-DEF-Back_Ribbon1_3.L",
        "OW-DEF-Back_Ribbon1_1.R",
        "OW-DEF-Back_Ribbon1_2.R",
        "OW-DEF-Back_Ribbon1_3.R",
        "OW-DEF-Collar.L",
        "OW-DEF-Collar.R",
        "OW-DEF-Neck_Armor",
        "OW-DEF-Shoulder.R",
        "OW-DEF-Waist_Ribbon1_1.L",
        "OW-DEF-Waist_Ribbon1_2.L",
        "OW-DEF-Waist_Ribbon1_3.L",
        "OW-DEF-Waist_Ribbon1_1.R",
        "OW-DEF-Waist_Ribbon1_2.R",
        "OW-DEF-Waist_Ribbon1_3.R",
    }


@singleton
def copy_weight_vertex_group() -> dict:
    return {
        "OW-DEF-Forearm_Wrist.L": "DEF-Forearm_2.L",
        "OW-DEF-Forearm_Wrist.R": "DEF-Forearm_2.R",
    }
