from typing import override

from bpy.types import Context, Panel, UILayout

from ...shared.models.enums_ow_skin import OWSkin
from ...panel import MainPanel
from .props_scene_ow import OWSceneProperties
from .ops_action_match_ow import ActionMatchOWOperator
from .ops_print_unnamed_ow_bone import PrintUnnamedOWBonesOperator
from .ops_rename_ow_bone import RenameOWBonesOperator


class OWMainPanel(MainPanel, Panel):
    bl_idname: str = "MELDTOOL_PT_ow_main"
    bl_label: str = "守望先锋"
    bl_options: set = {"DEFAULT_CLOSED"}

    @override
    def draw(self, context: Context) -> None:
        ow_props: OWSceneProperties = context.scene.meldtool_scene_properties.ow  # type: ignore
        column1: UILayout = self.layout.column()
        column1.prop(ow_props, property="current_skin")
        column1.prop(ow_props, property="action_selection")
        draw_box(self, context=context)


def draw_box(self: Panel, context: Context) -> None:
    box = self.layout.box()
    ow_props: OWSceneProperties = context.scene.meldtool_scene_properties.ow  # type: ignore
    rename_ow_bones: str = "命名守望先锋骨骼(-1)"
    current_skin: OWSkin = OWSkin(ow_props.current_skin)
    if current_skin is None:
        pass
    elif current_skin == OWSkin.SHARED:
        rename_ow_bones = f"命名 {current_skin.value} 骨骼(173)"
    elif current_skin == OWSkin.ANA_CLASSIC:
        rename_ow_bones = f"命名 {current_skin.value} 骨骼(238)"
    elif current_skin == OWSkin.MERCY_CLASSIC:
        rename_ow_bones = f"命名 {current_skin.value} 骨骼(267)"
    elif current_skin == OWSkin.VENTURE_OVERWATCH2:
        rename_ow_bones = f"命名 {current_skin.value} 骨骼(0)"
    elif current_skin == OWSkin.KIRIKO_OVERWATCH2:
        rename_ow_bones = f"命名 {current_skin.value} 骨骼(0)"
    elif current_skin == OWSkin.GENJI_CLASSIC:
        rename_ow_bones = f"命名 {current_skin.value} 骨骼(0)"
    elif current_skin == OWSkin.TRACER_OVERWATCH2:
        rename_ow_bones = f"命名 {current_skin.value} 骨骼(211)"
    else:
        self.bl_label = "Unknown OWSkin"
    column1: UILayout = box.column()
    column1.label(text="重命名")
    column1.operator(RenameOWBonesOperator.bl_idname, text=rename_ow_bones)
    column1.operator(
        PrintUnnamedOWBonesOperator.bl_idname,
        text=PrintUnnamedOWBonesOperator.bl_label,
        icon="CONSOLE",
    )
    column1.operator(
        ActionMatchOWOperator.bl_idname, text=ActionMatchOWOperator.bl_label
    )


registry: list = [OWMainPanel]
