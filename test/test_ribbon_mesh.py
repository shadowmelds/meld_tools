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
