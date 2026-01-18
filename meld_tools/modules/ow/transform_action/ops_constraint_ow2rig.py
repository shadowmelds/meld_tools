from typing import override

import bpy
from bpy.types import Context, Object

from .._utils import skin_data

from ....shared.base.base_operator import BaseOperator
from ....shared.models.enums_ow_skin import OWSkin
from ....shared.utils import transform_action_utils
from .props_scene_ow_transform_action import OWTransfromActionSceneProperties


class ConstraintOW2RigOperator(BaseOperator):
    bl_idname: str = "meldtool.constraint_ow2rig"
    bl_label: str = "约束绑定骨骼至原始动画骨骼"

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
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
        ow_armature: Object = bpy.data.objects[
            ow_transform_action.ow_armature_selection
        ]

        # constraint_bones 根据不同的皮肤选择进行改变
        current_skin: OWSkin = OWSkin(
            context.scene.meldtool_scene_properties.ow.current_skin  # type: ignore
        )
        constraint_bones: dict[str, str] = skin_data.get_skin_constrains_bones(
            current_skin
        )
        transform_action_utils.constraint_rig(
            redirect_armature=ow_armature,
            rig_armature=rig_armature,
            constraint_bones=constraint_bones,
        )
        self.report({"INFO"}, "操作完成！")
        return {"FINISHED"}


registry: list = [ConstraintOW2RigOperator]
