from typing import override

from bpy.types import Context, Panel, UILayout

from ..panel import MainPanel
from .props_object_meld_rig import MeldRigObjectProperties


class MeldRigPanel(MainPanel, Panel):
    bl_idname: str = "MELDTOOL_PT_meld_rig"
    bl_label: str = "MeldRig"

    @classmethod
    @override
    def poll(cls: type["MeldRigPanel"], context: Context) -> bool:
        return context.object is not None and context.object.type == "ARMATURE"

    @override
    def draw_header(self, context: Context) -> None:
        properties_meld_rig: MeldRigObjectProperties = (
            context.object.meldtool_object_properties.meld_rig
        )
        layout = self.layout
        layout.prop(properties_meld_rig, "enabled", text="")

    @override
    def draw(self, context: Context) -> None:
        column: UILayout = self.layout.column()
        column.operator("meldtool.generate", text="生成骨架")


registry: list = [MeldRigPanel]
