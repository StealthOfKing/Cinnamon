#!/usr/bin/env python

# Generic widget container.

# All CSW container classes are variations of Gtk.Grid. To control how a
# widget is added to a container (column width locked or otherwise) use:
#     widget.grid_align = True  # allow the parent container to width lock this widget
#                         False # do not width lock any widget components

from gi.repository import Gtk
from InputWidget import InputWidget
from Widget import Widget

COLUMN_SPACING=2
ROW_SPACING=2

HORIZONTAL_LEFT_INDENT=0
HORIZONTAL_RIGHT_INDENT=0

VERTICAL_LEFT_INDENT=40
VERTICAL_RIGHT_INDENT=40

class Container(Widget, Gtk.Grid):
    column = 0  # Current column number.
    columns = 99
    row = 0 # Current row number.
    indent_children = True
    expand_children = False

    def __init__(self, **descriptor):
        Gtk.Grid.__init__(self)

        descriptor["align"] = descriptor.get("align", [-1,-1])
        descriptor["expand"] = descriptor.get("expand", [True, False])

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
        print str(type(self))+".add_widget(..., "+str(type(widget))+", "+str(column)+", "+str(row)+")"
        if widget.grid_align:   # Add widget components to individual grid cells.
            print "    aligned"
            if hasattr(widget, "prefix"):
                self.attach(widget.prefix, column, row, 1, 1)
                column = column + 1

            self.attach(widget, column, row, 1, 1)
            column = column + 1

            if hasattr(widget, "suffix"):
                self.attach(widget.suffix, column, row, 1, 1)
                column = column + 1
        else:   # Wrap widget components with box and add to grid.
            if hasattr(widget, "prefix") or hasattr(widget, "suffix"):
                print "    wrapped"
                wrapper = Gtk.Grid()
                wrapper.set_valign(widget.get_valign())
                wrapper.set_vexpand(widget.get_vexpand())
                widget.wrapper = wrapper

                c = 0
                if hasattr(widget, "prefix"):
                    wrapper.attach(widget.prefix, c, 0, 1, 1)
                    c = c + 1

                wrapper.attach(widget, c, 0, 1, 1)
                c = c + 1

                if hasattr(widget, "suffix"):
                    wrapper.attach(widget.suffix, c, 0, 1, 1)
                    c = c + 1

                widget = wrapper
            self.attach(widget, column, row, 3, 1)
            column = column + 3
        return column

    def add_row(self, widgets, column, row, indent_children):
        for widget in widgets:
            column = self.add_widget(widget, column, row)
        # Fixes how grid allocates extra space, helping tightly pack
        # components according to their intended definitions.
        if column < 3:
            last = Gtk.Grid()
            last.set_hexpand(True)
            self.attach(last, 2, row, 1, 1)
        else:
            last = widgets[-1]
        if indent_children:
            widgets[0].set_margin_left(widgets[ 0].margin[3] + VERTICAL_LEFT_INDENT * widgets[0].indent)
            last.set_margin_right(widgets[-1].margin[1] + VERTICAL_RIGHT_INDENT)
        return column

    def add_vertical(self, *widgets, **descriptor):   # Add widgets vertically (++rows).
        indent_children = descriptor.get("indent_children", self.indent_children)
        columns = descriptor.get("columns", self.columns)
        column = descriptor.get("column", 0)
        row = self.row
        for widget in widgets:
            if type(widget) == list:    # Add row of widgets.
                self.add_row(widget, column, row, indent_children)
            else:   # Individual widget.
                self.add_row([widget], column, row, indent_children)
            row = row + 1
        self.row = row
        return self

    def add(self, *widgets, **descriptor):    # Add widgets based on current orientation.
        if self.get_orientation() == Gtk.Orientation.HORIZONTAL:
            # TODO: add_horizontal has not been maintained or checked for correctness.
            self.add_horizontal(*widgets)
        else:
            self.add_vertical(*widgets, **descriptor)
        return self

