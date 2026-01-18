from bpy.props import BoolProperty, IntProperty
from bpy.types import PropertyGroup


class DriversSceneProperties(PropertyGroup):
    active_driver: IntProperty(name="活动驱动器", default=-1)

    hide_viewport: BoolProperty(
        name="视图中隐藏",
        default=False,
    )
    hide_render: BoolProperty(
        name="渲染中隐藏",
        default=False,
    )
    collision_use: BoolProperty(
        name="碰撞开启",
        default=False,
    )
    show_viewport: BoolProperty(
        name="视图（物理）",
        default=False,
    )
    show_render: BoolProperty(
        name="渲染（物理）",
        default=False,
    )
    cache_frame_start: BoolProperty(
        name="模拟起始帧（物理）",
        default=False,
    )
    cache_frame_end: BoolProperty(
        name="模拟结束帧（物理）",
        default=False,
    )
    damped_track_enabled: BoolProperty(
        name="阻尼追踪",
        default=False,
    )
    override_paste: BoolProperty(
        name="覆盖",
        default=False,
    )


registry: list = [
    DriversSceneProperties,
]
