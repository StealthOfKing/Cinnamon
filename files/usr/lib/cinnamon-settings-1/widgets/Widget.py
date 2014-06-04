#!/usr/bin/env python

# Widget is a simple class for implementing Setting based dependencies
# and other properties common to both InputWidgets and Containers.

from gi.repository import Gtk
import Settings

# Validator functions for Gtk.Variant type strings.
# Currently does not handle enums.
validate_boolean = lambda x:x
validate_number  = lambda x:x!=0
validate_string  = lambda x:x!=""
validators = {}
validators.update({ t:validate_boolean for t in 'b'})   # BOOLEAN
validators.update({ t:validate_number for t in 'ynqiuxthd'})    # BYTE, INT16, UINT16, INT32, UINT32, INT64, UINT64, HANDLE, DOUBLE
validators.update({ t:validate_string for t in 'sog'})  # STRING, OBJECT_PATH, STRING

# Helper function translates between the older set_alignment(float(x),float(y))
# style and gtk3 set_h/valign(Gtk.Align.*).
def get_align(align):
    if type(align) == Gtk.Align:
        return align
    if align == 0:
        return Gtk.Align.START
    if align == 0.5:
        return Gtk.Align.CENTER
    if align == 1:
        return Gtk.Align.END
    return Gtk.Align.FILL

# Widget provides a common API for all input widgets, non-input widgets
# and containers.
class Widget(object):
    indent = 1
    margin = [0,0,0,0]
    lock_width = False

    def __init__(self, **descriptor):
        # Dependencies?
        if "depends" in descriptor:
            self.dependencies = []
            depends = descriptor["depends"]
            enabled = True
            for i in range(len(depends)):
                setting = depends[i]
                negate = setting[0] == '!'  # First char ! means negate the dependency.
                settings, key = Settings.parse(setting[1:] if negate else setting)
                settings.connect("changed::"+key, self.on_dependency_changed)
                variant = settings.get_value(key)
                # Opportunity here to add a custom validator function should any module require it (currently unsupported).
                validator = validators[variant.get_type_string()]
                enabled = enabled and (validator(variant.unpack()) != negate)
                self.dependencies.append({ "settings":settings, "key":key, "negate":negate, "validator":validator })
            self.set_sensitive(enabled)

        if "align" in descriptor:
            align = descriptor["align"]
            self.set_halign(get_align(align[0]))
            self.set_valign(get_align(align[1]))

        if "classes" in descriptor:
            classes = descriptor["classes"]
            style_context = self.get_style_context()
            for c in classes:
                style_context.add_class(c)

        if "expand" in descriptor:
            self.set_hexpand(descriptor["expand"][0])
            self.set_vexpand(descriptor["expand"][1])

        if "indent" in descriptor:
            self.indent = descriptor["indent"]
        
        if "lock_width" in descriptor:
            self.lock_width = descriptor["lock_width"]

        if "margin" in descriptor:
            margin = descriptor["margin"]
            self.margin = margin
            self.set_margin_top   (margin[0])
            self.set_margin_right (margin[1])
            self.set_margin_bottom(margin[2])
            self.set_margin_left  (margin[3])

        if "tooltip" in descriptor:
            self.set_tooltip_text(descriptor["tooltip"])

        # Events
        if "clicked" in descriptor:
            self.connect("clicked", descriptor["clicked"])

    def validate_dependencies(self):    # Validate all dependencies and update this widget's sensitivity.
        dependencies = self.dependencies
        enabled = True
        for dependency in dependencies: # Revalidate all dependencies.
            if dependency["validator"](dependency["settings"].get_value(dependency["key"]).unpack()) == dependency["negate"]:
                enabled = False
                break
        super(self.__class__, self).set_sensitive(enabled)

    def on_dependency_changed(self, settings, key):   # Called when a dependency changes.
        self.validate_dependencies()

