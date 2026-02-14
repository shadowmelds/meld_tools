"""
对现有骨骼修改的工作流
"""

import bpy
from bpy.types import Armature, Context, Object

from ..models.result import Result


def revise(context: Context, old_rig: Object | None = None) -> Result:
    # 1. 原始骨架 复制 新目标骨架
    # 2. 新目标骨架 生成
    # 3. 替换原始骨架，出错终止

    target_rig: Object = create_target_rig_obj()

    revise_target_rig(target_rig)

    if old_rig:
        replace_old_with_new_rig(old_rig, target_rig)
    else:
        ...


def create_target_rig_obj(context: Context, old_rig: Object) -> Object:
    """使用旧目标骨架创建新的目标骨架"""
    if not old_rig:
        raise RuntimeError("未找到 old_rig")
    target_rig_name: str = "NEW-" + old_rig.name

    old_target_rig: Object | None = bpy.data.objects.get(target_rig_name)

    if old_target_rig:
        bpy.data.objects.remove(old_target_rig)

    target_rig_armature: Armature = old_rig.data.copy()
    target_rig: Object = old_rig.copy()
    target_rig.name = target_rig_name
    target_rig.data = target_rig_armature
    context.scene.collection.objects.link(target_rig)

    return target_rig


def revise_target_rig(target_rig: Object) -> None: ...


def replace_old_with_new_rig(old_rig: Object, new_rig: Object) -> Result:
    """新目标骨骼替换旧目标骨骼"""

    old_name: str = old_rig.name
    old_rig_name: str = "OLD-" + old_name

    old_rig.name = old_rig_name
    old_rig.data.name = old_rig_name

    new_rig.name = old_name
    new_rig.data.name = old_name
