#!/usr/bin/env python

# Numerical scale widget.

from gi.repository import Gtk
from Adjustment import Adjustment
from Range import Range

class Scale(Range):
    def __init__(self, **descriptor):
        orientation = Gtk.Orientation.HORIZONTAL
        if "orientation" in descriptor:
            orientation = descriptor["orientation"]

        Range.__init__(self, Gtk.Scale.new(orientation, Adjustment(**descriptor)), **descriptor)

        if "draw_value" in descriptor:
            self.gtk_widget.set_draw_value(descriptor["draw_value"])
        if "has_origin" in descriptor:
            self.gtk_widget.set_has_origin(descriptor["has_origin"])

        if "marks" in descriptor:
            marks = descriptor["marks"]
            for i in range(len(marks)):
                self.gtk_widget.add_mark(marks[i][0], marks[i][1], str(marks[i][2]))

        # Not sure if its a Cinnamon theming issue, but GtkScale has no
        # minimum width by default. Note this fix doesn't take into
        # account the potential for future re-orientation.
        if self.gtk_widget.get_orientation() == Gtk.Orientation.HORIZONTAL:
            self.gtk_widget.set_size_request(100, -1)
        else:
            self.gtk_widget.set_size_request(-1, 100)

        digits = 0
        if "digits" in descriptor:
            digits = descriptor["digits"]
        self.gtk_widget.set_digits(digits)

