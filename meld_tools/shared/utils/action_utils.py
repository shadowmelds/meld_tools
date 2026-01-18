import re
from typing import Any

from bpy.types import PoseBone

from ..models.data_path_info import DataPathInfo


def get_bone_path_info(data_path: str) -> DataPathInfo | None:
    """以 DataPathInfo 类型返回 data_path 中关键数据
    data_path的结构是: pose.bones["骨骼"].rotation_quaternion
    """
    if "pose.bones" in data_path:
        match = re.search(r'pose\.bones\["(.*?)"\]\.(\w+)', data_path)
        if match:
            bone_name: str = match.group(1)  # 骨骼名称
            property_name: str = match.group(
                2
            )  # 属性名称（如 location, rotation_euler 等）
            return DataPathInfo(bone_name=bone_name, property_name=property_name)
        else:
            return None
    return None


def get_bone_property_by_index(
    pose_bone: PoseBone,
    property_name: str,  # rotation_quaternion, rotation_euler...
    index: int,
) -> float:
    """
    根据属性名称和索引，动态获取骨骼的对应属性的特定维度的值
    """
    # 欧拉旋转索引顺序：
    # rotation_euler[0] 0.0  X轴
    # rotation_euler[1] 0.0  Y轴
    # rotation_euler[2] 0.0  Z轴

    # 四元数旋转索引顺序：
    # rotation_quaternion[0] 0.0  W轴
    # rotation_quaternion[1] 0.0  X轴
    # rotation_quaternion[2] 0.0  Y轴
    # rotation_quaternion[3] 0.0  Z轴

    # 动态获取 PoseBone 的 property 值
    property: Any = getattr(pose_bone, property_name, None)
    pose_bone.rotation_quaternion

    if property is not None:
        if 0 <= index < len(property):  # 确保 index 在有效范围内
            return property[index]  # 返回对应轴的值
        else:
            return None
    else:
        return None
