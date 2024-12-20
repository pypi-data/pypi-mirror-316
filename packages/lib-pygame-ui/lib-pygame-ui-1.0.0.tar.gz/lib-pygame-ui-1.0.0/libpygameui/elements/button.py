import pygame
import typing

from .. import _utils
from . import wrap

class Button(_utils.decorators.ElementInterface):

    def __init__(

        self,
        surface: pygame.Surface,
        rect: pygame.Rect,
        text: _utils.unions.DictParam = {},
        outline: _utils.unions.DictParam = {},
        image: _utils.unions.DictParam = {},
        color: _utils.unions.DictParam = {},
        cursor: _utils.unions.DictParam = {},
        border: _utils.unions.DictParam = {},
        with_event: bool = True,
        hide: bool = False,
        alpha: int = 255,
        only_press: list[_utils.unions.Flags] | tuple[_utils.unions.Flags] = [_utils.constants.PRESS_LEFT],
        press_speed: int = 50

    ) -> None:

        super().__init__(Button, ['surface'])

        self.event = _utils.events.ElementEvent(self)

        self.surface = surface
        self.rect = rect
        self.text = text
        self.outline = outline
        self.image = image
        self.color = color
        self.cursor = cursor
        self.border = border
        self.with_event = with_event
        self.hide = hide
        self.alpha = alpha
        self.only_press = only_press
        self.press_speed = press_speed

        self._send_event = True

        self.__pressed = False
        self.__last_pressed_time = 0
        self.__initial_pressed_state = _utils.constants.DEFAULT

    def _render_and_draw(self, interaction: _utils.unions.Flags) -> None:
        if not self.is_outside():

            rect = self.rect
            button_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
            surf_rect = button_surface.get_rect()

            if 'font' not in self.text:
                font = self.text['font'] = pygame.font.SysFont('arial', 20)
            else:
                font = self.text['font']

            text = self.text.get('text', '')
            outline_size = self.outline.get('size', 0)
            image = self.image.get('surface', None)
            rect_border_kw = {'border_' + kw.replace('-', '_'): value for kw, value in self.border.items()}
            size_with_outline = (rect.width - outline_size * 2, rect.height - outline_size * 2)
            with_outline = outline_size > 0

            match interaction:

                case _utils.constants.ELEMENT_INACTIVE:
                    text_color = self.text.get('inactive-color', self.color.get('text-inactive-color', self.text.get('color', '#000000')))
                    text_background_color = self.text.get('bg-inactive-color', self.color.get('text-bg-inactive-color', None))
                    outline_color = self.outline.get('inactive-color', self.color.get('outline-inactive-color', self.outline.get('color', '#3d3d3d')))
                    color = self.color.get('inactive', self.color.get('color', '#ffffff'))

                case _utils.constants.ELEMENT_HOVER:
                    text_color = self.text.get('hover-color', self.color.get('text-hover-color', self.text.get('color', '#000000')))
                    text_background_color = self.text.get('bg-hover-color', self.color.get('text-bg-hover-color', None))
                    outline_color = self.outline.get('hover-color', self.color.get('outline-hover-color', self.outline.get('color', '#3d3d3d')))
                    color = self.color.get('hover', self.color.get('color', '#ebebeb'))

                case _utils.constants.ELEMENT_ACTIVE:
                    text_color = self.text.get('active-color', self.color.get('text-active-color', self.text.get('color', '#ffffff')))
                    text_background_color = self.text.get('bg-active-color', self.color.get('text-bg-active-color', None))
                    outline_color = self.outline.get('active-color', self.color.get('outline-active-color', self.outline.get('color', '#3d3d3d')))
                    color = self.color.get('active', self.color.get('color', '#d6d6d6'))

            if not self.hide:
                if with_outline:
                    # outline
                    rect_outline_border_kw = {key: value + outline_size for key, value in rect_border_kw.items()}
                    pygame.draw.rect(button_surface, outline_color, surf_rect, **rect_outline_border_kw)

                    # main area
                    pygame.draw.rect(button_surface, color, (((rect.width - size_with_outline[0]) / 2,
                                                       (rect.height - size_with_outline[1]) / 2),
                                                      size_with_outline), **rect_border_kw)
                else:
                    # main area
                    pygame.draw.rect(button_surface, color, surf_rect, **rect_border_kw)

            if image is not None:
                image_to_resize = self.image.get('resize', None)
                image_position = self.image.get('position', _utils.tools.get_rect_kwargs_center)
                if image_to_resize is not None:
                    image = pygame.transform.scale(image, image_to_resize)

                if isinstance(image_position, dict):
                    button_surface.blit(image, image.get_rect(**image_position))
                else:
                    button_surface.blit(image, image.get_rect(**image_position(surf_rect)))

            if text:
                text_antialias = self.text.get('antialias', True)
                text_wrap_kw = self.text.get('wrap', False) or {}
                text_position = self.text.get('position', _utils.tools.get_rect_kwargs_center)

                if not text_wrap_kw:
                    text_surface = font.render(text, text_antialias, text_color, text_background_color)
                else:
                    if text_wrap_kw is True:
                        text_wrap_kw = {}

                    kw_len = text_wrap_kw.get('length', rect.width)
                    is_len_area = kw_len == 'area'
                    wrap_length = rect.width if is_len_area else kw_len
                    if is_len_area and with_outline:
                        wrap_length = size_with_outline[0]

                    text_surface = wrap.render_wrap(
                        font,
                        text,
                        wrap_length,
                        text_antialias,
                        text_color,
                        text_background_color,
                        text_wrap_kw.get('line-gap', 0),
                        text_wrap_kw.get('tab-size', 4),
                        text_wrap_kw.get('alignment', 'center'),
                        text_wrap_kw.get('method', 'word')
                    )

                if isinstance(text_position, dict):
                    button_surface.blit(text_surface, text_surface.get_rect(**text_position))
                else:
                    button_surface.blit(text_surface, text_surface.get_rect(**text_position(surf_rect)))

            button_surface.set_alpha(self.alpha)

            self.surface.blit(button_surface, self.rect)

    def is_outside(self) -> bool:
        return _utils.tools.is_partially_outside(self.surface.get_rect(), self.rect)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and self.with_event:

            self.__initial_pressed_state = _utils.constants.DEFAULT
            self.__pressed = False

            if event.button == 1 and self.event.hover and _utils.constants.PRESS_LEFT in self.only_press:
                self.__initial_pressed_state = _utils.constants.PRESS_LEFT
                self.__pressed = True
            elif event.button == 2 and self.event.hover and _utils.constants.PRESS_MIDDLE in self.only_press:
                self.__initial_pressed_state = _utils.constants.PRESS_MIDDLE
                self.__pressed = True
            elif event.button == 3 and self.event.hover and _utils.constants.PRESS_RIGHT in self.only_press:
                self.__initial_pressed_state = _utils.constants.PRESS_RIGHT
                self.__pressed = True

    def update(self) -> _utils.events.ElementEvent:
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse_pos)

        self.event.press = _utils.constants.DEFAULT
        self.event.interaction = _utils.constants.ELEMENT_INACTIVE
        self.event.hover = is_hover
        self.event.cursor_active = False

        if not self.is_outside():
            current_time = pygame.time.get_ticks()
            get_pressed = _utils.tools.mouse_pressed(self.only_press)
            any_pressed = (get_pressed[0] or get_pressed[1] or get_pressed[2])

            if (cursor := self.cursor.get('active', None)) is not None and is_hover:
                self.event.cursor_active = True
                pygame.mouse.set_cursor(cursor)
            elif (cursor := self.cursor.get('inactive', None)) is not None:
                pygame.mouse.set_cursor(cursor)

            if any_pressed and is_hover:
                self.event.interaction = _utils.constants.ELEMENT_ACTIVE
            elif is_hover:
                self.event.interaction = _utils.constants.ELEMENT_HOVER

            if not self.with_event and is_hover:
                if current_time - self.__last_pressed_time > self.press_speed and any_pressed:
                    if get_pressed[0]:
                        press = _utils.constants.PRESS_LEFT
                    elif get_pressed[1]:
                        press = _utils.constants.PRESS_MIDDLE
                    elif get_pressed[2]:
                        press = _utils.constants.PRESS_RIGHT
                    self.__pressed = False
                    self.__last_pressed_time = current_time
                    self.event.press = press
                    if self._send_event:
                        self.event._send_event()

            elif self.with_event and is_hover:
                if self.__pressed and any_pressed:
                    pass
                elif current_time - self.__last_pressed_time > self.press_speed and self.__pressed:
                    self.__pressed = False
                    self.__last_pressed_time = current_time
                    self.event.press = self.__initial_pressed_state
                    if self._send_event:
                        self.event._send_event()

            if not (is_hover or any_pressed):
                self.__pressed = False

        return self.event

    def draw_and_update(self) -> _utils.events.ElementEvent:
        self.update()
        self._render_and_draw(self.event.interaction)
        return self.event

    def draw_inactive(self) -> None:
        self.__pressed = False
        self._render_and_draw(_utils.constants.ELEMENT_INACTIVE)
        self.event._reset()

    def draw_hover(self) -> None:
        self.__pressed = False
        self._render_and_draw(_utils.constants.ELEMENT_HOVER)
        self.event._reset()

    def draw_active(self) -> None:
        self.__pressed = False
        self._render_and_draw(_utils.constants.ELEMENT_ACTIVE)
        self.event._reset()

class Range(_utils.decorators.ElementInterface):

    def __init__(

        self,
        surface: pygame.Surface,
        rect: pygame.Rect,
        outline: _utils.unions.DictParam = {},
        color: _utils.unions.DictParam = {},
        cursor: _utils.unions.DictParam = {},
        border: _utils.unions.DictParam = {},
        track: _utils.unions.DictParam = {},
        track_fill: _utils.unions.DictParam = {},
        thumb: _utils.unions.DictParam = {},
        value: _utils.unions.DictParam = {},
        hide: _utils.unions.DictParam = {},
        alpha: _utils.unions.DictParam = {},
        reversed: _utils.unions.DictParam = {},
        horizontal: bool = True,
        drag_middle_mouse: bool = True,
        with_event: bool = False,
        only_press: list[_utils.unions.Flags] | tuple[_utils.unions.Flags] = [_utils.constants.PRESS_LEFT],
        press_speed: int = 50

    ) -> None:

        super().__init__(Range, ['surface'])

        self.__button_track = Button(surface=surface, rect=rect)
        self.__button_track_fill = self.__button_track.copy()
        self.__button_thumb = self.__button_track.copy()

        self.__button_track._send_event = False
        self.__button_track_fill._send_event = False
        self.__button_thumb._send_event = False

        self.event = _utils.events.ElementEvent(self)

        self.surface = surface
        self.outline = outline
        self.color = color
        self.cursor = cursor
        self.border = border
        self.track = track
        self.track_fill = track_fill
        self.thumb = thumb
        self.value = value
        self.hide = hide
        self.horizontal = horizontal
        self.reversed = reversed
        self.drag_middle_mouse = drag_middle_mouse
        self.with_event = with_event
        self.alpha = alpha
        self.only_press = only_press
        self.press_speed = press_speed

        self.__detected_scrolling_mouse = False
        self.__pressed = False

        self.rect = rect

    @property
    def surface(self) -> pygame.Surface:
        return self.__surface

    @property
    def rect(self) -> pygame.Rect:
        return self.__rect

    @surface.setter
    def surface(self, new: pygame.Surface) -> None:
        self.__surface = new
        self.__button_track.surface = new
        self.__button_track_fill.surface = new
        self.__button_thumb.surface = new

    @rect.setter
    def rect(self, new: pygame.Rect) -> None:
        self.__rect = new
        self.__button_track.rect = new.copy()
        self._update_rect()

    def _get_values(self) -> tuple[_utils.unions.Number,
                                    _utils.unions.Number,
                                    _utils.unions.Number,
                                    _utils.unions.Number | None,
                                    type[_utils.unions.Number]]:

        min_value = self.value.get('min', 0)

        if 'value' not in self.value:
            self.value['value'] = min_value

        return (min_value,
                self.value.get('max', 100),
                self.value['value'],
                self.value.get('step', None),
                self.value.get('output', float))

    def _snap_step(self,
                    value: _utils.unions.Number,
                    min_value: _utils.unions.Number,
                    step: _utils.unions.Number,
                    output: type[_utils.unions.Number]) -> _utils.unions.Number:

        # handle snapping to steps
        rest = (value - min_value) % step
        if rest < step / 2:
            return output(value - rest)
        else:
            return output(value + (step - rest))

    def _update_rect(self, mouse_pos: tuple[int, int] | None = None) -> None:
        min_value, max_value, value, step, output = self._get_values()

        rect = self.__rect
        track_fill_rect = self.__button_track_fill.rect
        thumb_rect = self.__button_thumb.rect

        reversed = self.reversed.get('all', False)
        use_thumb = self._use_thumb()

        if step is not None:
            self.event.value = self.value['value'] = value = self._snap_step(value, min_value, step, output)

        if mouse_pos is not None:
            xm, ym = mouse_pos
            if self.horizontal:
                relative_position = _utils.tools.get_save_value((xm - rect.left) / rect.width, 0, 1)
            else:
                relative_position = _utils.tools.get_save_value((ym - rect.top) / rect.height, 0, 1)

            self.event.value = value = self.value['value'] = output(
                max_value - relative_position * (max_value - min_value)
                if reversed else
                min_value + relative_position * (max_value - min_value)
            )

            if step is not None:
                self.event.value = self.value['value'] = value = self._snap_step(value, min_value, step, output)

        if self.horizontal:
            track_fill_rect.size = (((value - min_value) / (max_value - min_value)) * rect.width, rect.height)

            if reversed:
                track_fill_rect.left = rect.right - track_fill_rect.width
            else:
                track_fill_rect.left = rect.left

            if use_thumb:
                thumb_rect.size = self.thumb['size']
                thumb_rect.top = rect.top + (rect.height - thumb_rect.height) / 2
                thumb_rect.left = (
                    track_fill_rect.left - thumb_rect.width / 2
                    if reversed else
                    track_fill_rect.right - thumb_rect.width / 2
                )
        else:
            track_fill_rect.size = (((value - min_value) / (max_value - min_value)) * rect.height, rect.width)

            if reversed:
                track_fill_rect.top = rect.bottom - track_fill_rect.height
            else:
                track_fill_rect.top = rect.top

            if use_thumb:
                thumb_rect.size = self.thumb['size']
                thumb_rect.left = rect.left + (rect.width - thumb_rect.width) / 2
                thumb_rect.top = (
                    track_fill_rect.top - thumb_rect.height / 2
                    if reversed else
                    track_fill_rect.bottom - thumb_rect.height / 2
                )

    def _render_and_draw(self, interaction: _utils.unions.Flags, updated: bool = True) -> None:
        if not self.is_outside():

            self.__button_track.outline = self.outline.get('track', self.track.get('outline', {}))
            self.__button_track_fill.outline = self.outline.get('track-fill', self.track_fill.get('outline', {}))
            self.__button_thumb.outline = self.outline.get('thumb', self.thumb.get('outline', {}))

            self.__button_track.color = self.color.get('track', self.track.get('color', {
                'inactive': '#4a4a4a',
                'hover': '#575757',
                'active': '#383838'
            }))
            self.__button_track_fill.color = self.color.get('track-fill', self.track_fill.get('color', {
                'inactive': '#4f8fe3',
                'hover': '#76a5e3',
                'active': '#2e72c9'
            }))
            self.__button_thumb.color = self.color.get('thumb', self.thumb.get('color', {}))

            self.__button_track.border = self.border.get('track', self.track.get('border', {
                'radius': 50
            }))
            self.__button_track_fill.border = self.border.get('track-fill', self.track_fill.get('border', {
                'radius': 50
            }))
            self.__button_thumb.border = self.border.get('thumb', self.thumb.get('border', {
                'radius': 100
            }))

            self.__button_track.hide = self.hide.get('track', self.track.get('hide', False))
            self.__button_track_fill.hide = self.hide.get('track-fill', self.track_fill.get('hide', False))
            self.__button_thumb.hide = self.hide.get('thumb', self.thumb.get('hide', False))

            self.__button_track.alpha = self.alpha.get('track', self.track.get('alpha', 255))
            self.__button_track_fill.alpha = self.alpha.get('track-fill', self.track_fill.get('alpha', 255))
            self.__button_thumb.alpha = self.alpha.get('thumb', self.thumb.get('alpha', 255))

            match interaction:

                case _utils.constants.ELEMENT_INACTIVE:
                    if updated:
                        self.__button_track._render_and_draw(_utils.constants.ELEMENT_INACTIVE)
                    else:
                        self.__button_track.draw_inactive()
                    self.__button_track_fill.draw_inactive()
                    if self._use_thumb():
                        self.__button_thumb.draw_inactive()

                case _utils.constants.ELEMENT_HOVER:
                    if updated:
                        self.__button_track._render_and_draw(_utils.constants.ELEMENT_HOVER)
                    else:
                        self.__button_track.draw_hover()
                    self.__button_track_fill.draw_hover()
                    if self._use_thumb():
                        self.__button_thumb.draw_hover()

                case _utils.constants.ELEMENT_ACTIVE:
                    if updated:
                        self.__button_track._render_and_draw(_utils.constants.ELEMENT_ACTIVE)
                    else:
                        self.__button_track.draw_active()
                    self.__button_track_fill.draw_active()
                    if self._use_thumb():
                        self.__button_thumb.draw_active()

    def _use_thumb(self) -> bool:
        return 'size' in self.thumb

    def set_value(self, value: _utils.unions.Number) -> None:
        min_value, max_value, _, _, output = self._get_values()
        self.event.value = self.value['value'] = _utils.tools.get_save_value(output(value), min_value, max_value)
        self._update_rect()

    def is_outside(self) -> bool:
        return (
            self.__button_track.is_outside() or
            _utils.tools.is_partially_outside(self.surface.get_rect(), self.__button_thumb.rect)
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        self.__button_track.with_event = self.with_event
        self.__button_track.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN and self.drag_middle_mouse:
            detected = False
            value = self.value['value']
            step = self.value.get('step', None)
            up, down = (5, 4) if self.reversed.get('scroll', False) else (4, 5)

            if step is None:
                step = 1

            if event.button == up and self.event.hover:
                value += step
                detected = True
            elif event.button == down and self.event.hover:
                value -= step
                detected = True

            if detected:
                self.__detected_scrolling_mouse = True

                self.event.press = _utils.constants.PRESS_SCROLL
                self.event.dragging = True

                self.set_value(value)
                self.event._send_event()

    def update(self) -> _utils.events.ElementEvent:
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.__rect.collidepoint(mouse_pos)
        use_thumb = self._use_thumb()

        if use_thumb:
            is_hover = is_hover or self.__button_thumb.rect.collidepoint(mouse_pos)

        self.event.press = _utils.constants.DEFAULT
        self.event.interaction = _utils.constants.ELEMENT_INACTIVE
        self.event.hover = is_hover
        self.event.cursor_active = False

        if not self.is_outside():
            get_pressed = _utils.tools.mouse_pressed(self.only_press)
            any_pressed = (get_pressed[0] or get_pressed[1] or get_pressed[2])

            if not self.__detected_scrolling_mouse:
                self.event.dragging = False

            if (cursor := self.cursor.get('active', None)) is not None and ((is_hover or self.__pressed)
                                                                            if self.cursor.get('active-outside', True) else
                                                                            is_hover):
                self.event.cursor_active = True
                pygame.mouse.set_cursor(cursor)
            elif (cursor := self.cursor.get('inactive', None)) is not None:
                pygame.mouse.set_cursor(cursor)

            self.__button_track.update()

            if is_hover:
                self.event.interaction = _utils.constants.ELEMENT_HOVER
            elif self.__button_track.event.interaction == _utils.constants.ELEMENT_ACTIVE:
                self.event.interaction = _utils.constants.ELEMENT_ACTIVE

            if (track_press := self.__button_track.event.press) and self.with_event:
                self.event.press = track_press
                self.event.dragging = True
                self._update_rect(mouse_pos)
                return self.event

            elif any_pressed and not self.with_event:
                if is_hover:
                    self.__pressed = True

                if self.__pressed:
                    self.event.interaction = _utils.constants.ELEMENT_ACTIVE
                    self.event.dragging = True

                    if get_pressed[0]:
                        self.event.press = _utils.constants.PRESS_LEFT
                    elif get_pressed[1]:
                        self.event.press = _utils.constants.PRESS_MIDDLE
                    elif get_pressed[2]:
                        self.event.press = _utils.constants.PRESS_RIGHT

                    self._update_rect(mouse_pos)
                    self.event._send_event()
                    return self.event

            elif not self.with_event:
                self.__pressed = False

            if self.__detected_scrolling_mouse:
                self.__detected_scrolling_mouse = False

        return self.event

    def draw_and_update(self) -> _utils.events.ElementEvent:
        self.update()
        self._render_and_draw(self.event.interaction)
        return self.event

    def draw_inactive(self) -> None:
        self.__pressed = False
        self._render_and_draw(_utils.constants.ELEMENT_INACTIVE, False)
        self.event._reset()

    def draw_hover(self) -> None:
        self.__pressed = False
        self._render_and_draw(_utils.constants.ELEMENT_HOVER, False)
        self.event._reset()

    def draw_active(self) -> None:
        self.__pressed = False
        self._render_and_draw(_utils.constants.ELEMENT_ACTIVE, False)
        self.event._reset()

__all__ = [
    'Button',
    'Range'
]