from ....shared.models.rigging.human import Human
from ....shared.utils.singleton import singleton
from .._models.collection_bones import CollectionBones
from .._models.enums_ow_bone_collection import OWBoneCollection


@singleton
def point_bones() -> CollectionBones:
    return CollectionBones(
        collection=OWBoneCollection.POINT,
        prefix="OW-",
        bones={
            "bone_03BD": Human(
                base_name="upper_arm_point", side="L"
            ),  # 不明上臂定位骨骼.L
            "bone_03BE": Human(
                base_name="upper_arm_point", side="R"
            ),  # 不明上臂定位骨骼.R
            "bone_0180": Human(
                base_name="carpals_point", side="L"
            ),  # 不明腕部定位骨骼.L
            "bone_0181": Human(
                base_name="carpals_point", side="R"
            ),  # 不明腕部定位骨骼.R
            "bone_05F0": Human(base_name="head_point", index=2),  # 不明头部定位骨骼2
            "bone_097F": Human(base_name="hips_point", index=2),
            "bone_0984": Human(base_name="hips_point", index=3),
            "bone_0985": Human(base_name="hips_point", index=4),
            "bone_0095": Human(base_name="hammer_point"),
            "bone_006B": Human(base_name="backpack_point"),
        },
    )


@singleton
def extra_bones() -> CollectionBones:
    return CollectionBones(
        collection=OWBoneCollection.EXTRA,
        prefix="OW-",
        bones={},
    )


@singleton
def extra_deform_bones() -> CollectionBones:
    return CollectionBones(
        collection=OWBoneCollection.EXTRA_DEFORM,
        prefix="OW-DEF-",
        bones={
            "bone_0ADE": Human(base_name="blinkers"),
            "bone_017A": Human(base_name="backpack"),
            "bone_008B": Human(base_name="backpack_lanyard"),
            "bone_0069": Human(base_name="backpack_wheel"),
            "bone_017B": Human(base_name="backpack_chimney", side="L"),
            "bone_017C": Human(base_name="backpack_chimney", side="R"),
            "bone_2E23": Human(base_name="eye_mask"),
            "bone_0427": Human(base_name="mustache", index=1, side="L"),  # 上唇胡
            "bone_2C70": Human(base_name="mustache", index=2, side="L"),  # 上唇胡
            "bone_2C72": Human(base_name="mustache", index=3, side="L"),  # 上唇胡
            "bone_0428": Human(base_name="mustache", index=1, side="R"),  # 上唇胡
            "bone_2C71": Human(base_name="mustache", index=2, side="R"),  # 上唇胡
            "bone_2C73": Human(base_name="mustache", index=3, side="R"),  # 上唇胡
            "bone_0177": Human(base_name="sideburns", side="L"),  # 盘胡子
            "bone_0178": Human(base_name="sideburns", side="R"),  # 盘胡子
            "bone_0171": Human(base_name="beard", index=1, side="L"),  # 辫胡子
            "bone_0173": Human(base_name="beard", index=2, side="L"),  # 辫胡子
            "bone_0175": Human(base_name="beard", index=3, side="L"),  # 辫胡子
            "bone_0172": Human(base_name="beard", index=1, side="R"),  # 辫胡子
            "bone_0174": Human(base_name="beard", index=2, side="R"),  # 辫胡子
            "bone_0176": Human(base_name="beard", index=3, side="R"),  # 辫胡子
            "bone_00C5": Human(base_name="codpiece", index=1),
            "bone_0179": Human(base_name="codpiece", index=2),
            "bone_017D": Human(base_name="clip", index=1),
            "bone_017E": Human(base_name="clip", index=2),
            "bone_017F": Human(base_name="clip", position="inner"),
        },
    )
