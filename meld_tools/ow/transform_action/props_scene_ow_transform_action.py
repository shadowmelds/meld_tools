from bpy.props import EnumProperty
from bpy.types import Context, PropertyGroup

from ...common.utils import properties_utils


class OWTransfromActionSceneProperties(PropertyGroup):
    def get_armature_objects(self, context: Context) -> list[tuple]:  # -> Any:
        armatures: list[tuple] = []
        for obj in context.scene.objects:
            if obj.type == "ARMATURE":
                armatures.append(
                    (obj.name, obj.name, obj.name)
                )  # identifier, name, description

        # 确保至少有一个选项（如占位符）
        if not armatures:
            armatures.append(("NONE", "None", "No options available"))
        return properties_utils.intern_enum_items(armatures)

    ow_armature_selection: EnumProperty(
        name="守望先锋骨架",
        description="选择一个骨架物体",
        items=get_armature_objects,
        default=0,
    )
    rig_armature_selection: EnumProperty(
        name="绑定骨架",
        description="选择一个骨架物体",
        items=get_armature_objects,
        default=0,
    )


registry: list = [
    OWTransfromActionSceneProperties,
]
