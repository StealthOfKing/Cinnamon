#!/usr/bin/env python

import CinnamonSettingsWidgets as CSW

class Module(CSW.Module):
    id = "fonts"
    name = _("Fonts")
    tooltip = _("Configure system fonts")
    keywords = _("font, size, small, large")
    icon = "cs-fonts"
    category = "appear"

    def on_module_selected(self):
        self.add(
            CSW.Section(_("Font Selection"), lock_widths=2).add(
                CSW.FontButton(
                    setting = "org.cinnamon.desktop.interface/font-name",
                    label   = _("Default font")
                ),
                CSW.FontButton(
                    setting = "org.gnome.desktop.interface/document-font-name",
                    label   = _("Document font")
                ),
                CSW.FontButton(
                    setting = "org.gnome.desktop.interface/monospace-font-name",
                    label   = _("Monospace font")
                ),
                CSW.FontButton(
                    setting = "org.cinnamon.desktop.wm.preferences/titlebar-font",
                    label   = _("Window title font"),
                )
            ),
            CSW.Separator(),
            CSW.Section(_("Font Settings"), lock_widths=2).add(
                CSW.SpinButton(
                    setting = "org.cinnamon.desktop.interface/text-scaling-factor",
                    label   = _("Text scaling factor"),
                    min=0.5, max=3.0, step=0.1, page=0.2, digits=1
                ),
                CSW.ComboBox(
                    setting = "org.cinnamon.settings-daemon.plugins.xsettings/antialiasing",
                    label   = _("Antialiasing"),
                    options = [
                        ["none",      _("None")],
                        ["grayscale", _("Grayscale")],
                        ["rgba",      _("RGBA")]
                    ],
                    tooltip = _("Antialiasing makes on screen text smoother and easier to read")
                ),
                CSW.ComboBox(
                    setting = "org.cinnamon.settings-daemon.plugins.xsettings/hinting",
                    label   = _("Hinting"),
                    options = [
                        ["none",   _("None")],
                        ["slight", _("Slight")],
                        ["medium", _("Medium")],
                        ["full",   _("Full")]
                    ],
                    tooltip = _("Hinting allows for producing clear, legible text on screen.")
                )
            )
        )

