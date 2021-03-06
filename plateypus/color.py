"""Colorscheme implementation for use instead of magic strings."""

from collections import namedtuple

RGBA = namedtuple("RGBA", ["red", "green", "blue", "alpha"])


def f2hex(flo):
    """Convert floating point value `flo` (`0 <= f <=1`) to a zero-padded hex string."""
    if not 0 <= flo <= 1:
        raise ValueError("value must be between 0 and 1 (inclusive)", flo)
    intval = round(255 * flo)
    return f"{intval:X}".zfill(2)


def hex2f(hexval):
    """Convert zero-padded hex string value to float."""
    return int(hexval, 16) / 255


def hex2rgba(hexval):
    """Convert HTML-style hex color string to RGBA tuple."""
    hexlen = len(hexval)
    if not hexlen in (7, 9) or hexval[0] != "#":
        raise ValueError("value must be an HTML-style color code (#rrggbb[aa])", hexval)
    red = hex2f(hexval[1:3])
    green = hex2f(hexval[3:5])
    blue = hex2f(hexval[5:7])
    alpha = hex2f(hexval[7:9]) if hexlen == 9 else 1
    return RGBA(red=red, blue=blue, green=green, alpha=alpha)


class Color:
    """Class representing a color with convenience methods."""

    def __init__(self, hexval="#00000000"):
        self.rgba = hex2rgba(hexval)

    def __eq__(self, other):
        """Test equality for two colors by comparing their hex value."""
        if isinstance(other, Color):
            return self.hex == other.hex
        return False

    @property
    def hex(self):
        """Color expressed as HTML-style hex string."""
        return (
            f"#{f2hex(self.rgba.red)}{f2hex(self.rgba.green)}{f2hex(self.rgba.blue)}"
            f"{f2hex(self.rgba.alpha)}"
        )

    @property
    def kv_color(self):
        """Color expressed as a list appropriate for use with Kivy."""
        return [self.rgba.red, self.rgba.green, self.rgba.blue, self.rgba.alpha]


class AppColors:
    """The actual colors used in the app."""

    # The class properties need to be pre-declared in order to be usable
    # in the .kv files, which are built before `init()` can be called.
    darkest = darker = medium = lighter = lightest = Color()

    @staticmethod
    def init(cfg):
        """Initialize the colors as class properties."""
        sect = "COLORSCHEME"
        AppColors.darkest = Color(cfg.get(sect, "darkest"))
        AppColors.darker = Color(cfg.get(sect, "darker"))
        AppColors.medium = Color(cfg.get(sect, "medium"))
        AppColors.lighter = Color(cfg.get(sect, "lighter"))
        AppColors.lightest = Color(cfg.get(sect, "lightest"))
