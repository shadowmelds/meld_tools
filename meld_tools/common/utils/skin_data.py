from ..data.overwatch_skin import (
    ana_classic,
    genji_classic,
    kiriko_overwatch2,
    mercy_classic,
    ow_shared,
    tracer_overwatch2,
    venture_overwatch2,
)
from ..models.collection_bones import CollectionBones
from ..models.enums_ow_bone_collection import OWBoneCollection
from ..models.enums_ow_skin import OWSkin


def get_skin_bones(skin: OWSkin, shared: bool = True) -> dict:
    """根据皮肤返回相应骨骼字典，没有指定皮肤返回基础骨骼"""
    skin_func_map: dict = {
        OWSkin.ANA_CLASSIC: ana_classic.all_bones,
        OWSkin.MERCY_CLASSIC: mercy_classic.all_bones,
        OWSkin.VENTURE_OVERWATCH2: venture_overwatch2.all_bones,
        OWSkin.KIRIKO_OVERWATCH2: kiriko_overwatch2.all_bones,
        OWSkin.GENJI_CLASSIC: genji_classic.all_bones,
        OWSkin.TRACER_OVERWATCH2: tracer_overwatch2.all_bones,
    }
    base: dict = ow_shared.all_bones()
    specific: dict = skin_func_map.get(skin)
    if specific and shared:
        return specific() | base
    elif specific and not shared:
        return specific()
    return base


def get_skin_vertex_group(skin: OWSkin, shared: bool = True) -> set:
    """根据皮肤返回相应顶点组集合，没有指定皮肤返回基础顶点组"""
    skin_func_map: dict = {
        OWSkin.MERCY_CLASSIC: mercy_classic.vertex_group,
        OWSkin.KIRIKO_OVERWATCH2: kiriko_overwatch2.vertex_group,
        OWSkin.GENJI_CLASSIC: genji_classic.vertex_group,
        OWSkin.TRACER_OVERWATCH2: tracer_overwatch2.vertex_group,
    }

    shared: set = ow_shared.vertex_group()
    specific: set = skin_func_map.get(skin)
    if specific and shared:
        return specific() | shared
    elif specific and not shared:
        return specific()
    return shared


def get_copy_weight_vertex_group(skin: OWSkin, shared: bool = True) -> dict:
    skin_func_map: dict = {
        OWSkin.GENJI_CLASSIC: genji_classic.copy_weight_vertex_group,
        OWSkin.TRACER_OVERWATCH2: tracer_overwatch2.copy_weight_vertex_group,
    }
    shared: dict = ow_shared.copy_weight_vertex_group()
    specific: set = skin_func_map.get(skin)
    if specific and shared:
        return specific() | shared
    elif specific and not shared:
        return specific()
    return shared


def get_skin_constrains_bones(skin: OWSkin, shared: bool = True) -> dict | None:
    skin_fun_map: dict = {
        OWSkin.ANA_CLASSIC: ana_classic.constraint_bones,
        OWSkin.MERCY_CLASSIC: mercy_classic.constraint_bones,
    }

    base: dict = ow_shared.constraint_bones()
    specific: dict = skin_fun_map.get(skin)
    if specific and shared:
        return specific() | base
    elif specific and not shared:
        return specific()
    return base


def get_bones_with_collection(skin: OWSkin) -> list[CollectionBones]:
    collection_bones: list = [
        CollectionBones(
            bones=ow_shared.main_bones(), collection=OWBoneCollection.BASE_MAIN
        ),
        CollectionBones(
            bones=ow_shared.face_bones(), collection=OWBoneCollection.BASE_FACE
        ),
        CollectionBones(
            bones=ow_shared.stretch_bones(), collection=OWBoneCollection.BASE_STRETCH
        ),
    ]

    match skin:
        case OWSkin.SHARED:
            pass
        case OWSkin.ANA_CLASSIC:
            collection_bones.append(
                CollectionBones(
                    bones=ana_classic.point_bones(),
                    collection=OWBoneCollection.POINT,
                )
            )
            collection_bones.append(
                CollectionBones(
                    bones=ana_classic.extra_bones(),
                    collection=OWBoneCollection.EXTRA,
                )
            )
        case OWSkin.MERCY_CLASSIC:
            collection_bones.append(
                CollectionBones(
                    bones=mercy_classic.point_bones(),
                    collection=OWBoneCollection.POINT,
                )
            )
            collection_bones.append(
                CollectionBones(
                    bones=mercy_classic.extra_bones(),
                    collection=OWBoneCollection.EXTRA,
                )
            )
        case OWSkin.VENTURE_OVERWATCH2:
            collection_bones.append(
                CollectionBones(
                    bones=venture_overwatch2.point_bones(),
                    collection=OWBoneCollection.POINT,
                )
            )
            collection_bones.append(
                CollectionBones(
                    bones=venture_overwatch2.extra_bones(),
                    collection=OWBoneCollection.EXTRA,
                )
            )
        case OWSkin.KIRIKO_OVERWATCH2:
            collection_bones.append(
                CollectionBones(
                    bones=kiriko_overwatch2.extra_bones(),
                    collection=OWBoneCollection.EXTRA,
                ),
            )
        case OWSkin.GENJI_CLASSIC:
            collection_bones.append(
                CollectionBones(
                    bones=genji_classic.extra_bones(),
                    collection=OWBoneCollection.EXTRA,
                ),
            )
        case OWSkin.TRACER_OVERWATCH2:
            collection_bones.append(
                CollectionBones(
                    bones=tracer_overwatch2.point_bones(),
                    collection=OWBoneCollection.POINT,
                )
            )
            collection_bones.append(
                CollectionBones(
                    bones=tracer_overwatch2.extra_bones(),
                    collection=OWBoneCollection.EXTRA,
                )
            )
    return collection_bones
