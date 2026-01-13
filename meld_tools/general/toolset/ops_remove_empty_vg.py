from typing import override

from bpy.types import Context, Object

from ...common.base.base_operator import BaseOperator


class RemoveEmptyVGOperator(BaseOperator):
    bl_idname: str = "meldtool.remove_empty_vg"
    bl_label: str = "移除空顶点组"
    bl_options: set = {"REGISTER", "UNDO"}
    bl_description: str = "移除选中物体的所有空顶点组"

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        return cls.validate_active_object_mesh(context.object)

    @override
    def execute(self, context: Context) -> set[str]:
        active_object: Object | None = context.active_object
        if self.validate_active_object_mesh(active_object, self):
            return {"CANCELLED"}
        _count: int = 0

        used_group_names: set = set()  # 顶点组名
        for mesh_vertex in active_object.data.vertices:  # type: ignore # 获取目标的每个顶点
            for vg_element in mesh_vertex.groups:  # 获取当前顶点所在的顶点组数据
                used_group_names.add(active_object.vertex_groups[vg_element.group].name)

        for vg in active_object.vertex_groups[:]:  # 使用切片副本避免索引问题
            if vg.name not in used_group_names:
                print(f"删除空顶点组: {vg.name}")
                active_object.vertex_groups.remove(vg)
                _count += 1

        self.report({"INFO"}, f"操作完成！已处理{_count}项")
        return {"FINISHED"}


registry: list = [RemoveEmptyVGOperator]
