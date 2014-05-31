#!/usr/bin/env python

import CinnamonSettingsWidgets as CSW

class Module(CSW.Module):
    id = "notifications"
    name = _("Notifications")
    tooltip = _("Manage notification settings")
    keywords = _("notifications")
    icon = "cs-notifications"
    category = "prefs"

    def on_module_selected(self):
        self.add(
            CSW.Section(_("Behaviour")).add(
                CSW.CheckButton(
                    setting = "org.cinnamon/display-notifications",
                    label   = _("Display notifications"),
                    tooltip = _("Check this to enable notifications")
                ),
                CSW.VBox(depends=["org.cinnamon/display-notifications"]).add(
                    CSW.CheckButton(
                        setting = "org.cinnamon.desktop.notifications/fade-on-mouseover",
                        label   = _("Notifications fade out"),
                        tooltip = _("Check this to allow notifications to fade on mouseover")
                    ),
                    CSW.CheckButton(
                        setting = "org.cinnamon.desktop.notifications/remove-old",
                        label   = _("Remove old notifications"),
                        tooltip = _("Check this to allow notifications to timeout")
                    )
                )
            )
        )

