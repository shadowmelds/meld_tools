from bpy.props import IntProperty
from bpy.types import PropertyGroup


class PublicSceneProperties(PropertyGroup):
    frame_start: IntProperty(name="Frame Start", default=1, description="开始帧")
    frame_end: IntProperty(name="Frame End", default=250, description="结束帧")


registry: list = [
    PublicSceneProperties,
]
