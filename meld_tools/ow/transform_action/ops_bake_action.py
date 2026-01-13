from typing import override

import bpy
from bpy.types import (
    Context,
    Object,
)

from ...common.base.base_operator import BaseOperator
from ...common.models.enums_ow_skin import OWSkin
from ...common.utils import skin_data, transform_action_utils
from ...public.props_scene_public import PublicSceneProperties
from .props_scene_ow_transform_action import OWTransfromActionSceneProperties


class BakeActionOperator(BaseOperator):
    bl_idname: str = "meldtool.bake_action"
    bl_label: str = "烘焙动画至绑定"

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        ow_transform_action: OWTransfromActionSceneProperties = (
            context.scene.meldtool_scene_properties.ow_transform_action  # type: ignore
        )
        state: str = ow_transform_action.rig_armature_selection
        return cls.validate(bool(state) and state != "NONE", "没有选择绑定骨架")

    @override
    def execute(self, context: Context) -> set[str]:
        public_props: PublicSceneProperties = (
            context.scene.meldtool_scene_properties.public  # type: ignore
        )
        ow_transform_action: OWTransfromActionSceneProperties = (
            context.scene.meldtool_scene_properties.ow_transform_action  # type: ignore
        )
        rig_armature: Object = bpy.data.objects[
            ow_transform_action.rig_armature_selection
        ]
        ow_armature: Object = bpy.data.objects[
            ow_transform_action.ow_armature_selection
        ]
        current_skin: OWSkin = OWSkin(
            context.scene.meldtool_scene_properties.ow.current_skin  # type: ignore
        )
        constraint_bones: dict[str, str] = skin_data.get_skin_constrains_bones(
            current_skin
        )
        try:
            transform_action_utils.bake_action(
                redirect_armature=ow_armature,
                rig_armature=rig_armature,
                constraint_bones=constraint_bones,
                frame_start=public_props.frame_start,
                frame_end=public_props.frame_end,
                simple=True,
            )
        except Exception as e:
            self.report({"ERROR"}, str(e))
            return {"CANCELLED"}

        self.report({"INFO"}, "操作完成！")
        return {"FINISHED"}


registry: list = [BakeActionOperator]
