from .._models.collection_bones import CollectionBones
from .._models.enums_ow_skin import OWSkin
from . import (
    ana_classic,
    genji_classic,
    kiriko_overwatch2,
    mercy_classic,
    ow_shared,
    ow_shared_old,
    torbjorn_overwatch2,
    tracer_overwatch2,
    venture_overwatch2,
)


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
    base: dict = ow_shared_old.all_bones()
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

    shared: set = ow_shared_old.vertex_group()
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
    shared: dict = ow_shared_old.copy_weight_vertex_group()
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

    base: dict = ow_shared_old.constraint_bones()
    specific: dict = skin_fun_map.get(skin)
    if specific and shared:
        return specific() | base
    elif specific and not shared:
        return specific()
    return base


def get_bones_with_collection(skin: OWSkin) -> list[CollectionBones]:
    collection_bones: list = [
        ow_shared.base_deform(),
        ow_shared.face_deform(),
        ow_shared.other_deform(),
        ow_shared.no_deform(),
    ]

    match skin:
        case OWSkin.SHARED:
            pass
        case OWSkin.ANA_CLASSIC:
            ...
        case OWSkin.MERCY_CLASSIC:
            ...
        case OWSkin.VENTURE_OVERWATCH2:
            collection_bones.append(venture_overwatch2.extra_deform_bones())
            collection_bones.append(venture_overwatch2.point_bones())
            collection_bones.append(venture_overwatch2.extra_bones())
        case OWSkin.KIRIKO_OVERWATCH2:
            ...
        case OWSkin.GENJI_CLASSIC:
            ...
        case OWSkin.TRACER_OVERWATCH2:
            ...
        case OWSkin.TORBJORN_OVERWATCH2:
            collection_bones.append(torbjorn_overwatch2.extra_deform_bones())
            collection_bones.append(torbjorn_overwatch2.point_bones())
            pass
    return collection_bones
