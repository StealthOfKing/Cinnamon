#!/usr/bin/env python

# Boolean input interface.

from InputWidget import InputWidget

class ToggleButton(InputWidget):
    fallback = False

    def __init__(self, gtk_widget, **descriptor):
        InputWidget.__init__(self, gtk_widget, **descriptor)
        if "setting" in descriptor:
            self.changed = gtk_widget.connect('toggled', self.on_changed)

    def get_value(self):
        return self.gtk_widget.get_active()
    def set_value(self, value):
        self.gtk_widget.set_active(value)

