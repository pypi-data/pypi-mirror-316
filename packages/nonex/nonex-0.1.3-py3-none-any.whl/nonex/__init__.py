from typing import Callable, Iterable, TypeVar

T = TypeVar("T")


def nonethrows(value: T | None, msg: str | None = None) -> T:
    """Coerce a value to non-optional. Raise TypeError if the value is None"""
    if value is None:
        raise TypeError(msg or "Unexpected None")
    return value


def first(
    iterable: Iterable[T], filter_func: Callable[[T], bool] | None = None
) -> T | None:
    """Get the first element from an iterable. Returns None if empty"""
    filtered = filter(lambda x: filter_func(x) if filter_func else True, iterable)
    try:
        return next(filtered)
    except StopIteration:
        return None


def firstx(iterable: Iterable[T], filter_func: Callable[[T], bool] | None = None) -> T:
    """Get the first element from an iterable. Raises TypeError if empty"""
    return nonethrows(first(iterable, filter_func))
