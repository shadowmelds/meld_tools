from typing import override

from bpy.types import Context, Object

from ...common.base.base_operator import BaseOperator
from ...common.utils.armature_utils import get_selected_ebones


class AlignBonesOperator(BaseOperator):
    bl_idname: str = "meldtool.align_bones"
    bl_label: str = "骨骼尾端 XY 对齐到头部 XY"
    bl_options: set = {"REGISTER", "UNDO"}
    bl_description: str = "选中所有骨骼尾端 XY 对齐到头部 XY"

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        return cls.validate_armature_edit(context)

    @override
    def execute(self, context: Context) -> set[str]:
        active_armature: Object | None = context.active_object
        if self.validate_armature_edit(context, active_armature, self):
            return {"CANCELLED"}
        selected_bones = get_selected_ebones(active_armature)
        if self.validate(bool(selected_bones), "没有选择任何骨骼"):
            return {"CANCELLED"}

        for ebone in selected_bones:
            head = ebone.head
            tail = ebone.tail

            # 将尾端 x、y 对齐到头部
            tail.x = head.x
            tail.y = head.y

        self.report({"INFO"}, f"操作完成！已处理{len(selected_bones)}项")
        return {"FINISHED"}


registry: list = [AlignBonesOperator]
