from typing import override

from bpy.types import Context, Panel, UILayout

from ...common.models.scripts import Script, ScriptID, get_scripts
from ...panel import MainPanel
from .ops_scripts import RemoveScriptOperator, WriteScriptOperator


class ScriptsPanel(MainPanel, Panel):
    bl_idname: str = "MELDTOOL_PT_scripts"
    bl_label: str = "脚本"
    bl_parent_id: str = "MELDTOOL_PT_general_main"
    bl_options: set = {"DEFAULT_CLOSED"}

    @override
    def draw(self, context: Context) -> None:
        scripts: dict[str, Script] = get_scripts(context)
        column1: UILayout = self.layout.column(align=True)
        row1: UILayout = column1.row(align=True)
        operator: WriteScriptOperator = row1.operator(
            WriteScriptOperator.bl_idname, text="写入批量移除顶点组脚本", icon="TEXT"
        )
        operator.script_name = scripts[ScriptID.REMOVE_VERTEX_GROUPS].name
        operator = row1.operator(RemoveScriptOperator.bl_idname, icon="TRASH", text="")
        operator.script_name = scripts[ScriptID.REMOVE_VERTEX_GROUPS].name

        row2: UILayout = column1.row(align=True)
        operator = row2.operator(
            WriteScriptOperator.bl_idname, text="写入合并权重脚本", icon="TEXT"
        )
        operator.script_name = scripts[ScriptID.MERGE_WEIGHT_VGROUPS].name
        operator = row2.operator(RemoveScriptOperator.bl_idname, icon="TRASH", text="")
        operator.script_name = scripts[ScriptID.MERGE_WEIGHT_VGROUPS].name


registry: list = [ScriptsPanel]
