import logging
from logging import Logger

from bpy.types import ArmatureBones, Bone, BoneCollection, Context, Object

from ...BoneUtil import getBoneName
from ...shared.base.base_operator import BaseOperator
from ...shared.models.result import Result
from ...shared.utils import armature_utils
from ...shared.utils.armature_utils import get_bone_collection
from ._data.skin_data import get_bones_with_collection
from ._models.collection_bones import CollectionBones
from ._models.enums_ow_bone_collection import OWBoneCollection
from ._models.enums_ow_skin import OWSkin


class RenameOWBonesOperator(BaseOperator):
    bl_idname: str = "meldtool.rename_ow_bones"
    bl_label: str = "为守望先锋骨骼重命名"
    bl_options: set = {"REGISTER", "UNDO"}
    bl_description: str = (
        "将守望先锋骨骼名改为具有可读性的名称，并且整理进骨骼集合，这依赖于插件内的记录"
    )

    logger: Logger = logging.getLogger()

    @classmethod
    def poll(cls, context: Context) -> bool:
        return cls.validate_armature_pose(context)

    def execute(self, context: Context) -> set[str]:
        active_armature: Object = context.active_object

        if self.validate_armature_pose(context, active_armature, self):
            return {"CANCELLED"}

        skin: OWSkin = OWSkin(
            context.scene.meldtool_scene_properties.ow.current_skin  # type: ignore
        )

        result: Result = self._rename(
            active_armature,
            get_bones_with_collection(skin),
        )

        self.logger.info(result.message)
        self.report({"INFO"}, result.message)
        return {"FINISHED"}

    def _rename(
        self,
        active_armature: Object,
        collection_bones: list[CollectionBones],
    ) -> Result:
        _success_num: int = 0
        _named_num: int = 0

        # 活动骨架所有骨骼
        armature_bones: ArmatureBones = active_armature.data.bones  # type: ignore

        self.logger.debug(f"当前角色所有骨骼数量为：{len(armature_bones)}")
        self.logger.debug(
            f"当全部需要重命名骨骼数量为：{sum(len(d.bones) for d in collection_bones)}"
        )

        for item in collection_bones:
            # 创建相应骨骼集合（不存在则创建）
            bone_collection: BoneCollection = get_bone_collection(
                armature=active_armature, name=item.collection.value
            )
            # 获取未命名骨骼集合（如果存在）为了可能二次命名需要从中移除掉
            unnamed_bone_collection: BoneCollection = get_bone_collection(
                armature=active_armature,
                name=OWBoneCollection.UNNAMED.value,
                auto_create=False,
            )
            # 设定当前骨骼集合为活动
            active_armature.data.collections.active = bone_collection  # type: ignore

            for ow_key, human in item.bones.items():
                # 如果被 io_scene_owm 命名过，则需要进行处理
                owm_key: str = getBoneName(ow_key)
                new_name: str = f"{item.prefix}{human.get_name()}"  # 加上前缀
                final_key: str = owm_key if ow_key != owm_key else ow_key
                if (
                    new_name != "" and final_key in armature_bones
                ):  # 未命名骨骼存在于骨架
                    bone: Bone = armature_bones.get(final_key)
                    # 指定至相应骨骼集合
                    bone_collection.assign(bone)
                    if (
                        unnamed_bone_collection
                    ):  # 如果有未命名骨骼集合，则移除已命名骨骼
                        unnamed_bone_collection.unassign(bone)
                    bone.name = new_name
                    named_boen_name: str = bone.name
                    if named_boen_name != new_name:
                        self.logger.warning(
                            f"命名冲突，应为{new_name} 冲突变为 {named_boen_name}"
                        )
                    _success_num += 1
                elif new_name in armature_bones:  # 已命名骨骼存在于骨架
                    _named_num += 1
                    self.logger.debug(f"{new_name} 已命名骨骼存在于骨架")
                else:
                    # 有的角色可能不含某些骨骼
                    self.logger.debug(f"{new_name} 未识别到")

        # 整理未命名和布料骨骼
        _cloth_count, _unname_count = self._organize_unnamed(active_armature)

        return Result.ok(
            message=f"已命名：{_success_num}, 未命名：{_unname_count}, 已存在：{_named_num}"
        )

    def _organize_unnamed(self, active_armature: Object) -> tuple[int, int]:
        """整理不需要重命名的骨骼到对应集合"""
        cloth_count: int = 0
        unname_count: int = 0
        armature_bones: ArmatureBones = active_armature.data.bones  # type: ignore

        cloth_bone_collection: BoneCollection = armature_utils.get_bone_collection(
            armature=active_armature, name=OWBoneCollection.CLOTH.value
        )
        unnamed_bone_collection: BoneCollection = armature_utils.get_bone_collection(
            armature=active_armature, name=OWBoneCollection.UNNAMED.value
        )

        for bone in armature_bones:
            if bone.name.startswith(
                "cloth_"
            ):  # cloth_开头的骨骼单独再放进 Cloth 骨骼集合
                cloth_bone_collection.assign(bone)
                cloth_count += 1
            elif bone.name.startswith(
                "bone_"
            ):  # 未命名的骨骼单独再放进 Unamed 骨骼集合
                unnamed_bone_collection.assign(bone)
                unname_count += 1
        return cloth_count, unname_count


registry: list = [RenameOWBonesOperator]
