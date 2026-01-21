from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Literal


@dataclass(frozen=True)
class Human:
    part: HumanPart | None = None
    base_name: str | None = None
    position: Literal[
        "upper",
        "lower",
        "middle",
        "corner",
        "inner",
        "outer",
        "tip",
        "NONE",
    ] = "NONE"
    index: int = -1
    side: Literal["L", "R", "NONE"] = "NONE"

    def get_name(self) -> str:
        name: str

        if self.base_name:
            name = self.base_name
        elif self.part:
            name = self.part.value
        else:
            raise ValueError("Human 没有 base_name 也没有 part，无法命名")

        if self.position != "NONE":
            name += f"_{self.position}"

        if self.index != -1:
            name += f"_{self.index}"

        if self.side != "NONE":
            name += f".{self.side}"

        return name


class HumanPart(StrEnum):
    HEAD = "head"  # 头
    NECK = "neck"  # 脖子
    CHEST = "chest"  # 胸
    SPINE = "spine"  # 脊柱
    HIPS = "hips"  # 臀部

    SHOULDER = "shoulder"  # 肩膀
    UPPER_ARM = "upper_arm"  # 上臂
    FOREARM = "forearm"  # 小臂
    WRIST = "wrist"  # 手腕

    FINGER_THUMB = "finger_thumb"  # 拇指
    FINGER_INDEX = "finger_index"  # 食指
    FINGER_MIDDLE = "finger_middle"  # 中指
    FINGER_RING = "finger_ring"  # 无名指
    FINGER_PINKY = "finger_pinky"  # 小指

    FINGER_THUMB_CARPAL = "finger_thumb_carpal"  # 拇指掌骨
    FINGER_INDEX_CARPAL = "finger_index_carpal"  # 食指掌骨
    FINGER_MIDDLE_CARPAL = "finger_middle_carpal"  # 中指掌骨
    FINGER_RING_CARPAL = "finger_ring_carpal"  # 无名指掌骨
    FINGER_PINKY_CARPAL = "finger_pinky_carpal"  # 小指掌骨

    THIGH = "thigh"  # 大腿
    KNEE = "knee"  # 小腿
    FOOT = "foot"  # 脚
    TOES = "toes"  # 脚趾

    EYE = "eye"  # 眼
    TEETH = "teeth"  # 牙齿
    TONGUE = "tongue"
    EAR = "ear"  # 耳朵

    EYEBROW = "eyebrow"  # 眉
    EYELID = "eyelid"  # 眼皮
    CHEEK_UPPER = "cheek_upper"  # 脸颊上
    CHEEK = "cheek"  # 脸颊
    CHEEK_LOWER = "laugh_lower"  # 脸颊下，法令纹
    NOSE = "nose"  # 鼻子
    NOSE_BRIEGE = "nose_bridge"  # 鼻子
    LIP_UPPER = "lip_upper"  # 上嘴唇
    LIP = "lip"  # 嘴唇
    LIP_LOWER = "lip_lower"  # 下嘴唇
    CHIN = "chin"  # 颌
    JAW = "jaw"  # 颌
