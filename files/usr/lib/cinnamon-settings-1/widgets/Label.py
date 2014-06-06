#!/usr/bin/env python

# Gtk.Label wrapper with shorthand for markup and fix for alignment.

from gi.repository import Gtk
from Widget import Widget

class Label(Widget, Gtk.Label):
    grid_align = False

    def __init__(self, *args, **descriptor):
        Gtk.Label.__init__(self)

        descriptor["align" ] = descriptor.get("align" , [0,-1])
        descriptor["expand"] = descriptor.get("expand", [False,False])

        Widget.__init__(self, **descriptor)

        if "label" in descriptor:
            self.set_label(descriptor["label"])
        elif "markup" in descriptor:
            self.set_markup(descriptor["markup"])
        elif "mnemonic" in descriptor:
            self.set_text_with_mnemonic(descriptor["mnemonic"])
        elif "markup_with_mnemonic" in descriptor:
            self.set_markup_with_mnemonic(descriptor["markup_with_mnemonic"])

