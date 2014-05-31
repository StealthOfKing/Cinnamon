#!/usr/bin/env python

# Generic widget container.

# All Containers have a unique property, lock_widths. lock_widths controls
# the number of InputWidget columns to width lock via Gtk.SizeGroup.
#
#     container.lock_widths = 0 # no width lock
#                             1 # width lock gtk_prefix
#                             2 # width lock gtk_prefix, gtk_widget
#                             3 # width lock gtk_prefix, gtk_widget, gtk_suffix
#
# Each Container's lock_widths can be overriden on a per Widget basis, using
# the widget property lock_width.
#
#     widget.lock_width = True  # allow the parent container to width lock this widget
#                         False # do not width lock any widget components

from gi.repository import Gtk
from Widget import Widget

COLUMN_SPACING=2
ROW_SPACING=2

HORIZONTAL_LEFT_INDENT=0
HORIZONTAL_RIGHT_INDENT=0

VERTICAL_LEFT_INDENT=40
VERTICAL_RIGHT_INDENT=40

class Container(Gtk.Grid, Widget):
    lock_widths = 1 # Lock the first column only (gtk_prefix).
    column = 0  # Current column number.
    row = 0 # Current row number.
    indent_children = True

    def __init__(self, **descriptor):
        descriptor["expand"] = descriptor.get("expand", [True, True])

        Gtk.Grid.__init__(self)
        Widget.__init__(self, **descriptor)

        self.set_column_spacing(COLUMN_SPACING)
        self.set_row_spacing(ROW_SPACING)

        if "indent_children" in descriptor:
            self.indent_children = descriptor["indent_children"]

        if "lock_widths" in descriptor:
            self.lock_widths = descriptor["lock_widths"]
        if "orientation" in descriptor:
            self.set_orientation(descriptor["orientation"])

        # Lock label column width by default using Gtk.SizeGroup.
        lock_widths = self.lock_widths
        width_locks = []
        for i in range(lock_widths):    # One size group per column.
            width_locks.append(Gtk.SizeGroup(mode=Gtk.SizeGroupMode.HORIZONTAL))
        self.width_locks = width_locks

    def add_horizontal(self, *widgets): # Add widgets horizontally (++columns).
        for widget in widgets:
            if (self.indent_children):
                widget.set_margin_left (widget.margin[3] + HORIZONTAL_LEFT_INDENT * widget.indent)
                widget.set_margin_right(widget.margin[1] + HORIZONTAL_RIGHT_INDENT)
            Gtk.Grid.attach(self, widget, self.column, self.row, 1, 1)
            self.column = self.column + 1

    def add_vertical(self, *widgets):   # Add widgets vertically (++rows).
        lock_widths = self.lock_widths
        width_locks = self.width_locks
        for widget in widgets:
            if type(widget) == list:
                if (self.indent_children):
                    widget[0].set_margin_left (widget[0].margin[3] + VERTICAL_LEFT_INDENT * widget[0].indent)
                self.column = 0
                for i in range(len(widget)):
                    self.attach(widget[i], self.column, self.row, 1, 1)
                    self.column = self.column + 1
                widget[i].set_margin_right(widget[i].margin[1] + VERTICAL_RIGHT_INDENT)
            else:
                if (self.indent_children):
                    widget.set_margin_right(widget.margin[1] + VERTICAL_RIGHT_INDENT)
                    widget.set_margin_left (widget.margin[3] + VERTICAL_LEFT_INDENT * widget.indent)
                self.attach(widget, self.column, self.row, 1, 1)
                if widget.lock_width:
                    if lock_widths >= 1 and hasattr(widget, "gtk_prefix"):
                        width_locks[0].add_widget(widget.gtk_prefix)
                    if lock_widths >= 2 and hasattr(widget, "gtk_widget"):
                        width_locks[1].add_widget(widget.gtk_widget)
                    if lock_widths >= 3 and hasattr(widget, "gtk_suffix"):
                        width_locks[2].add_widget(widget.gtk_suffix)

            self.row = self.row + 1
        return self

    def add(self, *widgets):    # Add widgets based on current orientation.
        if self.get_orientation() == Gtk.Orientation.HORIZONTAL:
            self.add_horizontal(*widgets)
        else:
            self.add_vertical(*widgets)
        return self

