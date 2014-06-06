#!/usr/bin/env python

# Stack widget.

from gi.repository import Gtk
from Widget import Widget

class Stack(Widget, Gtk.Stack):
    def __init__(self, **descriptor):
        Gtk.Stack.__init__(self)
        Widget.__init__(self, **descriptor)

    def add(self, **widgets):    # Add widgets based on current orientation.
        for name, widget in widgets.iteritems():
            self.add_named(widget, name)
        return self

