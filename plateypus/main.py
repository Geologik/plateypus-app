"""This is the Plateypus app."""

from os.path import abspath

from kivy.app import App
from kivy.core.window import Window
from kivy.garden.iconfonts import register as register_iconfont
from kivy.properties import StringProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from packaging.version import Version

from plateypus.color import AppColors

VERSION = Version("0.0.1")


class FieldDropDown(DropDown):
    """Dropdown containing possible fields to search."""

    pass


class Plateypus(GridLayout):
    """Root layout."""

    query = StringProperty()
    field = StringProperty("plate")

    def do_add_query_field(self):
        """Add another query field row."""
        raise NotImplementedError

    def do_search(self):
        """Execute a search."""
        raise NotImplementedError


class PlateypusApp(App):
    """The main application class."""

    def build(self):
        register_iconfont(
            "default_font", "assets/fa-v5.8.2-solid-900.ttf", "assets/fontawesome.fontd"
        )
        AppColors.init(self.config)
        Window.clearcolor = AppColors.darker.kv_color
        return Plateypus()

    def build_config(self, config):
        config.setdefaults("BACKEND", dict(url="http://127.0.0.1:5000"))
        config.setdefaults(
            "COLORSCHEME",
            dict(
                darkest="#212922",
                darker="#294936",
                medium="#3E6259",
                lighter="#5B8266",
                lightest="#C9F8D9",
            ),
        )


if __name__ == "__main__":  # pragma: no cover
    PlateypusApp().run()
