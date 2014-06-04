#!/usr/bin/env python

# Table container widget.

from gi.repository import Gtk
from Container import Container

class Table(Container):
    expand_children = True
    indent_children = False

    def __init__(self, **descriptor):
        descriptor["orientation"] = Gtk.Orientation.VERTICAL
        Container.__init__(self, **descriptor)

