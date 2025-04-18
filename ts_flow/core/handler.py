from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import (
    Any,
    Generic,
    TypeVar,
)

__all__ = ["Handler", "T", "U", "V"]

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")


class Handler(ABC, Generic[T, U]):
    def __init__(self, source: Handler[Any, T] | None = None):
        self._source = source

    @property
    def source(self) -> Handler[Any, T] | None:
        return self._source

    @source.setter
    def source(self, value: Handler[Any, T]) -> None:
        if self._source is not None:
            raise RuntimeError("Cannot change already setted source")
        self._source = value

    @abstractmethod
    def __iter__(self) -> Iterator[U]:
        pass

    def __or__(self, other: Handler[U, V]) -> Pipeline[T, V]:
        return Pipeline(self, other)


class Pipeline(Handler[T, V]):
    def __init__(self, first: Handler[T, U], second: Handler[U, V]):
        super().__init__()
        self.first = first

        if second.source is not None:
            raise ValueError(
                f"Cannot create Pipeline: second handler {type(second).__name__} "
                f"already has a source {type(second.source).__name__}. "
                "Use explicit set_source() or rebuild pipeline chain."
            )

        self.second = second
        self.second.source = self.first

    def __iter__(self) -> Iterator[V]:
        self.second_iterator = iter(self.second)
        return self.second_iterator
