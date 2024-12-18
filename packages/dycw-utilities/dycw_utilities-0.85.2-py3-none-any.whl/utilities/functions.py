from __future__ import annotations

from dataclasses import dataclass
from functools import _lru_cache_wrapper, partial, wraps
from re import findall
from types import (
    BuiltinFunctionType,
    FunctionType,
    MethodDescriptorType,
    MethodType,
    MethodWrapperType,
    WrapperDescriptorType,
)
from typing import TYPE_CHECKING, Any, TypeVar, cast, overload

from typing_extensions import ParamSpec, override

if TYPE_CHECKING:
    from collections.abc import Callable


_P = ParamSpec("_P")
_T = TypeVar("_T")
_U = TypeVar("_U")


def ensure_not_none(obj: _T | None, /, *, desc: str = "Object") -> _T:
    """Ensure an object is not None."""
    if obj is None:
        raise EnsureNotNoneError(desc=desc)
    return obj


@dataclass(kw_only=True, slots=True)
class EnsureNotNoneError(Exception):
    desc: str = "Object"

    @override
    def __str__(self) -> str:
        return f"{self.desc} must not be None"


def first(pair: tuple[_T, Any], /) -> _T:
    """Get the first element in a pair."""
    return pair[0]


@overload
def get_class(obj: type[_T], /) -> type[_T]: ...
@overload
def get_class(obj: _T, /) -> type[_T]: ...
def get_class(obj: _T | type[_T], /) -> type[_T]:
    """Get the class of an object, unless it is already a class."""
    return obj if isinstance(obj, type) else type(obj)


def get_class_name(obj: Any, /) -> str:
    """Get the name of the class of an object, unless it is already a class."""
    return get_class(obj).__name__


def get_func_name(obj: Callable[..., Any], /) -> str:
    """Get the name of a callable."""
    if isinstance(obj, BuiltinFunctionType):
        return obj.__name__
    if isinstance(obj, FunctionType):
        name = obj.__name__
        pattern = r"^.+\.([A-Z]\w+\." + name + ")$"
        try:
            (full_name,) = findall(pattern, obj.__qualname__)
        except ValueError:
            return name
        return full_name
    if isinstance(obj, MethodType):
        return f"{get_class_name(obj.__self__)}.{obj.__name__}"
    if isinstance(
        obj,
        MethodType | MethodDescriptorType | MethodWrapperType | WrapperDescriptorType,
    ):
        return obj.__qualname__
    if isinstance(obj, _lru_cache_wrapper):
        return cast(Any, obj).__name__
    if isinstance(obj, partial):
        return get_func_name(obj.func)
    return get_class_name(obj)


def get_func_qualname(obj: Callable[..., Any], /) -> str:
    """Get the qualified name of a callable."""
    if isinstance(
        obj, BuiltinFunctionType | FunctionType | MethodType | _lru_cache_wrapper
    ):
        return f"{obj.__module__}.{obj.__qualname__}"
    if isinstance(
        obj, MethodDescriptorType | MethodWrapperType | WrapperDescriptorType
    ):
        return f"{obj.__objclass__.__module__}.{obj.__qualname__}"
    if isinstance(obj, partial):
        return get_func_qualname(obj.func)
    return f"{obj.__module__}.{get_class_name(obj)}"


def identity(obj: _T, /) -> _T:
    """Return the object itself."""
    return obj


def is_none(obj: Any, /) -> bool:
    """Check if an object is `None`."""
    return obj is None


def is_not_none(obj: Any, /) -> bool:
    """Check if an object is not `None`."""
    return obj is not None


def not_func(func: Callable[_P, bool], /) -> Callable[_P, bool]:
    """Lift a boolean-valued function to return its conjugation."""

    @wraps(func)
    def wrapped(*args: _P.args, **kwargs: _P.kwargs) -> bool:
        return not func(*args, **kwargs)

    return wrapped


def second(pair: tuple[Any, _U], /) -> _U:
    """Get the second element in a pair."""
    return pair[1]


__all__ = [
    "EnsureNotNoneError",
    "ensure_not_none",
    "first",
    "get_class",
    "get_class_name",
    "get_func_name",
    "get_func_qualname",
    "identity",
    "is_none",
    "is_not_none",
    "not_func",
    "second",
]
