import bpy

# 填写顶点组名称
vertext_groups = ["vertext_group1", "vertext_group2"]

for obj in bpy.context.selected_objects:
    if obj.type != "MESH":
        continue

    # 先收集要删的组名，再删
    names = [vg.name for vg in obj.vertex_groups if vg.name in vertext_groups]
    for name in names:
        vg = obj.vertex_groups.get(name)
        if vg:
            obj.vertex_groups.remove(vg)
            print(f"已删除 {obj.name} 的顶点组: {name}")

print("完成。")
