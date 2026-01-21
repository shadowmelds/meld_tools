from typing import Any


def check_duplicates_in_dict(target_dict: dict[Any, Any]) -> bool:
    """
    检查字典是否存在重复值
    注意：值必须是可哈希的 (Hashable)。
    对于 dataclass，请确保定义了 frozen=True 或实现 __hash__。
    如果包含不可哈希对象（如 list），此函数将抛出 TypeError。
    """

    values: Any = target_dict.values()
    return len(set(values)) < len(values)
