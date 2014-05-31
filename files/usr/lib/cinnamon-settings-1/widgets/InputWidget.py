#!/usr/bin/env python

# InputWidget is an extension of Gtk.Box that provides a common API for
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

class InputWidget(Gtk.Grid, Widget):
    settings = False
    lock_width = True
    column = 0
    row = 0

    #gtk_prefix
    #gtk_widget
    #gtk_suffix

    def __init__(self, gtk_widget, **descriptor):
        descriptor["align"] = descriptor.get("align", [0,0.5])

        # Automatically indent widgets with dependencies.
        if not "indent" in descriptor and "depends" in descriptor:
            self.indent = self.indent + 1

        Gtk.Grid.__init__(self)
        Widget.__init__(self, **descriptor)

        self.set_column_spacing(COLUMN_SPACING)
        self.set_row_spacing(ROW_SPACING)

        components = []

        # Prefix, typically used for label.
        gtk_prefix = descriptor.pop("label", descriptor.pop("prefix", None))
        if gtk_prefix != None:
            if type(gtk_prefix) == str:
                gtk_prefix = Label(markup_with_mnemonic=gtk_prefix)
            if gtk_prefix.get_mnemonic_keyval() and gtk_widget:
                gtk_prefix.set_mnemonic_widget(gtk_widget)
            self.attach(gtk_prefix, 0, self.row, 1, 1)
            self.gtk_prefix = gtk_prefix
            components.append(gtk_prefix)
        elif self.lock_width:   # A placeholder... the other option is to
            # recode the way containers add widgets and lock column widths.
            gtk_prefix = Gtk.Box()
            self.attach(gtk_prefix, 0, self.row, 1, 1)
            self.gtk_prefix = gtk_prefix
            components.append(gtk_prefix)

        # Add the widget inbetween prefix and suffix.
        if gtk_widget:
            self.gtk_widget = gtk_widget
            gtk_widget.set_valign(Gtk.Align.CENTER)
            self.attach(gtk_widget, 1, self.row, 1, 1)
            components.append(gtk_widget)

        # Suffix, typically used for units.
        gtk_suffix = descriptor.pop("units", descriptor.pop("suffix", None))
        if gtk_suffix != None:
            if type(gtk_suffix) == str:
                gtk_suffix = Label(markup_with_mnemonic=gtk_suffix)
            if gtk_suffix.get_mnemonic_keyval() and gtk_widget:
                gtk_suffix.set_mnemonic_widget(gtk_widget)
            self.attach(gtk_suffix, 2, self.row, 1, 1)
            self.gtk_suffix = gtk_suffix
            components.append(gtk_suffix)

        # Tooltip attached to full widget.
        if "tooltip" in descriptor:
            self.set_tooltip_text(descriptor["tooltip"])

        # Visibility, show unless specified otherwise.
        if "show" in descriptor and not descriptor["show"]:
            self.hide()
        else:
            self.show()

        # Setting?
        if "setting" in descriptor:
            self.settings, self.key = Settings.parse(descriptor["setting"])
            self.setting_handler = self.settings.connect("changed::"+self.key, self.on_file_changed)

        if "changed" in descriptor:
            gtk_widget.connect("changed", partial(descriptor["changed"], self))

        # Set the initial value for this widget.
        if "value" in descriptor:
            self.set_value(descriptor["value"])
        elif self.settings:
            variant = self.settings.get_value(self.key)
            self.type = variant.get_type_string()
            self.set_value(variant.unpack())

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

    def on_changed(self, gtk_widget):   # Called when the input value changes.
        self.save_value(self.get_value())
    def on_file_changed(self, settings, key):   # Called when the file's value changes.
        self.set_value(self.load_value())
