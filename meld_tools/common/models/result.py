from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Iterator, Optional, TypeVar

T = TypeVar("T")


@dataclass
class Result(Generic[T]):
    success: bool = True
    data: Optional[T] = None
    success_count: int = 0
    error_count: int = 0

    @property
    def message(self) -> str:
        return f"成功：{self.success_count}" + (
            f", 失败：{self.error_count}" if self.error_count > 0 else ""
        )

    def __iter__(self) -> Iterator:
        """允许对象被解包: success, data, message = result"""
        yield self.success
        yield self.data
        yield self.message

    def __bool__(self) -> bool:
        return self.success

    @classmethod
    def ok(
        cls,
        data: T = None,
        success_count: int = 1,
        error_count: int = 0,
        message: str = "success",
    ) -> Result[T]:
        return Result(
            success=True,
            data=data,
            success_count=success_count,
            error_count=error_count,
            message=message,
        )

    @classmethod
    def fail(cls, message: str, count: int = 1) -> Result:
        return Result(success=False, message=message, error_count=count)
