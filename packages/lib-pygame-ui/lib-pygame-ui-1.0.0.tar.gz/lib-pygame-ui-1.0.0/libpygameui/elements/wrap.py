import pygame
import typing
import re

from .. import _utils

def wrap_mono(

    font: pygame.font.Font,
    text: str,
    length: _utils.unions.Number,
    tab_size: int = 4

) -> list[str]:

    text = text.replace('\r', '').replace('\t', ' ' * tab_size)
    parts = []
    current_part = ''

    for char in text:
        if font.size(current_part + char)[0] <= length:
            current_part += char
        else:
            parts.append(current_part)
            current_part = char

    if current_part:
        parts.append(current_part)

    return parts

def wrap_word(

    font: pygame.font.Font,
    text: str,
    length: _utils.unions.Number,
    tab_size: int = 4

) -> list[str]:

    tab_spaces = ' ' * tab_size
    text = text.replace('\r', '')
    words = text.split(' ')
    lines = []
    current_line = ''
    hyphenate_parrent = r'(?<=-)(?=(?!-).)'

    for word in words:
        word = word.replace('\t', tab_spaces)
        test_line = current_line + ' ' + word if current_line else word

        if font.size(test_line)[0] <= length:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)

            current_line = ''
            hyphenated_parts = re.split(hyphenate_parrent, word)

            for part in hyphenated_parts:
                wrapped_parts = wrap_mono(font, part, length, 0)

                for wrapped_part in wrapped_parts:
                    if font.size(current_line + wrapped_part)[0] <= length:
                        current_line += wrapped_part
                    else:
                        if current_line:
                            lines.append(current_line)
                        current_line = wrapped_part

    if current_line:
        lines.append(current_line)

    return lines

def wrap_text(

    font: pygame.font.Font,
    text: str,
    length: _utils.unions.Number,
    tab_size: int = 4,
    method: _utils.unions.WrapMethod = 'word'

) -> list[str]:

    lines = text.split('\n')
    wrapped_lines = []

    for line in lines:

        match method:

            case 'word':
                wrapped_lines.extend(wrap_word(font, line, length, tab_size))
            case 'mono':
                wrapped_lines.extend(wrap_mono(font, line, length, tab_size))

    return wrapped_lines

def render_wrap(

    font: pygame.font.Font,
    text: str,
    length: _utils.unions.Number,
    antialias: bool | typing.Literal[0, 1],
    color: _utils.unions.ColorValue,
    background: typing.Optional[_utils.unions.ColorValue] = None,
    line_gap: int = 0,
    tab_size: int = 4,
    alignment: _utils.unions.TextAlignment = 'left',
    method: _utils.unions.WrapMethod = 'word'

) -> pygame.Surface:

    wrapped_lines = wrap_text(font, text, length, tab_size, method)

    if alignment == 'fill':
        if text and len(wrapped_lines) == 1 and ' ' not in wrapped_lines[0]:
            max_width = font.size(text)[0]
        elif text:
            max_width = length
        else:
            max_width = 0
    else:
        max_width = max(font.size(line)[0] for line in wrapped_lines)

    total_height = sum(font.size(line)[1] for line in wrapped_lines) + line_gap * (len(wrapped_lines) - 1)
    surface = pygame.Surface((max_width, total_height), pygame.SRCALPHA)
    offset_y = 0

    if background is not None:
        surface.fill(background)

    for line in wrapped_lines:

        if alignment == 'fill':
            offset_x = 0
            words = line.split(' ')
            total_words_width = sum(font.size(word)[0] for word in words)
            extra_space = length - total_words_width

            if len(words) > 1:
                space_between_words = extra_space / (len(words) - 1)
            else:
                space_between_words = extra_space

            for word in words:
                word_surface = font.render(word, antialias, color)
                surface.blit(word_surface, (offset_x, offset_y))
                offset_x += word_surface.get_width() + space_between_words

        else:
            text_surface = font.render(line, antialias, color)
            text_width = text_surface.get_width()

            match alignment:

                case 'left':
                    surface.blit(text_surface, (0, offset_y))
                case 'center':
                    surface.blit(text_surface, ((max_width - text_width) / 2, offset_y))
                case 'right':
                    surface.blit(text_surface, (max_width - text_width, offset_y))

        offset_y += font.size(line)[1] + line_gap

    return surface

__all__ = [
    'wrap_mono',
    'wrap_word',
    'wrap_text',
    'render_wrap'
]