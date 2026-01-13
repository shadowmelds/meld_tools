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
        "bone_002C": "OW-Palm_Point1.L",  # 定位手心1.L
        "bone_002D": "OW-Palm_Point2.L",  # 定位手心2.L
        "bone_002E": "OW-Palm_Point3.L",  # 定位手心3.L
        "bone_0596": "OW-Hips_Point1",
        "bone_097F": "OW-Hips_Point2",
        "bone_0984": "OW-Hips_Point3",
        "bone_0985": "OW-Hips_Point4",
        "bone_0605": "OW-Hips_Point5",
        "bone_0606": "OW-Hips_Point6",
        "bone_0595": "OW-Hips_Point7",
        "bone_004A": "OW-Palm_Point1.R",  # 定位手心1.R
        "bone_004B": "OW-Palm_Point2.R",  # 定位手心2.R
        "bone_002F": "OW-Palm_Point3.R",  # 定位手心3.R
        "bone_03BD": "OW-UpperArm_Point.L",  # 不明上臂定位骨骼.L
        "bone_03BE": "OW-UpperArm_Point.R",  # 不明上臂定位骨骼.R
    }


@singleton
def extra_bones() -> dict:
    return {
        "bone_0709": "OW-DEF-Tweake_Forearm.L",  # 调整肘部.L
        "bone_070A": "OW-DEF-Tweake_Forearm.R",  # 调整肘部1.R
        "bone_00E4": "OW-DEF-Tweake_Thumb2.L",  # 调整拇指2.L
        "bone_00E6": "OW-DEF-Tweake_Thumb1.L",  # 调整拇指1.L
        "bone_00EA": "OW-DEF-Tweake_Pinky.L",  # 调整小指.L
        "bone_00E2": "OW-DEF-Tweake_Thumb3.L",  # 调整拇指3.L
        "bone_00DE": "OW-DEF-Tweake_Thumb4.L",  # 调整拇指4.L
        "bone_0140": "OW-DEF-Needle",  # 针头
        "bone_013E": "OW-DEF-Syringe",  # 针管
        "bone_00E5": "OW-DEF-Tweake_Thumb2.R",  # 调整拇指2.R
        "bone_00E7": "OW-DEF-Tweake_Thumb1.R",  # 调整拇指1.R
        "bone_00EB": "OW-DEF-Tweake_Pinky.R",  # 调整小指.R
        "bone_00E3": "OW-DEF-Tweake_Thumb3.R",  # 调整拇指3.R
        "bone_00DF": "OW-DEF-Tweake_Thumb4.R",  # 调整拇指4.R
        "bone_094F": "OW-DEF-Spine4",  # 调整胸部
        "bone_0954": "OW-DEF-Tweake_Hood.L",  # 调整帽兜.L
        "bone_094C": "OW-DEF-Tweake_Hood.R",  # 调整帽兜.R
        "bone_0952": "OW-DEF-Tweake_Knee.L",  # 调整膝盖.L
        "bone_0950": "OW-DEF-Tweake_Thigh.L",  # 调整大腿.L
        "bone_0953": "OW-DEF-Tweake_Knee.R",  # 调整膝盖.R
        "bone_0951": "OW-DEF-Tweake_Thigh.R",  # 调整大腿.R
        "bone_085E": "OW-DEF-Bag",  # 挎包
        "bone_00A3": "OW-Cloth3_1",  # 衣身3_1
        "bone_00A4": "OW-Cloth3_2",  # 衣身3_2
        "bone_00A5": "OW-Cloth3_3",  # 衣身3_3
        "bone_00A6": "OW-Cloth3_4",  # 衣身3_4
        "bone_0936": "OW-Cloth1_1",  # 衣身1_1
        "bone_0938": "OW-Cloth1_2",  # 衣身1_2
        "bone_0944": "OW-Cloth1_3",  # 衣身1_3
        "bone_0948": "OW-Cloth1_4",  # 衣身1_4
        "bone_093F": "OW-Cloth5_1",  # 衣身5_1
        "bone_093C": "OW-Cloth5_2",  # 衣身5_2
        "bone_0942": "OW-Cloth5_3",  # 衣身5_3
        "bone_0946": "OW-Cloth5_4",  # 衣身5_4
        "bone_0937": "OW-Cloth2_1",  # 衣身2_1
        "bone_093A": "OW-Cloth2_2",  # 衣身2_2
        "bone_0945": "OW-Cloth2_3",  # 衣身2_3
        "bone_0949": "OW-Cloth2_4",  # 衣身2_4
        "bone_0940": "OW-Cloth4_1",  # 衣身4_1
        "bone_093D": "OW-Cloth4_2",  # 衣身4_2
        "bone_0943": "OW-Cloth4_3",  # 衣身4_3
        "bone_0947": "OW-Cloth4_4",  # 衣身4_4
        "bone_008B": "OW-DEF-Loincloth1",  # 裆布1
        "bone_0069": "OW-DEF-Loincloth2",  # 裆布2
        "bone_006A": "OW-DEF-Loincloth3",  # 裆布3
        "bone_012E": "OW-DEF-Kneepad.L",  # 护膝.L
        "bone_012D": "OW-DEF-Kneepad.R",  # 护膝.R
    }


@singleton
def constraint_bones() -> dict:
    return {
        "OW-DEF-Finger_Index_Carpal.L": "FK-Finger_Index_Carpal.L",  # 测试中
        "OW-DEF-Finger_Index_Carpal.R": "FK-Finger_Index_Carpal.R",  # 测试中
        "OW-DEF-Finger_Middle_Carpal.L": "FK-Finger_Middle_Carpal.L",  # 测试中
        "OW-DEF-Finger_Middle_Carpal.R": "FK-Finger_Middle_Carpal.R",  # 测试中
        "OW-DEF-Finger_Ring_Carpal.L": "FK-Finger_Ring_Carpal.L",  # 测试中
        "OW-DEF-Finger_Ring_Carpal.R": "FK-Finger_Ring_Carpal.R",  # 测试中
        "OW-DEF-Finger_Pinky_Carpal.L": "FK-Finger_Pinky_Carpal.L",  # 测试中
        "OW-DEF-Finger_Pinky_Carpal.R": "FK-Finger_Pinky_Carpal.R",  # 测试中
        # 部件
        "OW-DEF-Loincloth1": "FK-Loincloth1",
        "OW-DEF-Loincloth2": "FK-Loincloth2",
        "OW-DEF-Kneepad.L": "Kneepad.L",
        "OW-DEF-Kneepad.R": "Kneepad.R",
    }
