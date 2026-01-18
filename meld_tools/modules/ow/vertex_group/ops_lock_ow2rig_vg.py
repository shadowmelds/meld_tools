from typing import override

from bpy.types import Context, Object

from ....shared.base.base_operator import BaseOperator
from ....shared.models.enums_ow_skin import OWSkin
from .._utils import skin_data


class LockOW2RigVGOperator(BaseOperator):
    bl_idname: str = "meldtool.lock_ow2rig_vg"
    bl_label: str = "锁定绑定顶点组"
    bl_options: set = {"REGISTER", "UNDO"}
    bl_description: str = "锁定从守望先锋顶点组复制的绑定顶点组"

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

        for vertex_group in active_object.vertex_groups:
            if vertex_group.name in skin_vertex_group:
                vertex_group.lock_weight = True
                processed_number += 1

        self.report({"INFO"}, f"操作完成！已处理{processed_number}项")
        return {"FINISHED"}


class UnlockOW2RigVGOperator(BaseOperator):
    bl_idname: str = "meldtool.unlock_ow2rig_vg"
    bl_label: str = "取消锁定绑定顶点组"
    bl_options: set = {"REGISTER", "UNDO"}
    bl_description: str = "取消锁定从守望先锋顶点组复制的绑定顶点组"

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

        for vertex_group in active_object.vertex_groups:
            if vertex_group.name in skin_vertex_group():
                vertex_group.lock_weight = False
                processed_number += 1

        self.report({"INFO"}, f"操作完成！已处理{processed_number}项")
        return {"FINISHED"}


registry: list = [LockOW2RigVGOperator, UnlockOW2RigVGOperator]
