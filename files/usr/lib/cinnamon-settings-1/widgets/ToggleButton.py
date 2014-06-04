#!/usr/bin/env python

# Boolean input interface.

from InputWidget import InputWidget

class ToggleButton(InputWidget):
    fallback = False

    def __init__(self, **descriptor):
        InputWidget.__init__(self, **descriptor)
        if "setting" in descriptor:
            self.changed = self.connect('toggled', ToggleButton.on_changed)

    def _get_value(self):
        return self.get_active()
    def _set_value(self, value):
        self.set_active(value)

