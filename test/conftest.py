from pathlib import Path
from typing import Any, Callable, Generator

import bpy
import pytest
from bpy.types import Context, Scene

from .install import disable_this, install_this


@pytest.fixture(scope="session")
def install_addon() -> Generator[None, Any, None]:
    install_this(bpy.context)
    yield
    disable_this()


@pytest.fixture
def context(install_addon: Generator) -> Context:
    return bpy.context


@pytest.fixture
def context_blend(context: Context) -> Context:
    blend_path = Path(__file__).parent / Path("test.blend")
    bpy.ops.wm.open_mainfile(filepath=blend_path.as_posix())
    return context


@pytest.fixture
def scene_mesh(context_blend: Context) -> Callable[..., Scene | None]:
    return lambda obj_name: select_scene_and_object(context_blend, "MESH", obj_name)


@pytest.fixture
def scene_ribbon_mesh(context_blend: Context) -> Callable[..., Scene | None]:
    return lambda obj_name: select_scene_and_object(
        context_blend, "ribbon_mesh", obj_name
    )


def select_scene_and_object(
    context: Context, scene_name: str, obj_name: str = None
) -> Scene | None:
    context.window_manager.windows[0].scene = bpy.data.scenes[scene_name]
    if context.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")
    if obj_name:
        obj = bpy.data.objects[obj_name]
        context.view_layer.objects.active = obj
        obj.hide_set(False)
        obj.select_set(True)
    return context.scene
