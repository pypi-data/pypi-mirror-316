import synchronicity.combined_types
import typing
import typing_extensions

class BlockingFoo:
    singleton: BlockingFoo

    def __init__(self, arg: str):
        ...

    class __getarg_spec(typing_extensions.Protocol):
        def __call__(self) -> str:
            ...

        async def aio(self) -> str:
            ...

    getarg: __getarg_spec

    class __gen_spec(typing_extensions.Protocol):
        def __call__(self) -> typing.Generator[int, None, None]:
            ...

        def aio(self) -> typing.AsyncGenerator[int, None]:
            ...

    gen: __gen_spec

    @staticmethod
    def some_static(arg: str) -> float:
        ...

    @classmethod
    def clone(cls, foo: BlockingFoo) -> BlockingFoo:
        ...


_T_Blocking = typing.TypeVar("_T_Blocking", bound="BlockingFoo")

class __listify_spec(typing_extensions.Protocol):
    def __call__(self, t: _T_Blocking) -> typing.List[_T_Blocking]:
        ...

    async def aio(self, t: _T_Blocking) -> typing.List[_T_Blocking]:
        ...

listify: __listify_spec


@typing.overload
def overloaded(arg: str) -> float:
    ...

@typing.overload
def overloaded(arg: int) -> int:
    ...


class __returns_foo_spec(typing_extensions.Protocol):
    def __call__(self) -> BlockingFoo:
        ...

    async def aio(self) -> BlockingFoo:
        ...

returns_foo: __returns_foo_spec


class __wrapped_make_context_spec(typing_extensions.Protocol):
    def __call__(self, a: float) -> synchronicity.combined_types.AsyncAndBlockingContextManager[str]:
        ...

    def aio(self, a: float) -> typing.AsyncContextManager[str]:
        ...

wrapped_make_context: __wrapped_make_context_spec


P = typing_extensions.ParamSpec("P")

R = typing.TypeVar("R")

R_INNER = typing.TypeVar("R_INNER", covariant=True)

P_INNER = typing_extensions.ParamSpec("P_INNER")

class CallableWrapper(typing.Generic[P, R]):
    def __init__(self, /, *args, **kwargs):
        ...

    class __func_spec(typing_extensions.Protocol[R_INNER, P_INNER]):
        def __call__(self, *args: P_INNER.args, **kwargs: P_INNER.kwargs) -> R_INNER:
            ...

        async def aio(self, *args: P_INNER.args, **kwargs: P_INNER.kwargs) -> R_INNER:
            ...

    func: __func_spec[R, P]


def wrap_callable(c: typing.Callable[P, R]) -> CallableWrapper[P, R]:
    ...


some_instance: typing.Optional[BlockingFoo]