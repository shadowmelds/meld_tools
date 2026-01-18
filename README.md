
### 这是什么

个人 blender 插件，用于学习、实现更方便工作流。

### 安装插件

```
# 克隆仓库（含子模块）
git clone --recurse-submodules https://github.com/shadowmelds/meld_tools.git
```

符号链接工具：[Link Shell Extension](https://schinagl.priv.at/nt/hardlinkshellext/hardlinkshellext.html)

插件符号链接地址：

```
~\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons
```

### 学习资料参考

- [CloudRig](https://projects.blender.org/Mets/CloudRig)
- [blender_studio_utils](https://projects.blender.org/Mets/blender_studio_utils)
- [Creating multifile add-on for Blender](https://b3d.interplanety.org/en/creating-multifile-add-on-for-blender/)
- [插件](https://docs.blender.org/manual/zh-hans/5.0/advanced/extensions/addons.html)
- [如何创建扩展](https://docs.blender.org/manual/zh-hans/5.0/advanced/extensions/getting_started.html)
- [Blender Python API](https://docs.blender.org/api/current/info_quickstart.html)
- [Addon Test](https://codeberg.org/semagnum/addon_testing)

### 测试

1. 安装 Python 3.11（Blender5.0 正在使用的）

https://www.python.org/downloads/release/python-3117/

2. 创建虚拟环境，安装依赖
```powershell
py -3.11 -m venv .venv
```

3. 激活 Python 3.11 虚拟环境

```powershell
.\.venv\Scripts\activate
```

4. 安装依赖

```powershell
pip install -r requirements-dev.txt
```

5. 运行测试

```powershell
pytest -v
```

6. 运行测试并启用覆盖率可视化

```
pip install coverage pytest-cov
pytest -v --durations=0 --cov=./meld_tools --cov-report=html --cov-branch
```
通过`htmlcov/index.html`在网页浏览器中打开文件来查看覆盖率统计信息


### 代办列表

1. 目前所有骨架生成或修改的ops都是直接对目标骨架修改而且出错直接终止，没有撤销的操作；将骨架修改的流程改用临时骨架替换原始骨架的方式而不是直接在原始骨架上修改


```
meld_tools
├─ meld_tools
│  ├─ __init__.py                # 核心引擎：仅负责扫描 modules 文件夹并自动挂载
│  ├─ blender_manifest.toml
│  ├─ core/                      # 【核心层】禁止任何业务关键词（无 ow, 无 rig）
│  │  ├─ base/                   # 抽象基类 (BaseOperator, BasePanel)
│  │  ├─ path.py                 # 动态寻址引擎
│  │  └─ registration.py         # 自动注册工厂 (Auto-Register)
│  ├─ shared/                    # 【共享层】跨模块复用的原子逻辑
│  │  ├─ math/                   # 纯数学计算
│  │  ├─ blender/                # 封装 bpy 的工具类 (mesh, arm, bone)
│  │  └─ models/                 # 通用协议 (Result, BoneInfo)
│  ├─ modules/                   # 【领域层】每个子目录都是一个完整的微型插件
│  │  ├─ ow/                     # Overwatch 领域 (高度内聚自治)
│  │  │  ├─ __init__.py          # 导出入口
│  │  │  ├─ data/                # 资源与静态配置 (Skin scripts, Enums)
│  │  │  ├─ main/                # 核心逻辑
│  │  │  │  ├─ ops.py
│  │  │  │  └─ ui.py
│  │  │  ├─ transform/           # 变换逻辑
│  │  │  │  ├─ ops.py
│  │  │  │  ├─ props.py
│  │  │  │  └─ ui.py
│  │  │  └─ vgroup/              # 顶点组逻辑
│  │  │     ├─ ops.py
│  │  │     └─ ui.py
│  │  ├─ rig/                    # Rigging 领域
│  │  │  ├─ data/                # Rig 预设与配置文件
│  │  │  ├─ core_logic.py        # 核心算法
│  │  │  ├─ ops.py
│  │  │  ├─ props.py
│  │  │  └─ ui.py
│  │  └─ general/                # 通用工具领域
│  │     ├─ phys/                # 物理工具包 (ops, props, ui, data)
│  │     ├─ ribbon/              # 缎带工具包 (ops, props, ui, data)
│  │     └─ toolset/             # 杂项工具包
│  ├─ developer/                 # 开发环境扩展
│  └─ public/                    # 插件级全局状态
└─ ... (外部配置如 clean_cache.ps1, test 等)
```