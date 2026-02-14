from dataclasses import dataclass

from ....shared.models.rigging.human import Human
from .enums_ow_bone_collection import OWBoneCollection


@dataclass
class CollectionBones:
    collection: OWBoneCollection
    bones: dict[str, Human]
    prefix: str = ""
