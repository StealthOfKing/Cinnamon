#!/usr/bin/env python

# App chooser widget. This widget does not use GSettings.

# Internally Gtk.AppChooserButton uses the following model:
#     appinfo, name, label, icon, custom, separator

from gi.repository import Gio, Gtk
from InputWidget import InputWidget

class AppChooserButton(Gtk.AppChooserButton, InputWidget):
    also = False

    def __init__(self, **descriptor):
        Gtk.AppChooserButton.__init__(self, content_type=descriptor.get("content_type", ""))

        if "options" in descriptor:
            # Append the separator only if we have >= 1 apps in the chooser.
            if self.get_app_info():
                self.append_separator()

            options = descriptor["options"]
            for option in sorted(options, key=lambda option:option[1]):
                print option[0]
                self.append_custom_item(option[0], option[1], Gio.ThemedIcon.new(option[2] if len(option) >= 3 else ""))

        InputWidget.__init__(self, **descriptor)

        # Show selected default app at top?
        self.set_show_default_item(descriptor.get("default", True))

        # Custom file dialog?
        if "dialog" in descriptor:
            self.set_show_dialog_item(descriptor["dialog"])
        if "heading" in descriptor:
            self.set_heading(descriptor["heading"])

        if "also" in descriptor:
            self.also = descriptor["also"]
            self.connect("changed", self.on_changed_also)

        if "setting" in descriptor:
            self.changed = self.connect("changed", AppChooserButton.on_changed)

    def _get_value(self):
        current = self.get_model()[self.get_active_iter()]
        return current[1] if current[4] else current[0].get_commandline()
    def _set_value(self, value):
        self.set_active_custom_item(value)

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

