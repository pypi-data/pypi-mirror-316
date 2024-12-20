import pygame
import typing

from . import _utils

def set_cursor_global(

        elements: _utils.unions.Elements,
        inactive: typing.Optional[_utils.unions.CursorValue] = None,
        active: typing.Optional[_utils.unions.CursorValue] = None,
        set_active: bool = True

    ) -> None:

    any_pressed = False

    for element in elements:

        if hasattr(element, 'cursor'):
            if set_active:
                element.cursor['active'] = active
            element.cursor['inactive'] = None

        if str(element) in ('Button', 'Range') and element.event.cursor_active and not any_pressed:
            any_pressed = True

    if inactive is not None and not any_pressed:
        pygame.mouse.set_cursor(inactive)

class Manager(_utils.decorators.ElementInterface):

    def __init__(

        self,
        elements: _utils.unions.Elements,
        cursor_global_param: _utils.unions.DictParam = {}

    ) -> None:

        super().__init__(Manager, ['elements'])

        self.elements = elements
        self.cursor_global_param = cursor_global_param

    def handle_event(self, event: pygame.event.Event) -> None:
        for element in self.elements:
            element.handle_event(event)

    def update(self) -> None:
        set_cursor_global(self.elements, **self.cursor_global_param)
        for element in self.elements:
            element.update()

    def draw_and_update(self) -> None:
        set_cursor_global(self.elements, **self.cursor_global_param)
        for element in self.elements:
            if hasattr(element, 'draw_and_update'):
                element.draw_and_update()
            else:
                element.update()

    def draw_inactive(self) -> None:
        for element in self.elements:
            if hasattr(element, 'draw_inactive'):
                element.draw_inactive()

    def draw_hover(self) -> None:
        for element in self.elements:
            if hasattr(element, 'draw_hover'):
                element.draw_hover()

    def draw_active(self) -> None:
        for element in self.elements:
            if hasattr(element, 'draw_active'):
                element.draw_active()

__all__ = [
    'set_cursor_global',
    'Manager'
]