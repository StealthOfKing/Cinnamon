#!/usr/bin/env python

# CinnamonWidgets.py is an attempt to establish a common API between the
# two main types of settings (XletSettingsWidgets.py used for applets
# and SettingsWidgets.py for system configuration).
#
# Widget components are handled by the Gtk framework internally.
#
# As part of a flexible framework, each type of widget accepts a varying
# and optional list of named parameters:
#
#     applet       - applet settings path
#     key          - applet or schema key identifier
#     prefix/label - leading text, used for description
#     schema       - GSettings schema path
#     show         - show or hide the widget
#     suffix/units - trailing text, used for units
#     tooltip      - mouseover text, used for detailed description
#     value        - the initial value
#
# The key value (in combination with applet or schema) defines a local
# user setting (via JSON or GSettings respectively) to bind with the
# user input.
#
# Widget expects all descendants to define the following methods:
#
#     get_value(self) - returns the widget's current value
#     set_value(self) - sets the widget's current value
#
# Each class must inform Settings of its base data type and default
# value via the static variables type and default.

try:
    import sys
    sys.path.append('./bin')
    sys.path.append('./widgets')

    # Populate CSW namespace with all widgets.
    from AppChooserButton import AppChooserButton
    from Background import Background
    from Box import Box
    from Button import Button
    from Category import Category
    from CheckButton import CheckButton
    from ComboBox import ComboBox
    from CWidget import CWidget
    from Entry import Entry
    from FontButton import FontButton
    from HBox import HBox
    from Label import Label
    from MediaAppChooserButton import MediaAppChooserButton
    from Menu import Menu
    from Scale import Scale
    from Section import Section
    from Separator import Separator
    import Settings
    from SpinButton import SpinButton
    from Stack import Stack
    from Table import Table
    from VBox import VBox
except Exception, e:
    print e

# Extra CSS provider.
from gi.repository import Gdk, Gtk
css_provider = Gtk.CssProvider()
css_provider.load_from_path("./CinnamonSettingsWidgets.css")
Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

# Module provides the base interface for all settings modules to inherit.
class Module:
    loaded      = False # Controlled internally, always False by default.
    stand_alone = False

    def add_widget(self, widget):
        self.widgets.append(widget)

    def add(self, *widgets):
        for widget in widgets:
            self.gtk_grid.add(widget)
