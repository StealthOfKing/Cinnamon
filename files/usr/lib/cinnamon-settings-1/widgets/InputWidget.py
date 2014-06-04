#!/usr/bin/env python

# InputWidget is an extension of Gtk.Grid that provides a common API for
# all input widgets. It provides prefix, suffix, tooltip and visibility.
# All child Gtk component widgets are stored with the gtk_ prefix.

# The layout of all input widgets follows the pattern:
#
#     InputWidget[ [gtk_prefix] [gtk_widget] [gtk_suffix] ]
#
# where gtk_prefix is usually a Label, widget is the raw Gtk.Widget, and
# gtk_suffix is usually a Label. gtk_prefix and gtk_suffix are optional.

from functools import partial
from gi.repository import GLib, Gtk
from Label import Label
from Widget import Widget
import Settings

# Constants
COLUMN_SPACING = 4
ROW_SPACING = 2

class InputWidget(Widget):
    settings = False
    lock_width = True

    #prefix
    #suffix

    def __init__(self, **descriptor):
        # Fixes some widgets... inparticular ComboBox.
#        descriptor["align"] = descriptor.get("align", [0,0.5])

        # Automatically indent widgets with dependencies.
        if not "indent" in descriptor and "depends" in descriptor:
            self.indent = self.indent + 1

        Widget.__init__(self, **descriptor)

#        self.set_column_spacing(COLUMN_SPACING)
#        self.set_row_spacing(ROW_SPACING)

        # Prefix, typically used for label.
        prefix = descriptor.pop("label", descriptor.pop("prefix", None))
        if prefix != None:
            if type(prefix) == str:
                prefix = Label(markup_with_mnemonic=prefix)
            if prefix.get_mnemonic_keyval():
                prefix.set_mnemonic_widget(self)
            self.prefix = prefix

        # Suffix, typically used for units.
        suffix = descriptor.pop("units", descriptor.pop("suffix", None))
        if suffix != None:
            if type(suffix) == str:
                suffix = Label(markup_with_mnemonic=suffix)
            if suffix.get_mnemonic_keyval():
                suffix.set_mnemonic_widget(self)
            self.suffix = suffix

        # Setting?
        if "setting" in descriptor:
            self.settings, self.key = Settings.parse(descriptor["setting"])
            self.setting_handler = self.settings.connect("changed::"+self.key, self.on_file_changed)

        if "changed" in descriptor:
            self.connect("changed", partial(descriptor["changed"], self))

        # Set the initial value for this widget.
        if "value" in descriptor:
            self._set_value(descriptor["value"])
        elif self.settings:
            variant = self.settings.get_value(self.key)
            self.type = variant.get_type_string()
            self._set_value(variant.unpack())

    def load_value(self):   # Load value from disk.
        try:
            return self.settings.get_value(self.key).unpack()
        except:
            print ("Could not find current value for key '%s' in xlet '%s'" % (self.key, self.settings.schema))
            return self.fallback
    def save_value(self, value):    # Save value to disk.
        try:
            self.settings.set_value(self.key, GLib.Variant(self.type, value))
        except Exception, e:
            print ("Could not set current value for key '%s' in xlet '%s'" % (self.key, self.settings.schema))
            print e

    def on_changed(self):   # Called when the input value changes.
        self.save_value(self._get_value())
    def on_file_changed(self, settings, key):   # Called when the file's value changes.
        self._set_value(self.load_value())

    def set_sensitive(self, flag):
        print "setting sensitivity..."
        if hasattr(self, "prefix"):
            print "setting prefix"
            Gtk.Widget.set_sensitive(self.prefix, flag)
        Gtk.Widget.set_sensitive(self, flag)
        if hasattr(self, "suffix"):
            Gtk.Widget.set_sensitive(self.suffix, flag)

