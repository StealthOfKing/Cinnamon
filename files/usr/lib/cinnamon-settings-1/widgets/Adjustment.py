#!/usr/bin/env python

# Adjustment is a helper function for constructing a Gtk.Adjustment from
# a descriptor. The default Adjustment is (0,0,100,1,10).

from gi.repository import Gtk

def Adjustment(**descriptor):
    return Gtk.Adjustment(
        descriptor.get("value", 0),
        descriptor.get("min",   0),
        descriptor.get("max", 100),
        descriptor.get("step",  1),
        descriptor.get("page", 10),
        0
    )
