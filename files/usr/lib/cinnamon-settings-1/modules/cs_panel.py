#!/usr/bin/env python

import CinnamonSettingsWidgets as CSW

class Module(CSW.Module):
    id = "panel"
    name = _("Panel")
    tooltip = _("Manage Cinnamon panel settings")
    keywords = _("panel, height, bottom, top, autohide, size, traditional, layout")
    icon = "cs-panel"
    category = "prefs"

    def on_module_selected(self):
        desktop_layout_combo_box = CSW.ComboBox(
            setting = "org.cinnamon/desktop-layout",
            label   = _("Panel layout"),
            options = [
                ["traditional", _("Traditional (panel at the bottom)")],
                ["flipped",     _("Flipped (panel at the top)")],
                ["classic",     _("Classic (panels at the top and at the bottom)")]
            ]
        )

        self.add(
            CSW.Section(_("Layout Options")).add(
                desktop_layout_combo_box,
                CSW.Label(
                    markup  = "<i><small>%s</small></i>" % _("Note: If you change the layout you will need to restart Cinnamon and Cinnamon Settings."),
                    classes = ["dim-label"]
                )
            ),
            CSW.Separator()
        )

        section = CSW.Section(_("Autohide Options"))
        layout_type = desktop_layout_combo_box._get_value()
        if layout_type != "classic":
            section.add(
                CSW.CheckButton(
                    setting = "org.cinnamon/panel-autohide",
                    label   = _("Autohide panel")
                ),
                CSW.SpinButton(
                    setting = "org.cinnamon/panel-show-delay",
                    depends = ["org.cinnamon/panel-autohide"],
                    label   = _("Show delay"),
                    units   = _("milliseconds"),
                    min=0, max=2000, step=50, page=200
                ),
                CSW.SpinButton(
                    setting = "org.cinnamon/panel-hide-delay",
                    depends = ["org.cinnamon/panel-autohide"],
                    label   = _("Hide delay"),
                    units   = _("milliseconds"),
                    min=0, max=2000, step=50, page=200
                )
            )
        else:
            section.add(
                CSW.CheckButton(
                    label   = _("Autohide top panel"),
                    setting = "org.cinnamon/panel-autohide"
                ),
                CSW.SpinButton(
                    setting = "org.cinnamon/panel-show-delay",
                    depends = ["org.cinnamon/panel-autohide"],
                    label   = _("Show delay"),
                    units   = _("milliseconds"),
                    min=0, max=2000, step=50, page=200
                ),
                CSW.SpinButton(
                    setting = "org.cinnamon/panel-hide-delay",
                    depends = ["org.cinnamon/panel-autohide"],
                    label   = _("Hide delay"),
                    units   = _("milliseconds"),
                    min=0, max=2000, step=50, page=200
                ),
                CSW.CheckButton(
                    label   = _("Autohide bottom panel"),
                    setting = "org.cinnamon/panel2-autohide"
                ),
                CSW.SpinButton(
                    setting = "org.cinnamon/panel2-show-delay",
                    depends = ["org.cinnamon/panel2-autohide"],
                    label   = _("Show delay"),
                    units   = _("milliseconds"),
                    min=0, max=2000, step=50, page=200
                ),
                CSW.SpinButton(
                    setting = "org.cinnamon/panel2-hide-delay",
                    depends = ["org.cinnamon/panel2-autohide"],
                    label   = _("Hide delay"),
                    units   =_("milliseconds"),
                    min=0, max=2000, step=50, page=200
                )
            )
        self.add(
            section,
            CSW.Separator(),
            CSW.Section(_("Size Options")).add(
                CSW.CheckButton(
                    setting = "org.cinnamon/panel-resizable",
                    label   = _("Use customized panel size (otherwise it's defined by the theme)")
                ),
                CSW.CheckButton(
                    setting = "org.cinnamon/panel-scale-text-icons",
                    depends = ["org.cinnamon/panel-resizable"],
                    label   = _("Allow Cinnamon to scale panel text and icons according to the panel heights")
                )
#        slider = GSettingsRange(_("Top panel height:"), _("Smaller"), _("Larger"), 20, 50, False, "int", False, "org.cinnamon", "panel-top-height", "org.cinnamon/panel-resizable", adjustment_step = 1.0)
#        slider.add_mark(25.0, Gtk.PositionType.TOP, None)
#        section.add_indented_expand(slider)
#        slider = GSettingsRange(_("Bottom panel height:"), _("Smaller"), _("Larger"), 20, 50, False, "int", False, "org.cinnamon", "panel-bottom-height", "org.cinnamon/panel-resizable", adjustment_step = 1.0)
#        slider.add_mark(25.0, Gtk.PositionType.TOP, None)
#        section.add_indented_expand(slider)
            ),
            CSW.Separator(),
            CSW.Section().add(
                CSW.CheckButton(
                    setting = "org.cinnamon/panel-edit-mode",
                    label   = _("Panel edit mode"),
                    indent  = 0
                )
            )
        )

