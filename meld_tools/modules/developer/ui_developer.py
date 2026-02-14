from bpy.types import Context, Panel, UILayout

from ...panel import MainPanel
from .ops_reload import RefreshLocalOperator, ReloadScriptOperator
from .ops_workflow_test import (
    CreateTargetRigOperator,
    ReplaceOldRigOperator,
    ReviseTargetRigOperator,
)


class DevelpoerMainPanel(MainPanel, Panel):
    bl_idname: str = "MELDTOOL_PT_developer_main"
    bl_label: str = "开发者"

    def draw(self, context: Context) -> None:
        row1: UILayout = self.layout.row()
        row1.operator(RefreshLocalOperator.bl_idname, icon="FILE_REFRESH")
        row1.operator(ReloadScriptOperator.bl_idname, icon="FILE_REFRESH")

        row2: UILayout = self.layout.row()
        row2.operator(CreateTargetRigOperator.bl_idname)
        row2.operator(ReviseTargetRigOperator.bl_idname)
        row2.operator(ReplaceOldRigOperator.bl_idname)


registry: list = [DevelpoerMainPanel]
