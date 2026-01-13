from typing import override

from bpy.types import Context, Panel, UILayout

from ...panel import MainPanel
from .ops_copy_ow2rig_vg import CopyOW2RigVG2Operator, CopyOW2RigVGOperator
from .ops_lock_ow2rig_vg import LockOW2RigVGOperator, UnlockOW2RigVGOperator
from .ops_remove_ow2rig_vg import RemoveOW2RigVGOperator
from .ops_rename_ow_vg import RenameOWVGOperator


class OWVertexGroupPanel(MainPanel, Panel):
    bl_idname: str = "MELDTOOL_PT_vertex_group"
    bl_label: str = "顶点组"
    bl_parent_id: str = "MELDTOOL_PT_ow_main"
    bl_options: set = {"DEFAULT_CLOSED"}

    @override
    def draw(self, context: Context) -> None:
        column: UILayout = self.layout.column()
        column.operator(RenameOWVGOperator.bl_idname, text="命名守望先锋顶点组")
        column.operator(
            CopyOW2RigVGOperator.bl_idname,
            text="复制守望先锋权重至绑定顶点组",
            icon="DUPLICATE",
        )
        column.operator(
            CopyOW2RigVG2Operator.bl_idname,
            text="复制守望先锋权重至绑定顶点组（兼容）",
            icon="DUPLICATE",
        )
        column.operator(
            LockOW2RigVGOperator.bl_idname, text="锁定绑定顶点组", icon="VIEW_LOCKED"
        )
        column.operator(
            UnlockOW2RigVGOperator.bl_idname,
            text="取消锁定绑定顶点组",
            icon="VIEW_UNLOCKED",
        )
        column.operator(
            RemoveOW2RigVGOperator.bl_idname, text="移除绑定顶点组", icon="TRASH"
        )


registry: list = [OWVertexGroupPanel]
