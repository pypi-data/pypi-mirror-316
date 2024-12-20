import pygame
import typing

if typing.TYPE_CHECKING:
    from . import decorators

Exceptions = Exception | BaseException
Number = int | float

Flags = int
Element = typing.Union['decorators.ElementInterface']
Elements = list['decorators.ElementInterface']
DictParam = dict[str, typing.Any]
WrapMethod = typing.Literal['word', 'mono']
TextAlignment = typing.Literal['left', 'center', 'right', 'fill']

ColorValue = tuple[int] | list[int] | str | pygame.Color
CursorValue = pygame.Cursor | int

__all__ = [
    'Exceptions',
    'Number',
    'Flags',
    'Element',
    'Elements',
    'DictParam',
    'WrapMethod',
    'TextAlignment',
    'ColorValue',
    'CursorValue',
]