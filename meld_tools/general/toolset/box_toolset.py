from bpy.types import Context, Object, UILayout

from ...properties import MeldToolObjectProperties
from .ops_align_bones import AlignBonesOperator
from .ops_expression_generator import ExpressionGeneratorOperator
from .ops_load_bone_collections import LoadBoneCollectionsOperator
from .ops_remove_empty_vg import RemoveEmptyVGOperator
from .ops_select_filter_vg import SelectFilterVGOperator


def draw(layout: UILayout, context: Context) -> None:
    box = layout.box()
    box.label(text="功能集")
    column1: UILayout = box.column()
    active_object: Object = context.active_object
    column1.operator(
        ExpressionGeneratorOperator.bl_idname, text=ExpressionGeneratorOperator.bl_label
    )
    column1.operator(
        RemoveEmptyVGOperator.bl_idname,
        text=RemoveEmptyVGOperator.bl_label,
        icon="BRUSH_DATA",
    )

    if (
        active_object is not None
        and active_object.type == "MESH"
        and hasattr(active_object, "meldtool_object_properties")
    ):
        props: MeldToolObjectProperties = active_object.meldtool_object_properties  # type: ignore
        if hasattr(props, "include_keyword"):
            box1 = box.box()
            vgcolumn: UILayout = box1.column()
            vgcolumn.prop(
                data=props, property="include_keyword", placeholder="关键词1,关键词2"
            )
            vgcolumn.operator(
                SelectFilterVGOperator.bl_idname,
                text=SelectFilterVGOperator.bl_label,
                icon="RESTRICT_SELECT_OFF",
            )

    column2: UILayout = box.column()
    column2.operator(AlignBonesOperator.bl_idname, text=AlignBonesOperator.bl_label)
    column2.operator(
        LoadBoneCollectionsOperator.bl_idname, text=LoadBoneCollectionsOperator.bl_label
    )
