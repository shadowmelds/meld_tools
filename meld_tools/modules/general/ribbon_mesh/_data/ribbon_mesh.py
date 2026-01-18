from bpy.types import BoneCollection, EditBone
from mathutils import Vector

from .....shared.models.bone_desc import BoneDesc


def step2_bone_desc(
    local_collection: BoneCollection,
    golbal_collection: BoneCollection,
    ribbon_collection: BoneCollection,
    base_middle_upp_bone: EditBone,
    base_middle_low_bone: EditBone,
    base_corn_l_bone: EditBone,
    base_corn_r_bone: EditBone,
    use_cloud_rig: bool = False,
) -> list[BoneDesc]:
    return [
        # ===================
        # Top1层
        # ===================
        BoneDesc(
            name="CTL-Lips_upp_main",
            position_bone=base_middle_upp_bone,
            tail_offset=Vector((0.0, 0.0, 0.0004)),
            bbone_x=0.0016,
            bbone_z=0.0016,
            calculate_roll="GLOBAL_POS_Z",
            collections=[golbal_collection, ribbon_collection],
            use_cloud_rig=use_cloud_rig,
        ),
        BoneDesc(
            name="CTL-Lips_low_main",
            position_bone=base_middle_low_bone,
            tail_offset=Vector((0.0, 0.0, 0.002)),
            bbone_x=0.0016,
            bbone_z=0.0016,
            calculate_roll="GLOBAL_POS_Z",
            collections=[golbal_collection, ribbon_collection],
            use_cloud_rig=use_cloud_rig,
        ),
        BoneDesc(
            name="CTL-Lips_corn.L",
            position_bone=base_middle_low_bone,
            tail_offset=Vector((0.0, 0.0, 0.0004)),
            bbone_x=0.0016,
            bbone_z=0.0016,
            calculate_roll="GLOBAL_POS_Z",
            auto_mirror=True,
            collections=[golbal_collection, ribbon_collection],
            use_cloud_rig=use_cloud_rig,
        ),
        # Top2层
        BoneDesc(
            name="CTL-Lips_upp_second",
            position_bone=base_middle_upp_bone,
            tail_offset=Vector((0.0, 0.0, 0.0018)),
            bbone_x=0.0005,
            bbone_z=0.0005,
            calculate_roll="GLOBAL_POS_Z",
            collections=[golbal_collection, ribbon_collection],
            use_cloud_rig=use_cloud_rig,
        ),
    ]
