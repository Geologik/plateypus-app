"""Test the Plateypus app."""

from functools import partial

from kivy.clock import Clock

from plateypus import main


def stop_kivy(app, *args):
    """Stop Kivy application.

    See https://github.com/KeyWeeUsr/KivyUnitTest#writing-unit-test-for-kivy-application
    """
    app.stop()


def test_tautology():
    """This test canary always passes."""
    assert 2 + 2 == 4


def test_app_build():
    """Verify that the app can be built and started."""
    app = main.PlateypusApp()
    Clock.schedule_once(partial(stop_kivy, app), 0.000001)
    app.run()
