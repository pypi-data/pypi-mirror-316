# From is a simple class that allows for easy encapsulation and chaining of functions.
#
# Note that the type of a From instance is not only From[T],
# but at the same time Callable[[U], From[T]].
import traceback

from typing import (
    Callable,
    Iterable,
    TypeVar,
    Generic,
)


T = TypeVar("T")
U = TypeVar("U")


class From(Generic[T]):
    """Base class"""

    def __init__(self, val: T = None):
        self.val = val

    def __eq__(self, other: "From"):
        return self.val == other.val

    def __repr__(self):
        return f"<{self.__class__.__name__} val=({self.val})>"

    def __bool__(self):
        return True if self.val else False

    def __call__(self, func):
        return self.unit(func)

    def __mul__(self, other: "From"):
        return self.fmap(lambda a: a * other.val)

    def __rmul__(self, other: "From"):
        return self.fmap(lambda a: a * other.val)

    def __add__(self, other: "From"):
        return self.fmap(lambda a: a + other.val)

    def __radd__(self, other: "From"):
        return self.fmap(lambda a: a + other.val)

    def __sub__(self, other: "From"):
        return self.fmap(lambda a: a - other.val)

    def __rsub__(self, other: "From"):
        return self.fmap(lambda a: a - other.val)

    def __truediv__(self, other: "From"):
        return self.fmap(lambda a: a / other.val)

    def __iter__(self):
        assert isinstance(self.val, Iterable)
        for i in self.val:
            yield self.unit(i)

    def __lshift__(self, method):
        return self.fmap(method)

    def __and__(self, method):
        return self.effect(method)

    @classmethod
    def unit(cls, val: U) -> "From[U]":
        """Return a new instance of the same encapsulating class, wrapping `val`"""
        return cls(val)  # type: ignore

    def fmap(self, func: Callable[[T], U]) -> "From[U]":
        """Return a new wrapped instance with `func` applied to self.val"""
        return self.unit(func(self.val))

    def bind(self, F: Callable[[T], "From[U]"]) -> "From[U]":
        """Return a new wrapped instance with `func` applied to self.val"""
        return F(self.val)

    def effect(self, func):
        """Return self while applying `func` to self.val"""
        func(self.val)
        return self

    def __rshift__(self, method) -> "From":
        return self.bind(method)


class Maybe(From[T]):
    def fmap(self, func: Callable[[T], U]) -> "Just[U] | Nothing":
        if self.val:
            return Just(func(self.val))
        return Nothing()

    def bind(self, F: Callable[[T], "Just[U] | Nothing"]) -> "Just[U] | Nothing":
        match self:
            case Nothing():
                return self
            case Maybe():
                return F(self.val)


class Nothing(Maybe[None]):
    def __init__(self, val: T | None = None):
        assert val is None
        self.val = val


class Just(Maybe[T]):
    def __init__(self, val: T | None):
        assert val is not None
        self.val = val


class Result(From[T]):
    def fmap(self, func: Callable[[T], U]) -> "Success[U] | Error":
        try:
            return Success(func(self.val))
        except Exception as e:
            return Error({"e": e, "stack": traceback.format_stack()})

    def bind(self, F: Callable[[T], "Success[U] | Error"]) -> "Success[U] | Error":
        match self:
            case Error():
                return self
            case Result():
                return F(self.val)


class Success(Result[T]):
    pass


class Error(Result[Exception]):
    pass


M = TypeVar("M", bound=From)


def hprint(s: str) -> Callable[..., None]:
    return lambda *args, **kwargs: print(
        f"[{s}]",
        *args,
        **kwargs,
    )


def index(i: int | str) -> Callable[[list[T]], T]:
    return lambda lst: lst[i]


def to(cls: type[From[U]]):
    def outer(func: Callable[[U], T]) -> Callable[[U], From[T]]:
        return lambda *args, **kwargs: cls(*args, **kwargs) << func

    return outer


def compose(
    f: From[T], g: Callable[[T], From[U]] = Nothing(), *hs: Callable[..., From]
) -> From:
    return compose(g(f.val), *hs) if g else f


def typeof(cls):
    def inner(obj):
        assert isinstance(obj, cls)

    return inner


if __name__ == "__main__":
    m = Maybe(2)
    assert m.fmap(lambda x: 3 * x) == Maybe(6)
    assert m
    assert not Maybe(None).fmap(
        lambda x: 3 * x
    )  # notice, type checker already protests. This will still work.
    assert Maybe(None) == Nothing()

    assert From(3) + From(2)
    assert From(2) / From(1)
    assert From(2) * From(2)
    assert From("1") + From("2")
    assert From("1") * From(2)

    @to(From[str])
    def test(s: str):
        return f"[{s}]"

    assert test("hi").effect(print) == Just("[hi]")
    a = "b"
    assert test("a").fmap(eval) == Just(["b"])
    assert test("a") != Nothing()

    @to(From)
    def id(val):
        return val

    def add1(val: int):
        return val + 1

    @to(Just)
    def just_add1(val: int):
        return add1(val)

    just_add1(1).effect(print)
    assert id(1).fmap(add1) == Just(2)
    assert compose(id(1), just_add1, just_add1, test) == Just("[3]")

    assert isinstance(Result(1) / Result(0), Error)
    assert not isinstance(Result(1) / Result(1), Error)
    assert isinstance(Result(1) / Result(1), Success)
    assert not isinstance(Result(1) / Result(0), Success)

    Result(1) << add1 << (lambda i: "[cool, I can chain...] " + str(i)) & print

    div: Callable[[int], Callable[[int], Result]] = lambda y: lambda x: Result(x).fmap(
        lambda x: x / y
    )

    x = Result(1) / Result(0)

    assert isinstance(
        (Result(1) >> div(2) & print) >> div(0) >> div(1) >> div(2), Error
    )

    assert isinstance(Result(1) >> div(2) & print, Success)
