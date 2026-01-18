from typing import override

from bpy.types import Context, Panel, UILayout

from .props_pose_bone_meld_rig import MeldRigPoseBoneProperties


class MeldRigPoseBonePanel(Panel):
    bl_idname: str = "MELDTOOL_PT_meld_rig_pose_bone"
    bl_label: str = "MeldRig Type"
    bl_space_type: str = "PROPERTIES"
    bl_region_type: str = "WINDOW"
    bl_context: str = "bone"

    @classmethod
    @override
    def poll(cls: type["MeldRigPoseBonePanel"], context: Context) -> bool:
        return (
            context.mode == "POSE"
            and context.object
            and context.object.type == "ARMATURE"
            and context.active_pose_bone is not None
            and context.object.meldtool_object_properties.meld_rig.enabled
        )

    @override
    def draw(self, context: Context) -> None:
        meld_rig: MeldRigPoseBoneProperties = (
            context.active_pose_bone.meldtool_pose_bone_properties.meld_rig
        )
        column: UILayout = self.layout.column()
        column.prop(meld_rig, "bone_type")


registry: list = [MeldRigPoseBonePanel]
