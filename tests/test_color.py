"""Tests for color module."""

from collections import namedtuple
from random import uniform

from pytest import approx, raises

from plateypus import color

InpExp = namedtuple("InpExp", ["input", "expected"])


def approx_rgba(rgba1, rgba2):
    """Assert that two RGBA values are approximately equal,
    allowing for floating point imprecisions."""
    assert isinstance(rgba1, color.RGBA)
    assert isinstance(rgba2, color.RGBA)
    assert approx(rgba1.red, rgba2.red)
    assert approx(rgba1.green, rgba2.green)
    assert approx(rgba1.blue, rgba2.blue)
    assert approx(rgba1.alpha, rgba2.alpha)
    return True


def test_rgba():
    """Test that RGBA is a namedtuple with relevant properties."""
    red = uniform(0, 1)
    green = uniform(0, 1)
    blue = uniform(0, 1)
    alpha = uniform(0, 1)
    rgba = color.RGBA(red, green, blue, alpha)
    assert rgba.red == red
    assert rgba.green == green
    assert rgba.blue == blue
    assert rgba.alpha == alpha


def test_f2hex():
    """Test that f2hex correctly converts float values to hex strings."""
    inp_exps = [
        InpExp(0, "00"),
        InpExp(0.1, "1A"),
        InpExp(0.25, "40"),
        InpExp(0.5, "80"),
        InpExp(2 / 3, "AA"),
        InpExp(1, "FF"),
    ]
    for inp_exp in inp_exps:
        assert color.f2hex(inp_exp.input) == inp_exp.expected


def test_f2hex_errors():
    """Test that f2hex raises errors on invalid input."""
    with raises(ValueError):
        color.f2hex(-1)
    with raises(ValueError):
        color.f2hex(2)
    with raises(TypeError):
        color.f2hex("foo")


def test_hex2f():
    """Test that hex2f correctly converts hex strings to floats."""
    inp_exps = [
        InpExp("00", 0),
        InpExp("1A", 0.1),
        InpExp("40", 0.25),
        InpExp("80", 0.5),
        InpExp("AA", 2 / 3),
        InpExp("FF", 1),
    ]
    for inp_exp in inp_exps:
        assert approx(color.hex2f(inp_exp.input), inp_exp.expected)


def test_hex2rgba():
    """Test that hex2rgba correctly converts hex strings to RGBA instances."""
    inp_exps = [
        InpExp("#000000", color.RGBA(0, 0, 0, 1)),
        InpExp("#00000000", color.RGBA(0, 0, 0, 0)),
        InpExp("#40FFAA80", color.RGBA(0.25, 1, 2 / 3, 0.5)),
    ]
    for inp_exp in inp_exps:
        assert approx_rgba(color.hex2rgba(inp_exp.input), inp_exp.expected)


def test_hex2rgba_errors():
    """Test that hex2rgba raises errors on invalid input."""
    with raises(ValueError):
        color.hex2rgba("")
    with raises(ValueError):
        color.hex2rgba("ABCDEF")
    with raises(TypeError):
        color.hex2rgba(42)


def test_color_class_init():
    """Test that Color instances are properly initialized."""
    inp_exps = [
        InpExp(color.Color(), color.RGBA(red=0, green=0, blue=0, alpha=0)),
        InpExp(color.Color("#000000"), color.RGBA(red=0, green=0, blue=0, alpha=1)),
        InpExp(color.Color("#40FFAA80"), color.RGBA(0.25, 1, 2 / 3, 0.5)),
    ]
    for inp_exp in inp_exps:
        assert approx_rgba(inp_exp.input.rgba, inp_exp.expected)


def test_color_class_hex():
    """Test that Color instances return correct hex strings."""
    inp_exps = [
        InpExp(color.Color(), "#00000000"),
        InpExp(color.Color("#000000"), "#000000FF"),
        InpExp(color.Color("#40FFAA80"), "#40FFAA80"),
    ]
    for inp_exp in inp_exps:
        assert inp_exp.input.hex == inp_exp.expected


def test_color_class_kivy_color():
    """Test that Color instances return correct list properties."""
    inp_exps = [
        InpExp(color.Color(), [0,0,0,0]),
        InpExp(color.Color("#000000"), [0,0,0,1]),
        InpExp(color.Color("#40FFAA80"), [0.25,1,2/3,0.5]),
    ]
    for inp_exp in inp_exps:
        assert approx(inp_exp.input.kivy_color, inp_exp.expected)
