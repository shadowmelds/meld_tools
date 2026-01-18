from typing import Callable, override

from bpy.types import (
    Context,
    CopyLocationConstraint,
    DampedTrackConstraint,
    Object,
    PoseBone,
)

from ....shared.base.base_operator import BaseOperator
from ....shared.utils.armature_utils import get_selected_pbones


class CopyLocationOperator(BaseOperator):
    bl_idname: str = "meldtool.copy_location"
    bl_label: str = "选中骨骼链添加复制位置"
    bl_options: set = {"REGISTER", "UNDO"}
    bl_description: str = "为选中骨骼链添加复制位置约束，目标为模拟网格物体顶点组"

    def _create_phys_copy_location_constraint(
        self,
        target_object: Object,
        parent_bone: PoseBone,
        callback: Callable[[], None] | None,
    ) -> None:
        """删除已存在的（如果有）复制位置约束，生成新的复制位置约束"""
        constraint: CopyLocationConstraint = parent_bone.constraints.get(
            "COPY_LOCATION"
        )
        if constraint is not None:
            parent_bone.constraints.remove(constraint)
        constraint = parent_bone.constraints.new("COPY_LOCATION")
        constraint.name = "COPY_LOCATION"
        constraint.target = target_object
        constraint.use_x = True
        constraint.use_y = True
        constraint.use_z = True
        constraint.subtarget = parent_bone.name
        constraint.influence = 1.0
        constraint.enabled = True
        if callback is not None:
            callback()  # 更新计数
        children = parent_bone.children
        if len(children) == 1:  # 在骨骼只有一个直接子骨骼时创建约束
            child: PoseBone = children[0]
            self._create_phys_copy_location_constraint(target_object, child, callback)

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        """活动物体为骨架并且在姿态模式 & 存在目标模拟网格"""
        return cls.validate_armature_pose(context) and cls.validate(
            context.scene.meldtool_scene_properties.phys.target_object is not None,  # type: ignore
            "未选择目标模拟网格",
        )

    @override
    def execute(self, context: Context) -> set[str]:
        active_armature: Object | None = context.active_object
        target_object: Object | None = (
            context.scene.meldtool_scene_properties.phys.target_object  # type: ignore
        )

        if self.validate_armature_pose(context, active_armature, self) or self.validate(
            target_object is not None, "未选择目标模拟网格", self
        ):
            return {"CANCELLED"}

        selected_bones: list[PoseBone] = get_selected_pbones(active_armature)
        if self.validate(bool(selected_bones), "没有选择任何骨骼"):
            return {"CANCELLED"}

        constraint_count: int = 0

        def _increment_callback() -> None:
            nonlocal constraint_count
            constraint_count += 1

        for start_bone in selected_bones:
            self._create_phys_copy_location_constraint(
                target_object, start_bone, _increment_callback
            )

        self.report({"INFO"}, f"成功创建: {constraint_count} 个约束")
        return {"FINISHED"}


class DampedTrackOperator(BaseOperator):
    bl_idname: str = "meldtool.damped_track"
    bl_label: str = "选中骨骼链添加阻尼追踪"
    bl_options: set = {"REGISTER", "UNDO"}
    bl_description: str = (
        "添加阻尼追踪约束到选中骨骼链，约束目标为模拟网格物体相应顶点组"
    )

    def _create_phys_damped_track_constraint(
        self,
        target_object: Object,
        parent_bone: PoseBone,
        callback: Callable[[], None] | None,
    ) -> None:
        constraint = parent_bone.constraints.get("TRACK_PHYS")
        if constraint is not None:
            parent_bone.constraints.remove(constraint)
        constraint: DampedTrackConstraint = parent_bone.constraints.new("DAMPED_TRACK")
        constraint.name = "TRACK_PHYS"
        constraint.target = target_object
        constraint.track_axis = "TRACK_Y"  # TRACK_NEGATIVE_Y
        constraint.subtarget = parent_bone.name
        constraint.influence = 1.0
        constraint.enabled = True
        if callback is not None:
            callback()  # 更新计数
        children = parent_bone.children
        if len(children) == 1:  # 在骨骼只有一个直接子骨骼时创建约束
            child: PoseBone = children[0]
            self._create_phys_damped_track_constraint(target_object, child, callback)

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        """活动物体为骨架并且在姿态模式 & 存在目标模拟网格"""
        return cls.validate_armature_pose(context) and cls.validate(
            context.scene.meldtool_scene_properties.phys.target_object is not None,  # type: ignore
            "未选择目标模拟网格",
        )

    @override
    def execute(self, context: Context) -> set[str]:
        active_armature: Object | None = context.active_object
        target_object: Object | None = (
            context.scene.meldtool_scene_properties.phys.target_object  # type: ignore
        )

        if self.validate_armature_pose(context, active_armature, self) or self.validate(
            target_object is not None, "未选择目标模拟网格", self
        ):
            return {"CANCELLED"}

        selected_bones: list[PoseBone] = get_selected_pbones(active_armature)
        if self.validate(bool(selected_bones), "没有选择任何骨骼"):
            return {"CANCELLED"}

        constraint_count: int = 0

        def _increment_callback() -> None:
            nonlocal constraint_count
            constraint_count += 1

            for start_bone in selected_bones:
                self._create_phys_damped_track_constraint(
                    target_object, start_bone, _increment_callback
                )

        self.report({"INFO"}, f"成功创建: {constraint_count} 个约束")
        return {"FINISHED"}


registry: list = [CopyLocationOperator, DampedTrackOperator]
