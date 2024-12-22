from abc import ABC
from collections.abc import Sequence
from typing import Awaitable, Callable, Self, final


type Listener = Callable[[], Awaitable[None]]
type Listeners = Listener | Sequence[Listener] | None


class AsyncContextManager(ABC):
    def __init__(self):
        self._on_started: list[Listener] = []
        self._on_stopped: list[Listener] = []
        self._is_started: bool = False

    def before_started(self, func: Listeners) -> None:
        if func:
            self._on_started[:0] = func if isinstance(func, Sequence) else (func,)

    def after_started(self, func: Listeners) -> None:
        if func:
            self._on_started.extend(func if isinstance(func, Sequence) else (func,))

    def before_stopped(self, func: Listeners) -> None:
        if func:
            self._on_stopped[:0] = func if isinstance(func, Sequence) else (func,)

    def after_stopped(self, func: Listeners) -> None:
        if func:
            self._on_stopped.extend(func if isinstance(func, Sequence) else (func,))

    async def start(self) -> None:
        for listener in self._on_started:
            await listener()

    async def stop(self) -> None:
        for listener in self._on_stopped:
            await listener()

    @property
    def is_started(self) -> bool:
        return self._is_started

    @final
    def assert_started(self) -> None:
        if not self._is_started:
            raise RuntimeError(f'{self.__class__.__name__} is already stopped')

    @final
    def assert_stopped(self) -> None:
        if self._is_started:
            raise RuntimeError(f'{self.__class__.__name__} is already started')

    async def __aenter__(self) -> Self:
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()


class AsyncOperator(AsyncContextManager, ABC):
    ...  # todo: pause/unpause


class AsyncResource(AsyncContextManager, ABC):
    ...
