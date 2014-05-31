#!/usr/bin/env python

import CinnamonSettingsWidgets as CSW

class Module(CSW.Module):
    id = "calendar"
    name = _("Date and Time")
    tooltip = _("Manage date and time settings")
    keywords = _("time, data, calendar, format, network, sync")
    icon = "cs-date-time"
    category = "prefs"
                
    def on_module_selected(self):
        self.add(
            CSW.Section(_("Date Settings")).add(
                CSW.CWidget("datetime")
            ),
            CSW.Separator(),
            CSW.Section(_("Date Format")).add(
                CSW.CheckButton(
                    setting = "org.cinnamon.desktop.interface/clock-use-24h",
                    label   = _("Use 24h clock"),
                    tooltip = _("Check this to enable 24 hour clock")
                ),
                CSW.CheckButton(
                    setting = "org.cinnamon.desktop.interface/clock-show-date",
                    label   = _("Display the date"),
                    tooltip = _("Check this to display the date next to the clock")
                ),
                CSW.CheckButton(
                    setting = "org.cinnamon.desktop.interface/clock-show-seconds",
                    label   = _("Display seconds"),
                    tooltip = _("Check this to show seconds on the clock")
                )
            )
        )

