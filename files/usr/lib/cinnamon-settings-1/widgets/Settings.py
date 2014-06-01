#!/usr/bin/env python

# Settings is a small library used to provide all widgets
# with their respective Gio.Settings instance.

from gi.repository import Gio

settings = {}   # Dictionary of all Gio.Settings objects indexed by their schema/applet identifier.

def get_settings(schema):   # Gets a Gio.Settings instance for a schema.
    if schema not in settings:
        settings[schema] = Gio.Settings(schema)
        settings[schema].schema = schema
    return settings[schema]

def get_applet_settings(applet):    # Gets a Gio.Settings instance for an applet.
    if applet not in settings:
        settings[applet] = Gio.Settings.new_with_backend(applet, Gio.SettingsBackend())
        settings[applet].applet = applet
    return settings[applet]

def parse(setting): # Parses a Setting string and return the appropriate Gio.Settings instance.
    setting = setting.split("/")
    if len(setting) != 2:
        print "Invalid setting identifier for {s} ({s})".format(self.__class__.__name__, any(descriptor["setting"], "None"))
    if '@' in setting: # Applet setting.
        settings = get_applet_settings(setting[0][1:])
    else:   # Global setting.
        settings = get_settings(setting[0])
    return (settings, setting[1])

