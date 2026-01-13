import bpy

obj = bpy.context.object

origin_vg_names = [
    "DEF-Spine0",
    "DEF-Spine1",
]

target_vg_name = "DEF-Spine0"


# 获取源顶点组
origin_vgs = []
for name in origin_vg_names:
    vg = obj.vertex_groups.get(name)
    if vg is None:
        raise ValueError(f"找不到源顶点组: {name}")
    origin_vgs.append(vg)

# 获取或创建目标顶点组
target_vg = obj.vertex_groups.get(target_vg_name)
if not target_vg:
    target_vg = obj.vertex_groups.new(name=target_vg_name)

for v in obj.data.vertices:
    new_weight = 0.0
    for vg in origin_vgs:
        try:
            new_weight += vg.weight(v.index)
        except RuntimeError:
            pass
    # 限制最终权重只能在 [0, 1] 之间
    new_weight = max(0.0, min(1.0, new_weight))
    target_vg.add([v.index], new_weight, "REPLACE")
print("完成：权重已合并并限制在 0~1 范围内。")
