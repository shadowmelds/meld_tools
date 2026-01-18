from typing import override

from bpy.types import (
    Context,
    Object,
)

from ....shared.base.base_operator import BaseOperator


class PrintSelectedBonesOperator(BaseOperator):
    bl_idname: str = "meldtool.print_selected_bones"
    bl_label: str = "打印选中骨骼"
    bl_description: str = "打印选中骨骼名到控制台"

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        return cls.validate_armature_pose_edit(context)

    @override
    def execute(self, context: Context) -> set[str]:
        active_armature: Object = context.active_object
        if self.validate_armature_pose_edit(context, active_armature, self):
            return {"CANCELLED"}

        bone_count: int = 0
        if context.mode == "POSE":
            for pose_bone in active_armature.pose.bones:
                if pose_bone.select:  # type: ignore
                    case_string: str = '"' + pose_bone.name + '",'
                    bone_count += 1
                    print(case_string)
        elif context.mode == "EDIT":
            for edit_bone in active_armature.data.edit_bones:  # type: ignore
                if edit_bone.select:
                    case_string: str = '"' + edit_bone.name + '",'
                    bone_count += 1
                    print(case_string)

        self.report({"INFO"}, f"已打印 {bone_count} 条")
        return {"FINISHED"}


registry: list = [PrintSelectedBonesOperator]
