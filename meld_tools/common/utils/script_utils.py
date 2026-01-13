import os

import bpy
from bpy.types import Text


def write_script(
    file_path: str,
    file_name: str,
    datablock: Text = None,
    use_fake_user: bool = True,
    use_module: bool = False,
    execute: bool = False,
) -> Text | None:
    text: Text
    if datablock:
        # 允许写入传入的 Text 数据块
        text: Text = datablock
    else:
        # 检查这个文件名的 Text 数据块是否已经存在
        text: Text = bpy.data.texts.get(file_name)
        # 不存在，创建它
        if not text:
            text = bpy.data.texts.new(name=file_name)
            text.use_fake_user = use_fake_user
    text.clear()
    # 注册（加载时运行）
    text.use_module = use_module

    full_path = os.path.join(file_path, file_name)

    # 读取文件内容写入 Text datablock
    if not os.path.exists(full_path):
        print(f"文件不存在: {full_path}")
        return None
    with open(full_path, "r") as file:
        for line in file:
            text.write(line)

    # 运行 UI 脚本
    if execute:
        exec(text.as_string(), {})
    return text


def run_script(
    file_name: str,
) -> bool:
    datablock: Text = bpy.data.texts.get(file_name)
    if not datablock:
        return False
    else:
        exec(datablock.as_string(), {})
        return True
