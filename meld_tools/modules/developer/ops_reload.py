from typing import override

import bpy
from bpy.types import Context

from ...shared.base.base_operator import BaseOperator


class RefreshLocalOperator(BaseOperator):
    bl_idname: str = "meldtool.refresh_local"
    bl_label: str = "刷新本地"
    bl_description: str = "似乎没有什么作用，但有时候插件有问题可以点一下"

    @override
    def execute(self, context: Context) -> set[str]:
        bpy.ops.extensions.repo_refresh_all()
        return {"FINISHED"}


class ReloadScriptOperator(BaseOperator):
    bl_idname: str = "meldtool.reload_scirpt"
    bl_label: str = "重载脚本"
    bl_description: str = "修改 MeldTool 源码后能直接重载插件，但如果修改了文件位置或者添加了文件可能不会被识别到"

    @override
    def execute(self, context: Context) -> set[str]:
        bpy.ops.script.reload()
        return {"FINISHED"}


registry: list = [
    RefreshLocalOperator,
    ReloadScriptOperator,
]
