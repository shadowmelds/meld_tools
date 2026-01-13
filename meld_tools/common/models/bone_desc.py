from dataclasses import dataclass, field
from typing import Literal

from bpy.types import BoneCollection, EditBone
from mathutils import Vector


@dataclass
class BoneDesc:
    """用于生成骨骼的信息"""

    name: str = "骨骼"
    # 头部 XYZ
    head: Vector | None = None
    # 生成骨骼位置在基于的骨骼
    position_bone: EditBone = None
    position_bone_by_name: str = None
    position_bone_location: Literal["HEAD", "TAIL"] = "HEAD"
    # 尾端 XYZ
    tail: Vector | None = None
    # 生成骨骼的尾端相当于头部的偏移
    tail_offset: Vector | None = None
    # 相连项
    use_connect: bool = False
    # 柔性骨骼显示的 X 向宽度
    bbone_x: float = 0.0
    # 柔性骨骼显示的 Z 向宽度
    bbone_z: float = 0.0
    # 父级
    parent: str | None = None
    # 是否镜像
    auto_mirror: bool = False
    # 是否自动计算
    calculate_roll: (
        Literal[
            "POS_X",
            "POS_Z",
            "GLOBAL_POS_X",
            "GLOBAL_POS_Y",
            "GLOBAL_POS_Z",
            "NEG_X",
            "NEG_Z",
            "GLOBAL_NEG_X",
            "GLOBAL_NEG_Y",
            "GLOBAL_NEG_Z",
            "ACTIVE",
            "VIEW",
            "CURSOR",
        ]
        | None
    ) = None
    # 所在集合
    collections: list[BoneCollection] = None
    # 骨骼显示为
    display_type: Literal[
        "ARMATURE_DEFINED", "OCTAHEDRAL", "STICK", "BBONE", "ENVELOPE", "WIRE"
    ] = "ARMATURE_DEFINED"
    # 骨骼配色
    palette: Literal[
        "DEFAULT",
        "THEME01",
        "THEME02",
        "THEME03",
        "THEME04",
        "THEME05",
        "THEME06",
        "THEME07",
        "THEME08",
        "THEME09",
        "THEME10",
        "THEME11",
        "THEME12",
        "THEME13",
        "THEME14",
        "THEME15",
        "THEME16",
        "THEME17",
        "THEME18",
        "THEME19",
        "THEME20",
        "CUSTOM",
    ] = "DEFAULT"
    # 自定义形状物体
    custom_shape: str | None = None
    # 自定义形状缩放 XYZ
    custom_shape_scale_xyz: Vector = field(
        default_factory=lambda: Vector((1.0, 1.0, 1.0))
    )
    # 自定义形状移动 XYZ
    custom_shape_translation: Vector = field(
        default_factory=lambda: Vector((0.0, 0.0, 0.0))
    )
    # 自定义形状旋转 XYZ
    custom_shape_rotation_euler: Vector = field(
        default_factory=lambda: Vector((0.0, 0.0, 0.0))
    )
    # 自定义形状线框模式宽度
    custom_shape_wire_width: float = 1.0
    rotation_mode: Literal[
        "QUATERNION",  # Quaternion (WXYZ).No Gimbal Lock.
        "XYZ",  # XYZ Euler.XYZ Rotation Order - prone to Gimbal Lock (default).
        "XZY",  # XZY Euler.XZY Rotation Order - prone to Gimbal Lock.
        "YXZ",  # YXZ Euler.YXZ Rotation Order - prone to Gimbal Lock.
        "YZX",  # YZX Euler.YZX Rotation Order - prone to Gimbal Lock.
        "ZXY",  # ZXY Euler.ZXY Rotation Order - prone to Gimbal Lock.
        "ZYX",  # ZYX Euler.ZYX Rotation Order - prone to Gimbal Lock.
        "AXIS_ANGLE",  # Axis Angle.Axis Angle (W+XYZ), defines a rotation around some axis defined by 3D-Vector.
    ] = "XYZ"
    # 锁定位置 XYZ
    lock_location: list[bool] = field(default_factory=lambda: [False, False, False])
    # 锁定旋转 XYZ
    lock_rotation: list[bool] = field(default_factory=lambda: [False, False, False])
    # 锁定旋转 W
    lock_rotation_w: bool = False
    # 锁定缩放 XYZ
    lock_scale: list[bool] = field(default_factory=lambda: [False, False, False])
    use_cloud_rig: bool = False
