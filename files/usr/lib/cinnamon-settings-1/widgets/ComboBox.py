#!/usr/bin/env python

# A multiple choice popup menu.

from gi.repository import Gtk
from InputWidget import InputWidget

# Load icon theme.
icon_theme = Gtk.IconTheme.get_default()

class ComboBox(InputWidget):
    icons = False

    def __init__(self, **descriptor):
        options = descriptor.get("options", False)
        # Derive model type from first option's value.
        value_type = type(options[0][0]) if options else str
        if descriptor.get("icons", False):  # value/label/icon
            self.icons = True
            model = Gtk.ListStore(value_type, str, GdkPixbuf.Pixbuf)
        else:   # value/label
            model = Gtk.ListStore(value_type, str)
        self.model = model

        if "alphabetical" in descriptor and descriptor["alphabetical"]: # Sort by label column.
            model.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        if options:
            self.add_options(options)

        combo_box = Gtk.ComboBox.new_with_model(model)
        InputWidget.__init__(self, combo_box, **descriptor)

        renderer = Gtk.CellRendererText()
        combo_box.pack_start(renderer, True)
        combo_box.add_attribute(renderer, "text", 1)

        if self.icons:
            renderer = Gtk.CellRendererPixbuf()
            combo_box.pack_start(renderer, False)
            combo_box.add_attribute(renderer, "pixbuf", 2)

        if "setting" in descriptor:
            self.changed = combo_box.connect('changed', self.on_changed)
        elif "index" in descriptor:
            combo_box.set_active(descriptor["index"])

    def add_options(self, options):
        model = self.model
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

    def get_value(self):
        return self.model[self.gtk_widget.get_active_iter()][0]
    def set_value(self, value):
        model = self.model
        for index in range(len(model)):
            option = model[index]
            if value == option[0]:
                self.gtk_widget.set_active(index)
                return

