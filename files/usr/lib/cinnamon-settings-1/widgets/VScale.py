#!/usr/bin/env python

# Vertical scale widget.

from gi.repository import Gtk
from Scale import Scale

class CinnamonVScale(CinnamonScale):
    def __init__(self, **descriptor):
        descriptor["orientation"] = Gtk.Orientation.VERTICAL
        CinnamonScale.__init__(self, **descriptor)

