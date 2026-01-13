from typing import Callable, override

from bpy.types import ArmatureBones, Bone, BoneCollection, Context, Object

from ...common.base.base_operator import BaseOperator
from ...common.models.enums_ow_bone_collection import OWBoneCollection
from ...common.models.enums_ow_skin import OWSkin
from ...common.utils import armature_utils, skin_data


class RenameOWBonesOperator(BaseOperator):
    bl_idname: str = "meldtool.rename_ow_bones"
    bl_label: str = "为所有骨骼重命名"
    bl_options: set = {"REGISTER", "UNDO"}
    bl_description: str = "将守望先锋骨骼名改为具有可读性的名称，这依赖于插件内的记录"

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        # 活动物体为骨架时才可用，否则处于不可用状态（按钮为灰色）
        return cls.validate_armature_pose(context)

    @override
    def execute(self, context: Context) -> set[str]:
        active_armature: Object = context.active_object

        if self.validate_armature_pose(context, active_armature, self):
            return {"CANCELLED"}

        current_skin: OWSkin = OWSkin(
            context.scene.meldtool_scene_properties.ow_main.current_skin  # type: ignore
        )
        success_num: int = 0
        named_num: int = 0
        cloth_num: int = 0

        # 重命名一些骨骼后更新计数
        def callback_count(a: int, b: int) -> None:
            nonlocal success_num, named_num
            success_num, named_num = success_num + a, named_num + b

        for item in skin_data.get_bones_with_collection(skin=current_skin):
            self._rename_bone_dict(
                active_armature=active_armature,
                bone_dict=item.bones,
                ow_bone_collection=item.collection,
                callback=callback_count,
            )

        # 活动骨架所有骨骼
        armature_bones: ArmatureBones = active_armature.data.bones  # type: ignore

        cloth_bone_collection: BoneCollection = armature_utils.get_bone_collection(
            armature=active_armature, name=OWBoneCollection.CLOTH.value
        )
        unamed_bone_collection: BoneCollection = armature_utils.get_bone_collection(
            armature=active_armature, name=OWBoneCollection.UNAMED.value
        )

        for bone in armature_bones:
            if bone.name.startswith(
                "cloth_"
            ):  # cloth_开头的骨骼单独再放进 Cloth 骨骼集合
                cloth_bone_collection.assign(bone)
                cloth_num += 1
            elif bone.name.startswith(
                "bone_"
            ):  # 未命名的骨骼单独再放进 Unamed 骨骼集合
                unamed_bone_collection.assign(bone)

        unnamed_num: int = f"{len(armature_bones) - (success_num + named_num + cloth_num)}"  # 计数也不含 cloth_ 这种骨骼

        self.report(
            {"INFO"}, f"已命名：{success_num}未命名：{unnamed_num}已存在：{named_num}"
        )
        return {"FINISHED"}

    def _rename_bone_dict(
        self,
        active_armature: Object,
        bone_dict: dict,
        ow_bone_collection: OWBoneCollection,
        callback: Callable[[int, int], None],
    ) -> None:
        """重命名骨骼，并将骨骼放置到相应的骨骼集合"""

        # 活动骨架所有骨骼
        armature_bones: ArmatureBones = active_armature.data.bones  # type: ignore

        success_num: int = 0
        named_num: int = 0

        # 创建相应骨骼集合（不存在则创建）
        bone_collection: BoneCollection = armature_utils.get_bone_collection(
            armature=active_armature, name=ow_bone_collection.value
        )
        # 获取未命名骨骼集合（如果存在）
        unamed_bone_collection: BoneCollection = armature_utils.get_bone_collection(
            armature=active_armature,
            name=OWBoneCollection.UNAMED.value,
            auto_create=False,
        )
        # 设定当前骨骼集合为活动
        active_armature.data.collections.active = bone_collection  # type: ignore

        for key, value in bone_dict.items():
            new_name: str = value
            if value != "" and key in armature_bones:  # 未命名骨骼存在于骨架
                bone: Bone = armature_bones[key]
                # 指定至相应骨骼集合
                bone_collection.assign(bone)
                if unamed_bone_collection:  # 如果有未命名骨骼集合，则移除已命名骨骼
                    unamed_bone_collection.unassign(bone)
                bone.name = new_name
                success_num += 1
            elif new_name in armature_bones:  # 已命名骨骼存在于骨架
                named_num += 1
        # 更新计数
        callback(success_num, named_num)


registry: list = [RenameOWBonesOperator]
