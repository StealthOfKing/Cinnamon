#!/usr/bin/env python

# Font chooser input widget.

from gi.repository import Gtk
from InputWidget import InputWidget

class FontButton(InputWidget):
    fallback = "sans serif"

    def __init__(self, **descriptor):
        InputWidget.__init__(self, Gtk.FontButton(), **descriptor)
        if "setting" in descriptor:
            self.gtk_widget.connect('font-set', self.on_changed)

    def _get_value(self):
        return self.gtk_widget.get_font_name()
    def _set_value(self, value):
        self.gtk_widget.set_font_name(value)
