from enum import StrEnum


class OWBoneCollection(StrEnum):
    """重命名后自动至骨骼集合"""

    BASE_DEFORM = "BASE_DEFORM"
    FACE_DEFORM = "FACE_DEFORM"
    OTHER_DEFORM = "OTHER_DEFORM"
    NO_DEFORM = "NO_DEFORM"
    POINT = "POINT"
    EXTRA = "EXTRA"
    EXTRA_DEFORM = "EXTRA_DEFORM"
    CLOTH = "CLOTH"
    UNNAMED = "UNNAMED"
    EXIST = "EXIST"
