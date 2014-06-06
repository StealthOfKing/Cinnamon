#!/usr/bin/env python

# String input widget.

from gi.repository import Gtk
from InputWidget import InputWidget

class Entry(InputWidget, Gtk.Entry):
    fallback = ""

    def __init__(self, **descriptor):
        Gtk.Entry.__init__(self)
        InputWidget.__init__(self, **descriptor)
        if "setting" in descriptor:
            self.changed = self.connect('changed', self.on_changed)

    def _get_value(self):
        return self.get_text()
    def _set_value(self, value):
        self.set_text(value)

