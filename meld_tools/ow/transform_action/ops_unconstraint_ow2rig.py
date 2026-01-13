from typing import override

import bpy
from bpy.types import Context, Object

from ...common.base.base_operator import BaseOperator
from ...common.models.enums_ow_skin import OWSkin
from ...common.utils import skin_data, transform_action_utils
from .props_scene_ow_transform_action import OWTransfromActionSceneProperties


class UnConstraintOW2RigOperator(BaseOperator):
    bl_idname: str = "meldtool.unconstraint_ow2rig"
    bl_label: str = "清除约束"
    bl_description: str = "守望先锋骨骼对应的绑定骨骼清除复制变换约束"

    @classmethod
    @override
    def poll(cls: type["UnConstraintOW2RigOperator"], context: Context):
        ow_transform_action: OWTransfromActionSceneProperties = (
            context.scene.meldtool_scene_properties.ow_transform_action  # type: ignore
        )

        return cls.validate(
            ow_transform_action.ow_armature_selection
            != ow_transform_action.rig_armature_selection,
            "ow骨架和绑定骨架不能是同一个骨架",
        )

    @override
    def execute(self, context: Context) -> set[str]:
        ow_transform_action: OWTransfromActionSceneProperties = (
            context.scene.meldtool_scene_properties.ow_transform_action  # type: ignore
        )
        rig_armature: Object = bpy.data.objects[
            ow_transform_action.rig_armature_selection
        ]
        current_skin: OWSkin = OWSkin(
            context.scene.meldtool_scene_properties.ow.current_skin  # type: ignore
        )
        constraint_bones: dict[str, str] = skin_data.get_skin_constrains_bones(
            current_skin
        )
        transform_action_utils.unconstraint_rig(rig_armature, constraint_bones)
        self.report({"INFO"}, "操作完成！")
        return {"FINISHED"}


registry: list = [UnConstraintOW2RigOperator]
