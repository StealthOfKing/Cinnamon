#!/usr/bin/env python

import CinnamonSettingsWidgets as CSW

class Module(CSW.Module):
    id = "workspaces"
    name = _("Workspaces")
    tooltip = _("Manage workspace preferences")
    keywords = _("workspace, osd, expo, monitor")
    icon = "cs-workspaces"
    category = "prefs"

    def on_module_selected(self):
        self.add(
            CSW.Section(_("On-Screen Display (OSD)")).add(
                CSW.CheckButton(
                    label   = _("Enable workspace OSD"),
                    setting = "org.cinnamon/workspace-osd-visible"
                ),
                CSW.VBox(depends=["org.cinnamon/workspace-osd-visible"], lock_widths=2).add(
                    CSW.SpinButton(
                        setting = "org.cinnamon/workspace-osd-duration",
                        label   = _("Workspace OSD duration"),
                        units   = _("milliseconds"),
                        min=0, max=2000, step=50, page=400
                    ),
                    CSW.SpinButton(
                        setting = "org.cinnamon/workspace-osd-x",
                        label   = _("Workspace OSD horizontal position"),
                        units   = _("percent of the monitor's width"),
                        min=0, max=100, step=5, page=50
                    ),
                    CSW.SpinButton(
                        setting = "org.cinnamon/workspace-osd-y",
                        label   = _("Workspace OSD vertical position"),
                        units   = _("percent of the monitor's height"),
                        min=0, max=100, step=5, page=50
                    )
                )
            ),
            CSW.Separator(),
            CSW.Section(_("Miscellaneous Options")).add(
                CSW.CheckButton(
                    setting = "org.cinnamon.muffin/workspace-cycle",
                    label   = _("Allow cycling through workspaces")
                ),
                CSW.CheckButton(
                    setting = "org.cinnamon.muffin/workspaces-only-on-primary",
                    label   = _("Only use workspaces on primary monitor (requires Cinnamon restart)")
                ),
                CSW.CheckButton(
                    setting = "org.cinnamon/workspace-expo-view-as-grid",
                    label   = _("Display Expo view as a grid")
                )
            )
        )

