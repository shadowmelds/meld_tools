from typing import Any, Callable


def singleton(func: Callable) -> Callable[[], Any]:
    """单例注解，使用方法：
    @singleton
    def func():
    """
    instances: dict = {}  # 用于存储实例的字典

    def wrapper() -> Any:
        if func not in instances:
            instances[func] = func()  # 只在第一次调用时创建实例
        return instances[func]

    return wrapper
