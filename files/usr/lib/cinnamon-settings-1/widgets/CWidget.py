#!/usr/bin/env python

# Specialised module for loading Gtk widgets written in C.

import capi
from gi.repository import Gtk

c_manager = capi.CManager()

def CWidget(name):
    try:
        widget = c_manager.get_c_widget(name)
        widget.indent = 1
        widget.margin = [0,0,0,0]
        widget.grid_align = False
        return widget
    except Exception, detail:
        print detail            

