#!/usr/bin/env python

# Boolean input widget.

from gi.repository import Gtk
from ToggleButton import ToggleButton

class CheckButton(ToggleButton, Gtk.CheckButton):
    grid_align = False

    def __init__(self, **descriptor):
        Gtk.CheckButton.__init__(self)

        if "label" in descriptor:   # Label position is reversed.
            descriptor["suffix"] = descriptor.pop("label")

        ToggleButton.__init__(self, **descriptor)

        if hasattr(self, "suffix"):
            event_box = Gtk.EventBox()
            event_box.add(self.suffix)
            self.suffix = event_box
            event_box.connect("button-press-event", self.on_button_press_event_label)

    def on_button_press_event_label(self, label, event):
        if event.button == 1:
            self._set_value(not self._get_value())

