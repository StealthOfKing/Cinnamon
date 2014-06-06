#!/usr/bin/env python

# Visual separator (horizontal).

from gi.repository import Gtk
from Widget import Widget

class Separator(Gtk.Separator, Widget):
    def __init__(self, **descriptor):
        Gtk.Separator.__init__(self)

        descriptor["expand"] = [True,False]

        Widget.__init__(self, **descriptor)

