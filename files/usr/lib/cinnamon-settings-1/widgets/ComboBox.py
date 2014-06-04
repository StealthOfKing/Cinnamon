#!/usr/bin/env python

# A multiple choice popup menu.

from gi.repository import Gtk
from InputWidget import InputWidget

# Load icon theme.
icon_theme = Gtk.IconTheme.get_default()

class ComboBox(Gtk.ComboBox, InputWidget):
    icons = False

    def __init__(self, **descriptor):
        Gtk.ComboBox.__init__(self)

        options = descriptor.get("options", False)
        # Derive model type from first option's value.
        value_type = type(options[0][0]) if options else str
        if descriptor.get("icons", False):  # value/label/icon
            self.icons = True
            model = Gtk.ListStore(value_type, str, GdkPixbuf.Pixbuf)
        else:   # value/label
            model = Gtk.ListStore(value_type, str)

        if "alphabetical" in descriptor and descriptor["alphabetical"]: # Sort by label column.
            model.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        self.set_model(model)

        if options:
            self.add_options(options)

        InputWidget.__init__(self, **descriptor)

        renderer = Gtk.CellRendererText()
        self.pack_start(renderer, True)
        self.add_attribute(renderer, "text", 1)

        if self.icons:
            renderer = Gtk.CellRendererPixbuf()
            self.pack_start(renderer, False)
            self.add_attribute(renderer, "pixbuf", 2)

        if "setting" in descriptor:
            self.changed = self.connect('changed', ComboBox.on_changed)
        elif "index" in descriptor:
            self.set_active(descriptor["index"])

    def add_options(self, options):
        model = self.get_model()
        icons = self.icons
        for option in options:
            if icons:
                model.append([
                    option[0],
                    option[1] if len(option) >= 1 else option[0],
                    icon_theme.choose_icon(option[2] if len(option) >= 2 else "")
                ])
            else:
                model.append([
                    option[0],
                    option[1] if len(option) >= 1 else option[0]
                ])

    def _get_value(self):
        return self.get_model()[self.get_active_iter()][0]
    def _set_value(self, value):
        model = self.get_model()
        for index in range(len(model)):
            option = model[index]
            if value == option[0]:
                self.set_active(index)
                return

