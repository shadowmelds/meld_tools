from typing import Callable

import bpy
from bpy.types import Context, Scene


def test_venture_rename(
    context: Context,
    scene_ow: Callable[..., Scene | None],
) -> None:  # pytest .\test\test_ow.py::test_venture_rename
    """测试重命名探奇骨骼"""
    scene: Scene = scene_ow("000000000109.118_Skeleton")
    bpy.ops.object.mode_set(mode="POSE")
    from bl_ext.meld_tools.meld_tools.modules.ow._models.enums_ow_skin import (
        OWSkin,
    )

    scene.meldtool_scene_properties.ow.current_skin = OWSkin.VENTURE_OVERWATCH2.value
    assert bpy.ops.meldtool.rename_ow_bones() == {"FINISHED"}
    assert bpy.ops.meldtool.print_unnamed_ow_bones() == {"FINISHED"}


def test_torbjorn_rename(
    context: Context,
    scene_ow: Callable[..., Scene | None],
) -> None:  # pytest .\test\test_ow.py::test_torbjorn_rename
    """测试重命名托比昂骨骼"""
    scene: Scene = scene_ow("00000000EBD2_Skeleton")
    bpy.ops.object.mode_set(mode="POSE")
    from bl_ext.meld_tools.meld_tools.modules.ow._models.enums_ow_skin import (
        OWSkin,
    )

    scene.meldtool_scene_properties.ow.current_skin = OWSkin.TORBJORN_OVERWATCH2.value
    assert bpy.ops.meldtool.rename_ow_bones() == {"FINISHED"}
    assert bpy.ops.meldtool.print_unnamed_ow_bones() == {"FINISHED"}
