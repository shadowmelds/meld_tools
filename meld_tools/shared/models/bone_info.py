import typing

from bpy.types import EditBone
from mathutils import Vector


class BoneInfo:
    def __init__(self, source: EditBone | typing.Self, **kwargs: typing.Any) -> None:
        # 头部 XYZ
        self.head = Vector((0, 0, 0))
        # 尾端 XYZ
        self.tail = Vector((0, 1, 0))
        # 扭转（滚动）
        self.roll = 0
        # 头部半径（仅限封套形变）
        self.head_radius = 0.1
        # 尾端半径（仅限封套形变）
        self.tail_radius = 0.05
        # 相连项
        self.use_connect = False
        # 柔性骨骼显示的 X 向宽度
        self.bbone_x = 0.0
        # 柔性骨骼显示的 Z 向宽度
        self.bbone_z = 0.0
        # 指向骨骼 x 轴的向量（只读）
        self.x_axis = Vector()
        # 指向骨骼 y 轴的向量（只读）
        self.y_axis = Vector()
        # 指向骨骼 z 轴的向量（只读）
        self.z_axis = Vector()
        # 自定义形状物体
        self.custom_shape = None
        # 自定义形状重写变换
        self.custom_shape_transform = None
        # 自定义形状缩放 XYZ
        self.custom_shape_scale_xyz = Vector((1.0, 1.0, 1.0))
        # 自定义形状移动 XYZ
        self.custom_shape_translation = Vector((0.0, 0.0, 0.0))
        # 自定义形状旋转 XYZ
        self.custom_shape_rotation_euler = Vector((0.0, 0.0, 0.0))
        # 自定义形状线框模式宽度
        self.custom_shape_wire_width = 1.0
        # 自定义形状缩放到骨骼长度
        self.use_custom_shape_bone_size = True
        # 旋转模式
        self.rotation_mode = "QUATERNION"
        # 锁定位置 XYZ
        self.lock_location = [False, False, False]
        # 锁定旋转 XYZ
        self.lock_rotation = [False, False, False]
        # 锁定旋转 W
        self.lock_rotation_w = False
        # 锁定缩放 XYZ
        self.lock_scale = [False, False, False]
        # IK 拉伸
        self.ik_stretch = 0
        # 锁定 IK X向
        self.lock_ik_x = False
        # 锁定 IK Y向
        self.lock_ik_y = False
        # 锁定 IK Z向
        self.lock_ik_z = False
        # IK 硬度 X向
        self.ik_stiffness_x = 0
        # IK 硬度 Y向
        self.ik_stiffness_y = 0
        # IK 硬度 Z向
        self.ik_stiffness_z = 0
        # 限制 IK X轴的移动
        self.use_ik_limit_x = False
        # 限制 IK Y轴的移动
        self.use_ik_limit_y = False
        # 限制 IK Z轴的移动
        self.use_ik_limit_z = False
        # IK 限定角 X 最小值
        self.ik_min_x = 0
        # IK 限定角 X 最大值
        self.ik_max_x = 0
        # IK 限定角 Y 最小值
        self.ik_min_y = 0
        # IK 限定角 Y 最大值
        self.ik_max_y = 0
        # IK 限定角 Z 最小值
        self.ik_min_z = 0
        # IK 限定角 Y 最大值
        self.ik_max_z = 0
