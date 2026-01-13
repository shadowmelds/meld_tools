from bpy.props import EnumProperty
from bpy.types import Context, PropertyGroup

from ..common.models.enums_bone_type import BoneType


class MeldRigPoseBoneProperties(PropertyGroup):
    def type_item(self, context: Context) -> list[tuple]:
        return [
            (
                BoneType.MELD_COPY.value,
                BoneType.MELD_COPY.value,
                BoneType.MELD_COPY.value,
            )
        ]

    bone_type: EnumProperty(
        name="生成类型", description="不同类型会对生成骨架有不同结果", items=type_item
    )


registry = [
    MeldRigPoseBoneProperties,
]
