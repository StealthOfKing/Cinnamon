#!/usr/bin/env python

# Horizontal container widget.

from gi.repository import Gtk
from Box import Box

class HBox(Box):
    def __init__(self, **descriptor):
        descriptor["orientation"] = Gtk.Orientation.HORIZONTAL
        Box.__init__(self, **descriptor)

