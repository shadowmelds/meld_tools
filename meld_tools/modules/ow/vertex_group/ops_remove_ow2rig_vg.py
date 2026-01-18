from typing import override

from bpy.types import (
    Context,
    Object,
)

from ....shared.base.base_operator import BaseOperator
from ....shared.models.enums_ow_skin import OWSkin
from .._utils import skin_data


class RemoveOW2RigVGOperator(BaseOperator):
    bl_idname: str = "meldtool.remove_ow2rig_vg"
    bl_label: str = "移除绑定顶点组"
    bl_options: set = {"REGISTER", "UNDO"}
    bl_description: str = "移除选中网格模型从守望先锋顶点组复制的绑定顶点组"

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        # 仅当有选中网格物体且物体未隐藏时，面板才可见
        return cls.validate_active_object_mesh(context.active_object)

    @override
    def execute(self, context: Context) -> set[str]:
        active_object: Object = context.active_object
        processed_number: int = 0

        skin: OWSkin = OWSkin(
            context.scene.meldtool_scene_properties.ow_main.current_skin  # type: ignore
        )
        skin_vertex_group: set = skin_data.get_skin_vertex_group(skin)

        for vertex_group in active_object.vertex_groups[:]:
            if vertex_group.name in skin_vertex_group:
                active_object.vertex_groups.remove(vertex_group)
                processed_number += 1

        self.report({"INFO"}, f"操作完成！已处理{processed_number}项")
        return {"FINISHED"}


registry: list = [RemoveOW2RigVGOperator]
