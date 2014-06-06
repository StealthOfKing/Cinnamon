#!/usr/bin/env python

# Button input widget.

# Despite inheriting InputWidget, Button intentionally does not work
# with Settings (schema/applet/key).

from gi.repository import Gtk
from InputWidget import InputWidget

class Button(InputWidget, Gtk.Button):
    def __init__(self, **descriptor):
        Gtk.Button.__init__(self)

        descriptor["expand"] = descriptor.get("expand", [False,False])

        InputWidget.__init__(self, **descriptor)

        if "image" in descriptor:
            self.gtk_button_image = Gtk.Image()
            self.gtk_button_image.set_from_file(descriptor["image"])
            self.set_image(self.gtk_button_image)

        if "menu" in descriptor:
            self.connect("button-release-event", self.on_button_release_event_menu, descriptor["menu"])

        self.set_use_underline(True)
        if "text" in descriptor:
            self.set_label(descriptor["text"])

        # Events
        if "clicked" in descriptor:
            self.connect("clicked", descriptor["clicked"])
            del descriptor["clicked"]

    def on_button_release_event_menu(self, button, event, menu):
        if event.button == 1:
            menu.popup(None, None, self.popup_menu_below_button, None, event.button, event.time)
            menu.show_all()

    def popup_menu_below_button(self, menu, data):
        # Fetch coordinates of the button relative to window.
        alloc = self.get_allocation()
        # Convert coordinates to X11-relative.
        unused_var, window_x, window_y = self.get_window().get_origin()
        return (
            window_x + alloc.x,
            window_y + alloc.y + alloc.height,   # Move menu below.
            True    # push_in is True, menu will remain inside screen.
        )

#   def _get_value(self):
#       pass
#   def _set_value(self, value):
#       pass

