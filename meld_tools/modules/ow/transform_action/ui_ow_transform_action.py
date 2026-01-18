from typing import override

from bpy.types import Context, Panel, UILayout

from ....panel import MainPanel
from ....public.ops_refresh_frame import (
    RefreshFrameStartOperator,
    RrefreshFrameEndOperator,
)
from ....public.props_scene_public import PublicSceneProperties
from .ops_bake_action import BakeActionOperator
from .ops_constraint_ow2rig import ConstraintOW2RigOperator
from .ops_unconstraint_ow2rig import UnConstraintOW2RigOperator
from .props_scene_ow_transform_action import OWTransfromActionSceneProperties


class OWTransfromActionPanel(MainPanel, Panel):
    bl_idname: str = "MELDTOOL_PT_action"
    bl_label: str = "传递动作"
    bl_parent_id: str = "MELDTOOL_PT_ow_main"
    bl_options: set = {"DEFAULT_CLOSED"}

    @override
    def draw(self, context: Context) -> None:
        ow_transform_action: OWTransfromActionSceneProperties = (
            context.scene.meldtool_scene_properties.ow_transform_action  # type: ignore
        )
        public_props: PublicSceneProperties = (
            context.scene.meldtool_scene_properties.public  # type: ignore
        )

        column: UILayout = self.layout.column()
        column.prop(ow_transform_action, property="ow_armature_selection")
        column.prop(ow_transform_action, property="rig_armature_selection")
        column.operator(
            ConstraintOW2RigOperator.bl_idname,
            text="绑定骨架约束至守望先锋骨架",
            icon="CONSTRAINT_BONE",
        )
        column.operator(
            UnConstraintOW2RigOperator.bl_idname,
            text=UnConstraintOW2RigOperator.bl_label,
            icon="BRUSH_DATA",
        )

        row: UILayout = self.layout.row()
        row1: UILayout = row.row(align=True)
        row1.prop(data=public_props, property="frame_start")
        row1.operator(RefreshFrameStartOperator.bl_idname, icon="FILE_REFRESH", text="")

        row2: UILayout = row.row(align=True)
        row2.prop(data=public_props, property="frame_end")
        row2.operator(RrefreshFrameEndOperator.bl_idname, icon="FILE_REFRESH", text="")

        column1: UILayout = self.layout.column()
        column1.operator(BakeActionOperator.bl_idname, text="烘焙动作", icon="PLAY")


registry: list = [OWTransfromActionPanel]
