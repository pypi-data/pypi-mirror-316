import inspect
import pygame
import typing
import copy
import abc

from . import tools

if typing.TYPE_CHECKING:
    from . import unions
    from . import events

class Interface:

    def __init__(self, child_class: object, except_copy: list[str] = []) -> None:
        self._child_class = child_class
        self._except_copy = except_copy

    def __str__(self) -> str:
        return self.__class__.__name__

    def __copy__(self):
        return self.copy()

    def __deepcopy__(self, memo: dict):
        return self.copy()

    def get_param(self) -> 'unions.DictParam':
        signature = inspect.signature(self.__init__)
        return {name: getattr(self, name) for name in signature.parameters}

    def set_param(self, **kwargs) -> None:
        for name, value in kwargs.items():
            setattr(self, name, value)

    def copy(self, **kwargs) -> typing.Self:
        params = self.get_param()

        for key, value in params.items():
            if key not in self._except_copy and key not in kwargs:
                params[key] = copy.deepcopy(value)

        return self._child_class(**(params | kwargs))

class ElementInterface(abc.ABC, Interface):

    @abc.abstractmethod
    def __init__(self, child_class: 'ElementInterface', except_copy: list[str] = []) -> None:
        super().__init__(child_class, except_copy)

    @abc.abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self) -> 'events.ElementEvent':
        raise NotImplementedError

__all__ = [
    'Interface',
    'ElementInterface'
]