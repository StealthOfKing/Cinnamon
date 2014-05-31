#!/usr/bin/env python

import CinnamonSettingsWidgets as CSW
from gi.repository import Gio

class Module(CSW.Module):
    id = "desktop"
    name = _("Desktop")
    tooltip = _("Manage your desktop icons")
    keywords = _("desktop, home, button, trash")
    icon = "cs-desktop"
    category = "prefs"

    def load_check(self):
        return 'org.nemo' in Gio.Settings.list_schemas()

    def on_module_selected(self):
        nemo_desktop_schema = CSW.Settings.get_settings("org.nemo.desktop")
        nemo_desktop_keys = nemo_desktop_schema.list_keys()

        section = CSW.Section(_("Desktop Icons")).add(
            CSW.Label(
                markup="<i><small>%s</small></i>" % _("Select the items you want to see on the desktop:"),
                classes=["dim-label"]
            )
        )
        if "computer-icon-visible" in nemo_desktop_keys:
            section.add(CSW.CheckButton(
                setting = "org.nemo.desktop/computer-icon-visible",
                label   = _("Computer")
            ))
        if "home-icon-visible" in nemo_desktop_keys:
            section.add(CSW.CheckButton(
                setting = "org.nemo.desktop/home-icon-visible",
                label   = _("Home")
            ))
        if "trash-icon-visible" in nemo_desktop_keys:
            section.add(CSW.CheckButton(
                setting = "org.nemo.desktop/trash-icon-visible",
                label   = _("Trash")
            ))
        if "volumes-visible" in nemo_desktop_keys:
            section.add(CSW.CheckButton(
                setting = "org.nemo.desktop/volumes-visible",
                label   = _("Mounted volumes")
            ))
        if "network-icon-visible" in nemo_desktop_keys:
            section.add(CSW.CheckButton(
                label   = _("Network"),
                setting = "org.nemo.desktop/network-icon-visible"
            ))
        self.add(section)
