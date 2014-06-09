#!/usr/bin/env python

import CinnamonSettingsWidgets as CSW

LOCK_DELAY_OPTIONS = [
    (0, _("Immediately")),
    (15, _("After 15 seconds")),
    (30, _("After 30 seconds")),
    (60, _("After 1 minute")),
    (120, _("After 2 minutes")),
    (180, _("After 3 minutes")),
    (300, _("After 5 minutes")),
    (600, _("After 10 minutes")),
    (1800, _("After 30 minutes")),
    (3600, _("After 1 hour"))
]

class Module(CSW.Module):
    id = "screensaver"
    name = _("Lock Screen")
    tooltip = _("Manage screen lock settings")
    keywords = _("screensaver, lock, password, away, message")
    icon = "cs-screensaver"
    category = "prefs"

    def on_module_selected(self):
        self.add(
            CSW.Section(_("Lock Settings")).add(
                CSW.CheckButton(
                    setting = "org.cinnamon.settings-daemon.plugins.power/lock-on-suspend",
                    label   = _("Lock the computer when put to sleep"),
                    tooltip = _("Enable this option to require a password when the computer wakes up from suspend")
                ),
                [
                    CSW.CheckButton(
                        setting = "org.cinnamon.desktop.screensaver/lock-enabled",
                        label   = _("Lock the computer when the screen turns off "),
                        tooltip = _("Enable this option to require a password when the screen turns itself off, or when the screensaver activates after a period of inactivity")
                    ),
                    CSW.ComboBox(
                        setting = "org.cinnamon.desktop.screensaver/lock-delay",
                        depends = ["org.cinnamon.desktop.screensaver/lock-enabled"],
                        options = [
                            (   0, _("Immediately")),
                            (  15, _("After 15 seconds")),
                            (  30, _("After 30 seconds")),
                            (  60, _("After 1 minute")),
                            ( 120, _("After 2 minutes")),
                            ( 180, _("After 3 minutes")),
                            ( 300, _("After 5 minutes")),
                            ( 600, _("After 10 minutes")),
                            (1800, _("After 30 minutes")),
                            (3600, _("After 1 hour"))
                        ],
                        tooltip = _("This option defines the amount of time to wait before locking the screen, after showing the screensaver or after turning off the screen")
                    )
                ]
            ),
            CSW.Separator(),
            CSW.Section(_("Away Message")).add(
                CSW.Entry(
                    setting = "org.cinnamon.screensaver/default-message",
                    label   = _("Show this message when the screen is locked"),
                    tooltip = _("This is the default message displayed on your lock screen")
                ),
                CSW.CheckButton(
                    setting = "org.cinnamon.screensaver/ask-for-away-message",
                    label   = _("Ask for a custom message when locking the screen from the menu"),
                    tooltip = _("This option allows you to type a message each time you lock the screen from the menu")
                )
            )
        )

