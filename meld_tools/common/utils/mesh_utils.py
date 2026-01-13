from bpy.types import Object, VertexGroup


def get_vertex_group(
    object: Object, name: str, auto_create: bool = True
) -> VertexGroup:
    """获取目标网格物体顶点组"""
    vertex_group: VertexGroup | None = object.vertex_groups.get(name)
    if auto_create and vertex_group is None:
        vertex_group = object.vertex_groups.new(name=name)
    return vertex_group
