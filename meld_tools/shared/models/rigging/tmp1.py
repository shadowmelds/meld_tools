from enum import StrEnum
from typing import Iterable

from bpy.types import Context, PoseBone


class RigID(StrEnum):
    MELD_RIG = "meld_rig"
    RIGIFY = "rigify"
    CLOUD_RIG = "cloud_rig"
    MHX = "mhx"
    OW = "overwatch"


def get_similar_bones(bone_name: str, rig_id: RigID) -> str:
    """根据找到指定绑定框架对应的骨骼名"""
    ...


def main(context: Context) -> None:
    # rigify、mhx、cloud_rig
    # 通过任意一个名称获取同类

    bones: Iterable[PoseBone] = context.active_object.pose.bones
    for bone in bones:
        rigify_bone_name: str = get_similar_bones(name=bone.name, rig_id=RigID.RIGIFY)
        bone.name = rigify_bone_name


if __name__ == "__main__":
    main()
