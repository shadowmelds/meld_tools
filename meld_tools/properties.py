import bpy
from bpy.app.handlers import persistent
from bpy.props import PointerProperty, StringProperty
from bpy.types import Object, PropertyGroup, Text

from .general.drivers.props_scene_drivers import DriversSceneProperties
from .general.phys.props_scene_phys import PhysSceneProperties
from .general.ribbon_mesh.props_scene_ribbon_mesh import (
    RibbonMeshSceneProperties,
)
from .general.toolset.props_scene_toolset import ToolsetSceneProperties
from .ow.props_scene_ow import OWSceneProperties
from .ow.transform_action.props_scene_ow_transform_action import (
    OWTransfromActionSceneProperties,
)
from .public.props_scene_public import PublicSceneProperties
from .rig.props_object_meld_rig import MeldRigObjectProperties
from .rig.props_pose_bone_meld_rig import MeldRigPoseBoneProperties


class MeldToolObjectProperties(PropertyGroup):
    """物体属性主要是功能需要在选中活动物体时使用"""

    include_keyword: StringProperty(name="包含", default="")
    meld_rig: PointerProperty(type=MeldRigObjectProperties)


class MeldToolPoseBoneProperties(PropertyGroup):
    """姿态骨骼属性"""

    meld_rig: PointerProperty(type=MeldRigPoseBoneProperties)


class MeldToolSceneProperties(PropertyGroup):
    """场景属性主要是在任何情况下都能使用"""

    public: PointerProperty(type=PublicSceneProperties)
    toolset: PointerProperty(type=ToolsetSceneProperties)
    phys: PointerProperty(type=PhysSceneProperties)
    ribbon_mesh: PointerProperty(type=RibbonMeshSceneProperties)
    drivers: PointerProperty(type=DriversSceneProperties)
    ow: PointerProperty(type=OWSceneProperties)
    ow_transform_action: PointerProperty(type=OWTransfromActionSceneProperties)


@persistent  # 确保切换文件也能重新调用
def init_properties(dummy=None) -> None:  # type: ignore
    """场景准备就绪后回调设置属性默认值"""

    # 检查碰撞脚本是否存在并被注册
    text: Text = bpy.data.texts.get("collision_fix.py")
    phys: PhysSceneProperties = bpy.context.scene.meldtool_scene_properties.phys  # type: ignore
    if text:
        phys.use_module_collision_fix = text.use_module

    # 检查丝带网格目标骨架是否启用 CloudRig
    armature: Object = (
        bpy.context.scene.meldtool_scene_properties.ribbon_mesh.target_armature  # type: ignore
    )
    ribbon_mesh: RibbonMeshSceneProperties = (
        bpy.context.scene.meldtool_scene_properties.ribbon_mesh  # type: ignore
    )
    if armature:
        if hasattr(armature, "cloudrig"):
            ribbon_mesh.use_cloud_rig = armature.cloudrig.enabled  # type: ignore
        else:
            ribbon_mesh.use_cloud_rig = False


registry: list = [
    MeldToolSceneProperties,
    MeldToolObjectProperties,
    MeldToolPoseBoneProperties,
]


def register() -> None:
    bpy.types.Scene.meldtool_scene_properties = bpy.props.PointerProperty(  # type: ignore
        type=MeldToolSceneProperties
    )
    bpy.types.Object.meldtool_object_properties = bpy.props.PointerProperty(  # type: ignore
        type=MeldToolObjectProperties
    )
    bpy.types.PoseBone.meldtool_pose_bone_properties = bpy.props.PointerProperty(  # type: ignore
        type=MeldToolPoseBoneProperties
    )
    bpy.app.handlers.load_post.append(init_properties)


def unregister() -> None:
    # 清除 Scene、Object、PoseBone.. 的 PointerProperty
    del bpy.types.Scene.meldtool_scene_properties  # type: ignore
    del bpy.types.Object.meldtool_object_properties  # type: ignore
    del bpy.types.PoseBone.meldtool_pose_bone_properties  # type: ignore
