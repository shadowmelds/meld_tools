from typing import Callable

import bpy
from bpy.types import Context, Scene


def test_revise_workflow(
    context: Context,
    scene_revise_workflow: Callable[..., Scene | None],
) -> None:  # pytest .\test\test_revise_workflow.py::test_revise_workflow
    scene: Scene = scene_revise_workflow(None)
    assert bpy.ops.meldtool.create_target_rig() == {"FINISHED"}
    assert bpy.ops.meldtool.revise_target_rig() == {"FINISHED"}
    assert bpy.ops.meldtool.replace_old_rig() == {"FINISHED"}
