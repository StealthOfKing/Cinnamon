#!/usr/bin/env python

# Section used to group similar settings under a header.

from gi.repository import Gtk
from Container import Container
from Label import Label

class Section(Container):
    def __init__(self, *args, **descriptor):
        descriptor["orientation"] = descriptor.pop("orientation", Gtk.Orientation.VERTICAL)
        Container.__init__(self, **descriptor)

        self.set_border_width(6)

        if args:
            label = args[0]
            # Watch the pixel margin here... might need changed for theming.
            if type(args[0]) == str:
                label = Label(markup="<b>%s</b>" % label, align=[0,0], indent=0, margin=[0,0,3,3])
            Gtk.Grid.attach(self, label, self.column, self.row, 3, 1)
            self.row = self.row + 1

