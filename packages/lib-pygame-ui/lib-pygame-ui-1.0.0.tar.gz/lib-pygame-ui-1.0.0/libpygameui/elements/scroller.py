import pygame
import typing

from .. import _utils

class Scroller(_utils.decorators.ElementInterface):

    def __init__(

        self,
        clock: typing.Optional[pygame.time.Clock] = None,
        scroll: _utils.unions.DictParam = {},
        speed: _utils.unions.DictParam = {},
        axis: _utils.unions.DictParam = {},
        reversed: _utils.unions.DictParam = {},
        only_press: _utils.unions.Flags = _utils.constants.PRESS_LEFT

    ) -> None:

        super().__init__(Scroller, ['clock'])

        self.event = _utils.events.ElementEvent(self)

        if clock is None:
            self.clock = pygame.time.Clock()
        else:
            self.clock = clock

        self.scroll = scroll
        self.speed = speed
        self.axis = axis
        self.reversed = reversed
        self.only_press = only_press

        self.__scroll_speed_x = 0
        self.__scroll_speed_y = 0
        self.__stopped_time = 0
        self.__last_updated = 0
        self.__last_mouse_pos = (0, 0)
        self.__rscrolling = False
        self.__pressed = False
        self.__initial_anchor_drag_state = False

    @property
    def offset(self) -> tuple[_utils.unions.Number, _utils.unions.Number]:
        return (self.event.offset_x, self.event.offset_y)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_scroll_speed = self.speed.get('scroll', 25)

            if event.button == self.only_press:
                self.event.dragging = True

                self.__last_mouse_pos = pygame.mouse.get_pos()
                self.__scroll_speed_x = 0
                self.__scroll_speed_y = 0
                self.__stopped_time = 0

            elif mouse_scroll_speed is not None and not (self.event.anchor_scroll or self.event.anchor):
                up, down = (5, 4) if self.reversed.get('scroll', False) else (4, 5)
                axis_scroll = self.axis.get('scroll', 'y')

                if event.button == up:
                    self.event.scrolling = True
                    if 'x' in axis_scroll:
                        self.event.offset_x += mouse_scroll_speed
                    if 'y' in axis_scroll:
                        self.event.offset_y += mouse_scroll_speed

                elif event.button == down:
                    self.event.scrolling = True
                    if 'x' in axis_scroll:
                        self.event.offset_x -= mouse_scroll_speed
                    if 'y' in axis_scroll:
                        self.event.offset_y -= mouse_scroll_speed

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == self.only_press:
                self.event.dragging = False
                if self.__stopped_time >= self.scroll.get('stop-threshold', 500):
                    self.__scroll_speed_x = 0
                    self.__scroll_speed_y = 0

    def update(self) -> _utils.events.ElementEvent:
        current_time = pygame.time.get_ticks()

        if current_time - self.__last_updated >= self.speed.get('update', 16):
            self.__last_updated = current_time
            mouse_pressed = pygame.mouse.get_pressed()[self.only_press - 1]
            (min_x_scroll, max_x_scroll), (min_y_scroll, max_y_scroll) = self.scroll.get(
                'min-max-xy',
                (self.scroll.get('min-xy', None), self.scroll.get('max-xy', None))
            )

            self.event.inertia = False

            if mouse_pressed and not self.__pressed:
                self.__initial_anchor_drag_state = self.event.anchor_drag or self.event.anchor
                self.__pressed = True
            elif not mouse_pressed and self.__pressed:
                self.__pressed = False

            if (self.event.anchor_drag or self.event.anchor) and self.__initial_anchor_drag_state:
                self.event.dragging = False

            if self.event.dragging:
                mouse_pos = pygame.mouse.get_pos()
                dx, dy = mouse_pos[0] - self.__last_mouse_pos[0], mouse_pos[1] - self.__last_mouse_pos[1]
                self.__scroll_speed_x = dx
                self.__scroll_speed_y = dy
                self.__last_mouse_pos = mouse_pos

                if dx == 0 and dy == 0:
                    self.__stopped_time += self.clock.get_time()
                else:
                    self.__stopped_time = 0

            elif self.scroll.get('inertia', True):
                momentum = self.scroll.get('momentum', 0.9)

                self.__scroll_speed_x *= momentum
                self.__scroll_speed_y *= momentum

                if abs(self.__scroll_speed_x) < 0.1 and abs(self.__scroll_speed_y) < 0.1:
                    self.__scroll_speed_x = 0
                    self.__scroll_speed_y = 0
                else:
                    self.event.inertia = True

            else:
                self.__scroll_speed_x = 0
                self.__scroll_speed_y = 0

            if (keyboard_speed := self.speed.get('keyboard', 15)) is not None and not (self.event.anchor_keyboard or self.event.anchor):
                keyboard_press = pygame.key.get_pressed()
                axis_keyboard = self.axis.get('keyboard', 'xy')
                keyboard_reversed = self.reversed.get('keyboard', False)

                self.event.keyboard_scrolling = False

                if keyboard_reversed:

                    if 'x' in axis_keyboard:
                        if keyboard_press[pygame.K_LEFT]:
                            self.event.offset_x += keyboard_speed
                            self.event.keyboard_scrolling = True
                        elif keyboard_press[pygame.K_RIGHT]:
                            self.event.offset_x -= keyboard_speed
                            self.event.keyboard_scrolling = True

                    if 'y' in axis_keyboard:
                        if keyboard_press[pygame.K_UP]:
                            self.event.offset_y += keyboard_speed
                            self.event.keyboard_scrolling = True
                        elif keyboard_press[pygame.K_DOWN]:
                            self.event.offset_y -= keyboard_speed
                            self.event.keyboard_scrolling = True

                else:

                    if 'x' in axis_keyboard:
                        if keyboard_press[pygame.K_LEFT]:
                            self.event.offset_x -= keyboard_speed
                            self.event.keyboard_scrolling = True
                        elif keyboard_press[pygame.K_RIGHT]:
                            self.event.offset_x += keyboard_speed
                            self.event.keyboard_scrolling = True

                    if 'y' in axis_keyboard:
                        if keyboard_press[pygame.K_UP]:
                            self.event.offset_y -= keyboard_speed
                            self.event.keyboard_scrolling = True
                        elif keyboard_press[pygame.K_DOWN]:
                            self.event.offset_y += keyboard_speed
                            self.event.keyboard_scrolling = True

            self.event.offset_x += self.__scroll_speed_x
            self.event.offset_y += self.__scroll_speed_y

            if self.__rscrolling:
                self.__rscrolling = False
                self.event.scrolling = False
            elif self.event.scrolling:
                self.__rscrolling = True

            self.event.offset_x = _utils.tools.get_save_value(self.event.offset_x, min_x_scroll, max_x_scroll)
            self.event.offset_y = _utils.tools.get_save_value(self.event.offset_y, min_y_scroll, max_y_scroll)

            self.event._send_event()

        return self.event

    def set_offset(self, offset: tuple[_utils.unions.Number, _utils.unions.Number] | list[_utils.unions.Number]) -> None:
        self.event.offset_x = offset[0]
        self.event.offset_y = offset[1]

    def apply(self, screen_surface: pygame.Surface, surface: pygame.Surface) -> None:
        screen_surface.blit(surface, self.offset)

class ScrollerX(Scroller):

    def __init__(

        self,
        clock: typing.Optional[pygame.time.Clock] = None,
        scroll: _utils.unions.DictParam = {},
        speed: _utils.unions.DictParam = {},
        reversed: _utils.unions.DictParam = {},
        only_press: _utils.unions.Flags = _utils.constants.PRESS_LEFT

    ) -> None:

        super().__init__(
            clock=clock,
            scroll=scroll,
            speed=speed,
            axis={
                'scroll': 'x',
                'keyboard': 'x'
            },
            reversed=reversed,
            only_press=only_press,
        )

        self._child_class = ScrollerX

    @property
    def scroll(self) -> _utils.unions.DictParam:
        return self.__scroll

    @scroll.setter
    def scroll(self, new: _utils.unions.DictParam) -> None:
        self.__scroll = {
            'min-max-xy': (
                new.get(
                    'min-max-x',
                    (new.get('min-x', None), new.get('max-x', None))
                ),
                (new['y'], new['y'])
            ),
            **new
        }

class ScrollerY(Scroller):

    def __init__(

        self,
        clock: typing.Optional[pygame.time.Clock] = None,
        scroll: _utils.unions.DictParam = {},
        speed: _utils.unions.DictParam = {},
        reversed: _utils.unions.DictParam = {},
        only_press: _utils.unions.Flags = _utils.constants.PRESS_LEFT

    ) -> None:

        super().__init__(
            clock=clock,
            scroll=scroll,
            speed=speed,
            axis={
                'scroll': 'y',
                'keyboard': 'y'
            },
            reversed=reversed,
            only_press=only_press
        )

        self._child_class = ScrollerY

    @property
    def scroll(self) -> _utils.unions.DictParam:
        return self.__scroll

    @scroll.setter
    def scroll(self, new: _utils.unions.DictParam) -> None:
        self.__scroll = {
            'min-max-xy': (
                (new['x'], new['x']),
                new.get(
                    'min-max-y',
                    (new.get('min-y', None), new.get('max-y', None))
                )
            ),
            **new
        }

__all__ = [
    'Scroller',
    'ScrollerX',
    'ScrollerY'
]