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
    UILayout,
)
from mathutils import Vector

from ....shared.base.base_operator import BaseOperator
from ._data import ribbon_mesh
from ....shared.models.bone_desc import BoneDesc
from ....shared.models.result import Result
from ....shared.utils import armature_utils, name_utils
from ....shared.utils.object_utils import is_transform_applied
from .props_scene_ribbon_mesh import RibbonMeshSceneProperties


class RibbonMeshCollections(StrEnum):
    MOUTH_MCH = "Mouth MCH"
    MOUTH_MICRO = "Mouth Micro"
    MOUTH_LOCAL = "Mouth Local"
    MOUTH_GLOBAL = "Mouth Global"
    MOUTH_RIBBON = "Mouth Ribbon"


class GenerateInherentBonesSteps(StrEnum):
    ALL = "ALL"
    STEP_1 = "BLOCK_1"
    STEP_2 = "BLOCK_2"


class GenerateInherentBonesOperator(BaseOperator):
    bl_idname: str = "meldtool.generate_inherent_bones"
    bl_label: str = "生成固有骨骼"
    bl_options: set = {"REGISTER", "UNDO"}
    bl_description: str = "生成丝带结构的固有骨骼"

    action: bpy.props.EnumProperty(
        name="Action",
        items=[
            (GenerateInherentBonesSteps.ALL, "全部", ""),
            (GenerateInherentBonesSteps.STEP_1, "MCH+Micor", ""),
            (GenerateInherentBonesSteps.STEP_2, "Local+Global", ""),
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
    def poll(cls, context: Context) -> bool:
        ribbon_mesh: RibbonMeshSceneProperties = (
            context.scene.meldtool_scene_properties.ribbon_mesh
        )

        return (
            cls.validate_armature_edit(context, context.active_object)
            and cls.validate(
                bool(ribbon_mesh.empty_object_collection), "请设置空物体集合"
            )
            and cls.validate(bool(ribbon_mesh.target_armature), "请设置目标骨架")
            and cls.validate(bool(ribbon_mesh.target_parent_bone), "请设置目标父骨骼")
        )

    @override
    def execute(self, context: Context) -> set[str]:
        active_armature: Object = context.active_object
        if self.validate_armature_edit(context, active_armature, self):
            return {"CANCELLED"}

        if self.validate(
            is_transform_applied(active_armature), "请先 Ctrl+A 应用所有变换", self
        ):
            return {"CANCELLED"}

        ribbon_mesh: RibbonMeshSceneProperties = (
            context.scene.meldtool_scene_properties.ribbon_mesh
        )

        if self.validate(
            bool(ribbon_mesh.target_armature), "请设置目标骨架", self
        ) and self.validate(
            bool(ribbon_mesh.target_parent_bone), "请设置目标父骨骼", self
        ):
            return {"CANCELLED"}

        collection_all_objects: Iterable[Object] = (
            ribbon_mesh.empty_object_collection.all_objects
        )
        empty_objects: list[Object] = [
            empty for empty in collection_all_objects if empty.type == "EMPTY"
        ]

        def _step_1() -> Result:
            return self._generate_bones1(
                context=context,
                active_armature=active_armature,
                target_parent_bone_name=ribbon_mesh.target_parent_bone,
                empty_objects=empty_objects,
                use_cloud_rig=ribbon_mesh.use_cloud_rig,
            )

        def _step_2() -> Result:
            return self._generate_bones2(
                context=context,
                active_armature=active_armature,
                use_cloud_rig=ribbon_mesh.use_cloud_rig,
            )

        steps: dict[GenerateInherentBonesSteps, tuple] = {
            GenerateInherentBonesSteps.ALL: (_step_1, _step_2),
            GenerateInherentBonesSteps.STEP_1: (_step_1,),
            GenerateInherentBonesSteps.STEP_2: (_step_2),
        }

        for index, step in enumerate(steps[self.action]):
            if not (result := step()):
                self.report(
                    {"ERROR"}, f"{self.action} step: {index + 1}: " + result.message
                )
                return {"CANCELLED"}

        self.report({"INFO"}, "完成")
        return {"FINISHED"}

    def _generate_bones1(
        self,
        context: Context,
        active_armature: Object,
        target_parent_bone_name: str,
        empty_objects: list[Object],
        use_cloud_rig: bool = True,
    ) -> Result:
        if context.mode != "EDIT_ARMATURE" and bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode="EDIT", toggle=False)
        target_parent_bone: EditBone = active_armature.data.edit_bones.get(
            target_parent_bone_name
        )
        if not target_parent_bone:
            return Result.fail(f"无法找到 {target_parent_bone_name} 骨骼")
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

        def _check_names() -> Result:
            # 检查是否存在同名骨骼，存在提前终止
            for empty in empty_objects:
                empty_name: str = name_utils.object_name_to_bone_name(empty.name)
                micro_bone_name: str = name_utils.replace_start_keywords("", empty_name)
                mch_bone_name: str = name_utils.replace_start_keywords(
                    "MCH", empty_name
                )
                if micro_bone_name in ebones:
                    return Result(
                        f"生成Micro失败：已存在相同名称骨骼：{micro_bone_name}",
                    )
                if mch_bone_name in ebones:
                    return Result(
                        f"生成MCH失败：已存在相同名称骨骼：{mch_bone_name}",
                    )
            return Result.ok()

        def _init_list_bone_desc() -> Result[list[BoneDesc]]:
            list_bone_desc: list[BoneDesc] = []
            for empty in empty_objects:
                empty_name: str = name_utils.object_name_to_bone_name(empty.name)
                mch_bone: BoneDesc = BoneDesc(
                    name=name_utils.replace_start_keywords("MCH", empty_name),
                    head=target_parent_bone.head.copy(),
                    tail=empty.matrix_world.translation.copy(),
                    parent=target_parent_bone.name,
                    display_type="STICK",
                    collections=[mch_collection],
                    use_cloud_rig=use_cloud_rig,
                    calculate_roll="GLOBAL_POS_Z",
                )
                list_bone_desc.append(mch_bone)
            for empty in empty_objects:
                empty_name: str = name_utils.object_name_to_bone_name(empty.name)
                mch_bone_name: str = name_utils.replace_start_keywords(
                    "MCH", empty_name
                )
                micro_bone: BoneDesc = BoneDesc(
                    name=name_utils.replace_start_keywords("", empty_name),
                    position_bone_by_name=mch_bone_name,
                    position_bone_location="TAIL",
                    tail_offset=Vector((0.0, 0.0, 0.001)),
                    parent=mch_bone_name,
                    collections=[micro_collection],
                    bbone_x=0.00035,
                    bbone_z=0.00035,
                    palette="THEME01",
                    calculate_roll="GLOBAL_POS_Z",
                )
                list_bone_desc.append(micro_bone)

            return Result(data=list_bone_desc)

        def _generate(list_bone_desc: list[BoneDesc]) -> Result:
            return armature_utils.create_ebone_with_desc(
                active_armature=active_armature,
                list_bone_desc=list_bone_desc,
            )

        def _set_pose_mode(list_bone_desc: list[BoneDesc]) -> Result:
            if context.mode != "POSE" and bpy.ops.object.mode_set.poll():
                bpy.ops.object.mode_set(mode="POSE")
            return armature_utils.setup_pbone_with_desc(
                active_armature=active_armature,
                list_bone_desc=list_bone_desc,
            )

        def _set_constraint(list_bone_desc: list[BoneDesc]) -> Result:
            for bone_desc in list_bone_desc:
                # constraint: DampedTrackConstraint = mch_pose_bone.constraints.new('STRETCH_TO')
                # constraint.name = "拉伸到空物体"
                # constraint.target = empty
                # constraint.enabled = True
                pass

        if not (result := _check_names()):
            return result

        if not (result := _init_list_bone_desc()):
            return result

        list_bone_desc: list[BoneDesc] = result.data

        if not (result := _generate(list_bone_desc)):
            return result

        if not (result := _set_pose_mode(list_bone_desc)):
            return result

        return Result.ok()

    def _generate_bones2(
        self,
        context: Context,
        active_armature: Object,
        use_cloud_rig: bool = False,
    ) -> Result:
        if context.mode != "EDIT_ARMATURE" and bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode="EDIT", toggle=False)
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

        def _check_names() -> Result:
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
                    if any(name_utils.match_with_wildcard(p, name) for p in patterns):
                        return Result.fail(
                            f"Setp2未生成生成：{key}已存在相同名称骨骼：{name}"
                        )
            return Result.ok()

        def _init_list_bone_desc() -> Result[list[BoneDesc]]:
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
                return Result.fail("未生成：必要骨骼不全")

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
            return Result.ok(data=list_bone_desc)

        def _generate(list_bone_desc: list[BoneDesc]) -> Result:
            return armature_utils.create_ebone_with_desc(
                active_armature=active_armature,
                list_bone_desc=list_bone_desc,
            )

        def _set_pose_mode(list_bone_desc: list[BoneDesc]) -> Result:
            if context.mode != "POSE" and bpy.ops.object.mode_set.poll():
                bpy.ops.object.mode_set(mode="POSE")
            return armature_utils.setup_pbone_with_desc(
                active_armature=active_armature,
                list_bone_desc=list_bone_desc,
            )

        def _mirror(list_bone_desc: list[BoneDesc]) -> Result:
            return armature_utils.mirror_ebone_with_desc(
                active_armature=active_armature,
                list_bone_desc=list_bone_desc,
            )

        if not (result := _check_names()):
            return result

        if not (result := _init_list_bone_desc()):
            return result

        list_bone_desc: list[BoneDesc] = result.data

        if not (result := _generate(list_bone_desc)):
            return result

        if not (result := _set_pose_mode(list_bone_desc)):
            return result

        if not (result := _mirror(list_bone_desc)):
            return result

        return result.ok()


registry: list = [GenerateInherentBonesOperator]
