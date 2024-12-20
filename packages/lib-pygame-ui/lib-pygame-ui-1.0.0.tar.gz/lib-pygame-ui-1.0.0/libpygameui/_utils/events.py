from . import decorators
from . import constants
from . import unions

import copy
import typing
import pygame

class ElementEvent:

    def __init__(self, element: unions.Element) -> None:

        self.element = element
        self.element_name = str(element)

        match self.element_name:

            case 'Button':
                self.interaction = constants.DEFAULT
                self.press = constants.DEFAULT
                self.hover = False
                self.cursor_active = False

            case 'Range':
                self.interaction = constants.DEFAULT
                self.press = constants.DEFAULT
                self.hover = False
                self.cursor_active = False
                self.dragging = False
                self.value = 0

            case 'Scroller' | 'ScrollerX' | 'ScrollerY':
                self.press = constants.DEFAULT
                self.keyboard_scrolling = False
                self.scrolling = False
                self.dragging = False
                self.inertia = False
                self.anchor = False
                self.anchor_drag = False
                self.anchor_scroll = False
                self.anchor_keyboard = False
                self.offset_x = 0
                self.offset_y = 0

    def __copy__(self):
        return self.copy()

    def copy(self) -> 'ElementEvent':
        return copy.deepcopy(self)

    def _reset(self) -> None:
        self.__init__(self.element)

    def _send_event(self) -> None:
        match self.element_name:

            case 'Button':
                event = pygame.event.Event(
                    constants.BUTTON,
                    element=self.element,
                    press=self.press
                )

            case 'Range':
                event = pygame.event.Event(
                    constants.RANGE,
                    element=self.element,
                    press=self.press,
                    value=self.value
                )

            case 'Scroller' | 'ScrollerX' | 'ScrollerY':
                event = pygame.event.Event(
                    constants.SCROLLER,
                    element=self.element,
                    press=self.press,
                    keyboard_scrolling=self.keyboard_scrolling,
                    scrolling=self.scrolling,
                    dragging=self.dragging,
                    inertia=self.inertia,
                    anchor=self.anchor,
                    anchor_drag=self.anchor_drag,
                    anchor_scroll=self.anchor_scroll,
                    anchor_keyboard=self.anchor_keyboard,
                    offset_x=self.offset_x,
                    offset_y=self.offset_y,
                    offset=(self.offset_x, self.offset_y)
                )

        pygame.event.post(event)

__all__ = [
    'ElementEvent'
]