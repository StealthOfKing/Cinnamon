#!/usr/bin/env python

import CinnamonSettingsWidgets as CSW
from gi.repository import Gio, Gtk, GObject, Gdk

class Module(CSW.Module):
    name = _("Window Tiling and Edge Flip")
    tooltip = _("Manage window tiling preferences")
    keywords = _("window, tile, flip, tiling, snap, snapping")
    icon = "cs-tiling"
    category = "prefs"

    def on_module_selected(self):
        self.add(
            CSW.Section(_("Tiling and Snapping Settings")).add(
                CSW.CheckButton(
                    setting = "org.cinnamon.muffin/edge-tiling",
                    label   = _("Enable Window Tiling and Snapping")
                ),
                CSW.VBox(depends=["org.cinnamon.muffin/edge-tiling"]).add(
                    CSW.SpinButton(
                        setting = "org.cinnamon.muffin/tile-hud-threshold",
                        label   = _("Tiling HUD visibility threshold"),
                        min=1, max=300, step=1, page=10, units=_("pixels")
                    ),
                    CSW.ComboBox(
                        setting = "org.cinnamon.muffin/snap-modifier",
                        label   = _("Modifier to use for toggling between tile and snap mode"),
                        options = [
                            ["",        "Disabled"],
                            ["Super",   _("Super (Windows)")],
                            ["Alt",     _("Alt")],
                            ["Shift",   _("Shift")],
                            ["Control", _("Control")]
                        ]
                    ),
                    CSW.CheckButton(
                        setting = "org.cinnamon.muffin/tile-maximize",
                        label   = _("Maximize, instead of tile, when dragging a window to the top edge")
                    ),
                    CSW.CheckButton(
                        setting = "org.cinnamon/hide-snap-osd",
                        label   = _("Prevent the snap on-screen-display from showing")
                    )
                )
            ),
            CSW.Separator(),
            CSW.Section(_("Edge Flip Settings")).add(
                CSW.CheckButton(
                    setting = "org.cinnamon/enable-edge-flip",
                    label   = _("Enable Edge Flip")
                ),
                CSW.SpinButton(
                    setting = "org.cinnamon/edge-flip-delay",
                    depends = ["org.cinnamon/enable-edge-flip"],
                    label   = _("Edge Flip delay"),
                    min=1, max=3000, step=1, page=10, units=_("ms")
                )
            ),
            CSW.Separator(),
            CSW.Section(_("Miscellaneous Settings")).add(
                CSW.CheckButton(
                    setting = "org.cinnamon.muffin/invert-workspace-flip-direction",
                    label   = _("Invert the left and right arrow key directions used to shift workspaces during a window drag")
                ),
                CSW.CheckButton(
                    setting = "org.cinnamon.muffin/legacy-snap",
                    label   = CSW.Label(label=_("Enable legacy window snapping (hold <Shift> while dragging a window)"))
                )
            )
        )

