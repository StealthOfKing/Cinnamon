#!/usr/bin/env python

# Category is a Gtk.Box containing the header and module icons for each
# respective System Settings category. The header is build from Gtk.Icon
# and Gtk.Label. Each category has its own Gtk.ListStore,
# Gtk.TreeModelFilter and Gtk.IconView for rendering the icons.

from gi.repository import Gtk, Pango

class Category(Gtk.Box):
    def __init__(self, descriptor, separator, min_pix_length, min_label_length):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)

        # Create root Gtk.ListStore and Gtk.TreeModelFilter used for Gtk.IconView.
        self.store = Gtk.ListStore(str, str, str, bool, object)
        self.filter = self.store.filter_new()
        self.filter.set_visible_column(3)

        if separator:    # No separator for first category.
            widget = Gtk.Separator.new(Gtk.Orientation.HORIZONTAL)
            self.pack_start(widget, False, False, 10)

        # Create category header.
        box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 4)
        self.pack_start(box, False, False, 0)
        # Icon
        img = Gtk.Image.new_from_icon_name(descriptor["icon"], Gtk.IconSize.BUTTON)
        box.pack_start(img, False, False, 4)
        # Label
        widget = Gtk.Label()
        widget.set_use_markup(True)
        widget.set_markup('<span size="12000">%s</span>' % descriptor["label"])
        widget.set_alignment(.5, .5)
        box.pack_start(widget, False, False, 1)

        # Create IconView.
        widget = Gtk.IconView(self.filter)
        widget.set_tooltip_column(2)
        widget.set_item_width(min_pix_length)
        widget.set_item_padding(0)
        widget.set_column_spacing(18)
        widget.set_row_spacing(18)
        widget.set_margin(20)

        pixbuf_renderer = Gtk.CellRendererPixbuf()
        text_renderer = Gtk.CellRendererText(ellipsize=Pango.EllipsizeMode.NONE, wrap_mode=Pango.WrapMode.WORD_CHAR, wrap_width=0, width_chars=min_label_length, alignment=Pango.Alignment.CENTER)

        text_renderer.set_alignment(.5, 0)
        area = widget.get_area()
        area.pack_start(pixbuf_renderer, True, True, False)
        area.pack_start(text_renderer, True, True, False)
        area.add_attribute(pixbuf_renderer, "icon-name", 1)
        pixbuf_renderer.set_property("stock-size", Gtk.IconSize.DIALOG)

        area.add_attribute(text_renderer, "text", 0)

        self.gtk_icon_view = widget
        self.pack_start(widget, False, False, 0)

    def select_item(self, item):
        self.gtk_icon_view.set_cursor(item, None, False)
        self.gtk_icon_view.select_path(item)
        self.gtk_icon_view.grab_focus()

    def get_current_column(self):
        s, path, cell = self.gtk_icon_view.get_cursor()
        if path:
            return self.gtk_icon_view.get_item_column(path)
