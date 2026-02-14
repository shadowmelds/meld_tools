import logging
from logging import Logger
from typing import Final, Iterable

import bpy
from bpy.types import Context, Object, PoseBone

from ...shared.base.base_operator import BaseOperator
from ...shared.utils.revise_rig_workflow import (
    create_target_rig_obj,
    replace_old_with_new_rig,
)

old_rig_name: Final[str] = "old_rig"


class CreateTargetRigOperator(BaseOperator):
    bl_idname: str = "meldtool.create_target_rig"
    bl_label: str = "1.创建目标骨架"
    bl_description: str = "创建目标骨架"

    logger: Logger = logging.getLogger()

    def execute(self, context: Context) -> set[str]:
        old_rig: Object = bpy.data.objects[old_rig_name]
        target_rig: Object = create_target_rig_obj(context, old_rig)
        self.logger.info(
            f"骨架成功创建：{target_rig.name} 骨骼数量：{len(target_rig.data.bones)}"
        )
        return {"FINISHED"}


class ReviseTargetRigOperator(BaseOperator):
    bl_idname: str = "meldtool.revise_target_rig"
    bl_label: str = "2.修改目标骨架"
    bl_description: str = "修改目标骨架"

    logger: Logger = logging.getLogger()
    target_rig_name: str = "NEW-" + old_rig_name

    def execute(self, context: Context) -> set[str]:
        target_rig: Object = bpy.data.objects[self.target_rig_name]
        self._revise(target_rig)
        return {"FINISHED"}

    def _revise(self, target_rig: Object) -> None:
        if not target_rig:
            raise RuntimeError(f"未找到 {self.target_rig_name}")
        bpy.ops.object.mode_set(mode="POSE")
        pbones: Iterable[PoseBone] = target_rig.pose.bones
        for pbone in pbones:
            pbone.rotation_mode = "XYZ"
            self.logger.debug(f"{pbone.name} 的旋转模式改为 XYZ")


class ReplaceOldRigOperator(BaseOperator):
    bl_idname: str = "meldtool.replace_old_rig"
    bl_label: str = "3.替换旧骨架"
    bl_description: str = "替换旧骨架"
    target_rig_name: str = "NEW-" + old_rig_name

    def execute(self, context: Context) -> set[str]:
        old_rig: Object = bpy.data.objects[old_rig_name]
        target_rig: Object = bpy.data.objects[self.target_rig_name]
        bpy.ops.object.mode_set(mode="OBJECT")
        replace_old_with_new_rig(old_rig, target_rig)
        return {"FINISHED"}


registry: list = [
    CreateTargetRigOperator,
    ReviseTargetRigOperator,
    ReplaceOldRigOperator,
]
