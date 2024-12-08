"""Wrap the generator to allow pattern matching.

Consider an iterator (generator with no return value).
>>> generator = iter((1, 2))

>>> match matcher(generator):
...     case Node(0, Node(1, Empty())):
...         print("Try to match the whole sequence")
...     case Node(1, rest):
...         print("Starts with 1 then", list(rest))
Starts with 1 then [2]

A more advanced use case is for `contextmanager`-like generators, 
where the number of yields is known ahead of time.

The following example a generator with 2 yields and a return statement:

>>> def wrapper():
...     yield "object_1"
...     yield "object_2"
...     return "result"

>>> match matcher(wrapper()):
...     case Node(obj1, Node(obj2, Empty(result))):
...         print(obj1, obj2, result)
object_1 object_2 result
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generator, Generic, Iterator, TypeVar

T = TypeVar("T")
R = TypeVar("R")


def matcher(gen: Generator[T, None, R]) -> Node[T, R] | Empty[T, R]:
    """Wrap the generator to inspect the head elements.

    Whilst the original generator will be partially consumed
    the wrapped generator will preserve the inspected elements.

    >>> from itertools import count
    >>> match matcher(count()):
    ...     case Node(1, Node(1, _)):
    ...         print("Starts with two 1s")
    ...     case Node(0, Node(1, _)):
    ...         print("Starts with a 0 and a 1")
    Starts with a 0 and a 1
    """
    gen = iter(gen)
    try:
        return Node(next(gen), gen)
    except StopIteration as e:
        return Empty(e.value)


@dataclass
class Node(Generic[T, R]):
    """An element at the front of the generator."""

    value: T
    gen: Generator[T, None, R]
    _cached: Node[T, R] | Empty[T, R] | None = field(init=False, default=None)

    __match_args__ = ("value", "next")

    def __iter__(self) -> Generator[T, None, R]:
        """Generate the same contents as the original generator.

        This is a destructive iteration, meaning you cannot iterate again.
        """
        yield self.value
        if self._cached:
            yield from self._cached
        else:
            yield from self.gen

    @property
    def next(self) -> Node[T, R] | Empty[T, R]:
        """Get the next node in the generator."""
        if not self._cached:
            self._cached = matcher(self.gen)
        return self._cached


@dataclass(frozen=True)
class Empty(Generic[T, R]):
    """The end of the generator.

    `value` stores the return value of the generator.
    """

    value: R

    def __iter__(self) -> Iterator[T]:
        """Generate the same contents as the original generator.

        in this cases the generator ends with original return value.
        """
        yield from ()
        return self.value
