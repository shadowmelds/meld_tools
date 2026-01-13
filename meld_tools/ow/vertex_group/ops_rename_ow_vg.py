from typing import override

from bpy.types import (
    Context,
    Object,
)

from ...common.base.base_operator import BaseOperator
from ...common.models.enums_ow_skin import OWSkin
from ...common.utils import skin_data


class RenameOWVGOperator(BaseOperator):
    bl_idname: str = "meldtool.rename_ow_vg"
    bl_label: str = "重命名OW顶点组"
    bl_options: set = {"REGISTER", "UNDO"}
    bl_description: str = (
        "将选中网格物体的守望先锋顶点组改为具有可读性的名称，这依赖于插件内的记录"
    )

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
        bones: dict = skin_data.get_skin_bones(skin)

        for vertex_group in active_object.vertex_groups:
            vertex_group_name: str = vertex_group.name
            if vertex_group_name in bones:
                vertex_group.name = bones[vertex_group_name]
                processed_number += 1

        self.report({"INFO"}, f"操作完成！已处理{processed_number}项")
        return {"FINISHED"}


registry: list = [RenameOWVGOperator]
