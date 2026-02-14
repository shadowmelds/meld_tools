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
            "bone_0180": Human(
                base_name="carpals_point", side="L"
            ),  # 不明腕部定位骨骼.L
            "bone_0181": Human(
                base_name="carpals_point", side="R"
            ),  # 不明腕部定位骨骼.R
            "bone_007D": Human(base_name="head_point", index=1),  # 不明头部定位骨骼1
            "bone_05F0": Human(base_name="head_point", index=2),  # 不明头部定位骨骼2
            "bone_097F": Human(base_name="hips_point", index=2),
            "bone_0984": Human(base_name="hips_point", index=3),
            "bone_0985": Human(base_name="hips_point", index=4),
            "bone_0605": Human(base_name="hips_point", index=5),
            "bone_0606": Human(base_name="hips_point", index=6),
            "bone_002C": Human(
                base_name="palm_point", index=1, side="L"
            ),  # 定位手心1.L
            "bone_002D": Human(
                base_name="palm_point", index=2, side="L"
            ),  # 定位手心2.L
            "bone_002E": Human(
                base_name="palm_point", index=3, side="L"
            ),  # 定位手心3.L
            "bone_004A": Human(
                base_name="palm_point", index=1, side="R"
            ),  # 定位手心1.R
            "bone_004B": Human(
                base_name="palm_point", index=2, side="R"
            ),  # 定位手心2.R
            "bone_002F": Human(
                base_name="palm_point", index=3, side="R"
            ),  # 定位手心3.R
        },
    )


@singleton
def extra_deform_bones() -> CollectionBones:
    return CollectionBones(
        collection=OWBoneCollection.EXTRA_DEFORM,
        prefix="OW-DEF-",
        bones={
            "bone_0AE2": Human(base_name="finger_index_armor", side="L"),
            "bone_0AE5": Human(base_name="finger_middle_armor", side="L"),
            "bone_0AE8": Human(base_name="finger_ring_armor", side="L"),
            "bone_0AEB": Human(base_name="finger_pinky_armor", side="L"),
            "bone_0A96": Human(base_name="finger_index_armor", side="R"),
            "bone_0A97": Human(base_name="finger_middle_armor", side="R"),
            "bone_0A98": Human(base_name="finger_ring_armor", side="R"),
            "bone_0A99": Human(base_name="finger_pinky_armor", side="R"),
            "bone_00DE": Human(base_name="finger_thumb_tweak", side="L"),
            "bone_00DF": Human(base_name="finger_thumb_tweak", side="R"),
            "bone_0506": Human(base_name="shoulder_tweak", side="L"),
            "bone_0507": Human(base_name="shoulder_tweak", side="R"),
            "bone_076D": Human(base_name="earmuff", side="L"),
            "bone_0796": Human(base_name="earmuff", side="R"),
            "bone_07A9": Human(base_name="hair_1_1"),
            "bone_07AE": Human(base_name="hair_1_2"),
            "bone_07B3": Human(base_name="hair_2_1"),
            "bone_07B8": Human(base_name="hair_2_2"),
            "bone_06F5": Human(base_name="knee_tweak", side="L"),
            "bone_06F6": Human(base_name="knee_tweak", side="R"),
            "bone_008E": Human(base_name="shoe_thruster", index=1, side="L"),
            "bone_0090": Human(base_name="shoe_thruster", index=2, side="L"),
            "bone_008F": Human(base_name="shoe_thruster", index=1, side="R"),
            "bone_0091": Human(base_name="shoe_thruster", index=2, side="R"),
            "bone_0094": Human(base_name="carabiner", index=1),
            "bone_0096": Human(base_name="carabiner", index=2),
            "bone_14CF": Human(base_name="skirt_left"),
            "bone_14D0": Human(base_name="skirt_back"),
            "bone_017A": Human(base_name="backpack"),
            "bone_017B": Human(base_name="backpack_side", side="L"),
            "bone_017C": Human(base_name="backpack_side", side="R"),
            "bone_0092": Human(base_name="backpack_carabiner", index=1),
            "bone_0097": Human(base_name="backpack_carabiner", index=2),
            "bone_04C5": Human(base_name="backpack_carabiner", index=3),
            "bone_0093": Human(base_name="backpack_carabiner", index=4),
            "bone_0095": Human(base_name="backpack_carabiner", index=5),
            "bone_008C": Human(base_name="backpack_thruster", side="L"),
            "bone_008D": Human(base_name="backpack_thruster", side="R"),
            "bone_3B6F": Human(base_name="backpack_hoop", side="L"),
            "bone_3B70": Human(base_name="backpack_hoop", side="R"),
        },
    )


@singleton
def extra_bones() -> CollectionBones:
    return CollectionBones(
        collection=OWBoneCollection.EXTRA,
        prefix="OW-",
        bones={
            "bone_07AA": Human(base_name="hair_3"),
            "bone_0083": Human(base_name="hair_4"),
            "bone_07B4": Human(base_name="hair_5"),
            "bone_14D2": Human(base_name="skirt_left", index=1),
            "bone_14D5": Human(base_name="skirt_left", index=2),
            "bone_14D8": Human(base_name="skirt_left", index=3),
            "bone_14D3": Human(base_name="skirt_back", index=1),
            "bone_14D6": Human(base_name="skirt_back", index=2),
            "bone_14D9": Human(base_name="skirt_back", index=3),
            "bone_14E1": Human(base_name="collar_upper", side="L"),
            "bone_14E3": Human(base_name="collar_upper", side="R"),
            "bone_14DE": Human(base_name="collar_lower", side="L"),
            "bone_14E0": Human(base_name="collar_lower", side="R"),
            "bone_2BAE": Human(base_name="excavator"),
            "bone_37DC": Human(base_name="excavator", index=1),
        },
    )


@singleton
def all_bones() -> dict:
    return {}
