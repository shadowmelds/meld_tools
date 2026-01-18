from typing import override

from bpy.types import ArmatureBones, BoneCollection, Context, Object

from ...shared.base.base_operator import BaseOperator
from ...shared.models.enums_ow_bone_collection import OWBoneCollection
from ...shared.utils import armature_utils
from ._data import ana_classic


class PrintUnnamedOWBonesOperator(BaseOperator):
    bl_idname: str = "meldtool.print_unnamed_ow_bones"
    bl_label: str = "打印未命名骨骼"
    bl_description: str = "重命名守望先锋骨骼遗漏的骨骼名将打印到控制台"

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        return cls.validate_armature_pose(context)

    @override
    def execute(self, context: Context) -> set[str]:
        active_armature: Object = context.active_object
        if self.validate_armature_pose(context, active_armature, self):
            return {"CANCELLED"}

        armature_bones: ArmatureBones = active_armature.data.bones  # type: ignore

        exist_bone_collection: BoneCollection = armature_utils.get_bone_collection(
            armature=active_armature, name=OWBoneCollection.EXIST.value
        )

        for bone in armature_bones:
            if bone.name.startswith("cloth_") or bone.name.startswith("OW-"):
                pass
            elif bone.name in ana_classic.point_bones():
                # 如果未命名骨骼存在于 ana_classic_point_bones 则指定至 exist 骨骼集合：
                exist_bone_collection.assign(bone)
                print(f"point exist: {bone.name}")
            else:
                print(f"unamed: {bone.name}")

        self.report({"INFO"}, "操作完成！")
        return {"FINISHED"}


registry: list = [PrintUnnamedOWBonesOperator]
