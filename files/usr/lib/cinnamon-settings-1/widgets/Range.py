#!/usr/bin/env python

# Numerical scale interface.

from InputWidget import InputWidget

class Range(InputWidget):
    fallback = 0

    def __init__(self, gtk_widget, **descriptor):
        InputWidget.__init__(self, gtk_widget, **descriptor)
        if "setting" in descriptor:
            self.changed = self.gtk_widget.connect('value-changed', self.on_changed)

    def get_value(self):
        return self.gtk_widget.get_value()
    def set_value(self, value):
        self.gtk_widget.set_value(value)

