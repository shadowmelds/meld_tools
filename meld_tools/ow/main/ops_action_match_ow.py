from typing import override

import bpy
from bpy.types import (
    Action,
    ActionChannelbag,
    ActionChannelbagFCurves,
    ActionSlots,
    ActionStrip,
    Context,
)

from ...common.base.base_operator import BaseOperator
from ...common.models.data_path_info import DataPathInfo
from ...common.models.enums_ow_skin import OWSkin
from ...common.utils.action_utils import get_bone_path_info
from ...common.utils.skin_data import get_skin_bones
from ...common.utils.ui import force_refresh_animation


class ActionMatchOWOperator(BaseOperator):
    bl_idname: str = "meldtool.action_match_ow"
    bl_label: str = "动作通道匹配命名骨骼"
    bl_description: str = (
        "将选中的守望先锋原始动作数据中的通道骨骼修改到已命名后的骨骼名以匹配新命名骨架"
    )

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        return cls.validate(
            bool(context.scene.meldtool_scene_properties.ow.action_selection)  # type: ignore
        )

    @override
    def execute(self, context: Context) -> set[str]:
        action: Action = bpy.data.actions[
            context.scene.meldtool_scene_properties.ow.action_selection  # type: ignore
        ]
        legacy_slot: ActionSlots | None = next(
            (slot for slot in action.slots if slot.name_display == "Legacy Slot"), None
        )

        fcurves: ActionChannelbagFCurves = None
        if legacy_slot is not None:
            strip: ActionStrip = action.layers[0].strips[0]
            action_channelbag: ActionChannelbag = strip.channelbag(legacy_slot)  # type: ignore
            fcurves = action_channelbag.fcurves
        else:
            fcurves = action.fcurves

        current_skin: OWSkin = OWSkin(
            context.scene.meldtool_scene_properties.ow.current_skin  # type: ignore
        )
        bone_dict: dict = get_skin_bones(current_skin)

        for fcurve in fcurves:
            data_path_info: DataPathInfo = get_bone_path_info(fcurve.data_path)
            bone_name: str = data_path_info.bone_name
            property_name: str = data_path_info.property_name
            if bone_name in bone_dict:
                fcurve.data_path = (
                    f'pose.bones["{bone_dict[bone_name]}"].{property_name}'
                )

        force_refresh_animation(context)

        self.report({"INFO"}, "操作完成！")
        return {"FINISHED"}


registry: list = [ActionMatchOWOperator]
