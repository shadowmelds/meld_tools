from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, Iterator, Optional, TypeVar

T = TypeVar("T")


@dataclass
class Result(Generic[T]):
    success: bool = True
    data: Optional[T] = None
    success_count: int = 0
    error_count: int = 0
    _message: Optional[str] = field(default="", repr=False)

    @property
    def message(self) -> str:
        return (
            self._message
            + (f"成功：{self.success_count}" if self.success_count > 0 else "")
            + (f", 失败：{self.error_count}" if self.error_count > 0 else "")
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
        success_count: int = 0,
        error_count: int = 0,
        message: str = "success",
    ) -> Result[T]:
        return Result(
            success=True,
            data=data,
            success_count=success_count,
            error_count=error_count,
            _message=message,
        )

    @classmethod
    def fail(cls, message: str, error_count: int = 1) -> Result:
        return Result(success=False, _message=message, error_count=error_count)
