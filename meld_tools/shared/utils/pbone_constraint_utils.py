from typing import Literal

from bpy.types import CopyTransformsConstraint, Object, PoseBone, PoseBoneConstraints


def remove_bone_constraint(pose_bone: PoseBone, constraint_name: str):
    """通过约束名删除指定骨骼的约束"""
    if pose_bone.constraints.get(constraint_name) is not None:
        pose_bone.constraints.remove(pose_bone.constraints.get(constraint_name))


def add_copy_transforms_constraint(
    owner_pose_bone: PoseBone,
    target_armature: Object,
    target_bone_name: str,
    name: str = "COPY_TRANSFORMS",
    target_space: Literal[
        "WORLD", "CUSTOM", "POSE", "LOCAL_WITH_PARENT", "LOCAL"
    ] = "LOCAL_OWNER_ORIENT",
    owner_space: Literal[
        "WORLD", "CUSTOM", "POSE", "LOCAL_WITH_PARENT", "LOCAL"
    ] = "LOCAL",
):
    """给指定绑定骨骼添加复制变换约束，如果复制变换约束已存在则不会添加"""
    target_constraint_bone: PoseBone = target_armature.pose.bones.get(target_bone_name)
    print(f"add_copy_transforms_constraint: {target_bone_name} 不存在")
    if (
        target_constraint_bone is not None
        and owner_pose_bone.constraints.get(name) is None
    ):
        constraint: CopyTransformsConstraint = owner_pose_bone.constraints.new(
            "COPY_TRANSFORMS"
        )
        constraint.name = name
        constraint.target = target_armature
        constraint.subtarget = target_bone_name
        constraint.target_space = target_space
        constraint.owner_space = owner_space
        constraint.enabled = True


def move_top_constraint(pose_bone: PoseBone, constraint_name: str):
    """将约束移动到约束列表最前面"""
    # 获取骨骼的约束列表
    constraints: PoseBoneConstraints = pose_bone.constraints
    index = constraints.find(constraint_name)
    if index > 1 and len(constraints) > 1:
        constraints.move(index, 0)
