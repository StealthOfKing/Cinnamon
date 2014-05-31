#!/usr/bin/env python

# Vertical container widget.

from gi.repository import Gtk
from Box import Box

class VBox(Box):
    def __init__(self, **descriptor):
        descriptor["orientation"] = Gtk.Orientation.VERTICAL
        Box.__init__(self, **descriptor)
