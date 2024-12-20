import typing
import pygame

from . import unions
from . import constants

def _raised(
        exception: unions.Exceptions,
        from_exception: unions.Exceptions | None

) -> None:

    if from_exception:
        raise exception from from_exception
    raise exception

def asserter(

    condition: bool,
    exception: unions.Exceptions | str,
    from_exception: unions.Exceptions | None = None

) -> None:
    if not condition:
        if isinstance(exception, str):
            _raised(AssertionError(exception), from_exception)
        _raised(exception, from_exception)

def name(obj: typing.Any) -> str:
    return type(obj).__name__

def floor_value(value: unions.Number, step: unions.Number) -> unions.Number:
    rest = value % step
    if rest < step / 2:
        return value - rest
    return value + (step - rest)

def get_save_value(value: unions.Number, nmin: unions.Number, nmax: unions.Number) -> unions.Number:
    return min(nmax, max(nmin, value))

def get_rect_kwargs_center(rect: pygame.Rect) -> unions.DictParam:
    return {'center': rect.center}

def is_partially_outside(rect: pygame.Rect, other: pygame.Rect) -> bool:
    return not (
        rect.collidepoint(other.left, other.top) or
        rect.collidepoint(other.right, other.top) or
        rect.collidepoint(other.left, other.bottom) or
        rect.collidepoint(other.right, other.bottom) or
        other.collidepoint(rect.left, rect.top) or
        other.collidepoint(rect.right, rect.top) or
        other.collidepoint(rect.left, rect.bottom) or
        other.collidepoint(rect.right, rect.bottom)
    )

def mouse_pressed(only_press: list[unions.Flags] | tuple[unions.Flags]) -> tuple[bool, bool, bool]:
    pressed = pygame.mouse.get_pressed()
    return (
        pressed[0] if constants.PRESS_LEFT in only_press else False,
        pressed[1] if constants.PRESS_MIDDLE in only_press else False,
        pressed[2] if constants.PRESS_RIGHT in only_press else False
    )

__all__ = [
    'asserter',
    'name',
    'floor_value',
    'get_save_value',
    'get_rect_kwargs_center',
    'is_partially_outside',
    'mouse_pressed'
]