#!/usr/bin/env python

# Numerical scale interface.

from InputWidget import InputWidget

class Range(InputWidget):
    fallback = 0

    def __init__(self, **descriptor):
        InputWidget.__init__(self, **descriptor)
        if "setting" in descriptor:
            self.changed = self.connect('value-changed', Range.on_changed)

    def _get_value(self):
        return self.get_value()
    def _set_value(self, value):
        self.set_value(value)

