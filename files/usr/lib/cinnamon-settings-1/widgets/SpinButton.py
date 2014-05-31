#!/usr/bin/env python

# Numerical input widget with handles.

from gi.repository import Gtk
from Adjustment import Adjustment
from InputWidget import InputWidget

class SpinButton(InputWidget):
    fallback = 0

    def __init__(self, **descriptor):
        climb = descriptor.get("climb", 0.25)
        digits = descriptor.get("digits", 0)
        InputWidget.__init__(self, Gtk.SpinButton.new(Adjustment(**descriptor), climb, digits), **descriptor)
        if "setting" in descriptor:
            self.changed = self.gtk_widget.connect('changed', self.on_changed)

    def get_value(self):
        return self.gtk_widget.get_value()
    def set_value(self, value):
        self.gtk_widget.set_value(value)

