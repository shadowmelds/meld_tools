from typing import override

from bpy.types import Context, Panel, UILayout

from ..panel import MainPanel
from .ops_reload import RefreshLocalOperator, ReloadScriptOperator


class DevelpoerMainPanel(MainPanel, Panel):
    bl_idname: str = "MELDTOOL_PT_developer_main"
    bl_label: str = "开发者"

    @override
    def draw(self, context: Context) -> None:
        row1: UILayout = self.layout.row()
        row1.operator(RefreshLocalOperator.bl_idname, icon="FILE_REFRESH")
        row1.operator(ReloadScriptOperator.bl_idname, icon="FILE_REFRESH")


registry: list = [DevelpoerMainPanel]
