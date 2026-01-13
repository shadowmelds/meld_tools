import bpy
from bpy.props import (
    BoolProperty,
    PointerProperty,
)
from bpy.types import Context, Object, PropertyGroup, Text


class PhysSceneProperties(PropertyGroup):
    def update_use_module_collision_fix(self, context: Context) -> None:
        text: Text = bpy.data.texts.get("collision_fix.py")
        phys: PhysSceneProperties = context.scene.meldtool_scene_properties.phys  # type: ignore

        if text and text.use_module != phys.use_module_collision_fix:
            text.use_module = phys.use_module_collision_fix

    use_module_collision_fix: BoolProperty(
        name="注册",
        description="注册",
        default=True,
        update=update_use_module_collision_fix,
    )

    target_object: PointerProperty(
        name="目标物体",
        type=Object,
        description="选择目标物体",
        poll=lambda self, object: object.type == "MESH",  # type: ignore
    )


registry: list = [
    PhysSceneProperties,
]
