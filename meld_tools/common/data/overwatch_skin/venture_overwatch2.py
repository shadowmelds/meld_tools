from ...utils.singleton import singleton


@singleton
def all_bones() -> dict:
    return point_bones() | extra_bones()


@singleton
def point_bones() -> dict:
    return {
        "bone_0180": "OW-Carpals_Point.L",  # 不明腕部定位骨骼.L
        "bone_0181": "OW-Carpals_Point.R",  # 不明腕部定位骨骼.R
        "bone_007D": "OW-Head_Point1",  # 不明头部定位骨骼1
        "bone_05F0": "OW-Head_Point2",  # 不明头部定位骨骼2
        "bone_097F": "OW-Hips_Point2",
        "bone_0984": "OW-Hips_Point3",
        "bone_0985": "OW-Hips_Point4",
        "bone_0605": "OW-Hips_Point5",
        "bone_0606": "OW-Hips_Point6",
        "bone_004A": "OW-Palm_Point1.R",  # 定位手心1.R
        "bone_004B": "OW-Palm_Point2.R",  # 定位手心2.R
        "bone_002F": "OW-Palm_Point3.R",  # 定位手心3.R
        "bone_002C": "OW-Palm_Point1.L",  # 定位手心1.L
        "bone_002D": "OW-Palm_Point2.L",  # 定位手心2.L
        "bone_002E": "OW-Palm_Point3.L",  # 定位手心3.L
        # 不 ana 与重复
        "bone_011C": "OW-Palm_Parent_Point.L",  # 定位手心父父级.L
        "bone_011D": "OW-Palm_Parent_Point.R",  # 定位手心父父级.R
        "bone_007E": "OW-Head_Point3",  # 不明头部定位骨骼2
    }


@singleton
def extra_bones() -> dict:
    return {
        "bone_0709": "OW-DEF-Tweake_Elbow.L",  # 调整肘部.L
        "bone_0AE2": "OW-DEF-Index_Armor.L",
        "bone_0AE5": "OW-DEF-Middle_Armor.L",
        "bone_00EA": "OW-DEF-Tweake_Pinky.L",  # 调整小指.L
        "bone_0AEB": "OW-DEF-Pinky_Armor.L",
        "bone_0AE8": "OW-DEF-Ring_Armor.L",
        "bone_00DE": "OW-DEF-Tweake_Thumb4.L",  # 调整拇指4.L
        "bone_00E4": "OW-DEF-Tweake_Thumb2.L",  # 调整拇指2.L
        "bone_00E6": "OW-DEF-Tweake_Thumb1.L",  # 调整拇指1.L
        "bone_00E2": "OW-DEF-Tweake_Thumb3.L",  # 调整拇指3.L
        "bone_0506": "OW-DEF-Tweake_Shoulder.L",  # 调整肩部.L
        "bone_14E1": "OW-Collar_Upper.L",
        "bone_070A": "OW-DEF-Tweake_Elbow.R",  # 调整肘部1.R
        "bone_0A96": "OW-DEF-Index_Armor.R",
        "bone_0A97": "OW-DEF-Middle_Armor.R",
        "bone_00EB": "OW-DEF-Tweake_Pinky.R",  # 调整小指.R
        "bone_0A99": "OW-DEF-Pinky_Armor.R",
        "bone_0A98": "OW-DEF-Ring_Armor.R",
        "bone_00DF": "OW-DEF-Tweake_Thumb4.R",  # 调整拇指4.R
        "bone_00E5": "OW-DEF-Tweake_Thumb2.R",  # 调整拇指2.R
        "bone_00E7": "OW-DEF-Tweake_Thumb1.R",  # 调整拇指1.R
        "bone_00E3": "OW-DEF-Tweake_Thumb3.R",  # 调整拇指3.R
        "bone_0507": "OW-DEF-Tweake_Shoulder.R",  # 调整肩部.L
        "bone_14E3": "OW-Collar_Upper.R",
        "bone_076D": "OW-DEF-Earmuff.L",
        "bone_0796": "OW-DEF-Earmuff.R",
        "bone_07A9": "OW-DEF-Hair1_1",
        "bone_07AE": "OW-DEF-Hair1_2",
        "bone_07B3": "OW-DEF-Hair5_1",
        "bone_07B8": "OW-DEF-Hair5_2",
        "bone_07AA": "OW-Hair2",
        "bone_0083": "OW-Hair3",
        "bone_07B4": "OW-Hair4",
        "bone_2B12": "OW-DEF-Eyelash3.L",
        "bone_2B15": "OW-DEF-Eyelash3.R",
        "bone_2AC9": "OW-DEF-EyeBrow_Bottom1.L",
        "bone_2ACA": "OW-DEF-EyeBrow_Bottom1.R",
        "bone_2ACB": "OW-DEF-EyeBrow_Bottom2.L",
        "bone_2ACC": "OW-DEF-EyeBrow_Bottom2.R",
        "bone_2B10": "OW-DEF-Eyelash1.L",
        "bone_2B11": "OW-DEF-Eyelash2.L",
        "bone_2B13": "OW-DEF-Eyelash1.R",
        "bone_2B14": "OW-DEF-Eyelash2.R",
        "bone_14DE": "OW-Collar_Lower.L",
        "bone_14E0": "OW-Collar_Lower.R",
        "bone_06F5": "OW-DEF-Tweake_Knee.L",  # 调整膝盖.L
        "bone_008E": "OW-DEF-Shoe_Thruster2.L",
        "bone_0090": "OW-DEF-Shoe_Thruster1.L",
        "bone_06F6": "OW-DEF-Tweake_Knee.R",  # 调整膝盖.R
        "bone_008F": "OW-DEF-Shoe_Thruster2.R",
        "bone_0091": "OW-DEF-Shoe_Thruster1.R",
        "bone_0094": "OW-DEF-Hips_Quickdraw1",
        "bone_0096": "OW-DEF-Hips_Quickdraw2",
        "bone_14CF": "OW-DEF-Cloth_Left1",
        "bone_14D2": "OW-Cloth_Left2",
        "bone_14D5": "OW-Cloth_Left3",
        "bone_14D8": "OW-Cloth_Left4",
        "bone_14D0": "OW-Cloth_Back1",
        "bone_14D3": "OW-Cloth_Back2",
        "bone_14D6": "OW-Cloth_Back3",
        "bone_14D9": "OW-Cloth_Back4",
        # 装备和武器
        "bone_017A": "",
        "bone_017B": "",
        "bone_017C": "",
        "bone_3B6F": "",
        "bone_3B70": "",
        "bone_008C": "",
        "bone_008D": "",
        "bone_0092": "",
        "bone_0093": "",
        "bone_0095": "",
        "bone_0097": "",
        "bone_04C5": "",
        "bone_011C": "",
        "bone_011D": "",
        "bone_2BAE": "",
        "bone_37DC": "",
        "bone_3C8E": "",
        "bone_0AC9": "",
        "bone_0ACA": "",
        "bone_0098": "",
        "bone_3C8C": "",
        "bone_3C6A": "",
        "bone_3C64": "",
        "bone_3C65": "",
        "bone_3C66": "",
        "bone_3C67": "",
        "bone_3C68": "",
        "bone_3C69": "",
        "bone_0912": "",
        "bone_2C7C": "",
        "bone_006F": "",
        "bone_0070": "",
        "bone_04C9": "",
        "bone_0071": "",
        "bone_04C8": "",
        "bone_04CB": "",
        "bone_0072": "",
        "bone_04CA": "",
        "bone_0A23": "",
        "bone_0A26": "",
        "bone_3B6A": "",
        "bone_3C8D": "",
        "bone_04C7": "",
        "bone_04C6": "",
    }
