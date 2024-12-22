import random
from enum import Enum
from typing import Self

from pryttier.math import Vector3


class RGB:
    def __init__(self, r, g, b):
        self.rgb = (r, g, b)
        self.r = r
        self.g = g
        self.b = b

    @classmethod
    def random(cls):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return RGB(r, g, b)

    def __repr__(self):
        return f"({self.r}, {self.g}, {self.b})"

    def __mul__(self, other: int | float | Self):
        if isinstance(other, int) or isinstance(other, float):
            return RGB(int(self.r * other), int(self.g * other), int(self.b * other))
        if isinstance(other, RGB):
            return RGB(int(self.r * other.r), int(self.g * other.g), int(self.b * other.b))

    def __truediv__(self, other: int | float | Self):
        if isinstance(other, int) or isinstance(other, float):
            return RGB(int(self.r / other), int(self.g / other), int(self.b / other))
        if isinstance(other, RGB):
            return RGB(int(self.r / other.r), int(self.g / other.g), int(self.b / other.b))

    def complement(self):
        return RGB(255 - self.r, 255 - self.g, 255 - self.b)

    def toVector(self):
        return Vector3(self.r, self.g, self.b)


class AnsiColor:
    def __init__(self, colorCode: int):
        self.code = f"\033[{colorCode}m"

    @property
    def value(self):
        return self.code


class AnsiRGB:
    def __init__(self, rgb: RGB | tuple[int, int, int]):
        if isinstance(rgb, RGB):
            self.code = f"\u001b[38;2;{rgb.r};{rgb.g};{rgb.b}m"
        elif isinstance(rgb, tuple):
            self.code = f"\u001b[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"

    @property
    def value(self):
        return self.code


class AnsiRGB_BG:
    def __init__(self, rgb: RGB | tuple[int, int, int]):
        if isinstance(rgb, RGB):
            self.code = f"\u001b[48;2;{rgb.r};{rgb.g};{rgb.b}m"
        elif isinstance(rgb, tuple):
            self.code = f"\u001b[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m"

    @property
    def value(self):
        return self.code


class AnsiColors(Enum):
    BLACK = AnsiColor(30)
    RED = AnsiColor(31)
    GREEN = AnsiColor(32)
    YELLOW = AnsiColor(33)  # orange on some systems
    BLUE = AnsiColor(34)
    MAGENTA = AnsiColor(35)
    CYAN = AnsiColor(36)
    LIGHT_GRAY = AnsiColor(37)
    DARK_GRAY = AnsiColor(90)
    BRIGHT_RED = AnsiColor(91)
    BRIGHT_GREEN = AnsiColor(92)
    BRIGHT_YELLOW = AnsiColor(93)
    BRIGHT_BLUE = AnsiColor(94)
    BRIGHT_MAGENTA = AnsiColor(95)
    BRIGHT_CYAN = AnsiColor(96)
    WHITE = AnsiColor(97)

    RESET = '\033[0m'  # called to return to standard terminal text color


def coloredText(text: str, color: AnsiColors | AnsiColor | AnsiRGB | AnsiRGB_BG, reset: bool = True) -> str:
    if reset:
        text = color.value + text + AnsiColors.RESET.value
    elif not reset:
        text = color.value + text

    return text
