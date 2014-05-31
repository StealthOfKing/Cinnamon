#!/usr/bin/env python

# Horizontal scale widget.

from gi.repository import Gtk
from Scale import Scale

class HScale(Scale):
    def __init__(self, **descriptor):
        descriptor["orientation"] = Gtk.Orientation.HORIZONTAL
        Scale.__init__(self, **descriptor)

