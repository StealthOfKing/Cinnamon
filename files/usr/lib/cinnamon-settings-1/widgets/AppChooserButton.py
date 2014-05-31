#!/usr/bin/env python

# App chooser widget. This widget does not use GSettings.

# Internally Gtk.AppChooserButton uses the following model:
#     appinfo, name, label, icon, custom, separator

from gi.repository import Gio, Gtk
from InputWidget import InputWidget

class AppChooserButton(InputWidget):
    also = False

    def __init__(self, **descriptor):
        chooser = Gtk.AppChooserButton(content_type=descriptor.get("content_type", ""))
        self.model = chooser.get_model()

        # Show selected default app at top?
        chooser.set_show_default_item(descriptor.get("default", True))

        if "options" in descriptor:
            options = descriptor["options"]
            for option in sorted(options, key=lambda option:option[1]):
                chooser.append_custom_item(option[0], option[1], Gio.ThemedIcon.new(option[2] if len(option) >= 3 else ""))

        # Custom file dialog?
        if "dialog" in descriptor:
            chooser.set_show_dialog_item(descriptor["dialog"])
        if "heading" in descriptor:
            chooser.set_heading(descriptor["heading"])

        InputWidget.__init__(self, chooser, **descriptor)

        if "also" in descriptor:
            self.also = descriptor["also"]
            chooser.connect("changed", self.on_changed_also)

        if "setting" in descriptor:
            self.changed = chooser.connect("changed", self.on_changed)

    def get_value(self):
        current = self.model[self.gtk_widget.get_active_iter()]
        return current[1] if current[4] else current[0].get_commandline()
    def set_value(self, value):
        self.gtk_widget.set_active_custom_item(value)

    def on_changed_also(self, gtk_button):
        info = gtk_button.get_app_info()
        if info and self.also:  # This default app applies to other types.
            also = self.also
            types = info.get_supported_types()
            for other in also:  # Partial match supported types vs target types.
                for i, t in enumerate(types):
                    if other in t:
                        del types[i]    # Remove to reduce future search complexity.
                        if not info.set_as_default_for_type(t):
                            print "Failed to set '%s' as the default application for '%s'" % (info.get_name(), t)

