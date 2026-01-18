import bpy
from bpy.types import (
    Action,
    ActionChannelbag,
    ActionChannelbagFCurves,
    ActionGroup,
    ActionLayer,
    ActionSlot,
    ActionSlots,
    ActionStrip,
    AnimData,
    FCurve,
    Keyframe,
    Object,
    PoseBone,
)

from ..models.data_path_info import DataPathInfo
from . import action_utils, pbone_constraint_utils


def constraint_rig(
    redirect_armature: Object, rig_armature: Object, constraint_bones: dict[str, str]
) -> None:
    """约束绑定骨骼至原始动画骨骼"""
    # 确保绑定骨架是活动物体
    bpy.context.view_layer.objects.active = rig_armature
    # 确保绑定骨架被选中以切换至姿态模式
    rig_armature.select_set(True)
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode="POSE")

    for key, value in constraint_bones.items():
        pose_bone = rig_armature.pose.bones.get(value)
        if pose_bone:
            pbone_constraint_utils.add_copy_transforms_constraint(
                owner_pose_bone=pose_bone,
                target_armature=redirect_armature,
                target_bone_name=key,
                name="MELD_COPY_TRANSFORMS",
            )
            pbone_constraint_utils.move_top_constraint(
                pose_bone=pose_bone, constraint_name="MELD_COPY_TRANSFORMS"
            )
        else:
            print(f"{value} 不存在")


def unconstraint_rig(rig_armature: Object, constraint_bones: dict[str, str]):
    """清除用于传递动作的复制变换约束"""
    bpy.context.view_layer.objects.active = rig_armature
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode="POSE")
    for key, value in constraint_bones.items():
        pbone_constraint_utils.remove_bone_constraint(
            pose_bone=rig_armature.pose.bones.get(value),
            constraint_name="MELD_COPY_TRANSFORMS",
        )


def bake_action(
    redirect_armature: Object,
    rig_armature: Object,
    constraint_bones: dict[str, str],
    frame_start: int,
    frame_end: int,
    simple: bool = False,
) -> None:
    """烘焙动画至绑定"""
    bpy.context.view_layer.objects.active = rig_armature
    # 切换到姿态模式
    rig_armature.select_set(True)
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode="POSE")

    anim_data: AnimData = rig_armature.animation_data
    if not anim_data:
        anim_data = rig_armature.animation_data_create()
    rig_armature_action: Action = bpy.data.actions.new(
        name=f"{rig_armature.name}_BakeAction"
    )
    rig_armature_action_slot: ActionSlot = rig_armature_action.slots.new(
        id_type="OBJECT", name=rig_armature.name
    )
    rig_armature_action_layer: ActionLayer = rig_armature_action.layers.new("Layer")
    rig_armature_action_strip: ActionStrip = rig_armature_action_layer.strips.new(
        type="KEYFRAME"
    )
    rig_armature_action_channelbag: ActionChannelbag = (
        rig_armature_action_strip.channelbag(rig_armature_action_slot, ensure=True)
    )

    redirect_armature_action: Action = redirect_armature.animation_data.action
    legacy_slot: ActionSlots | None = next(
        (slot for slot in redirect_armature_action.slots), None
    )
    redirect_armature_fcurves: ActionChannelbagFCurves = None
    if legacy_slot is not None:
        strip: ActionStrip = redirect_armature_action.layers[0].strips[0]
        redirect_armature_action_channelbag: ActionChannelbag = strip.channelbag(
            legacy_slot
        )
        redirect_armature_fcurves = redirect_armature_action_channelbag.fcurves
    else:
        redirect_armature_fcurves = redirect_armature_action.fcurves

    # 禁用自动插帧
    bpy.context.scene.tool_settings.use_keyframe_insert_auto = False
    # 将关键帧放在最开始，确保烘焙第一帧永远在起始位置
    bpy.context.scene.frame_set(frame=frame_start)

    for current_frame in range(
        frame_start, frame_end + 1
    ):  # 在当前帧需要烘焙全部关键帧一次
        print(f"Baking: {current_frame}")  # 在控制台显示当前正在烘焙的帧

        constraint_check: bool = False
        # 应用所有的用于传递动作的复制变换约束，获得骨骼实际变换
        for key, value in constraint_bones.items():
            # 检查骨骼是否存在指定约束
            constraint: bool = (
                rig_armature.pose.bones[value].constraints.get("MELD_COPY_TRANSFORMS")
                is not None
            )
            # 如果约束存在，应用它
            if constraint:
                rig_armature.data.bones.active = rig_armature.data.bones[value]
                bpy.ops.constraint.apply(
                    constraint="MELD_COPY_TRANSFORMS", owner="BONE"
                )  # 应用所有用于传递动作的复制变换约束
            else:
                constraint_check = True
                break
        if constraint_check:
            raise RuntimeError(f"约束不正确，检查：（{key}：{value}）")
        # 应用复制变换约束后的数据添加关键帧至 rig_armature_action_slot
        for (
            redirect_fcurve
        ) in redirect_armature_fcurves:  # 在当前 fcurve 烘焙全部关键帧一次
            redirect_data_path_info: DataPathInfo = action_utils.get_bone_path_info(
                redirect_fcurve.data_path
            )  # 获取当前 fcurve 骨骼名和属性名
            if (
                redirect_data_path_info is not None
                and redirect_data_path_info.bone_name in constraint_bones
            ):  # 确保该 fcurve 是需要烘焙的
                rig_bone_name: str = constraint_bones[redirect_data_path_info.bone_name]
                rig_bone: PoseBone = rig_armature.pose.bones[rig_bone_name]

                # array_index 表示轴向的索引的
                rig_keyframe_array_index: int = redirect_fcurve.array_index

                rig_keyframe_data_path: str = (
                    f'pose.bones["{rig_bone_name}"].rotation_euler'
                    if "rotation_quaternion" == redirect_data_path_info.property_name
                    else f'pose.bones["{rig_bone_name}"].{redirect_data_path_info.property_name}'
                )

                # 确保不生成 rotation_quaternion[3] 这条多余 Fcurve
                if (
                    "rotation_quaternion" == redirect_data_path_info.property_name
                    and rig_keyframe_array_index == 3
                ):
                    continue

                group: ActionGroup = None
                # 检查 ActionGroup 是否已存在
                if rig_bone_name not in rig_armature_action_channelbag.groups:
                    group = rig_armature_action_channelbag.groups.new(rig_bone_name)
                else:
                    group = rig_armature_action_channelbag.groups[rig_bone_name]

                # 为 rig_armature_action_slot 创建一个 FCurve 去记录关键帧
                rig_fcurve: FCurve = create_fcurve_if_not_exists(
                    rig_armature_action,
                    group,
                    rig_keyframe_data_path,
                    rig_keyframe_array_index,
                )

                if (
                    "rotation_quaternion" == redirect_data_path_info.property_name
                    and rig_keyframe_array_index != 3
                ):  # 确保记录旋转关键字时不记录到 rotation_quaternion[3]
                    for redirect_keyframe in redirect_fcurve.keyframe_points:
                        if (
                            not simple or current_frame == redirect_keyframe.co[0]
                        ):  # 简化而且没有关键帧不添加，非简化添加，帧值有关键帧才添加 关键帧到 rig_fcurve
                            value: float = action_utils.get_bone_property_by_index(
                                pose_bone=rig_bone,
                                property_name="rotation_euler",
                                index=rig_keyframe_array_index,
                            )
                            # 添加关键帧并记录属性和值
                            keyframe: Keyframe = rig_fcurve.keyframe_points.insert(
                                frame=current_frame, value=value
                            )
                            # 确保是关键帧是线性的
                            keyframe.interpolation = "LINEAR"
                            break  # 关键帧找到后就不必再查找了
                elif (
                    "rotation_quaternion" != redirect_data_path_info.property_name
                ):  # 确保记录非旋转关键字时不记录到 rotation_quaternion[3]
                    for redirect_keyframe in redirect_fcurve.keyframe_points:
                        if (
                            not simple or current_frame == redirect_keyframe.co[0]
                        ):  # 简化而且没有关键帧不添加，非简化添加，帧值有关键帧才添加 关键帧到 rig_fcurve
                            # 获取到实际变换后骨骼的属性值
                            value: float = action_utils.get_bone_property_by_index(
                                pose_bone=rig_bone,
                                property_name=redirect_data_path_info.property_name,
                                index=rig_keyframe_array_index,
                            )
                            # 添加关键帧并记录属性和值
                            keyframe: Keyframe = rig_fcurve.keyframe_points.insert(
                                frame=current_frame, value=value
                            )
                            # 确保是关键帧是线性的
                            keyframe.interpolation = "LINEAR"
                            break  # 关键帧找到后就不必再查找了
                rig_fcurve.update()  # 自动排序关键帧（以确保关键帧顺序正确）

        # 烘焙下一帧需要再次添加所有用于传递动作的复制变换约束
        if current_frame < frame_end:
            bpy.context.scene.frame_set(frame=current_frame + 1)
            for key, value in constraint_bones.items():
                pbone_constraint_utils.add_copy_transforms_constraint(
                    owner_pose_bone=rig_armature.pose.bones.get(value),
                    target_armature=redirect_armature,
                    target_bone_name=key,
                    name="MELD_COPY_TRANSFORMS",
                )
                pbone_constraint_utils.move_top_constraint(
                    pose_bone=rig_armature.pose.bones.get(value),
                    constraint_name="MELD_COPY_TRANSFORMS",
                )

    anim_data.action = rig_armature_action
    anim_data.action_slot = anim_data.action_suitable_slots[0]


# 用于缓存 fcurve 查找的字典
fcurve_cache: dict[tuple, FCurve] = {}


def create_fcurve_if_not_exists(
    rig_armature_action: Action,
    group: ActionGroup | None,
    rig_keyframe_data_path: str,
    rig_keyframe_array_index: int,
):
    """
    如果 FCurve 不存在，则创建 FCurve，并缓存 FCurve 查找结果
    :return 返回 FCurve（如果已存在，则返回现有 FCurve）
    """
    # 构造唯一键：将 data_path 和 index 组合成键
    fcurve_key: tuple = (rig_keyframe_data_path, rig_keyframe_array_index)

    rig_armature_action_slot: ActionSlot = rig_armature_action.slots[0]
    strip: ActionStrip = rig_armature_action.layers[0].strips[0]
    channelbag: ActionChannelbag = strip.channelbag(rig_armature_action_slot)
    # 尝试从缓存中查找 FCurve
    if fcurve_key in fcurve_cache:
        return fcurve_cache[fcurve_key]
    try:
        # 如果不存在，则创建新的 FCurve
        rig_fcurve: FCurve = channelbag.fcurves.new(
            data_path=rig_keyframe_data_path,
            index=rig_keyframe_array_index,  # index 代表轴向
        )

        if group is not None:
            rig_fcurve.group = group
        # 将新创建的 FCurve 存入缓存
        fcurve_cache[fcurve_key] = rig_fcurve
        return rig_fcurve
    except RuntimeError:
        # 如果 FCurve 已经存在（此时抛出异常），则查找并返回现有 FCurve
        for fcurve in channelbag.fcurves:
            if (
                fcurve.data_path == rig_keyframe_data_path
                and fcurve.array_index == rig_keyframe_array_index
            ):
                # 将找到的 FCurve 存入缓存
                fcurve_cache[fcurve_key] = fcurve
                return fcurve
