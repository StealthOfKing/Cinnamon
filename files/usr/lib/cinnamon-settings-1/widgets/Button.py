#!/usr/bin/env python

# Button input widget.

# Despite inheriting InputWidget, Button intentionally does not work
# with Settings (schema/applet/key).

from functools import partial
from gi.repository import Gtk
from InputWidget import InputWidget

class Button(InputWidget):
    def __init__(self, **descriptor):
        button = Gtk.Button()
        if "clicked" in descriptor:
            button.connect("clicked", partial(descriptor["clicked"], self))
            del descriptor["clicked"]

        descriptor["expand"] = [False,False]

        InputWidget.__init__(self, button, **descriptor)

        self.gtk_widget.set_use_underline(True)
        if "text" in descriptor:
            self.gtk_widget.set_label(descriptor["text"])

#   def get_value(self):
#       pass
#   def set_value(self, value):
#       pass

