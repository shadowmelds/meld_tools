from typing import override

from bpy.types import Context, Panel, UILayout

from ....panel import MainPanel
from .ops_print_selected_bones import PrintSelectedBonesOperator
from .ops_print_shape_keys import PrintShapeKeysOperator
from .ops_print_unlock_vg import PrintUnlockVGOperator
from .ops_print_visible_bones import PrintVisibleBonesOperator


class PrintsPanel(MainPanel, Panel):
    bl_idname: str = "MELDTOOL_PT_prints"
    bl_label: str = "打印到控制台"
    bl_parent_id: str = "MELDTOOL_PT_general_main"
    bl_options: set = {"DEFAULT_CLOSED"}

    @override
    def draw(self, context: Context) -> None:
        column: UILayout = self.layout.column()
        column1: UILayout = column.column(align=True)
        column1.operator(
            PrintVisibleBonesOperator.bl_idname,
            text=PrintVisibleBonesOperator.bl_label,
            icon="CONSOLE",
        )
        column1.operator(
            PrintSelectedBonesOperator.bl_idname,
            text=PrintSelectedBonesOperator.bl_label,
            icon="CONSOLE",
        )
        column2: UILayout = column.column(align=True)
        column2.operator(
            PrintUnlockVGOperator.bl_idname,
            text=PrintUnlockVGOperator.bl_label,
            icon="CONSOLE",
        )
        column2.operator(
            PrintShapeKeysOperator.bl_idname,
            text=PrintShapeKeysOperator.bl_label,
            icon="CONSOLE",
        )


registry: list = [PrintsPanel]
