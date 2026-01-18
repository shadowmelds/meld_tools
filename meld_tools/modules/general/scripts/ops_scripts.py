from typing import Literal, override

import bpy
from bpy.props import StringProperty
from bpy.types import Context, Event, Text

from ....shared.base.base_operator import BaseOperator
from ....shared.utils.script_utils import run_script, write_script
from ....paths import SCRIPT_PATH


class WriteScriptOperator(BaseOperator):
    bl_idname: str = "meldtool.write_script"
    bl_label: str = "写入指定脚本"
    bl_description: str = "写入指定脚本"

    script_name: StringProperty(name="脚本名")
    message: StringProperty(default="脚本 f{script_name} 已存在，是否覆盖？")

    @override
    def draw(self, context: Context) -> None:
        layout = self.layout
        layout.label(text=self.message)

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        return True

    @override
    def execute(self, context: Context) -> set[str]:
        if self.validate(bool(self.script_name), "文件名不能为空", self):
            return {"CANCELLED"}
        text: Text | None = write_script(
            file_path=SCRIPT_PATH,
            file_name=self.script_name,
        )
        if self.validate(
            text is not None, f"插件内不存在 {self.script_name} 请检查", self
        ):
            return {"CANCELLED"}
        self.report({"INFO"}, f"已成功写入 {self.script_name}")
        return {"FINISHED"}

    @override
    def invoke(
        self, context: Context, event: Event
    ) -> (
        set[
            Literal[
                "RUNNING_MODAL", "CANCELLED", "FINISHED", "PASS_THROUGH", "INTERFACE"
            ]
        ]
        | set[str]
    ):
        if self.script_name in bpy.data.texts:
            return context.window_manager.invoke_props_dialog(self)
        else:
            return self.execute(context)


class RemoveScriptOperator(BaseOperator):
    bl_idname: str = "meldtool.remove_script"
    bl_label: str = "移除指定脚本"
    bl_options: set = {"REGISTER", "UNDO"}
    bl_description: str = "移除指定脚本"

    script_name: StringProperty(name="脚本名")

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        return True

    @override
    def execute(self, context: Context) -> set[str]:
        if self.validate(bool(self.script_name), "文件名不能为空", self):
            return {"CANCELLED"}
        text: Text | None = bpy.data.texts.get(self.script_name)
        if self.validate_script(self.script_name, text, self):
            return {"CANCELLED"}
        bpy.data.texts.remove(text)
        self.report({"INFO"}, f"已移除 {self.script_name}")
        return {"FINISHED"}

    @override
    def invoke(
        self, context: Context, event: Event
    ) -> set[
        Literal["RUNNING_MODAL", "CANCELLED", "FINISHED", "PASS_THROUGH", "INTERFACE"]
    ]:
        return context.window_manager.invoke_confirm(self, event)


class RunScriptOperator(BaseOperator):
    bl_idname: str = "meldtool.run_script"
    bl_label: str = "运行指定脚本"
    bl_description: str = "运行指定脚本"

    script_name: StringProperty(name="脚本名")

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        return True

    @override
    def execute(self, context: Context) -> set[str]:
        if run_script(file_name=self.script_name):
            self.report({"INFO"}, f"已运行 {self.script_name}")
            return {"FINISHED"}
        else:
            self.report({"ERROR"}, f"{self.script_name} 不存在")
            return {"CANCELLED"}


registry: list = [WriteScriptOperator, RemoveScriptOperator, RunScriptOperator]
