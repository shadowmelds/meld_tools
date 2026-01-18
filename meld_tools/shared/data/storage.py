import copy
from typing import Any, Type

_storage_buffer: Any = None


def copy_to_internal_clipboard(data: Any) -> None:
    """复制数据：使用深拷贝确保数据独立"""
    global _storage_buffer
    _storage_buffer = copy.deepcopy(data)


def get_from_internal_clipboard() -> Any | None:
    """返回数据：返回缓冲区数据的副本"""
    if _storage_buffer is None:
        return None
    return copy.deepcopy(_storage_buffer)


def has_clipboard_data(check_type: Type | None = None) -> bool:
    """
    检查是否有可粘贴的数据（用于 UI 面板判断是否灰色显示按钮）
    """
    if _storage_buffer is None:
        return False

    if check_type is not None:
        # 验证数据是否是特定 DataClass 或类型
        return isinstance(_storage_buffer, check_type)

    return True


def clear_internal_clipboard() -> None:
    """清除剪贴板内容，释放内存"""
    global _storage_buffer
    _storage_buffer = None
