from typing import Any, Callable, override

from bpy.types import (
    Context,
    EditBone,
    Object,
    PoseBone,
)

from ...common.base.base_operator import BaseOperator
from ...common.utils.armature_utils import get_selected_epbones
from ...common.utils.name_utils import increment_last_number


class RenameBonesOperator(BaseOperator):
    bl_idname: str = "meldtool.rename_bones"
    bl_label: str = "命名骨骼链（尾数递增）"
    bl_options: set = {"REGISTER", "UNDO"}
    bl_description: str = "命名骨骼链，以根骨骼名中的数字以数字递增"

    def _rename_sequence(
        self, parent_bone: EditBone | PoseBone, callback: Callable[[], None] | None
    ) -> None:
        children: Any = parent_bone.children
        if len(children) == 1:  # 在骨骼只有一个直接子骨骼时命名这个直接子骨骼
            child: EditBone | PoseBone = children[0]
            new_name: str = increment_last_number(parent_bone.name, 1)
            if new_name == parent_bone.name:  # 如果遇到没有数字的骨骼，继续下去无意义。
                return
            child.name = new_name
            if callback is not None:
                callback()  # 更新计数
            self._rename_sequence(child, callback)

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        return cls.validate_armature_pose_edit(context)

    @override
    def execute(self, context: Context) -> set[str]:
        """在 Eidt Pose 模式下命名连续骨骼
        1_1.L -> 1_2.L -> 1_3.L
        """
        active_armature: Object = context.active_object
        if self.validate_armature_pose_edit(context, active_armature, self):
            return {"CANCELLED"}
        selected_bones: list[EditBone | PoseBone] = get_selected_epbones(
            active_armature
        )
        if self.validate(bool(selected_bones), "没有选择任何骨骼"):
            return {"CANCELLED"}

        rename_count: int = 0

        def _increment_callback() -> None:
            nonlocal rename_count
            rename_count += 1

        for start_bone in selected_bones:
            self._rename_sequence(parent_bone=start_bone, callback=_increment_callback)

        self.report({"INFO"}, f"已命名{rename_count}")
        return {"FINISHED"}


registry: list = [RenameBonesOperator]
