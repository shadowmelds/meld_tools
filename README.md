
### 这是什么

个人 blender 插件，用于学习、实现更方便工作流。

### 安装插件

符号链接工具：[Link Shell Extension](https://schinagl.priv.at/nt/hardlinkshellext/hardlinkshellext.html)

插件符号链接地址：

```
~\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\addons
```

### 学习资料参考

- [CloudRig](https://projects.blender.org/Mets/CloudRig)
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