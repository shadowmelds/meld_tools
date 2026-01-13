from ...utils.singleton import singleton


@singleton
def all_bones() -> dict:
    return main_bones() | face_bones() | stretch_bones()


@singleton
def main_bones() -> dict:
    return {
        "bone_0000": "OW-root0",
        "bone_0001": "OW-root1",
        "bone_0002": "OW-Torso-Spine1",
        "bone_00C1": "OW-Heel.L",  # 脚跟.L
        "bone_00C2": "OW-Heel.R",  # 脚跟.R
        "bone_0003": "OW-Spine2",  # 非形变腹部
        "bone_0004": "OW-Spine3",  # 非形变肋骨
        "bone_0005": "OW-Spine4",  # 非形变胸部
        "bone_0050": "OW-Shoulder.L",  # 非形变肩部.L
        "bone_000D": "OW-UpperArm.L",  # 非形变上臂.L
        "bone_000E": "OW-Forearm.L",  # 非形变肘部.L
        "bone_001C": "OW-DEF-Wrist.L",  # 手腕.L
        "bone_0020": "OW-DEF-Finger_Middle1.L",  # 中指1.L
        "bone_0021": "OW-DEF-Finger_Middle2.L",  # 中指2.L
        "bone_0022": "OW-DEF-Finger_Middle3.L",  # 中指3.L
        "bone_001D": "OW-DEF-Finger_Index1.L",  # 食指1.L
        "bone_001E": "OW-DEF-Finger_Index2.L",  # 食指2.L
        "bone_001F": "OW-DEF-Finger_Index3.L",  # 食指3.L
        "bone_0026": "OW-DEF-Finger_Ring1.L",  # 无名指1.L
        "bone_0027": "OW-DEF-Finger_Ring2.L",  # 无名指2.L
        "bone_0028": "OW-DEF-Finger_Ring3.L",  # 无名指3.L
        "bone_0029": "OW-DEF-Finger_Thumb1.L",  # 拇指1.L
        "bone_002A": "OW-DEF-Finger_Thumb2.L",  # 拇指2.L
        "bone_002B": "OW-DEF-Finger_Thumb3.L",  # 拇指3.L
        "bone_0023": "OW-DEF-Finger_Pinky1.L",  # 小指1.L
        "bone_0024": "OW-DEF-Finger_Pinky2.L",  # 小指2.L
        "bone_0025": "OW-DEF-Finger_Pinky3.L",  # 小指3.L
        "bone_0035": "OW-Shoulder.R",  # 非形变肩部.R
        "bone_0036": "OW-UpperArm.R",  # 非形变上臂.R
        "bone_0037": "OW-Forearm.R",  # 非形变肘部.R
        "bone_003A": "OW-DEF-Wrist.R",  # 手腕.L
        "bone_003E": "OW-DEF-Finger_Middle1.R",  # 中指1.R
        "bone_003F": "OW-DEF-Finger_Middle2.R",  # 中指2.R
        "bone_0040": "OW-DEF-Finger_Middle3.R",  # 中指3.R
        "bone_003B": "OW-DEF-Finger_Index1.R",  # 食指1.R
        "bone_003C": "OW-DEF-Finger_Index2.R",  # 食指2.R
        "bone_003D": "OW-DEF-Finger_Index3.R",  # 食指3.R
        "bone_0044": "OW-DEF-Finger_Ring1.R",  # 无名指1.R
        "bone_0045": "OW-DEF-Finger_Ring2.R",  # 无名指2.R
        "bone_0046": "OW-DEF-Finger_Ring3.R",  # 无名指3.R
        "bone_0047": "OW-DEF-Finger_Thumb1.R",  # 拇指1.R
        "bone_0048": "OW-DEF-Finger_Thumb2.R",  # 拇指2.R
        "bone_0049": "OW-DEF-Finger_Thumb3.R",  # 拇指3.R
        "bone_0041": "OW-DEF-Finger_Pinky1.R",  # 小指1.R
        "bone_0042": "OW-DEF-Finger_Pinky2.R",  # 小指2.R
        "bone_0043": "OW-DEF-Finger_Pinky3.R",  # 小指3.R
        "bone_0010": "OW-DEF-Neck",  # 脖子
        "bone_0011": "OW-DEF-Head",  # 整个头部的 Parent 骨
        "bone_0397": "OW-Eyelid_Upper.L",  # 眼睑上.L
        "bone_0396": "OW-Eyelid_Lower.L",  # 眼睑下.L
        "bone_0399": "OW-Eyelid_Upper.R",  # 眼睑上.R
        "bone_0398": "OW-Eyelid_Lower.R",  # 眼睑下.R
        "bone_039A": "OW-DEF-Eye.L",  # 眼球.L
        "bone_039B": "OW-DEF-Eye.R",  # 眼球.R
        "bone_000B": "OW-Head_Bottom",  # 头下半脸
        "bone_03B7": "OW-DEF-Teeth_Top",  # 牙齿上
        "bone_03BC": "OW-DEF-Jaw",  # 下巴
        "bone_03B8": "OW-DEF-Teeth_Bottom",  # 牙齿下
        "bone_03BB": "OW-DEF-Tongue1",  # 舌头1
        "bone_03BA": "OW-DEF-Tongue2",  # 舌头2
        "bone_03B9": "OW-DEF-Tongue3",  # 舌头3
        "bone_0053": "OW-Spine1",  # 非形变臀部
        "bone_0055": "OW-Thigh.L",  # 非形变大腿.L
        "bone_0059": "OW-Knee.L",  # 非形变膝盖.L
        "bone_005A": "OW-DEF-Foot.L",  # 脚.L
        "bone_005F": "OW-Thigh.R",  # 非形变大腿.R
        "bone_0063": "OW-Knee.R",  # 非形变膝盖.R
        "bone_0064": "OW-DEF-Foot.R",  # 脚.R
        # 测试中
        "bone_08D5": "OW-DEF-Pupil.L",  # 瞳孔.L
        "bone_0835": "OW-DEF-Finger_Index_Carpal.L",  # 食指腕骨.L
        "bone_0837": "OW-DEF-Finger_Middle_Carpal.L",  # 中指腕骨.L
        "bone_00E0": "OW-DEF-Finger_Pinky_Carpal.L",  # 小指腕骨.L
        "bone_0839": "OW-DEF-Finger_Ring_Carpal.L",  # 无名指腕骨.L
        "bone_0836": "OW-DEF-Finger_Index_Carpal.R",  # 食指腕骨.R
        "bone_0838": "OW-DEF-Finger_Middle_Carpal.R",  # 中指腕骨.R
        "bone_00E1": "OW-DEF-Finger_Pinky_Carpal.R",  # 小指腕骨.R
        "bone_083A": "OW-DEF-Finger_Ring_Carpal.R",  # 无名指腕骨.R
    }


@singleton
def face_bones() -> dict:
    return {
        "bone_0018": "OW-DEF-Eyebrow2.L",  # 眉毛2.L
        "bone_0014": "OW-DEF-Eyebrow2.R",  # 眉毛2.R
        "bone_03AC": "OW-DEF-Lip_Bottom2.L",  # 嘴唇下2.L
        "bone_03B1": "OW-DEF-Lip_Bottom2.R",  # 嘴唇下2.R
        "bone_03AF": "OW-DEF-Lip_Bottom3.L",  # 嘴唇下3.L
        "bone_03B2": "OW-DEF-Lip_Bottom3.R",  # 嘴唇下3.R
        "bone_03AB": "OW-DEF-Lip_Bottom_Mid",  # 嘴唇下.M
        "bone_03B0": "OW-DEF-Lip_Corner.L",  # 嘴角.L
        "bone_03B3": "OW-DEF-Lip_Corner.R",  # 嘴角.R
        "bone_03B6": "OW-DEF-Chin_Mid",  # 下巴.M
        "bone_03AD": "OW-DEF-Chin_Outer.L",  # 下巴外侧.L
        "bone_03AE": "OW-DEF-Chin_Outer.R",  # 下巴外侧.R
        "bone_03A6": "OW-DEF-Cheek_Jaw1.L",  # 脸颊下颚1.L
        "bone_03A7": "OW-DEF-Cheek_Jaw1.R",  # 脸颊下颚1.R
        "bone_03A0": "OW-DEF-Cheek_Jaw2.L",  # 脸颊下颚2.L
        "bone_03A1": "OW-DEF-Cheek_Jaw2.R",  # 脸颊下颚2.R
        "bone_039E": "OW-DEF-Cheek_Mid.L",  # 脸颊中.L
        "bone_039F": "OW-DEF-Cheek_Mid.R",  # 脸颊中.R
        "bone_03A9": "OW-DEF-Lip_Top2.L",  # 嘴唇上2.L
        "bone_03B4": "OW-DEF-Lip_Top2.R",  # 嘴唇上2.R
        "bone_03A8": "OW-DEF-Lip_Top3.L",  # 嘴唇上3.L
        "bone_03B5": "OW-DEF-Lip_Top3.R",  # 嘴唇上3.R
        "bone_03AA": "OW-DEF-Lip_Top_Mid",  # 嘴唇上.M
        "bone_071D": "OW-DEF-Cheek_Mid_Outer.L",  # 脸颊中外侧.L
        "bone_071E": "OW-DEF-Cheek_Mid_Outer.R",  # 脸颊中外侧.R
        "bone_060C": "OW-DEF-Cheek_LaughLine.L",  # 脸颊笑纹.L
        "bone_060D": "OW-DEF-Cheek_LaughLine.R",  # 脸颊笑纹.R
        "bone_038D": "OW-DEF-Eyelid_Bot1.L",  # 眼睑下1.L
        "bone_038E": "OW-DEF-Eyelid_Bot2.L",  # 眼睑下2.L
        "bone_038F": "OW-DEF-Eyelid_Bot3.L",  # 眼睑下3.L
        "bone_0391": "OW-DEF-Eyelid_Bot1.R",  # 眼睑下1.R
        "bone_0390": "OW-DEF-Eyelid_Bot2.R",  # 眼睑下2.R
        "bone_0392": "OW-DEF-Eyelid_Bot3.R",  # 眼睑下3.R
        "bone_038A": "OW-DEF-Eyelid_Top1.L",  # 眼睑上1.L
        "bone_038B": "OW-DEF-Eyelid_Top2.L",  # 眼睑上2.L
        "bone_038C": "OW-DEF-Eyelid_Top3.L",  # 眼睑上3.L
        "bone_0393": "OW-DEF-Eyelid_Top1.R",  # 眼睑上1.R
        "bone_0394": "OW-DEF-Eyelid_Top2.R",  # 眼睑上2.R
        "bone_0395": "OW-DEF-Eyelid_Top3.R",  # 眼睑上3.R
        "bone_0017": "OW-DEF-Eyebrow1.L",  # 眉毛1.L
        "bone_0015": "OW-DEF-Eyebrow1.R",  # 眉毛1.R
        "bone_0019": "OW-DEF-Eyebrow3.L",  # 眉毛3.L
        "bone_0013": "OW-DEF-Eyebrow3.R",  # 眉毛3.R
        "bone_0385": "OW-DEF-Eyebrow4.L",  # 眉毛4.L
        "bone_0384": "OW-DEF-Eyebrow4.R",  # 眉毛4.R
        "bone_0016": "OW-DEF-Eyebrow_Mid",  # 眉毛.M
        "bone_03A4": "OW-DEF-Cheek_Mid_Inner.L",  # 脸颊中内侧.L
        "bone_03A5": "OW-DEF-Cheek_Mid_Inner.R",  # 脸颊中内侧.L
        "bone_0008": "OW-DEF-Nose",  # 鼻尖
        "bone_0009": "OW-DEF-Nose.L",  # 鼻子.L
        "bone_000A": "OW-DEF-Nose.R",  # 鼻子.R
        "bone_0006": "OW-DEF-Eyelid_Corner_Inner.L",  # 眼睑角内.L
        "bone_0387": "OW-DEF-Eyelid_Corner_Inner.R",  # 眼睑角内.R
        "bone_0007": "OW-DEF-Eyelid_Corner_Outer.L",  # 眼睑角外.L
        "bone_0386": "OW-DEF-Eyelid_Corner_Outer.R",  # 眼睑角外.R
        "bone_0388": "OW-DEF-Nose_Bridge.L",  # 鼻梁.L
        "bone_0389": "OW-DEF-Nose_Bridge.R",  # 鼻梁.R
        "bone_0608": "OW-DEF-Cheek_Upper_Inner.L",  # 脸颊上内侧.L
        "bone_0609": "OW-DEF-Cheek_Upper_Inner.R",  # 脸颊上内侧.R
        "bone_060A": "OW-DEF-Cheek_Upper_Outer.L",  # 脸颊上外侧.L
        "bone_060B": "OW-DEF-Cheek_Upper_Outer.R",  # 脸颊上外侧.R
        "bone_03A2": "OW-DEF-Cheek_Upper_Middle.L",  # 脸颊上中.L
        "bone_03A3": "OW-DEF-Cheek_Upper_Middle.R",  # 脸颊上中.R
    }


@singleton
def stretch_bones() -> dict:
    return {
        "bone_0052": "OW-DEF-Spine2",  # 腹部
        "bone_0051": "OW-DEF-Spine3",  # 肋骨
        "bone_0031": "OW-DEF-UpperArm_1.L",  # 上臂1.L
        "bone_0030": "OW-DEF-Forearm_3.L",  # 肘部3.L
        "bone_001B": "OW-DEF-Forearm_2.L",  # 肘部2.L
        "bone_001A": "OW-DEF-Forearm_1.L",  # 肘部1.L
        "bone_004F": "OW-DEF-UpperArm_3.L",  # 上臂3.L
        "bone_0032": "OW-DEF-UpperArm_2.L",  # 上臂2.L
        "bone_0034": "OW-DEF-Shoulder.L",  # 肩部.L
        "bone_004D": "OW-DEF-UpperArm_1.R",  # 上臂1.R
        "bone_004C": "OW-DEF-Forearm_3.R",  # 肘部3.R
        "bone_0039": "OW-DEF-Forearm_2.R",  # 肘部2.R
        "bone_0038": "OW-DEF-Forearm_1.R",  # 肘部2.R
        "bone_0033": "OW-DEF-UpperArm_3.R",  # 上臂3.R
        "bone_004E": "OW-DEF-UpperArm_2.R",  # 上臂2.R
        "bone_000C": "OW-DEF-Shoulder.R",  # 肩部.R
        "bone_0012": "OW-DEF-Head_Top",  # 头顶
        "bone_000F": "OW-DEF-Spine4",  # 胸部
        "bone_0056": "OW-DEF-Thigh_1.L",  # 大腿1.L
        "bone_005B": "OW-DEF-Toes.L",  # 脚趾.L
        "bone_005E": "OW-DEF-Knee_3.L",  # 膝盖3.L
        "bone_005D": "OW-DEF-Knee_2.L",  # 膝盖2.L
        "bone_005C": "OW-DEF-Knee_1.L",  # 膝盖1.L
        "bone_0058": "OW-DEF-Thigh_3.L",  # 大腿3.L
        "bone_0057": "OW-DEF-Thigh_2.L",  # 大腿2.L
        "bone_0061": "OW-DEF-Thigh_2.R",  # 大腿2.R
        "bone_0060": "OW-DEF-Thigh_1.R",  # 大腿1.R
        "bone_0065": "OW-DEF-Toes.R",  # 脚趾.R
        "bone_0068": "OW-DEF-Knee_3.R",  # 膝盖2.R
        "bone_0067": "OW-DEF-Knee_2.R",  # 膝盖2.R
        "bone_0066": "OW-DEF-Knee_1.R",  # 膝盖1.R
        "bone_0062": "OW-DEF-Thigh_3.R",  # 大腿3.R
        "bone_0054": "OW-DEF-Spine1",  # 臀部
    }


@singleton
def constraint_bones() -> dict:
    return {
        "OW-root1": "root",
        "OW-DEF-Head": "FK-Head",
        "OW-DEF-Neck": "FK-Neck",
        "OW-Spine4": "FK-Spine4",
        "OW-Spine3": "FK-Spine3",
        "OW-Spine2": "FK-Spine2",
        "OW-Spine1": "HIP-Spine1",
        "OW-Torso-Spine1": "TORSO-Spine1",
        "OW-Shoulder.L": "FK-Shoulder.L",
        "OW-Shoulder.R": "FK-Shoulder.R",
        "OW-UpperArm.L": "FK-UpperArm.L",
        "OW-UpperArm.R": "FK-UpperArm.R",
        "OW-Forearm.L": "FK-Forearm.L",
        "OW-Forearm.R": "FK-Forearm.R",
        "OW-DEF-Wrist.L": "FK-Wrist.L",
        "OW-DEF-Wrist.R": "FK-Wrist.R",
        "OW-Thigh.L": "FK-Thigh.L",
        "OW-Thigh.R": "FK-Thigh.R",
        "OW-Knee.L": "FK-Knee.L",
        "OW-Knee.R": "FK-Knee.R",
        "OW-DEF-Foot.L": "FK-W-Foot.L",
        "OW-DEF-Foot.R": "FK-W-Foot.R",
        "OW-DEF-Toes.L": "FK-Toes.L",
        "OW-DEF-Toes.R": "FK-Toes.R",
        # Finger:
        "OW-DEF-Finger_Thumb1.L": "FK-Finger_Thumb1.L",
        "OW-DEF-Finger_Thumb2.L": "FK-Finger_Thumb2.L",
        "OW-DEF-Finger_Thumb3.L": "FK-Finger_Thumb3.L",
        "OW-DEF-Finger_Index1.L": "FK-Finger_Index1.L",
        "OW-DEF-Finger_Index2.L": "FK-Finger_Index2.L",
        "OW-DEF-Finger_Index3.L": "FK-Finger_Index3.L",
        "OW-DEF-Finger_Middle1.L": "FK-Finger_Middle1.L",
        "OW-DEF-Finger_Middle2.L": "FK-Finger_Middle2.L",
        "OW-DEF-Finger_Middle3.L": "FK-Finger_Middle3.L",
        "OW-DEF-Finger_Ring1.L": "FK-Finger_Ring1.L",
        "OW-DEF-Finger_Ring2.L": "FK-Finger_Ring2.L",
        "OW-DEF-Finger_Ring3.L": "FK-Finger_Ring3.L",
        "OW-DEF-Finger_Pinky1.L": "FK-Finger_Pinky1.L",
        "OW-DEF-Finger_Pinky2.L": "FK-Finger_Pinky2.L",
        "OW-DEF-Finger_Pinky3.L": "FK-Finger_Pinky3.L",
        "OW-DEF-Finger_Thumb1.R": "FK-Finger_Thumb1.R",
        "OW-DEF-Finger_Thumb2.R": "FK-Finger_Thumb2.R",
        "OW-DEF-Finger_Thumb3.R": "FK-Finger_Thumb3.R",
        "OW-DEF-Finger_Index1.R": "FK-Finger_Index1.R",
        "OW-DEF-Finger_Index2.R": "FK-Finger_Index2.R",
        "OW-DEF-Finger_Index3.R": "FK-Finger_Index3.R",
        "OW-DEF-Finger_Middle1.R": "FK-Finger_Middle1.R",
        "OW-DEF-Finger_Middle2.R": "FK-Finger_Middle2.R",
        "OW-DEF-Finger_Middle3.R": "FK-Finger_Middle3.R",
        "OW-DEF-Finger_Ring1.R": "FK-Finger_Ring1.R",
        "OW-DEF-Finger_Ring2.R": "FK-Finger_Ring2.R",
        "OW-DEF-Finger_Ring3.R": "FK-Finger_Ring3.R",
        "OW-DEF-Finger_Pinky1.R": "FK-Finger_Pinky1.R",
        "OW-DEF-Finger_Pinky2.R": "FK-Finger_Pinky2.R",
        "OW-DEF-Finger_Pinky3.R": "FK-Finger_Pinky3.R",
        # Head:
        "OW-DEF-Eyelid_Top1.L": "Eyelid_Top1.L",
        "OW-DEF-Eyelid_Top2.L": "Eyelid_Top2.L",
        "OW-DEF-Eyelid_Top3.L": "Eyelid_Top3.L",
        "OW-DEF-Eyelid_Top1.R": "Eyelid_Top1.R",
        "OW-DEF-Eyelid_Top2.R": "Eyelid_Top2.R",
        "OW-DEF-Eyelid_Top3.R": "Eyelid_Top3.R",
        "OW-DEF-Eye.L": "Eye.L",
        "OW-DEF-Eyebrow2.L": "Eyebrow2.L",
        "OW-DEF-Eyebrow2.R": "Eyebrow2.R",
        "OW-Head_Bottom": "Head_Bottom",
        "OW-DEF-Teeth_Top": "Teeth_Top",
        "OW-DEF-Jaw": "Jaw",
        "OW-DEF-Teeth_Bottom": "Teeth_Bottom",
        "OW-DEF-Tongue1": "FK-Tongue1",
        "OW-DEF-Tongue2": "FK-Tongue2",
        "OW-DEF-Tongue3": "FK-Tongue3",
        "OW-DEF-Lip_Bottom2.L": "Lip_Bottom2.L",
        "OW-DEF-Lip_Bottom2.R": "Lip_Bottom2.R",
        "OW-DEF-Lip_Bottom3.L": "Lip_Bottom3.L",
        "OW-DEF-Lip_Bottom3.R": "Lip_Bottom3.R",
        "OW-DEF-Lip_Bottom_Mid": "Lip_Bottom_Mid",
        "OW-DEF-Lip_Corner.L": "Lip_Corner.L",
        "OW-DEF-Lip_Corner.R": "Lip_Corner.R",
        "OW-DEF-Chin_Mid": "Chin_Mid",
        "OW-DEF-Chin_Outer.L": "Chin_Outer.L",
        "OW-DEF-Chin_Outer.R": "Chin_Outer.R",
        "OW-DEF-Cheek_Jaw1.L": "Cheek_Jaw1.L",
        "OW-DEF-Cheek_Jaw1.R": "Cheek_Jaw1.R",
        "OW-DEF-Cheek_Jaw2.L": "Cheek_Jaw2.L",
        "OW-DEF-Cheek_Jaw2.R": "Cheek_Jaw2.R",
        "OW-DEF-Cheek_Mid.L": "Cheek_Mid.L",
        "OW-DEF-Cheek_Mid.R": "Cheek_Mid.R",
        "OW-DEF-Lip_Top2.L": "Lip_Top2.L",
        "OW-DEF-Lip_Top2.R": "Lip_Top2.R",
        "OW-DEF-Lip_Top3.L": "Lip_Top3.L",
        "OW-DEF-Lip_Top3.R": "Lip_Top3.R",
        "OW-DEF-Lip_Top_Mid": "Lip_Top_Mid",
        "OW-DEF-Cheek_Mid_Outer.L": "Cheek_Mid_Outer.L",
        "OW-DEF-Cheek_Mid_Outer.R": "Cheek_Mid_Outer.R",
        "OW-DEF-Cheek_LaughLine.L": "Cheek_LaughLine.L",
        "OW-DEF-Cheek_LaughLine.R": "Cheek_LaughLine.R",
        "OW-DEF-Eyelid_Bot1.L": "Eyelid_Bot1.L",
        "OW-DEF-Eyelid_Bot2.L": "Eyelid_Bot2.L",
        "OW-DEF-Eyelid_Bot3.L": "Eyelid_Bot3.L",
        "OW-DEF-Eyelid_Bot1.R": "Eyelid_Bot1.R",
        "OW-DEF-Eyelid_Bot2.R": "Eyelid_Bot2.R",
        "OW-DEF-Eyelid_Bot3.R": "Eyelid_Bot3.R",
        "OW-DEF-Eyebrow1.L": "Eyebrow1.L",
        "OW-DEF-Eyebrow1.R": "Eyebrow1.R",
        "OW-DEF-Eyebrow3.L": "Eyebrow3.L",
        "OW-DEF-Eyebrow3.R": "Eyebrow3.R",
        "OW-DEF-Eyebrow4.L": "Eyebrow4.L",
        "OW-DEF-Eyebrow4.R": "Eyebrow4.R",
        "OW-DEF-Eyebrow_Mid": "Eyebrow_Mid",
        "OW-DEF-Cheek_Mid_Inner.L": "Cheek_Mid_Inner.L",
        "OW-DEF-Cheek_Mid_Inner.R": "Cheek_Mid_Inner.R",
        "OW-DEF-Nose": "Nose",
        "OW-DEF-Nose.L": "Nose.L",
        "OW-DEF-Nose.R": "Nose.R",
        "OW-DEF-Eyelid_Corner_Inner.L": "Eyelid_Corner_Inner.L",
        "OW-DEF-Eyelid_Corner_Inner.R": "Eyelid_Corner_Inner.R",
        "OW-DEF-Eyelid_Corner_Outer.L": "Eyelid_Corner_Outer.L",
        "OW-DEF-Eyelid_Corner_Outer.R": "Eyelid_Corner_Outer.R",
        "OW-DEF-Nose_Bridge.L": "Nose_Bridge.L",
        "OW-DEF-Nose_Bridge.R": "Nose_Bridge.R",
        "OW-DEF-Cheek_Upper_Inner.L": "Cheek_Upper_Inner.L",
        "OW-DEF-Cheek_Upper_Inner.R": "Cheek_Upper_Inner.R",
        "OW-DEF-Cheek_Upper_Outer.L": "Cheek_Upper_Outer.L",
        "OW-DEF-Cheek_Upper_Outer.R": "Cheek_Upper_Outer.R",
        "OW-DEF-Cheek_Upper_Middle.L": "Cheek_Upper_Middle.L",
        "OW-DEF-Cheek_Upper_Middle.R": "Cheek_Upper_Middle.R",
    }


@singleton
def vertex_group() -> set:
    return {
        # 躯干
        "DEF-Neck",
        "DEF-Head",
        "DEF-Shoulder.L",
        "DEF-UpperArm_1.L",
        "DEF-UpperArm_2.L",
        "DEF-Forearm_1.L",
        "DEF-Forearm_2.L",
        "DEF-Wrist.L",
        "DEF-Shoulder.R",
        "DEF-UpperArm_1.R",
        "DEF-UpperArm_2.R",
        "DEF-Forearm_1.R",
        "DEF-Forearm_2.R",
        "DEF-Wrist.R",
        "DEF-Spine1",
        "DEF-Spine2",
        "DEF-Spine3",
        "DEF-Spine4",
        "DEF-Thigh_1.L",
        "DEF-Thigh_2.L",
        "DEF-Knee_1.L",
        "DEF-Knee_2.L",
        "DEF-Foot.L",
        "DEF-Toes.L",
        "DEF-Thigh_1.R",
        "DEF-Thigh_2.R",
        "DEF-Knee_1.R",
        "DEF-Knee_2.R",
        "DEF-Foot.R",
        "DEF-Toes.R",
        # 手部
        "DEF-Finger_Thumb1.L",
        "DEF-Finger_Thumb2.L",
        "DEF-Finger_Thumb3.L",
        "DEF-Finger_Index_Carpal.L",
        "DEF-Finger_Index1.L",
        "DEF-Finger_Index2.L",
        "DEF-Finger_Index3.L",
        "DEF-Finger_Middle_Carpal.L",
        "DEF-Finger_Middle1.L",
        "DEF-Finger_Middle2.L",
        "DEF-Finger_Middle3.L",
        "DEF-Finger_Ring_Carpal.L",
        "DEF-Finger_Ring1.L",
        "DEF-Finger_Ring2.L",
        "DEF-Finger_Ring3.L",
        "DEF-Finger_Pinky_Carpal.L",
        "DEF-Finger_Pinky1.L",
        "DEF-Finger_Pinky2.L",
        "DEF-Finger_Pinky3.L",
        "DEF-Finger_Thumb1.R",
        "DEF-Finger_Thumb2.R",
        "DEF-Finger_Thumb3.R",
        "DEF-Finger_Index_Carpal.R",
        "DEF-Finger_Index1.R",
        "DEF-Finger_Index2.R",
        "DEF-Finger_Index3.R",
        "DEF-Finger_Middle_Carpal.R",
        "DEF-Finger_Middle1.R",
        "DEF-Finger_Middle2.R",
        "DEF-Finger_Middle3.R",
        "DEF-Finger_Ring_Carpal.R",
        "DEF-Finger_Ring1.R",
        "DEF-Finger_Ring2.R",
        "DEF-Finger_Ring3.R",
        "DEF-Finger_Pinky_Carpal.R",
        "DEF-Finger_Pinky1.R",
        "DEF-Finger_Pinky2.R",
        "DEF-Finger_Pinky3.R",
        # 脸
        "DEF-Eye.L",
        "DEF-Teeth_Top",
        "DEF-Cheek_Jaw1.L",
        "DEF-Cheek_Jaw1.R",
        "DEF-Cheek_Jaw2.L",
        "DEF-Cheek_Jaw2.R",
        "DEF-Cheek_LaughLine.L",
        "DEF-Cheek_LaughLine.R",
        "DEF-Cheek_Mid_Outer.L",
        "DEF-Cheek_Mid_Outer.R",
        "DEF-Jaw",
        "DEF-Teeth_Bottom",
        "DEF-Tongue1",
        "DEF-Tongue2",
        "DEF-Tongue3",
        "DEF-Chin_Mid",
        "DEF-Chin_Outer.L",
        "DEF-Chin_Outer.R",
        "DEF-Cheek_Mid.L",
        "DEF-Cheek_Mid.R",
        "DEF-Lip_Corner.L",
        "DEF-Lip_Corner.R",
        "DEF-Lip_Bottom2.L",
        "DEF-Lip_Bottom2.R",
        "DEF-Lip_Bottom3.L",
        "DEF-Lip_Bottom3.R",
        "DEF-Lip_Bottom_Mid",
        "DEF-Lip_Top_Mid",
        "DEF-Lip_Top3.L",
        "DEF-Lip_Top3.R",
        "DEF-Lip_Top2.L",
        "DEF-Lip_Top2.R",
        "DEF-Eyelid_Bot2.L",
        "DEF-Eyelid_Bot2.R",
        "DEF-Eyelid_Top2.L",
        "DEF-Eyelid_Top2.R",
        "DEF-Eye.R",
        "DEF-Eyelid_Top1.L",
        "DEF-Eyelid_Top1.R",
        "DEF-Eyelid_Top3.L",
        "DEF-Eyelid_Top3.R",
        "DEF-Cheek_Upper_Middle.L",
        "DEF-Cheek_Upper_Middle.R",
        "DEF-Eyelid_Bot1.L",
        "DEF-Eyelid_Bot1.R",
        "DEF-Cheek_Upper_Outer.L",
        "DEF-Cheek_Upper_Outer.R",
        "DEF-Cheek_Upper_Inner.L",
        "DEF-Cheek_Upper_Inner.R",
        "DEF-Nose_Bridge.L",
        "DEF-Nose_Bridge.R",
        "DEF-Nose_Tip",
        "DEF-Nose.L",
        "DEF-Nose.R",
        "DEF-Eyelid_Bot3.L",
        "DEF-Eyelid_Bot3.R",
        "DEF-Cheek_Mid_Inner.L",
        "DEF-Cheek_Mid_Inner.R",
        "DEF-Eyelid_Corner_Inner.L",
        "DEF-Eyelid_Corner_Inner.R",
        "DEF-Eyelid_Corner_Outer.L",
        "DEF-Eyelid_Corner_Outer.R",
        "DEF-Eyebrow2.L",
        "DEF-Eyebrow2.R",
        "DEF-Eyebrow1.L",
        "DEF-Eyebrow1.R",
        "DEF-Eyebrow3.L",
        "DEF-Eyebrow3.R",
        "DEF-Eyebrow4.L",
        "DEF-Eyebrow4.R",
        "DEF-Eyebrow_Mid",
    }


@singleton
def copy_weight_vertex_group() -> dict:
    return {
        "OW-DEF-Cheek_Jaw1.L": "DEF-Cheek_Jaw1.L",
        "OW-DEF-Cheek_Jaw1.R": "DEF-Cheek_Jaw1.R",
        "OW-DEF-Cheek_Jaw2.L": "DEF-Cheek_Jaw2.L",
        "OW-DEF-Cheek_Jaw2.R": "DEF-Cheek_Jaw2.R",
        "OW-DEF-Cheek_LaughLine.L": "DEF-Cheek_LaughLine.L",
        "OW-DEF-Cheek_LaughLine.R": "DEF-Cheek_LaughLine.R",
        "OW-DEF-Cheek_Mid.L": "DEF-Cheek_Mid.L",
        "OW-DEF-Cheek_Mid.R": "DEF-Cheek_Mid.R",
        "OW-DEF-Cheek_Mid_Inner.L": "DEF-Cheek_Mid_Inner.L",
        "OW-DEF-Cheek_Mid_Inner.R": "DEF-Cheek_Mid_Inner.R",
        "OW-DEF-Cheek_Mid_Outer.L": "DEF-Cheek_Mid_Outer.L",
        "OW-DEF-Cheek_Mid_Outer.R": "DEF-Cheek_Mid_Outer.R",
        "OW-DEF-Cheek_Upper_Inner.L": "DEF-Cheek_Upper_Inner.L",
        "OW-DEF-Cheek_Upper_Inner.R": "DEF-Cheek_Upper_Inner.R",
        "OW-DEF-Cheek_Upper_Middle.L": "DEF-Cheek_Upper_Middle.L",
        "OW-DEF-Cheek_Upper_Middle.R": "DEF-Cheek_Upper_Middle.R",
        "OW-DEF-Cheek_Upper_Outer.L": "DEF-Cheek_Upper_Outer.L",
        "OW-DEF-Cheek_Upper_Outer.R": "DEF-Cheek_Upper_Outer.R",
        "OW-DEF-Chin_Mid": "DEF-Chin_Mid",
        "OW-DEF-Chin_Outer.L": "DEF-Chin_Outer.L",
        "OW-DEF-Chin_Outer.R": "DEF-Chin_Outer.R",
        "OW-DEF-Eye.L": "DEF-Eye.L",
        "OW-DEF-Eye.R": "DEF-Eye.R",
        "OW-DEF-Eyebrow1.L": "DEF-Eyebrow1.L",
        "OW-DEF-Eyebrow1.R": "DEF-Eyebrow1.R",
        "OW-DEF-Eyebrow2.L": "DEF-Eyebrow2.L",
        "OW-DEF-Eyebrow2.R": "DEF-Eyebrow2.R",
        "OW-DEF-Eyebrow3.L": "DEF-Eyebrow3.L",
        "OW-DEF-Eyebrow3.R": "DEF-Eyebrow3.R",
        "OW-DEF-Eyebrow4.L": "DEF-Eyebrow4.L",
        "OW-DEF-Eyebrow4.R": "DEF-Eyebrow4.R",
        "OW-DEF-Eyebrow_Mid": "DEF-Eyebrow_Mid",
        "OW-DEF-Eyelid_Bot1.L": "DEF-Eyelid_Bot1.L",
        "OW-DEF-Eyelid_Bot1.R": "DEF-Eyelid_Bot1.R",
        "OW-DEF-Eyelid_Bot2.L": "DEF-Eyelid_Bot2.L",
        "OW-DEF-Eyelid_Bot2.R": "DEF-Eyelid_Bot2.R",
        "OW-DEF-Eyelid_Bot3.L": "DEF-Eyelid_Bot3.L",
        "OW-DEF-Eyelid_Bot3.R": "DEF-Eyelid_Bot3.R",
        "OW-DEF-Eyelid_Corner_Inner.L": "DEF-Eyelid_Corner_Inner.L",
        "OW-DEF-Eyelid_Corner_Inner.R": "DEF-Eyelid_Corner_Inner.R",
        "OW-DEF-Eyelid_Corner_Outer.L": "DEF-Eyelid_Corner_Outer.L",
        "OW-DEF-Eyelid_Corner_Outer.R": "DEF-Eyelid_Corner_Outer.R",
        "OW-DEF-Eyelid_Lower.L": "",
        "OW-DEF-Eyelid_Lower.R": "",
        "OW-DEF-Eyelid_Top1.L": "DEF-Eyelid_Top1.L",
        "OW-DEF-Eyelid_Top1.R": "DEF-Eyelid_Top1.R",
        "OW-DEF-Eyelid_Top2.L": "DEF-Eyelid_Top2.L",
        "OW-DEF-Eyelid_Top2.R": "DEF-Eyelid_Top2.R",
        "OW-DEF-Eyelid_Top3.L": "DEF-Eyelid_Top3.L",
        "OW-DEF-Eyelid_Top3.R": "DEF-Eyelid_Top3.R",
        "OW-DEF-Eyelid_Upper.L": "",
        "OW-DEF-Eyelid_Upper.R": "",
        "OW-DEF-Finger_Index1.L": "DEF-Finger_Index1.L",
        "OW-DEF-Finger_Index1.R": "DEF-Finger_Index1.R",
        "OW-DEF-Finger_Index2.L": "DEF-Finger_Index2.L",
        "OW-DEF-Finger_Index2.R": "DEF-Finger_Index2.R",
        "OW-DEF-Finger_Index3.L": "DEF-Finger_Index3.L",
        "OW-DEF-Finger_Index3.R": "DEF-Finger_Index3.R",
        "OW-DEF-Finger_Middle1.L": "DEF-Finger_Middle1.L",
        "OW-DEF-Finger_Middle1.R": "DEF-Finger_Middle1.R",
        "OW-DEF-Finger_Middle2.L": "DEF-Finger_Middle2.L",
        "OW-DEF-Finger_Middle2.R": "DEF-Finger_Middle2.R",
        "OW-DEF-Finger_Middle3.L": "DEF-Finger_Middle3.L",
        "OW-DEF-Finger_Middle3.R": "DEF-Finger_Middle3.R",
        "OW-DEF-Finger_Pinky1.L": "DEF-Finger_Pinky1.L",
        "OW-DEF-Finger_Pinky1.R": "DEF-Finger_Pinky1.R",
        "OW-DEF-Finger_Pinky2.L": "DEF-Finger_Pinky2.L",
        "OW-DEF-Finger_Pinky2.R": "DEF-Finger_Pinky2.R",
        "OW-DEF-Finger_Pinky3.L": "DEF-Finger_Pinky3.L",
        "OW-DEF-Finger_Pinky3.R": "DEF-Finger_Pinky3.R",
        "OW-DEF-Finger_Ring1.L": "DEF-Finger_Ring1.L",
        "OW-DEF-Finger_Ring1.R": "DEF-Finger_Ring1.R",
        "OW-DEF-Finger_Ring2.L": "DEF-Finger_Ring2.L",
        "OW-DEF-Finger_Ring2.R": "DEF-Finger_Ring2.R",
        "OW-DEF-Finger_Ring3.L": "DEF-Finger_Ring3.L",
        "OW-DEF-Finger_Ring3.R": "DEF-Finger_Ring3.R",
        "OW-DEF-Finger_Thumb1.L": "DEF-Finger_Thumb1.L",
        "OW-DEF-Finger_Thumb1.R": "DEF-Finger_Thumb1.R",
        "OW-DEF-Finger_Thumb2.L": "DEF-Finger_Thumb2.L",
        "OW-DEF-Finger_Thumb2.R": "DEF-Finger_Thumb2.R",
        "OW-DEF-Finger_Thumb3.L": "DEF-Finger_Thumb3.L",
        "OW-DEF-Finger_Thumb3.R": "DEF-Finger_Thumb3.R",
        "OW-DEF-Finger_Index_Carpal.L": "DEF-Finger_Index_Carpal.L",
        "OW-DEF-Finger_Middle_Carpal.L": "DEF-Finger_Middle_Carpal.L",
        "OW-DEF-Finger_Ring_Carpal.L": "DEF-Finger_Ring_Carpal.L",
        "OW-DEF-Finger_Pinky_Carpal.L": "DEF-Finger_Pinky_Carpal.L",
        "OW-DEF-Finger_Index_Carpal.R": "DEF-Finger_Index_Carpal.R",
        "OW-DEF-Finger_Middle_Carpal.R": "DEF-Finger_Middle_Carpal.R",
        "OW-DEF-Finger_Ring_Carpal.R": "DEF-Finger_Ring_Carpal.R",
        "OW-DEF-Finger_Pinky_Carpal.R": "DEF-Finger_Pinky_Carpal.R",
        "OW-DEF-Foot.L": "DEF-Foot.L",
        "OW-DEF-Foot.R": "DEF-Foot.R",
        "OW-DEF-Forearm_1.L": "DEF-Forearm_1.L",
        "OW-DEF-Forearm_1.R": "DEF-Forearm_1.R",
        "OW-DEF-Forearm_2.L": "DEF-Forearm_2.L",
        "OW-DEF-Forearm_2.R": "DEF-Forearm_2.R",
        "OW-DEF-Forearm_3.L": "DEF-Forearm_2.L",
        "OW-DEF-Forearm_3.R": "DEF-Forearm_2.R",
        "OW-DEF-Head": "DEF-Head",
        "OW-DEF-Head_Top": "DEF-Head_Top",  # "DEF-Head"
        "OW-DEF-Jaw": "DEF-Jaw",
        "OW-DEF-Knee_1.L": "DEF-Knee_1.L",
        "OW-DEF-Knee_1.R": "DEF-Knee_1.R",
        "OW-DEF-Knee_2.L": "DEF-Knee_2.L",
        "OW-DEF-Knee_2.R": "DEF-Knee_2.R",
        "OW-DEF-Knee_3.L": "DEF-Knee_2.L",
        "OW-DEF-Knee_3.R": "DEF-Knee_2.R",
        "OW-DEF-Lip_Bottom2.L": "DEF-Lip_Bottom2.L",
        "OW-DEF-Lip_Bottom2.R": "DEF-Lip_Bottom2.R",
        "OW-DEF-Lip_Bottom3.L": "DEF-Lip_Bottom3.L",
        "OW-DEF-Lip_Bottom3.R": "DEF-Lip_Bottom3.R",
        "OW-DEF-Lip_Bottom_Mid": "DEF-Lip_Bottom_Mid",
        "OW-DEF-Lip_Corner.L": "DEF-Lip_Corner.L",
        "OW-DEF-Lip_Corner.R": "DEF-Lip_Corner.R",
        "OW-DEF-Lip_Top2.L": "DEF-Lip_Top2.L",
        "OW-DEF-Lip_Top2.R": "DEF-Lip_Top2.R",
        "OW-DEF-Lip_Top3.L": "DEF-Lip_Top3.L",
        "OW-DEF-Lip_Top3.R": "DEF-Lip_Top3.R",
        "OW-DEF-Lip_Top_Mid": "DEF-Lip_Top_Mid",
        "OW-DEF-Neck": "DEF-Neck",
        "OW-DEF-Nose.L": "DEF-Nose.L",
        "OW-DEF-Nose.R": "DEF-Nose.R",
        "OW-DEF-Nose_Bridge.L": "DEF-Nose_Bridge.L",
        "OW-DEF-Nose_Bridge.R": "DEF-Nose_Bridge.R",
        "OW-DEF-Nose_Tip": "DEF-Nose_Tip",
        "OW-DEF-Shoulder.L": "DEF-Shoulder.L",
        "OW-DEF-Shoulder.R": "DEF-Shoulder.R",
        "OW-DEF-Spine1": "DEF-Spine1",
        "OW-DEF-Spine2": "DEF-Spine2",
        "OW-DEF-Spine3": "DEF-Spine3",
        "OW-DEF-Spine4": "DEF-Spine4",
        "OW-DEF-Teeth_Bottom": "DEF-Teeth_Bottom",
        "OW-DEF-Teeth_Top": "DEF-Teeth_Top",
        "OW-DEF-Thigh_1.L": "DEF-Thigh_1.L",
        "OW-DEF-Thigh_1.R": "DEF-Thigh_1.R",
        "OW-DEF-Thigh_2.L": "DEF-Thigh_2.L",
        "OW-DEF-Thigh_2.R": "DEF-Thigh_2.R",
        "OW-DEF-Thigh_3.L": "DEF-Thigh_2.L",
        "OW-DEF-Thigh_3.R": "DEF-Thigh_2.R",
        "OW-DEF-Toes.L": "DEF-Toes.L",
        "OW-DEF-Toes.R": "DEF-Toes.R",
        "OW-DEF-Tongue1": "DEF-Tongue1",
        "OW-DEF-Tongue2": "DEF-Tongue2",
        "OW-DEF-Tongue3": "DEF-Tongue3",
        "OW-DEF-UpperArm_1.L": "DEF-UpperArm_1.L",
        "OW-DEF-UpperArm_1.R": "DEF-UpperArm_1.R",
        "OW-DEF-UpperArm_2.L": "DEF-UpperArm_2.L",
        "OW-DEF-UpperArm_2.R": "DEF-UpperArm_2.R",
        "OW-DEF-UpperArm_3.L": "DEF-UpperArm_2.L",
        "OW-DEF-UpperArm_3.R": "DEF-UpperArm_2.R",
        "OW-DEF-Wrist.L": "DEF-Wrist.L",
        "OW-DEF-Wrist.R": "DEF-Wrist.R",
        "OW-Forearm.L": "",
        "OW-Forearm.R": "",
        "OW-Shoulder.L": "",
        "OW-Shoulder.R": "",
    }
