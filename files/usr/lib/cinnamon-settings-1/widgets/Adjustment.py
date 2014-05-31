#!/usr/bin/env python

# Adjustment is a helper function for constructing a Gtk.Adjustment from
# a descriptor. The default Adjustment is (0,0,100,1,10).

from gi.repository import Gtk

def Adjustment(**descriptor):
    value = 0
    if "value" in descriptor:
        value = descriptor["value"]
    min = 0
    if "min" in descriptor:
        min = descriptor["min"]
    max = 100
    if "max" in descriptor:
        max = descriptor["max"]
    step = 1
    if "step" in descriptor:
        step = descriptor["step"]
    page = 10
    if "page" in descriptor:
        page = descriptor["page"]
    return Gtk.Adjustment(value, min, max, step, page, 0)
