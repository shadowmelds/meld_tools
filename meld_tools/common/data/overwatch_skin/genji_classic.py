from ...utils.singleton import singleton


@singleton
def all_bones() -> dict:
    return extra_bones()


@singleton
def point_bones() -> dict:
    return {
        "": "",
    }


@singleton
def extra_bones() -> dict:
    return {
        "bone_00E8": "OW-DEF-Tweake_Wrist.L",
        "bone_00DE": "OW-DEF-Tweake_Thumb4.L",  # 调整拇指4.L
        "bone_00E4": "OW-DEF-Tweake_Thumb2.L",  # 调整拇指2.L
        "bone_00E6": "OW-DEF-Tweake_Thumb1.L",  # 调整拇指1.L
        "bone_00EA": "OW-DEF-Tweake_Pinky.L",  # 调整小指.L
        "bone_00E2": "OW-DEF-Tweake_Thumb3.L",  # 调整拇指3.L
        "bone_0624": "OW-DEF-Forearm_Armor3.L",
        "bone_0620": "OW-DEF-Forearm_Armor2.L",
        "bone_0622": "OW-DEF-Forearm_Armor1.L",
        "bone_00E9": "OW-DEF-Tweake_Wrist.R",
        "bone_00DF": "OW-DEF-Tweake_Thumb4.R",  # 调整拇指4.R
        "bone_00E5": "OW-DEF-Tweake_Thumb2.R",  # 调整拇指2.R
        "bone_00E7": "OW-DEF-Tweake_Thumb1.R",  # 调整拇指1.R
        "bone_00EB": "OW-DEF-Tweake_Pinky.R",  # 调整小指.R
        "bone_00E3": "OW-DEF-Tweake_Thumb3.R",  # 调整拇指3.R
        "bone_061F": "OW-DEF-Forearm_Armor3.R",
        "bone_0621": "OW-DEF-Forearm_Armor2.R",
        "bone_0623": "OW-DEF-Forearm_Armor1.R",
    }


@singleton
def vertex_group() -> set:
    return {
        "OW-DEF-Tweake_Wrist.L",
        "OW-DEF-Tweake_Thumb4.L",
        "OW-DEF-Tweake_Thumb2.L",
        "OW-DEF-Tweake_Thumb1.L",
        "OW-DEF-Tweake_Pinky.L",
        "OW-DEF-Tweake_Thumb3.L",
        "OW-DEF-Forearm_Armor3.L",
        "OW-DEF-Forearm_Armor2.L",
        "OW-DEF-Forearm_Armor1.L",
        "OW-DEF-Tweake_Wrist.R",
        "OW-DEF-Tweake_Thumb4.R",
        "OW-DEF-Tweake_Thumb2.R",
        "OW-DEF-Tweake_Thumb1.R",
        "OW-DEF-Tweake_Pinky.R",
        "OW-DEF-Tweake_Thumb3.R",
        "OW-DEF-Forearm_Armor3.R",
        "OW-DEF-Forearm_Armor2.R",
        "OW-DEF-Forearm_Armor1.R",
    }


@singleton
def copy_weight_vertex_group() -> dict:
    return {
        "OW-DEF-Tweake_Thumb1.L": "DEF-Finger_Thumb1.L",
        "OW-DEF-Tweake_Thumb2.L": "DEF-Finger_Thumb1.L",
        "OW-DEF-Tweake_Thumb4.L": "DEF-Finger_Thumb2.L",
        "OW-DEF-Tweake_Thumb3.L": "DEF-Finger_Index_Carpal.L",
        "OW-DEF-Tweake_Wrist.L": "DEF-Wrist.L",
        "OW-DEF-Tweake_Pinky.L": "DEF-Finger_Pinky_Carpal.L",
        "OW-DEF-Tweake_Thumb1.R": "DEF-Finger_Thumb1.R",
        "OW-DEF-Tweake_Thumb2.R": "DEF-Finger_Thumb1.R",
        "OW-DEF-Tweake_Thumb4.R": "DEF-Finger_Thumb2.R",
        "OW-DEF-Tweake_Thumb3.R": "DEF-Finger_Index_Carpal.R",
        "OW-DEF-Tweake_Wrist.R": "DEF-Wrist.R",
        "OW-DEF-Tweake_Pinky.R": "DEF-Finger_Pinky_Carpal.R",
    }
