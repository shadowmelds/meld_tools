from typing import override

from bpy.types import Context, Panel, UILayout

from ...common.models.scripts import Script, ScriptID, get_scripts
from ...panel import MainPanel
from ..scripts.ops_scripts import (
    RemoveScriptOperator,
    RunScriptOperator,
    WriteScriptOperator,
)
from .ops_generate_vg import GenerateVGOperator
from .ops_phys_constraints import CopyLocationOperator, DampedTrackOperator
from .ops_phys_objects import ConvertMeshOperator, CreateCurveOperator
from .ops_rename_bones import RenameBonesOperator
from .props_scene_phys import PhysSceneProperties


class PhysPanel(MainPanel, Panel):
    bl_idname: str = "MELDTOOL_PT_phys"
    bl_label: str = "物理绑定"
    bl_parent_id: str = "MELDTOOL_PT_general_main"
    bl_options: set = {"DEFAULT_CLOSED"}

    @override
    def draw(self, context: Context) -> None:
        phys: PhysSceneProperties = context.scene.meldtool_scene_properties.phys  # type: ignore
        collision_fix: Script = get_scripts(context)[ScriptID.COLLISION_FIX]

        column: UILayout = self.layout.column()
        column.operator(
            RenameBonesOperator.bl_idname, text=RenameBonesOperator.bl_label
        )
        column.operator(
            "wm.call_menu", text="布料预设", icon="PRESET"
        ).name = "MELDTOOL_MT_cloth_preset"

        box1: UILayout = column.box()
        # 物体选择器（带吸管功能）
        column1: UILayout = box1.column(align=True)
        column1.operator(
            CreateCurveOperator.bl_idname,
            text=CreateCurveOperator.bl_label,
            icon="OUTLINER_OB_CURVE",
        )
        column1.operator(
            ConvertMeshOperator.bl_idname,
            text=ConvertMeshOperator.bl_label,
            icon="OUTLINER_OB_MESH",
        )

        box1.prop(data=phys, property="target_object", text="目标物体")

        column2: UILayout = box1.column(align=True)
        column2.operator(
            GenerateVGOperator.bl_idname, text=GenerateVGOperator.bl_label, icon="ADD"
        )
        column2.operator(
            DampedTrackOperator.bl_idname,
            text=DampedTrackOperator.bl_label,
            icon="CONSTRAINT_BONE",
        )
        column2.operator(
            CopyLocationOperator.bl_idname,
            text=CopyLocationOperator.bl_label,
            icon="CONSTRAINT_BONE",
        )

        split: UILayout = column.split(factor=0.7, align=True)
        row1: UILayout = split.row(align=True)
        operator: WriteScriptOperator = row1.operator(
            WriteScriptOperator.bl_idname,
            text="写入碰撞修复脚本",
            icon="TEXT",
        )
        operator.script_name = collision_fix.name
        operator = row1.operator(RunScriptOperator.bl_idname, icon="PLAY", text="")
        operator.script_name = collision_fix.name
        operator = row1.operator(RemoveScriptOperator.bl_idname, icon="TRASH", text="")
        operator.script_name = collision_fix.name
        row2: UILayout = split.row(align=True)
        row2.prop(data=phys, property="use_module_collision_fix")


registry: list = [PhysPanel]
