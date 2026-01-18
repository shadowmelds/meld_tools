from typing import override

from bpy.types import Context

from ...shared.base.base_operator import BaseOperator


class GenerateOparetor(BaseOperator):
    bl_idname = "meldtool.generate"
    bl_label = "生成骨架"

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        return context.object.meldtool_object_properties.meld_rig.enabled == True

    @override
    def execute(self, context: Context) -> set[str]:
        return {"CANCELLED"}


registry = [GenerateOparetor]
