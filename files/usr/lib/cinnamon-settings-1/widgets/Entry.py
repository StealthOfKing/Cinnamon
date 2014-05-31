#!/usr/bin/env python

# String input widget.

from gi.repository import Gtk
from InputWidget import InputWidget

class Entry(InputWidget):
    fallback = ""

    def __init__(self, **descriptor):
        InputWidget.__init__(self, Gtk.Entry(), **descriptor)
        if "setting" in descriptor:
            self.changed = self.gtk_widget.connect('changed', self.on_changed)

    def get_value(self):
        return self.gtk_widget.get_text()
    def set_value(self, value):
        self.gtk_widget.set_text(value)

