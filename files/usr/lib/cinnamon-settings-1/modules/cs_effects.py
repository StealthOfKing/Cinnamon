#!/usr/bin/env python

import CinnamonSettingsWidgets as CSW
from gi.repository.Gtk import SizeGroup, SizeGroupMode

class Module(CSW.Module):
    id = "effects"
    name = _("Effects")
    tooltip = _("Control Cinnamon visual effects.")
    keywords = _("effects, fancy, window")
    icon = "cs-desktop-effects"
    category = "appear"

    # Destroy window effects
    transition_effects = [[effect] * 2 for effect in
                     ["easeInQuad",
                      "easeOutQuad",
                      "easeInOutQuad",
                      "easeInCubic",
                      "easeOutCubic",
                      "easeInOutCubic",
                      "easeInQuart",
                      "easeOutQuart",
                      "easeInOutQuart",
                      "easeInQuint",
                      "easeOutQuint",
                      "easeInOutQuint",
                      "easeInSine",
                      "easeOutSine",
                      "easeInOutSine",
                      "easeInExpo",
                      "easeOutExpo",
                      "easeInOutExpo",
                      "easeInCirc",
                      "easeOutCirc",
                      "easeInOutCirc",
                      "easeInElastic",
                      "easeOutElastic",
                      "easeInOutElastic",
                      "easeInBack",
                      "easeOutBack",
                      "easeInOutBack",
                      "easeInBounce",
                      "easeOutBounce",
                      "easeInOutBounce"]]              

    def on_module_selected(self):
        section = CSW.Section(_("Enable Effects"))  
        section.add(
            CSW.CheckButton(suffix=_("Enable desktop effects"), setting="org.cinnamon/desktop-effects"),
            CSW.CheckButton(suffix=_("Enable desktop effects on dialog boxes"), setting="org.cinnamon/desktop-effects-on-dialogs", depends="org.cinnamon/desktop-effects"),
            CSW.CheckButton(suffix=_("Enable fade effect on Cinnamon scrollboxes (like the Menu application list)"), setting="org.cinnamon/enable-vfade")
        )
        vbox.add(section)

        vbox.add(Gtk.Separator.new(Gtk.Orientation.HORIZONTAL))

        section = Section(_("Customize Effects"))
        #CLOSING WINDOWS
        effects = [["none", _("None")], ["scale", _("Scale")], ["fade", _("Fade")]]        
        section.add(self.make_effect_group(_("Closing windows:"), "close", effects))
        
        #MAPPING WINDOWS
        effects = [["none", _("None")], ["scale", _("Scale")], ["fade", _("Fade")]]        
        section.add(self.make_effect_group(_("Mapping windows:"), "map", effects))
        
        #MINIMIZING WINDOWS
        effects = [["none", _("None")], ["traditional", _("Traditional")], ["scale", _("Scale")], ["fade", _("Fade")]]
        section.add(self.make_effect_group(_("Minimizing windows:"), "minimize", effects))
        
        #MAXIMIZING WINDOWS
        effects = [["none", _("None")], ["scale", _("Scale")]]        
        section.add(self.make_effect_group(_("Maximizing windows:"), "maximize", effects))
        
        #UNMAXIMIZING WINDOWS
        effects = [["none", _("None")], ["scale", _("Scale")]]
        section.add(self.make_effect_group(_("Unmaximizing windows:"), "unmaximize", effects))

        #TILING WINDOWS
        effects = [["none", _("None")], ["scale", _("Scale")]]
        section.add(self.make_effect_group(_("Tiling and snapping windows:"), "tile", effects))
        
        vbox.add(section)

    def make_effect_group(self, group_label, key, effects):
        tmin, tmax, tstep, tdefault = (0, 2000, 50, 200)
        self.size_groups = getattr(self, "size_groups", [SizeGroup.new(SizeGroupMode.HORIZONTAL) for x in range(4)])
        root = "org.cinnamon"
        path = "org.cinnamon/desktop-effects"
        template = "desktop-effects-%s-%s"
        box = Gtk.HBox()
        label = Gtk.Label()
        label.set_markup(group_label)
        label.props.xalign = 0.0
        self.size_groups[0].add_widget(label)
        box.add(label)
        w = GSettingsComboBox("", root, template % (key, "effect"), path, effects)
        self.size_groups[1].add_widget(w)
        box.add(w)
        w = GSettingsComboBox("", root, template % (key, "transition"), path, self.transition_effects)
        self.size_groups[2].add_widget(w)
        box.add(w)
        w = GSettingsSpinButton("", root, template % (key, "time"), path, tmin, tmax, tstep, tdefault, _("milliseconds"))
        self.size_groups[3].add_widget(w)
        box.add(w)
        return box
