#!/usr/bin/env python

# Numerical scale widget.

from gi.repository import Gtk
from Range import Range

class Scale(Range, Gtk.Scale):
    def __init__(self, **descriptor):
        Gtk.Scale.__init__(self)

        Range.__init__(self, **descriptor)

        self.set_orientation(descriptor.get("orientation", Gtk.Orientation.HORIZONTAL))

        self.set_draw_value(descriptor.get("draw_value", False))

        if "has_origin" in descriptor:
            self.set_has_origin(descriptor["has_origin"])

        if "marks" in descriptor:
            marks = descriptor["marks"]
            for i in range(len(marks)):
                self.add_mark(marks[i][0], marks[i][1], str(marks[i][2]))

        # GtkScale has no minimum width by default. Note this fix doesn't
        # take into account the potential for future re-orientation.
        if self.get_orientation() == Gtk.Orientation.HORIZONTAL:
            self.set_size_request(256, -1)
        else:
            self.set_size_request(-1, 256)

        self.set_digits(descriptor.get("digits", 0))

