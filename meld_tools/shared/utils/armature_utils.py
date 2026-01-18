from typing import Iterable

import bpy
from bpy.types import (
    Armature,
    ArmatureEditBones,
    Bone,
    BoneCollection,
    Context,
    EditBone,
    Object,
    PoseBone,
)
from mathutils import Vector

from ..models.bone_desc import BoneDesc
from ..models.result import Result
from ..models.simple_bone import SimpleBone


def get_bone_collection(
    armature: Object, name: str, auto_create: bool = True
) -> BoneCollection | None:
    """获取指定名称骨骼集合, 如果不存在则创建骨骼集合并返回"""
    get_collection: BoneCollection = armature.data.collections_all.get(name)
    if get_collection is not None:
        return get_collection
    elif auto_create:
        return armature.data.collections.new(name)
    else:
        return None


def bone_visible_in_object_mode(bone: Bone, armature_data: Armature) -> bool:
    """指定骨骼是否在 Object 模式下是否可见"""
    # 初步判断（仅对骨骼本身被选中并隐藏的方法有效）
    if bone.hide or bone.hide_select:
        return False
    # 如果骨骼本身没有隐藏，而是被骨骼集合隐藏时
    if bone.collections is None or len(bone.collections) <= 0:
        # 没有骨骼集合直接判断可见
        return True
    else:
        # 用于判断指定的全部骨骼集合层级存在被隐藏的集合
        all_collection_not_hide: bool = True
        # 检查指定的全部骨骼集合以及层级->是否都存在隐藏状态的集合
        for target_collection in bone.collections:  # 骨骼被指定的骨骼集合
            for root_collection in armature_data.collections:  # 骨架的所有的根骨骼集合
                path: list[str] = find_target_collection_path(
                    target_collection, root_collection
                )  # 得到被指定骨骼集合的一次层级
                has_hide: bool = (
                    False  # 用于找到有隐藏层级、且指定骨骼层级不止一个时跳出循环
                )
                if path:  # 如果找到了骨骼层级
                    for each_parent_collection in path:
                        if (
                            armature_data.collections_all.get(
                                each_parent_collection
                            ).is_visible
                            == False
                        ):
                            # 骨骼所有父级层级集合有不可见状态，但是还需要检查是否另外指定其他骨骼集合层级
                            has_hide = True
                            all_collection_not_hide = False
                            if (
                                len(bone.collections) == 1
                            ):  # 骨骼只有被指定一个骨骼层级时，遇到有隐藏层级，直接断定这个骨骼不可见
                                return False
                            else:  # 骨骼还被指定了其他骨骼层级，进行下一轮层级检查
                                break
                    if not has_hide:
                        return True  # 骨骼的这一所在集合的所有父级集合都是可见状态 直接得到骨骼是可见的状态
                if has_hide:  # 骨骼的这一所在集合层级有隐藏的集合，直接再去遍历其他的指定集合，直到再次得到所有父级集合都是可见状态，否则判断为隐藏状态
                    break
        return all_collection_not_hide  # 没有骨骼集合也没有隐藏骨骼


def find_bone_collection_paths(bone: Bone, armature_data: Armature) -> list[tuple[str]]:
    """获取目标骨骼所在的所有骨骼层级"""
    paths: list[tuple[str]] = []
    for target_collection in bone.collections:  # 骨骼被指定的骨骼集合
        for root_collection in armature_data.collections:  # 骨架的所有的根骨骼集合
            path: tuple[str] = find_target_collection_path(
                target_collection, root_collection
            )  # 得到被指定骨骼集合的一次层级
            if path:  # 如果找到了骨骼层级
                paths.append(path)
    return paths


def find_target_collection_path(
    target_collection: BoneCollection,
    parent_collection: BoneCollection | None,
    path: tuple = (),
) -> tuple[str]:
    """递归骨骼层级，返回目标骨骼所在的集合的所有层级（含目标集合）"""

    if parent_collection:
        path += (parent_collection.name,)

    if parent_collection.name == target_collection.name:
        return path

    if (
        parent_collection
        and parent_collection.children is not None
        and len(parent_collection.children) > 0
    ):
        for collection in parent_collection.children:
            result: tuple[str] = find_target_collection_path(
                target_collection=target_collection,
                parent_collection=collection,
                path=path,
            )
            if result is not None:  # 如果找到了则会返回整个层级
                return result
    return None


def get_chains_data(
    selected_bones: list[PoseBone | EditBone],
) -> list[list[SimpleBone]]:
    """根据选中骨骼获取整个骨骼链"""
    chains_data: list[list[SimpleBone]] = []
    for bone in selected_bones:
        chain_data: list[SimpleBone] = [
            SimpleBone(name=bone.name, head=bone.head, tail=bone.tail)
        ]
        current: PoseBone | EditBone = bone

        while current.children and len(current.children) == 1:
            current = current.children[0]
            chain_data.append(
                SimpleBone(name=current.name, head=current.head, tail=current.tail)
            )

        if len(chain_data) > 0:
            chains_data.append(chain_data)

    return chains_data


def reorder_collections_by_dict(armature: Object, tree: dict[str, dict | None]):
    """根据现有dict结构，排序骨骼集合"""
    collections_all = armature.data.collections_all

    # 获取真实 parent 下的“直接子集合”
    def _get_children(parent: BoneCollection | None) -> list[BoneCollection]:
        # 注意：如果 parent 是 None ，就是获取到根集合
        return [child for child in collections_all if child.parent == parent]

    # 递归排序某一层级；parent 当前层级的父集合（根层就是 None），subtree 对应这一层的 dict 树结构
    def _reorder_level(
        parent: BoneCollection | None, subtree: dict[str, dict | None] | None
    ):
        if not subtree:
            return

        # 当前层的所有真实子集合（siblings）
        siblings: list[BoneCollection] = _get_children(parent)
        # 构造 "名字 → BoneCollection 对象" 的映射表
        # 后续按照 dict 顺序查找对应的 BoneCollection 要用
        name_and_collection: dict[str:BoneCollection] = {
            collection.name: collection for collection in siblings
        }

        # 从 dict 树（subtree）里获取排序优先级
        ordered: list[BoneCollection] = []
        for name in subtree.keys():  # 遍历你 dict 树的顺序
            collection: BoneCollection = name_and_collection.get(name)
            if collection:
                ordered.append(collection)  # 存在就按顺序加入 ordered

        # 把没出现在 dict 的子集合沉底
        leftovers: list[BoneCollection] = [
            collection for collection in siblings if collection not in ordered
        ]
        # final_order 是目标顺序（尽可能保持 dict 的顺序）
        final_order: list[BoneCollection] = ordered + leftovers

        # 用 collections_all 的“全局 index”排序（CloudRig 同源逻辑）
        # 把 "兄弟层局部顺序" 映射到 "全局 index" 再 move
        # Blender 的 collections.move 只能接受 GLOBAL index
        # siblings 是局部顺序，所以每一步都要重新计算
        for target_sibling_index, collection in enumerate(final_order):
            # 每移动一次 siblings 都会变化，因此实时重新获取
            siblings: list[BoneCollection] = _get_children(parent)
            # collection 在当前 siblings 中的位置（局部 index）
            current_sibling_index: int = siblings.index(collection)

            # 如果已经在正确位置就跳过
            if current_sibling_index != target_sibling_index:
                # 把“兄弟层局部 index”映射成“全局 index”
                from_global: int = collection.index
                # siblings[target_sibling_index] 才是要插入的目标对象
                to_global: int = siblings[target_sibling_index].index
                # move 只能使用 GLOBAL index，且必须用 collections.move
                armature.data.collections.move(from_global, to_global)

        # 递归：对子集合重复排序过程
        for name, child_tree in subtree.items():
            collection: BoneCollection = name_and_collection.get(name)
            # subtree[name] 不是 None 而且是 dict 才有子层级
            if collection and isinstance(child_tree, dict):
                _reorder_level(collection, child_tree)

    _reorder_level(None, tree)


def only_select_bones(
    context: Context, armature: Object, select_bones: list[EditBone | PoseBone]
) -> bool:
    if not armature or armature.type != "ARMATURE":
        return False

    mode = context.mode

    # ---------- Edit Mode ----------
    if mode == "EDIT_ARMATURE":
        # if not hasattr(bone, "select_head"):
        #     return False

        ebones: ArmatureEditBones = armature.data.edit_bones

        # 清空选择
        for b in ebones:
            b.select = b.select_head = b.select_tail = False
        last: EditBone | None = None
        for bone in select_bones:
            # 只选中目标
            bone.select = bone.select_head = bone.select_tail = True
            last = bone

        if last:
            ebones.active = last
            return True
        return False

    # ---------- Pose Mode ----------
    if mode == "POSE":
        pbs: Iterable[PoseBone] = armature.pose.bones

        # 清空选择
        for pb in pbs:
            pb.bone.select = False

        last: PoseBone | None = None
        for bone in select_bones:
            # 映射到 PoseBone
            if bone.__class__.__name__ != "PoseBone":
                bone = pbs.get(bone.name)
                if not bone:
                    continue
            bone.bone.select = True
            last = bone

        if last:
            armature.pose.bones.active = last
            return True

        return False

    # ---------- Object / 其他 ----------
    return False


def only_select_ebones(
    ebones: ArmatureEditBones,
    select_ebone: list[EditBone],
) -> bool:
    if select_ebone and ebones:
        # 清空选择
        for b in ebones:
            b.select = b.select_head = b.select_tail = False

        last: EditBone | None = None
        for bone in select_ebone:
            bone.select = bone.select_head = bone.select_tail = True
            last = bone
        if last:
            ebones.active = last
            return True

    return False


def create_ebone_with_desc(
    active_armature: Object,
    list_bone_desc: list[BoneDesc],
) -> Result:
    ebones: ArmatureEditBones = active_armature.data.edit_bones
    for bone_desc in list_bone_desc:
        head: Vector = None
        tail: Vector = None
        if bone_desc.head is not None:
            head = bone_desc.head
        elif bone_desc.position_bone is not None:
            if bone_desc.position_bone_location == "HEAD":
                head = bone_desc.position_bone.head.copy()
            elif bone_desc.position_bone_location == "TAIL":
                head = bone_desc.position_bone.tail.copy()
        elif bone_desc.position_bone_by_name is not None:
            position_ebone: EditBone | None = ebones.get(
                bone_desc.position_bone_by_name
            )
            if position_ebone:
                if bone_desc.position_bone_location == "HEAD":
                    head = position_ebone.head.copy()
                elif bone_desc.position_bone_location == "TAIL":
                    head = position_ebone.tail.copy()

        if head is None:
            return Result.fail(f"未生成：'{bone_desc.name}' 没有head参考位置")

        if bone_desc.tail is not None:
            tail = bone_desc.tail
        elif bone_desc.tail_offset is not None:
            tail = head.copy() + bone_desc.tail_offset

        if tail is None:
            return Result.fail(f"未生成：'{bone_desc.name}' 没有tail参考位置")

        ebone: EditBone = ebones.new(bone_desc.name)

        ebone.head = head
        ebone.tail = tail
        ebone.bbone_x = bone_desc.bbone_x
        ebone.bbone_z = bone_desc.bbone_z
        ebone.use_connect = bone_desc.use_connect
        if bone_desc.parent:
            parent: EditBone | None = ebones.get(bone_desc.parent)
            if parent:
                ebone.parent = parent
            else:
                return Result.fail(f"未找到父级 {bone_desc.parent}")

        if bone_desc.collections:
            for collection in bone_desc.collections:
                collection.assign(ebone)

        if bone_desc.calculate_roll and only_select_ebones(
            ebones=ebones, select_ebone=[ebone]
        ):
            if bone_desc.calculate_roll:
                bpy.ops.armature.calculate_roll(type=bone_desc.calculate_roll)

    return Result.ok()


def setup_pbone_with_desc(
    active_armature: Object,
    list_bone_desc: list[BoneDesc],
) -> Result:
    for bone_desc in list_bone_desc:
        bone: Bone = active_armature.data.bones.get(bone_desc.name)
        pbone: PoseBone = active_armature.pose.bones.get(bone_desc.name)
        if bone and pbone:
            bone.display_type = bone_desc.display_type
            bone.color.palette = bone_desc.palette
            if bone_desc.custom_shape:
                pbone.custom_shape = bone_desc.custom_shape
                pbone.custom_shape_scale_xyz = bone_desc.custom_shape_scale_xyz
                pbone.custom_shape_translation = bone_desc.custom_shape_translation
                pbone.custom_shape_rotation_euler = (
                    bone_desc.custom_shape_rotation_euler
                )
                pbone.custom_shape_wire_width = bone_desc.custom_shape_wire_width
            pbone.rotation_mode = bone_desc.rotation_mode
            pbone.lock_location = bone_desc.lock_location
            pbone.lock_rotation = bone_desc.lock_rotation
            pbone.lock_rotation_w = bone_desc.lock_rotation_w
            pbone.lock_scale = bone_desc.lock_scale
            if bone_desc.use_cloud_rig:
                if hasattr(pbone, "cloudrig_component"):
                    pbone.cloudrig_component.component_type = "Bone Copy"
        else:
            return Result.fail(
                message=f"'{bone_desc.name}'不存在，未能成功设置 PoseBone 属性",
            )
    return Result.ok(success_count=len(list_bone_desc))


def mirror_ebone_with_desc(
    active_armature: Object,
    list_bone_desc: list[BoneDesc],
) -> Result:
    """镜像传入的 BoneDesc"""
    ebones: ArmatureEditBones = active_armature.data.edit_bones
    # 清空选择
    for b in ebones:
        b.select = b.select_head = b.select_tail = False

    select_ebones: list[EditBone] = []
    for bone_desc in list_bone_desc:
        if bone_desc.auto_mirror:
            if ebone := ebones.get(bone_desc.name):
                select_ebones.append(ebone)
            else:
                return Result.fail(message=f"'{bone_desc.name}'不存在，未能镜像")
    if only_select_ebones(ebones=ebones, select_ebone=select_ebones):
        bpy.ops.armature.symmetrize()
    return Result.ok(success_count=len(select_ebones))


def get_selected_pbones(active_armature: Object) -> list[PoseBone]:
    return [
        pbone
        for pbone in active_armature.pose.bones
        if pbone.select  # type: ignore
    ]


def get_selected_ebones(active_armature: Object) -> list[EditBone]:
    return [
        ebone
        for ebone in active_armature.data.edit_bones  # type: ignore
        if ebone.select
    ]


def get_selected_epbones(active_armature: Object) -> list[EditBone | PoseBone]:
    selected_bones: list[EditBone | PoseBone] = []
    if active_armature.mode == "POSE":
        selected_bones = [pbone for pbone in active_armature.pose.bones if pbone.select]  # type: ignore
    elif active_armature.mode == "EDIT":
        selected_bones = [
            ebone
            for ebone in active_armature.data.edit_bones  # type: ignore
            if ebone.select
        ]
    return selected_bones
