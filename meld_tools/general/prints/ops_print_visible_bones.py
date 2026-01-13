from typing import override

from bpy.types import (
    ArmatureBones,
    Context,
    Object,
)

from ...common.base.base_operator import BaseOperator
from ...common.utils.armature_utils import bone_visible_in_object_mode


class PrintVisibleBonesOperator(BaseOperator):
    bl_idname: str = "meldtool.print_visible_bones"
    bl_label: str = "打印可见骨骼（不支持孤立显示）"
    bl_description: str = "打印可见骨骼（不支持孤立显示模式）"

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        active_armature: Object = context.active_object
        return cls.validate(
            active_armature is not None and active_armature.type == "ARMATURE",
            "活动物体不是骨架物体",
        )

    @override
    def execute(self, context: Context) -> set[str]:
        active_armature: Object = context.active_object
        if self.validate(
            active_armature is not None and active_armature.type == "ARMATURE",
            "活动物体不是网格物体",
            self,
        ):
            return {"CANCELLED"}

        bones: ArmatureBones = active_armature.data.bones  # type: ignore
        bone_count: int = 0
        for bone in bones:
            if bone_visible_in_object_mode(bone, active_armature.data):
                # case_string: str = "\tcase(\"" + active_armature.data.bones[bone.name].name + "\"):\n            return \"\""
                case_string: str = '"' + bone.name + '",'
                bone_count += 1
                print(case_string)

        print(bone_count)
        return {"FINISHED"}


registry: list = [PrintVisibleBonesOperator]
