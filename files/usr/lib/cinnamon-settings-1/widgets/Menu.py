#!/usr/bin/env python

# Popup menu widget.

from gi.repository import Gio, Gtk
from Widget import Widget

class MenuItem(Gtk.MenuItem):
    def __init__(self, **descriptor):
        Gtk.MenuItem.__init__(self)

        if "image" in descriptor:
            # Force 48px image size.
            file = Gio.File.new_for_path(descriptor["image"])
            file_icon = Gio.FileIcon(file=file)
            self.gtk_image = Gtk.Image.new_from_gicon(file_icon, Gtk.IconSize.DIALOG)            
            self.add(self.gtk_image)

        if "text" in descriptor:
            self.set_label(descriptor["text"])

class Menu(Gtk.Menu, Widget):
    row = 0 # Current row number.

    def __init__(self, **descriptor):
        Gtk.Menu.__init__(self)
        Widget.__init__(self, **descriptor)

    def add(self, *widgets, **descriptor):    # Add widgets based on current orientation.
        columns = descriptor.get("columns", 1)
        width = descriptor.get("width", 1)
        column = 0
        row = self.row
        for widget in widgets:
            self.attach(MenuItem(**widget), column, column+width, row, row+1)
            column = (column + width) % columns
            if (column == 0):
                row = row + 1
        self.row = row + 1
        return self

