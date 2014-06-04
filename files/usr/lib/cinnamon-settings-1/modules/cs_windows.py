#!/usr/bin/env python

import CinnamonSettingsWidgets as CSW

title_bar_click_options = [
    ['toggle-shade',                 _("Toggle Shade")],
    ['toggle-maximize',              _("Toggle Maximize")],
    ['toggle-maximize-horizontally', _("Toggle Maximize Horizontally")],
    ['toggle-maximize-vertically',   _("Toggle Maximize Vertically")],
    ['minimize',                     _("Minimize")],
    ['shade',                        _("Shade")],
    ['menu',                         _("Menu")],
    ['lower',                        _("Lower")],
    ['none',                         _("None")]
]

title_bar_buttons = [
    ("",         ""),
    ("menu",     _("Menu")),
    ("close",    _("Close")),
    ("minimize", _("Minimize")),
    ("maximize", _("Maximize")),
    ("stick",    _("Sticky")),
    ("shade",    _("Shade"))
]

class Module(CSW.Module):
    id = "windows"
    name = _("Windows")
    tooltip = _("Manage window preferences")
    keywords = _("windows, titlebar, edge, switcher, window list, attention, focus")
    icon = "cs-windows"
    category = "prefs"

    def on_module_selected(self):
        self.add(
            CSW.Section(_("Alt-Tab")).add(
                CSW.ComboBox(
                    setting = "org.cinnamon/alttab-switcher-style",
                    label   = _("Alt-Tab switcher style"),
                    options = [
                        ["icons",            _("Icons only")],
                        ["thumbnails",       _("Thumbnails only")],
                        ["icons+thumbnails", _("Icons and thumbnails")],
                        ["icons+preview",    _("Icons and window preview")],
                        ["preview",          _("Window preview (no icons)")],
                        ["coverflow",        _("Coverflow (3D)")],
                        ["timeline",         _("Timeline (3D)")]
                    ]
                ),
                CSW.CheckButton(
                    setting = "org.cinnamon/alttab-switcher-enforce-primary-monitor",
                    label   = _("Display the alt-tab switcher on the primary monitor instead of the active one")
                )
            ),
            CSW.Separator(),
            CSW.Section(_("Title Bar"), lock_widths=2).add(
                TitleBarButtonsOrderSelector(),
                CSW.ComboBox(
                    setting = "org.cinnamon.desktop.wm.preferences/action-double-click-titlebar",
                    label   = _("Action on title bar double-click"),
                    options = title_bar_click_options
                ),
                CSW.ComboBox(
                    setting = "org.cinnamon.desktop.wm.preferences/action-middle-click-titlebar",
                    label   = _("Action on title bar middle-click"),
                    options = title_bar_click_options
                ),
                CSW.ComboBox(
                    setting = "org.cinnamon.desktop.wm.preferences/action-right-click-titlebar",
                    label   = _("Action on title bar right-click"),
                    options = title_bar_click_options
                ),
                CSW.ComboBox(
                    setting = "org.cinnamon.desktop.wm.preferences/action-scroll-titlebar",
                    label   = _("Action on title bar with mouse scroll"),
                    options = [
                        ["none",    _("Nothing")],
                        ["shade",   _("Shade and unshade")],
                        ["opacity", _("Adjust opacity")]
                    ]
                )
            ),
            CSW.Separator(),
            CSW.Section(_("Window List")).add(
                CSW.CheckButton(
                    setting = "org.cinnamon/window-list-applet-alert",
                    label   = _("Show an alert in the window list when a window from another workspace requires attention")
                ),
                CSW.CheckButton(
                    setting = "org.cinnamon/window-list-applet-scroll",
                    label   = _("Enable mouse-wheel scrolling in the window list")
                )        
            ),
            CSW.Separator(),
            CSW.Section(_("Window Focus")).add(
                CSW.ComboBox(
                    setting = "org.cinnamon.desktop.wm.preferences/focus-mode", 
                    label   = _("Window focus mode"),
                    options = [
                        ["click", "Click"],
                        ["sloppy", "Sloppy"],
                        ["mouse",  "Mouse"]
                    ]
                ),
                CSW.CheckButton(
                    setting = "org.cinnamon.desktop.wm.preferences/auto-raise",
                    label   = _("Automatically raise focused windows")
                ),
                CSW.CheckButton(
                    setting = "org.cinnamon/bring-windows-to-current-workspace",
                    label   = _("Bring windows which require attention to the current workspace")
                ),
                CSW.CheckButton(
                    setting = "org.cinnamon/prevent-focus-stealing",
                    label   = _("Prevent focus stealing")
                ),        
                CSW.CheckButton(
                    setting = "org.cinnamon.muffin/attach-modal-dialogs",
                    label   = _("Attach dialog windows to their parent window's title bar")
                )
            ),
            CSW.Separator(),
            CSW.Section(_("Moving and Resizing Windows"), lock_widths=2).add(
                CSW.ComboBox(
                    setting = "org.cinnamon.desktop.wm.preferences/mouse-button-modifier",
                    label   = _("Special key to move windows"),
                    options = [
                        ["",          ""],
                        ["<Alt>",     _("<Alt>")],
                        ["<Super>",   _("<Super>")],
                        ["<Control>", _("<Control>")]
                    ]
                ),
                CSW.SpinButton(
                    label   = _("Window drag/resize threshold"),
                    setting = "org.cinnamon.muffin/resize-threshold",
                    min=1, max=100, step=1, page=10, units = _("pixels")
                )
            )
        )

import sys
sys.path.append('../widgets')
from gi.repository import Gtk
from InputWidget import InputWidget

class TitleBarButtonsOrderSelector(Gtk.Grid, InputWidget):
    fallback = ""
    lock_width = False

    def __init__(self, **descriptor):
        descriptor["setting"] = "org.cinnamon.muffin/button-layout"

        self.widgets = [[],[]]
        for i in range(2):
            widgets = self.widgets[i]
            for j in range(4):
                widget = CSW.ComboBox(options=title_bar_buttons)
                widgets.append(widget)

        Gtk.Grid.__init__(self)
        InputWidget.__init__(self, **descriptor)

        self.attach(CSW.Label(label=_("Left side title bar buttons" )), 0, 0, 1, 1)
        self.attach(CSW.Label(label=_("Right side title bar buttons")), 0, 1, 1, 1)

        for i in range(2):
            widgets = self.widgets[i]
            for j in range(4):
                self.attach(widgets[j], j+1, i, 1, 1)
                widgets[j].connect("changed", self.on_changed)

    def _get_value(self):
        return ','.join(widget._get_value() for widget in self.widgets[0]) + ':' + ','.join(widget._get_value() for widget in self.widgets[1])
    def _set_value(self, value):
        split = value.split(':')
        if not len(split):
            split = ["",""]
        for i in range(2):
            items = split[i]
            items = items.split(',') if len(items) > 0 else []
            widgets = self.widgets[i]
            for j in range(4):
                widgets[j]._set_value(items[j] if j < len(items) else "")
