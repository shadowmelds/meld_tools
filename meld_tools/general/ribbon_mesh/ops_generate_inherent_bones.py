from enum import StrEnum
from typing import Iterable, Literal, override

import bpy
from bpy.props import (
    StringProperty,
)
from bpy.types import (
    ArmatureEditBones,
    BoneCollection,
    Context,
    EditBone,
    Event,
    Object,
    Operator,
    UILayout,
)
from mathutils import Vector

from ...common.data.rigs import ribbon_mesh
from ...common.models.bone_desc import BoneDesc
from ...common.models.result_info import ResultInfo
from ...common.utils import armature_utils, name_utils, object_utils
from ...common.utils.function_utils import run_result
from .props_scene_ribbon_mesh import RibbonMeshSceneProperties


class RibbonMeshCollections(StrEnum):
    MOUTH_MCH = "Mouth MCH"
    MOUTH_MICRO = "Mouth Micro"
    MOUTH_LOCAL = "Mouth Local"
    MOUTH_GLOBAL = "Mouth Global"
    MOUTH_RIBBON = "Mouth Ribbon"


class GenerateImherentBonesActions(StrEnum):
    ALL = "ALL"
    STEP_1 = "BLOCK_1"
    STEP_2 = "BLOCK_2"


class GenerateInherentBonesOperator(Operator):
    bl_idname: str = "meldtool.generate_inherent_bones"
    bl_label: str = "生成固有骨骼"
    bl_options: set = {"REGISTER", "UNDO"}
    bl_description: str = "生成丝带结构的固有骨骼"

    action: bpy.props.EnumProperty(
        name="Action",
        items=[
            (GenerateImherentBonesActions.ALL, "全部", ""),
            (GenerateImherentBonesActions.STEP_1, "MCH+Micor", ""),
            (GenerateImherentBonesActions.STEP_2, "Local+Global", ""),
        ],
    )

    message: StringProperty(default="确保空物体集合内仅包含本次绑定的丝带所需的空物体")

    @override
    def invoke(
        self, context: Context, event: Event
    ) -> set[
        Literal["RUNNING_MODAL", "CANCELLED", "FINISHED", "PASS_THROUGH", "INTERFACE"]
    ]:
        return context.window_manager.invoke_props_dialog(self)

    @override
    def draw(self, context: Context) -> None:
        layout: UILayout = self.layout
        layout.label(text=self.message)

    @classmethod
    @override
    def poll(cls, context: Context):
        active_obj: Object = context.active_object
        ribbon_mesh: RibbonMeshSceneProperties = (
            context.scene.meldtool_scene_properties.ribbon_mesh
        )
        return (
            bool(ribbon_mesh.empty_object_collection)
            and bool(ribbon_mesh.target_armature)
            and bool(ribbon_mesh.target_parent_bone)
            and active_obj is not None
            and active_obj.type == "ARMATURE"
            and context.mode == "EDIT_ARMATURE"
        )

    def execute(self, context: Context):
        active_armature: Object = context.active_object
        if not object_utils.is_transform_applied(active_armature):
            self.report({"ERROR"}, "请先 Ctrl+A 应用所有变换")
            return {"CANCELLED"}

        ribbon_mesh: RibbonMeshSceneProperties = (
            context.scene.meldtool_scene_properties.ribbon_mesh
        )
        if context.mode != "EDIT_ARMATURE" and bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode="EDIT", toggle=False)

        collection_all_objects: Iterable[Object] = (
            ribbon_mesh.empty_object_collection.all_objects
        )
        emity_objects: list[Object] = [
            emity for emity in collection_all_objects if emity.type == "EMPTY"
        ]

        if self.action == GenerateImherentBonesActions.ALL:
            if not run_result(
                lambda: self.generate_bones1(
                    context=context,
                    active_armature=active_armature,
                    target_parent_bone_name=ribbon_mesh.target_parent_bone,
                    emity_objects=emity_objects,
                    use_cloud_rig=ribbon_mesh.use_cloud_rig,
                ),
                self,
            ):
                return {"CANCELLED"}
            if not run_result(
                lambda: self.generate_bones2(
                    context=context,
                    active_armature=active_armature,
                    emity_objects=emity_objects,
                    use_cloud_rig=ribbon_mesh.use_cloud_rig,
                ),
                self,
            ):
                return {"CANCELLED"}
        elif self.action == GenerateImherentBonesActions.STEP_1:
            if not run_result(
                lambda: self.generate_bones1(
                    context=context,
                    active_armature=active_armature,
                    target_parent_bone_name=ribbon_mesh.target_parent_bone,
                    emity_objects=emity_objects,
                    use_cloud_rig=ribbon_mesh.use_cloud_rig,
                ),
                self,
            ):
                return {"CANCELLED"}
        elif self.action == GenerateImherentBonesActions.STEP_2:
            if not run_result(
                lambda: self.generate_bones2(
                    context=context,
                    active_armature=active_armature,
                    emity_objects=emity_objects,
                    use_cloud_rig=ribbon_mesh.use_cloud_rig,
                ),
                self,
            ):
                return {"CANCELLED"}

        self.report({"INFO"}, "完成")
        return {"FINISHED"}

    def generate_bones1(
        self,
        context: Context,
        active_armature: Object,
        target_parent_bone_name: str,
        emity_objects: Iterable[Object],
        use_cloud_rig: bool = True,
    ) -> ResultInfo:
        target_parent_bone: EditBone = active_armature.data.edit_bones[
            target_parent_bone_name
        ]
        ebones: ArmatureEditBones = active_armature.data.edit_bones

        # 创建集合
        mch_collection: BoneCollection = armature_utils.get_bone_collection(
            armature=active_armature, name=RibbonMeshCollections.MOUTH_MCH
        )

        micro_collection: BoneCollection = armature_utils.get_bone_collection(
            armature=active_armature, name=RibbonMeshCollections.MOUTH_MICRO
        )

        # ==========================
        # 生成 Micro + MCH
        # ==========================

        def _check_names() -> ResultInfo:
            # 检查是否存在同名骨骼，存在提前终止
            for emity in emity_objects:
                emity_name: str = name_utils.object_name_to_bone_name(emity.name)
                micro_bone_name: str = name_utils.replace_start_keywords("", emity_name)
                mch_bone_name: str = name_utils.replace_start_keywords(
                    "MCH", emity_name
                )
                if micro_bone_name in ebones:
                    return ResultInfo(
                        status=False,
                        message=f"Setp1生成Micro失败：已存在相同名称骨骼：{micro_bone_name}",
                    )
                if mch_bone_name in ebones:
                    return ResultInfo(
                        status=False,
                        message=f"Setp1生成MCH失败：已存在相同名称骨骼：{mch_bone_name}",
                    )

        def _init_list_bone_desc() -> ResultInfo[list[BoneDesc]]:
            list_bone_desc: list[BoneDesc] = []
            for emity in emity_objects:
                emity_name: str = name_utils.object_name_to_bone_name(emity.name)
                mch_bone: BoneDesc = BoneDesc(
                    name=name_utils.replace_start_keywords("MCH", emity_name),
                    head=target_parent_bone.head.copy(),
                    tail=emity.matrix_world.translation.copy(),
                    parent=target_parent_bone.name,
                    display_type="STICK",
                    collections=[mch_collection],
                    use_cloud_rig=use_cloud_rig,
                    calculate_roll="GLOBAL_POS_Z",
                )
                list_bone_desc.append(mch_bone)
            for emity in emity_objects:
                mch_bone_name: str = name_utils.replace_start_keywords(
                    "MCH", emity_name
                )
                micro_bone: BoneDesc = BoneDesc(
                    name=name_utils.replace_start_keywords("", emity_name),
                    position_bone_by_name=mch_bone_name,
                    position_bone_location="TAIL",
                    tail_offset=Vector((0.0, 0.0, 0.001)),
                    parent=mch_bone_name,
                    bbone_x=0.00035,
                    bbone_z=0.00035,
                    palette="THEME01",
                    calculate_roll="GLOBAL_POS_Z",
                )
                list_bone_desc.append(micro_bone)

            return ResultInfo(data=list_bone_desc)

        def _generate(list_bone_desc: list[BoneDesc]) -> ResultInfo:
            return armature_utils.create_ebone_with_desc(
                active_armature=active_armature,
                context=context,
                list_bone_desc=list_bone_desc,
            )

        def _set_pose_mode(list_bone_desc: list[BoneDesc]) -> ResultInfo:
            return armature_utils.setup_pbone_with_desc(
                active_armature=active_armature,
                context=context,
                list_bone_desc=list_bone_desc,
            )

        def _set_constraint(list_bone_desc: list[BoneDesc]) -> ResultInfo:
            for bone_desc in list_bone_desc:
                # constraint: DampedTrackConstraint = mch_pose_bone.constraints.new('STRETCH_TO')
                # constraint.name = "拉伸到空物体"
                # constraint.target = emity
                # constraint.enabled = True
                pass

        if not (result := run_result(_check_names)):
            return result

        result: ResultInfo = run_result(_init_list_bone_desc)
        if not result:
            return result
        list_bone_desc: list[BoneDesc] = result.data

        if not (result := run_result(lambda: _generate(list_bone_desc))):
            return result

        if not (result := run_result(lambda: _set_pose_mode(list_bone_desc))):
            return result

    def generate_bones2(
        self,
        context: Context,
        active_armature: Object,
        use_cloud_rig: bool = False,
    ) -> ResultInfo | None:
        ebones: ArmatureEditBones = active_armature.data.edit_bones

        # 创建集合
        local_collection: BoneCollection = armature_utils.get_bone_collection(
            armature=active_armature, name=RibbonMeshCollections.MOUTH_LOCAL
        )
        golbal_collection: BoneCollection = armature_utils.get_bone_collection(
            armature=active_armature, name=RibbonMeshCollections.MOUTH_GLOBAL
        )
        ribbon_collection: BoneCollection = armature_utils.get_bone_collection(
            armature=active_armature, name=RibbonMeshCollections.MOUTH_RIBBON
        )

        def _check_names() -> ResultInfo:
            # 检查是否存在同名骨骼，存在提前终止
            check_names: dict[str, list] = {
                "Local": [
                    "CTL-Lips_corn_local.*",
                    "CTL-Lips_upp_local*CTL-Lips_low_local*",
                ],
                "Global": [
                    "CTL-Lips_upp_local",
                    "CTL-Lips_low_local",
                    "CTL-Lips_corn.*",
                    "CTL-Lips_upp_main",
                    "CTL-Lips_low_main",
                    "CTL-Lips_upp_second.*",
                    "CTL-Lips_low_second.*",
                ],
            }
            ebone_names = [ebone.name for ebone in ebones]
            for key, patterns in check_names.items():
                for name in ebone_names:
                    if any(name_utils.match_with_star(p, name) for p in patterns):
                        return ResultInfo(
                            status=False,
                            message=f"Setp2未生成生成：{key}已存在相同名称骨骼：{name}",
                        )

        def _init_list_bone_desc() -> ResultInfo[list[BoneDesc]]:
            if context.mode != "EDIT_ARMATURE" and bpy.ops.object.mode_set.poll():
                bpy.ops.object.mode_set(mode="EDIT", toggle=False)

            base_middle_upp_bone: EditBone | None = ebones.get("Lips_upp_micro")
            base_middle_low_bone: EditBone | None = ebones.get("Lips_low_micro")
            base_corn_l_bone: EditBone | None = ebones.get("Lips_corn_micro.L")
            base_corn_r_bone: EditBone | None = ebones.get("Lips_corn_micro.R")

            if not all(
                [
                    base_middle_upp_bone,
                    base_middle_low_bone,
                    base_corn_l_bone,
                    base_corn_r_bone,
                ]
            ):
                return ResultInfo(status=False, message="Step2 未生成：必要骨骼不全")

            # 思路：先生成有位置的部分，这部分比较简单，比如 Middle 和 Corner
            # 然后生成位置相对的部分
            list_bone_desc: list[BoneDesc] = ribbon_mesh.step2_bone_desc(
                local_collection=local_collection,
                golbal_collection=golbal_collection,
                ribbon_collection=ribbon_collection,
                base_middle_upp_bone=base_middle_upp_bone,
                base_middle_low_bone=base_middle_low_bone,
                base_corn_l_bone=base_corn_l_bone,
                base_corn_r_bone=base_corn_r_bone,
                use_cloud_rig=use_cloud_rig,
            )
            return ResultInfo(data=list_bone_desc)

        def _generate(list_bone_desc: list[BoneDesc]) -> ResultInfo:
            return armature_utils.create_ebone_with_desc(
                active_armature=active_armature,
                context=context,
                list_bone_desc=list_bone_desc,
            )

        def _set_pose_mode(list_bone_desc: list[BoneDesc]) -> ResultInfo:
            return armature_utils.setup_pbone_with_desc(
                active_armature=active_armature,
                context=context,
                list_bone_desc=list_bone_desc,
            )

        def _mirror(list_bone_desc: list[BoneDesc]) -> ResultInfo:
            return armature_utils.mirror_ebone_with_desc(
                active_armature=active_armature,
                context=context,
                list_bone_desc=list_bone_desc,
            )

        if not (result := run_result(_check_names)):
            return result

        result: ResultInfo = run_result(_init_list_bone_desc)
        if not result:
            return result
        list_bone_desc: list[BoneDesc] = result.data

        if not (result := run_result(lambda: _generate(list_bone_desc))):
            return result

        if not (result := run_result(lambda: _set_pose_mode(list_bone_desc))):
            return result

        if not (result := run_result(lambda: _mirror(list_bone_desc))):
            return result


registry: list = [GenerateInherentBonesOperator]
