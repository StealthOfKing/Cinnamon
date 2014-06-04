#!/usr/bin/env python

# Boolean input widget.

from gi.repository import Gtk
from ToggleButton import ToggleButton

class CheckButton(Gtk.CheckButton, ToggleButton):
    lock_width = False

    def __init__(self, **descriptor):
        if "label" in descriptor:   # Label position is reversed.
            descriptor["suffix"] = descriptor["label"]
            del descriptor["label"]
        Gtk.CheckButton.__init__(self)
        ToggleButton.__init__(self, **descriptor)

