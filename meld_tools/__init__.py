import importlib
import os
import sys
import typing
from typing import Any, Callable

# 1. 检查当前环境是否缺少 override
if not hasattr(typing, "override"):
    # 2. 定位插件自带的 typing_extensions.py
    current_dir = os.path.dirname(__file__)
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)  # 插入到最前面确保优先加载

    try:
        from .typing_extensions import override

        # 3. 动态注入到全局 typing 模块中
        typing.override = override
    except ImportError:
        # 4. 万一没找到文件，定义一个不起作用的装饰器作为保底
        def override(func: Callable) -> Callable[..., Any]:
            return func

        typing.override = override

from bpy.utils import register_class, unregister_class

from . import properties
from .modules.developer import (
    ops_reload,
    ui_developer,
)
from .modules.general import ui_general_main
from .modules.general.drivers import (
    ops_drivers,
    props_scene_drivers,
    ui_drivers,
)
from .modules.general.phys import (
    menu_cloth_preset,
    ops_generate_vg,
    ops_phys_constraints,
    ops_phys_objects,
    ops_rename_bones,
    props_scene_phys,
    ui_phys,
)
from .modules.general.prints import (
    ops_print_selected_bones,
    ops_print_shape_keys,
    ops_print_unlock_vg,
    ops_print_visible_bones,
    ui_prints,
)
from .modules.general.ribbon_mesh import (
    ops_generate_empty_objects,
    ops_generate_inherent_bones,
    props_scene_ribbon_mesh,
    ui_ribbon_mesh,
)
from .modules.general.scripts import (
    ops_scripts,
    ui_scripts,
)
from .modules.general.toolset import (
    ops_align_bones,
    ops_expression_generator,
    ops_load_bone_collections,
    ops_remove_empty_vg,
    ops_select_filter_vg,
    props_scene_toolset,
)
from .modules.ow import (
    ops_action_match_ow,
    ops_print_unnamed_ow_bone,
    ops_rename_ow_bone,
    props_scene_ow,
    ui_ow_main,
)
from .modules.ow.transform_action import (
    ops_bake_action,
    ops_constraint_ow2rig,
    ops_unconstraint_ow2rig,
    props_scene_ow_transform_action,
    ui_ow_transform_action,
)
from .modules.ow.vertex_group import (
    ops_copy_ow2rig_vg,
    ops_lock_ow2rig_vg,
    ops_remove_ow2rig_vg,
    ops_rename_ow_vg,
    ui_ow_vertex_group,
)
from .modules.rig import (
    ops_generate,
    props_object_meld_rig,
    props_pose_bone_meld_rig,
    ui_meld_rig,
    ui_meld_rig_pose_bone,
)
from .public import ops_refresh_frame, props_scene_public

ADDON_ROOT = os.path.dirname(os.path.realpath(__file__))

# 所有必须导入的模块
modules: list = [
    # prop
    props_scene_public,
    props_scene_toolset,
    props_scene_phys,
    props_scene_ribbon_mesh,
    props_scene_drivers,
    props_object_meld_rig,
    props_pose_bone_meld_rig,
    props_scene_ow,
    props_scene_ow_transform_action,
    properties,
    # general.public
    ops_refresh_frame,
    # general.script
    ops_scripts,
    # general.toolset
    ops_expression_generator,
    ops_remove_empty_vg,
    ops_select_filter_vg,
    ops_align_bones,
    ops_load_bone_collections,
    # general.prints
    ops_print_unlock_vg,
    ops_print_visible_bones,
    ops_print_selected_bones,
    ops_print_shape_keys,
    # general.phys
    menu_cloth_preset,
    ops_phys_constraints,
    ops_phys_objects,
    ops_generate_vg,
    ops_rename_bones,
    # general.drivers
    ops_drivers,
    # general.ribbon
    ops_generate_empty_objects,
    ops_generate_inherent_bones,
    # ow.main
    ops_action_match_ow,
    ops_print_unnamed_ow_bone,
    ops_rename_ow_bone,
    # ow.vertex_group
    ops_copy_ow2rig_vg,
    ops_lock_ow2rig_vg,
    ops_remove_ow2rig_vg,
    ops_rename_ow_vg,
    # ow.transform_action
    ops_bake_action,
    ops_constraint_ow2rig,
    ops_unconstraint_ow2rig,
    # developer.main
    ops_reload,
    # rig
    ops_generate,
    # panels
    ui_general_main,
    ui_prints,
    ui_phys,
    ui_ribbon_mesh,
    ui_scripts,
    ui_drivers,
    ui_meld_rig,
    ui_meld_rig_pose_bone,
    ui_ow_main,
    ui_ow_vertex_group,
    ui_ow_transform_action,
    ui_developer,
]


def register_unregister_modules(modules: list, register: bool) -> None:
    register_func = register_class if register else unregister_class
    for m in modules:
        if register:
            importlib.reload(m)
        if hasattr(m, "registry"):
            for c in m.registry:
                try:
                    register_func(c)
                except Exception as e:
                    un = "un" if not register else ""
                    print(
                        f"Warning: MeldTool failed to {un}register class: {c.__name__}"
                    )
                    print(f"meldtool {e}")
        if hasattr(m, "modules"):
            register_unregister_modules(m.modules, register)

        if register and hasattr(m, "register"):
            m.register()
        elif hasattr(m, "unregister"):
            m.unregister()


def register() -> None:
    register_unregister_modules(modules, True)


def unregister() -> None:
    register_unregister_modules(modules, False)
