import bpy
from bpy.props import (
    BoolProperty,
    PointerProperty,
    StringProperty,
)
from bpy.types import Context, Object, PropertyGroup


class RibbonMeshSceneProperties(PropertyGroup):
    def update_use_cloud_rig(self, context: Context):
        armature: Object = (
            bpy.context.scene.meldtool_scene_properties.ribbon_mesh.target_armature
        )
        ribbon_mesh: RibbonMeshSceneProperties = (
            bpy.context.scene.meldtool_scene_properties.ribbon_mesh
        )
        if armature:
            if hasattr(armature, "cloudrig"):
                ribbon_mesh.use_cloud_rig = armature.cloudrig.enabled
            else:
                ribbon_mesh.use_cloud_rig = False

    empty_object_collection: PointerProperty(
        name="空物体集合", type=bpy.types.Collection, description="选择空物体集合"
    )
    target_armature: PointerProperty(
        name="目标骨架",
        type=bpy.types.Object,
        description="选择目标骨架",
        poll=lambda self, obj: obj.type == "ARMATURE",
        update=update_use_cloud_rig,
    )
    target_parent_bone: StringProperty(
        name="目标父骨骼",
        description="选择目标骨骼",
    )
    use_cloud_rig: BoolProperty(
        name="使用 CloudRig",
        description="自动检测目标骨架是否启用 CloudRig",
        default=False,
    )


registry: list = [
    RibbonMeshSceneProperties,
]
