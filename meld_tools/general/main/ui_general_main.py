from typing import override

from bpy.types import Context, Panel

from ...panel import MainPanel
from ..toolset import box_toolset


class GeneralMainPanel(MainPanel, Panel):
    bl_idname: str = "MELDTOOL_PT_general_main"
    bl_label: str = "MeldTool"

    @override
    def draw(self, context: Context) -> None:
        layout = self.layout
        box_toolset.draw(layout=layout, context=context)


registry: list = [GeneralMainPanel]
