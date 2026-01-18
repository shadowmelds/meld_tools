## 1. 开始

克隆安装项目 https://projects.blender.org/Mets/CloudRig

Git 克隆，要克隆仓库，必须传递 --recurse-submodules 参数：

```powershell
git clone --recurse-submodules https://projects.blender.org/Mets/CloudRig.git
```

子模块

```
cd .\CloudRig\
git config --global url."https://projects.blender.org/".insteadOf git@git.blender.org:
git submodule sync --recursive
git submodule update --init --recursive
```

安装：将项目同名子目录软链接到

```
~\AppData\Roaming\Blender Foundation\Blender\5.0\extensions\user_default
```


## 2. 运行测试

按照 CloudRig/test/ReadMe.md 安装 Python 3.11（Blender 5.0 最新正在使用的 Python 版本）、创建 Python 虚拟环境，在虚拟环境内安装依赖项，运行测试。可选启用覆盖率可视化。

依赖项：
- [ bpy](https://download.blender.org/pypi/)  bpy 的 Python 模块，用于运行测试（无 UI）
- pytest  适用于 Python 3.11 的版本
- fake-bpy-module

```powershell
# 进入项目根目录
cd CloudRig
# 创建虚拟环境
py -3.11 -m venv .venv
# 激活虚拟环境
.\venv\Scripts\activate
# 安装所有依赖
pip install -r requirements-dev.txt
# 运行测试（详细模式）
pytest -v
# 运行测试并显示覆盖率
pip install coverage pytest-cov
pytest -v --durations=0 --cov=./CloudRig --cov-report=html --cov-branch
# 打开 htmlcov/index.html 查看覆盖率
```

## 测试分析

### 结构

- `tests.blend` 为测试用例提供测试样本，此文件会被多次加载，因此尽量保持文件轻量。
    - `Workflow Ops 场景` 主要用于测试 CloudRig 的 QoL 功能
    - `Simple 场景` 多组示例骨架，提供给各种简单测试用例
    - `Poses 场景` 主要用于测试极端姿态下重新生成校验
- `conftest.py` 为 pytest 的测试函数集。
    - `install_addon()`
        1. 整个测试开始前禁用 bpy 其他扩展库，添加仓库根目录作为扩展库，默认启用插件。
        2. 整个测试结束后禁用插件
    - `context()` 提供 bpy.context
    - `context_blend()` 提供 bpy.context，并打开 `tests.blend` 文件
    - `scene_workflow()` 提供 scene，设置场景：*Workflow Ops* 活动对象：*META-Sintel*
    - `scene_simple()` 提供 scene，设置场景：*Simple* 活动对象：*META-Simple*
    - `scene_poses()` 提供 scene，设置场景：*Poses*
    - `select_scene_and_object()` 设置场景和活动对象的具体实现
- `install.py` 为 bpy 设置插件扩展库、启用/禁用插件
- `post_gen.py` post_gen 工具的测试文本内容，它必需要写入到 `test.blend` 文本数据块中运行
- `run_in_blender.py` 插件内几个函数测试文本内容，它必需要写入到 `test.blend` 文本数据块中运行
- `test_misc.py` 未整理分类的测试，包括将需要写入 `test.blend` 的测试进行写入并执行
- `test_generate_metarigs.py` 测试添加所有示例 metarig 并生成最终骨架
- `test_pose_consistency.py` 对 `tests.blend` *Poses 场景* 中极端姿势的最终骨架重新生成检查姿态的变换是否和之前保持一致
- `test_rig_ui.py` 测试 CloudRig 面板上提供的功能
- `test_workflow_ops.py` 测试 CloudRig 提供的 QoL 功能（镜像、挤出、父子级操作）

## 机制探索

### 重新生成如何保证非破坏性

我很好奇 CloudRig 如果重新生成失败时骨架是如何保证不会破坏现有骨架，而生成成功如何保持骨架所有约束、驱动器、之类的不被破坏的？

- `cloud_generator.py/replace_old_with_new_rig()` 预先保存旧 rig 中的信息 然后删除它 并重映射到新 rig


