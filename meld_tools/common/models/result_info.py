from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


@dataclass(slots=True)
class ResultInfo(Generic[T]):
    status: bool = True
    success_count: int = 0
    failure_count: int = 0
    data: Optional[T] = None

    def __bool__(self) -> bool:
        return self.status

    @property
    def message(self) -> str:
        return f"成功：{self.success_count}, 失败：{self.failure_count}"
