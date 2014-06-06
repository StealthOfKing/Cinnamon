#!/usr/bin/env python

# Scrollable container with some styling.

# Used for all settings modules with only one page (no tabs).

from gi.repository import Gtk

class Background(Gtk.Viewport):
    def __init__(self):
        Gtk.Viewport.__init__(self)
        self.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        style = self.get_style_context()
        style.add_class("section-bg")

