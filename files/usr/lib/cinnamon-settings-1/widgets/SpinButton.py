#!/usr/bin/env python

# Numerical input widget with handles.

from gi.repository import Gtk
from Adjustment import Adjustment
from InputWidget import InputWidget

class SpinButton(InputWidget, Gtk.SpinButton):
    fallback = 0

    def __init__(self, **descriptor):
        Gtk.SpinButton.__init__(self)

        self.configure(
            Adjustment(**descriptor),
            descriptor.get("climb", 0.25),
            descriptor.get("digits", 0)
        )

        InputWidget.__init__(self, **descriptor)

        if "setting" in descriptor:
            self.changed = self.connect('changed', SpinButton.on_changed)

    def _get_value(self):
        return self.get_value()
    def _set_value(self, value):
        self.set_value(value)

