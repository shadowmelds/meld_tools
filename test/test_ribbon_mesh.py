from typing import Callable

import bpy
from bpy.types import Collection, Context, Scene


def test_generate_empty_objects(
    context: Context, scene_ribbon_mesh: Callable[..., Scene | None]
) -> None:
    scene: Scene = scene_ribbon_mesh("mouth_mesh")
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    collection: Collection | None = bpy.data.collections.get("emptys")
    assert collection is not None
    scene.meldtool_scene_properties.ribbon_mesh.empty_object_collection = collection
    assert bpy.ops.meldtool.generate_empty_objects() == {"FINISHED"}


def test_generate_inherent_bones(
    context: Context, scene_ribbon_mesh: Callable[..., Scene | None]
) -> None:
    scene: Scene = scene_ribbon_mesh("META-RIG")
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.armature.select_all(action="DESELECT")

    scene.meldtool_scene_properties.ribbon_mesh.target_armature = context.active_object
    scene.meldtool_scene_properties.ribbon_mesh.target_parent_bone = "mouth_parent"

    from bl_ext.meld_tools.meld_tools.modules.general.ribbon_mesh.ops_generate_inherent_bones import (
        GenerateInherentBonesSteps,
    )

    assert bpy.ops.meldtool.generate_inherent_bones(
        action=GenerateInherentBonesSteps.STEP_1
    ) == {"FINISHED"}
