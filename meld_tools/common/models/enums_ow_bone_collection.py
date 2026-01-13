from enum import Enum


class OWBoneCollection(Enum):
    """重命名后自动至骨骼集合"""

    BASE_MAIN = "BASE_MAIN"
    BASE_FACE = "BASE_FACE"
    BASE_STRETCH = "BASE_STRETCH"
    POINT = "POINT"
    EXTRA = "EXTRA"
    CLOTH = "CLOTH"
    UNAMED = "UNAMED"
    EXIST = "EXIST"
