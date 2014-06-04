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
    column = 0  # Current column number.
    row = 0 # Current row number.
    indent_children = True
    expand_children = False

    def __init__(self, **descriptor):
        descriptor["expand"] = descriptor.get("expand", [True, True])

        Gtk.Grid.__init__(self)
        Widget.__init__(self, **descriptor)

        self.set_column_spacing(COLUMN_SPACING)
        self.set_row_spacing(ROW_SPACING)

        if "indent_children" in descriptor:
            self.indent_children = descriptor["indent_children"]

        if "orientation" in descriptor:
            self.set_orientation(descriptor["orientation"])

    def add_horizontal(self, *widgets): # Add widgets horizontally (++columns).
        for widget in widgets:
            if (self.indent_children):
                widget.set_margin_left (widget.margin[3] + HORIZONTAL_LEFT_INDENT * widget.indent)
                widget.set_margin_right(widget.margin[1] + HORIZONTAL_RIGHT_INDENT)
            Gtk.Grid.attach(self, widget, self.column, self.row, 1, 1)
            self.column = self.column + 1

    def add_widget(self, widget, column, row):
        print "add_widget(..."+str(column)+", "+str(row)+")"
        if widget.lock_width:
            print "    "+str(type(widget))
            if hasattr(widget, "prefix"):
                self.attach(widget.prefix, column, row, 1, 1)
                if self.indent_children:
                    widget.prefix.set_margin_left(widget.margin[3] + VERTICAL_LEFT_INDENT * widget.indent)
                column = column + 1
            else:
                if self.indent_children:
                    widget.set_margin_left(widget.margin[3] + VERTICAL_LEFT_INDENT * widget.indent)

            if self.expand_children:
                widget.set_hexpand(True)
                widget.set_halign(Gtk.Align.FILL)
            self.attach(widget, column, row, 1, 1)
            column = column + 1

            if hasattr(widget, "suffix"):
                self.attach(widget.suffix, column, row, 1, 1)
                if self.indent_children:
                    widget.suffix.set_margin_right(widget.margin[1] + VERTICAL_RIGHT_INDENT)
                column = column + 1
            else:
                if self.indent_children:
                    widget.set_margin_right(widget.margin[1] + VERTICAL_RIGHT_INDENT)

            # Fixes how grid allocates extra space, helping tightly pack
            # components according to their intended definitions.
            box = Gtk.Box()
            box.set_hexpand(True)
            self.attach(box, 3, row, 1, 1)
        else:
            container = Gtk.Grid()
            if self.indent_children:
                container.set_margin_right(widget.margin[1] + VERTICAL_RIGHT_INDENT)
                container.set_margin_left (widget.margin[3] + VERTICAL_LEFT_INDENT * widget.indent)
            c = 0
            if hasattr(widget, "prefix"):
                container.attach(widget.prefix, c, 0, 1, 1)
                c = c + 1
            container.attach(widget, c, 0, 1, 1)
            c = c + 1
            if hasattr(widget, "suffix"):
                container.attach(widget.suffix, c, 0, 1, 1)
                c = c + 1
            self.attach(container, column, row, 4, 1)
            column = column + 4
        return column

    def add_vertical(self, *widgets, **descriptor):   # Add widgets vertically (++rows).
        columns = descriptor.get("columns", 3)
        column, row = descriptor.get("column", 0), self.row
        for widget in widgets:
            if type(widget) == list:    # Add row of widgets.
                if (self.indent_children):
                    widget[0].set_margin_left(widget[0].margin[3] + VERTICAL_LEFT_INDENT * widget[0].indent)
                for w in widget:
                    column = self.add_widget(w, column, row) % columns
                    if column == 0:
                        row = row + 1
                if (self.indent_children):
                    w.set_margin_right(w.margin[1] + VERTICAL_RIGHT_INDENT)
            else:   # Individual widget.
                column = self.add_widget(widget, column, row)
            column = 0
            row = row + 1
        self.column, self.row = column, row
        return self

    def add(self, *widgets, **descriptor):    # Add widgets based on current orientation.
        if self.get_orientation() == Gtk.Orientation.HORIZONTAL:
            self.add_horizontal(*widgets)
        else:
            self.add_vertical(*widgets, **descriptor)
        return self

