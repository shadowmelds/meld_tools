from bpy.types import ClothModifier, Object


def exists_specific_modifier(
    object: Object, modifier_type: str
) -> ClothModifier | None:
    """检查是否存在特定类型的修改器，如果存在返回这个修改器，仅支持存在单个同一类型修改器"""
    for modifier in object.modifiers:
        if modifier.type == modifier_type:
            return modifier
    return None
