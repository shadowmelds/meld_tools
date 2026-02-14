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

```python
# cloud_generator.py

class CloudRig_Generator():
    def generate(self, context):
        # 第一步处理 metarig
        metarig.data.pose_position = "REST"  # 让 metarig 处于静止姿态
        metarig.matrix_world = Matrix.Identity(4)  # 归零世界坐标上的变换
        context.view_layer.update()  # 刷新视图 （可能不需要了）

        # 检查 metarig 的版本是否是比目前插件更新版本的 CloudRig 生成的，如果是则需要先更新插件
        if self.params.metarig_version > current_metarig_version:
            ...
        # 临时存储驱动器 ？？？
        self.driver_map = map_pbones_to_drivers(self.metarig)
        # 创建目标骨架
        self.target_rig = create_target_rig_obj(context, metarig)
        # root 意外情况的处理
        if self.params.ensure_root:
            # 如果没有 root 骨骼会自动为 metarig 生成 root 骨骼
            self.ensure_root_bone_component(context, self.metarig, self.params.ensure_root)
            # 这里应该是直接修改了 metarig 给 “孤儿骨骼” 的父级自动设置为 root 骨骼？
            parent_orphans(metarig, self.params.ensure_root)

        # 通过实例化传入的姿势骨骼的绑定组件来生成虚拟骨骼，
        # 并调用它们的 create_bone_infos() 函数。
        # 注意：几乎可以在任何上下文中调用此函数！
        # 这是有意为之，因为叠加绘制代码会用到它！ 叠加绘制代码是 ？？？
        self.generate_abstraction_layer(context)
        # 将新骨架设置为活动物体
        focus_select_obj(context, self.target_rig)
        # 开始修改骨架
        bpy.ops.object.mode_set(mode='EDIT')

        # 一旦所有骨骼组件都创建了它们的骨骼信息（BoneInfos），我们就可以安全地
        # 创建组件之间的关系，因为所有骨骼都已存在。
        # 将此步骤单独设置非常重要，因为它可以实现宽松灵活的
        # 父级切换系统，允许用户选择任何骨骼作为父级。
        self.components_create_interactions(context)

        # 如果一个骨骼没有任何父级信息（孤儿）那么父级会被自动设置为 root
        if self.root_bone_info:
            self.parent_orphan_bone_infos_to_root()

        # 从所有 BoneInfo 中创建实际骨骼。
        # 除了名称之外，尚未写入任何骨骼数据。
        # 此函数应在 components_write_ebone_data() 之前调用，
        # 这样就可以在设置父级时无需担心创建顺序。
        self.components_create_real_bones()

        # 为 BoneInfos 写入 EditBone 数据，此函数不会创建 EditBone
        # 创建 EditBone 由 components_create_real_bones() 完成
        # 这样就可以在进行父子关系设置时无需担心顺序问题
        self.components_write_ebone_data()

        # 设置物体模式下的操作
        bpy.ops.object.mode_set(mode='OBJECT')

        # 创建组建的辅助物体（网格、曲线、晶格）
        self.components_create_helper_objs(context)
        # 应该是写入 PoseBone 的数据，但没看懂写入了什么
        self.components_write_pbone_data(context, self.target_rig)
        
        # 生成测试动作（如果需要）
        if self.params.generate_test_action:
            self.components_create_test_animation()

        # 这个应该是 action 约束相关的 ？？？
        if self.params.action_setups:
            ...
        # 加载并执行 cloudrig.py UI 脚本
        ensure_cloudrig_ui(self.target_rig)

        # 骨骼控件集合重新加载 ？？？ 应该是创建自定义的形状会收纳进专门的集合等操作
        if self.params.reload_widgets and self.params.widget_collection:
            for obj in self.params.widget_collection.objects:
                if not obj.name.startswith("WGT-"):
                    # This is a custom widget and it's not even following naming convention, so we're
                    # not gonna be able to reload it anyways.
                    continue
                self.ensure_widget(
                    context, obj.name.replace("WGT-", ""), overwrite=True
                )

        # 不理解它的作用（实验性功能）
        if self.params.auto_setup_gizmos and self.use_gizmos:
            ...

        # 已经存在的旧的目标骨架
        old_rig = self.params.target_rig
        # 执行用户自定义脚本
        self.execute_custom_script(context, old_rig, self.target_rig)

        if old_rig:
            # 如果旧的目标骨架存在则替换为新骨架
            self.replace_old_with_new_rig(
                context,
                old_rig=old_rig,
                new_rig=self.target_rig,
            )
        else:
            # 如果没有旧的目标骨架，则新骨架去掉标识前缀直接成为新骨架
            self.target_rig.name = self.target_rig.name.replace("NEW-", "")

        # 记录警告级别的问题
        self.log_minor_issues()

        # 旧的目标骨架被设置为新生成的骨架，以便下次重新生成
        self.params.target_rig = self.target_rig
        self.target_rig.data.name = self.target_rig.name

        # 在生成成功或失败后恢复变换
        self.restore_rig_states(context)

    def create_target_rig_obj(context, metarig) -> Object:
        ...

```

- `cloud_generator.py/replace_old_with_new_rig()` 预先保存旧 rig 中的信息 然后删除它 并重映射到新 rig


