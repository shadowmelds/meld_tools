from typing import Literal, override

from bpy.types import Context, Event, UILayout

from ...common.base.base_operator import BaseOperator
from .props_scene_toolset import ToolsetSceneProperties


class CopyExpressionOperator(BaseOperator):
    bl_idname: str = "meldtool.copy_expression"
    bl_label: str = "复制表达式"

    @override
    def execute(self, context: Context) -> set[str]:
        text: str = context.scene.meldtool_scene_properties.toolset.generator_result  # type: ignore
        context.window_manager.clipboard = text  # 复制到剪贴板
        self.report({"INFO"}, f"已复制: {text}")
        return {"FINISHED"}


class ExpressionGeneratorOperator(BaseOperator):
    bl_idname: str = "meldtool.expression_generator"
    bl_label: str = "表达式生成器"
    bl_description = "表达式生成器"

    @override
    def invoke(
        self, context: Context, event: Event
    ) -> set[
        Literal["RUNNING_MODAL", "CANCELLED", "FINISHED", "PASS_THROUGH", "INTERFACE"]
    ]:
        return context.window_manager.invoke_props_dialog(self, width=500)

    @override
    def draw(self, context: Context) -> None:
        properties_toolset: ToolsetSceneProperties = (
            context.scene.meldtool_scene_properties.toolset  # type: ignore
        )
        column: UILayout = self.layout.column()
        column.prop(properties_toolset, property="axis_start")
        column.prop(properties_toolset, property="axis_end")
        column.prop(properties_toolset, property="influence_start")
        column.prop(properties_toolset, property="influence_end")
        column.prop(properties_toolset, property="interpolation")
        column.prop(properties_toolset, property="clamp")
        column.prop(properties_toolset, property="angle")
        row: UILayout = column.row(align=True)
        row.prop(properties_toolset, property="generator_result")
        row.operator("meldtool.copy_expression", text="", icon="COPYDOWN")

    @override
    def execute(self, context: Context) -> set[str]:
        return {"INTERFACE"}


registry: list = [CopyExpressionOperator, ExpressionGeneratorOperator]
