from typing import override

from bpy.types import Context, Panel, UILayout

from ....panel import MainPanel
from .ops_generate_empty_objects import GenerateEmptyObjectsOperator
from .ops_generate_inherent_bones import (
    GenerateInherentBonesOperator,
    GenerateInherentBonesSteps,
)
from .props_scene_ribbon_mesh import RibbonMeshSceneProperties


class RibbonPanel(MainPanel, Panel):
    bl_idname: str = "MELDTOOL_PT_ribbon"
    bl_label: str = "丝带绑定"
    bl_parent_id: str = "MELDTOOL_PT_general_main"
    bl_options: set = {"DEFAULT_CLOSED"}

    @override
    def draw(self, context: Context) -> None:
        ribbon_mesh: RibbonMeshSceneProperties = (
            context.scene.meldtool_scene_properties.ribbon_mesh
        )
        column: UILayout = self.layout.column()
        box1: UILayout = column.box()
        box1.prop(
            data=ribbon_mesh, property="empty_object_collection", text="空物体集合"
        )
        box1.operator(
            operator=GenerateEmptyObjectsOperator.bl_idname,
            text="生成空物体",
            icon="EMPTY_AXIS",
        )
        column1: UILayout = box1.column(align=True)
        column1.prop(data=ribbon_mesh, property="target_armature", text="目标骨架")
        column2: UILayout = column1.column()
        column2.enabled = ribbon_mesh.target_armature is not None
        if ribbon_mesh.target_armature:
            column2.prop_search(
                data=ribbon_mesh,
                property="target_parent_bone",
                search_data=ribbon_mesh.target_armature.data,
                search_property="bones",
                text="目标父骨骼",
            )
        else:
            # 没选骨架——显示一个灰掉的空字段（不会报错）
            column2.prop(
                ribbon_mesh, "target_parent_bone", text="目标父骨骼", icon="BONE_DATA"
            )
        split: UILayout = box1.split(factor=0.6)
        split.operator(
            operator=GenerateInherentBonesOperator.bl_idname,
            text=GenerateInherentBonesOperator.bl_label,
            icon="BONE_DATA",
        ).action = GenerateInherentBonesSteps.ALL
        split.prop(data=ribbon_mesh, property="use_cloud_rig", text="CloudRig")
        column: UILayout = box1.column(align=True)
        column.operator(
            operator=GenerateInherentBonesOperator.bl_idname,
            text=GenerateInherentBonesOperator.bl_label + "1",
            icon="BONE_DATA",
        ).action = GenerateInherentBonesSteps.STEP_1
        column.operator(
            operator=GenerateInherentBonesOperator.bl_idname,
            text=GenerateInherentBonesOperator.bl_label + "2",
            icon="BONE_DATA",
        ).action = GenerateInherentBonesSteps.STEP_2


registry: list = [RibbonPanel]
