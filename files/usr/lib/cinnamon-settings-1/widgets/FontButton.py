#!/usr/bin/env python

# Font chooser input widget.

from gi.repository import Gtk
from InputWidget import InputWidget

class FontButton(InputWidget, Gtk.FontButton):
    fallback = "sans serif"

    def __init__(self, **descriptor):
        Gtk.FontButton.__init__(self)
        InputWidget.__init__(self, **descriptor)
        if "setting" in descriptor:
            self.connect('font-set', FontButton.on_changed)

    def _get_value(self):
        return self.get_font_name()
    def _set_value(self, value):
        self.set_font_name(value)

