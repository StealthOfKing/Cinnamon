#!/usr/bin/env python

# Affix is a helper function for constructing Widget's prefix and suffix
# components.

from gi.repository import Gtk

def Affix(value):
    label = Gtk.Label()
    label.set_use_markup(True)
    label.set_markup(value)
    return label
