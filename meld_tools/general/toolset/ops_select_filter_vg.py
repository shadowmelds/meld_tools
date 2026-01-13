from typing import override

import bpy
from bpy.types import Context, Object

from ...common.base.base_operator import BaseOperator


class SelectFilterVGOperator(BaseOperator):
    bl_idname: str = "meldtool.select_filter_vg"
    bl_label: str = "选中过滤顶点组"
    bl_options: set = {"REGISTER", "UNDO"}
    bl_description: str = "选中所有包含关键字的顶点组，执行自动切换至编辑模式"

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        return cls.validate(
            bool(context.object.meldtool_object_properties.include_keyword),  # type: ignore
            "没有设置关键字",
        ) and cls.validate_active_object_mesh(context.active_object)

    @override
    def execute(self, context: Context) -> set[str]:
        active_object: Object = context.active_object
        str_filter: str = context.object.meldtool_object_properties.include_keyword  # type: ignore
        if self.validate(
            bool(str_filter),  # type: ignore
            "没有设置关键字",
            self,
        ) and self.validate_mesh_edit(active_object, self):
            return {"CANCELLED"}

        keywords_list: list = str_filter.split(",")
        # 遍历活动物体顶点组
        for vertex_group in active_object.vertex_groups:
            if any(
                keywords in vertex_group.name for keywords in keywords_list
            ):  # 如果顶点组名称含关键字
                bpy.ops.object.vertex_group_set_active(group=str(vertex_group.name))
                bpy.ops.object.vertex_group_select()
        self.report({"INFO"}, "操作完成！")
        return {"FINISHED"}


registry: list = [SelectFilterVGOperator]
