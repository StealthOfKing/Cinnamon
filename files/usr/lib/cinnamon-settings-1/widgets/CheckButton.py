#!/usr/bin/env python

# Boolean input widget.

from gi.repository import Gtk
from ToggleButton import ToggleButton

class CheckButton(ToggleButton):
    lock_width = False

    def __init__(self, **descriptor):
        if "label" in descriptor:
            descriptor["suffix"] = descriptor["label"]
            del descriptor["label"]
        ToggleButton.__init__(self, Gtk.CheckButton(), **descriptor)

