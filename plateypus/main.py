"""This is the Plateypus app."""

from os.path import abspath

from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.label import Label
from packaging.version import Version

from plateypus.color import Color

COLORS = dict()
INI_SECTION = "colorscheme"
COLOR_DARKEST = "darkest"
COLOR_DARKER = "darker"
COLOR_MEDIUM = "medium"
COLOR_LIGHTER = "lighter"
COLOR_LIGHTEST = "lightest"
VERSION = Version("0.0.1")


def set_colors(cfg):
    COLORS[COLOR_DARKEST] = Color(cfg.get(INI_SECTION, COLOR_DARKEST))
    COLORS[COLOR_DARKER] = Color(cfg.get(INI_SECTION, COLOR_DARKER))
    COLORS[COLOR_MEDIUM] = Color(cfg.get(INI_SECTION, COLOR_MEDIUM))
    COLORS[COLOR_LIGHTER] = Color(cfg.get(INI_SECTION, COLOR_LIGHTER))
    COLORS[COLOR_LIGHTEST] = Color(cfg.get(INI_SECTION, COLOR_LIGHTEST))


class PlateypusApp(App):
    def build(self):
        set_colors(self.config)
        Window.clearcolor = COLORS[COLOR_DARKER].kivy_color
        splash = Label(
            text=f"[color={COLORS[COLOR_LIGHTEST].hex}][b]Plateypus[/b][/color]\n{VERSION}\n{abspath('.')}",
            markup=True,
        )
        return splash

    def build_config(self, config):
        config.setdefaults(
            INI_SECTION,
            {
                COLOR_DARKEST: "#212922",
                COLOR_DARKER: "#294936",
                COLOR_MEDIUM: "#3E6259",
                COLOR_LIGHTER: "#5B8266",
                COLOR_LIGHTEST: "#C9F8D9",
            },
        )


if __name__ == "__main__":
    PlateypusApp().run()
