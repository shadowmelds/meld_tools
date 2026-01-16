from typing import Callable

import bpy
from bpy.types import Scene


def test_print_unlock_vg(scene_mesh: Callable[..., Scene | None]) -> None:
    scene_mesh("苏珊娜")
    assert bpy.ops.meldtool.print_unlock_vg() == {"FINISHED"}
