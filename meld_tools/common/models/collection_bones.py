from dataclasses import dataclass
from .enums_ow_bone_collection import OWBoneCollection


@dataclass
class CollectionBones:
    bones: dict
    collection: OWBoneCollection
