#!/usr/bin/env python

import CinnamonSettingsWidgets as CSW

class Module(CSW.Module):
    id = "general"
    name = _("General")
    tooltip = _("Miscellaneous Cinnamon preferences")
    keywords = _("logging, click")
    icon = "cs-general"
    category = "prefs"

    def on_module_selected(self):
        self.add(
            CSW.Section(_("Desktop Scaling")).add(
                CSW.ComboBox(
                    setting = "org.cinnamon.desktop.interface/scaling-factor",
                    label   = _("User interface scaling:"),
                    options = [
                        [0, _("Auto")],
                        [1, _("Normal")],
                        [2, _("Double (Hi-DPI)")]
                    ]
                )
            ),
            CSW.Separator(),
            CSW.Section(_("Miscellaneous Options")).add(
                CSW.CheckButton(
                    setting = "org.cinnamon/enable-looking-glass-logs",
                    label   = _("Log LookingGlass output to ~/.cinnamon/glass.log (Requires Cinnamon restart)")
                )
            )
        )

