from pathlib import Path, PurePath

import bpy
from bpy.types import Context, UserExtensionRepoCollection


def install_this(context: Context, enable: bool = True):
    repos: UserExtensionRepoCollection = context.preferences.extensions.repos

    # 禁用其他所有扩展库
    for repo in repos:
        repo.enabled = False

    addon_name, repo_dir = get_repo_info()
    repos.new(name=addon_name, module=addon_name, custom_directory=repo_dir)

    if enable:
        assert bpy.ops.preferences.addon_enable(
            module=f"bl_ext.{addon_name}.{addon_name}"
        ) == {"FINISHED"}, f"安装 {addon_name} 失败"

    print(f"{addon_name} 已安装并启用" if enable else f"{addon_name} 已安装")


def disable_this() -> None:
    addon_name, repo_dir = get_repo_info()
    assert bpy.ops.preferences.addon_disable(
        module=f"bl_ext.{addon_name}.{addon_name}"
    ) == {"FINISHED"}, f"注销 {addon_name} 失败"


def enable_this() -> None:
    addon_name, repo_dir = get_repo_info()
    assert bpy.ops.preferences.addon_enable(
        module=f"bl_ext.{addon_name}.{addon_name}"
    ) == {"FINISHED"}, f"注册 {addon_name} 失败"


def get_repo_info() -> tuple[str, str]:
    file_path: Path = Path(__file__)
    dir_path: PurePath = file_path.parent.parent
    module_name: str = dir_path.name
    return module_name, dir_path.as_posix()
