#!/usr/bin/env python

# Settings is a small library used to provide all widgets
# with their respective Gio.Settings instance.

from gi.repository import Gio

settings = {}

def get_settings(schema):
    if schema not in settings:
        settings[schema] = Gio.Settings(schema)
        settings[schema].schema = schema
    return settings[schema]

def get_applet_settings(applet):
    if applet not in settings:
        settings[applet] = Gio.Settings.new_with_backend(applet, Gio.SettingsBackend())
        settings[applet].applet = applet
    return settings[applet]

def parse(setting):
    setting = setting.split("/")
    if len(setting) != 2:
        print "Invalid setting identifier for {s} ({s})".format(self.__class__.__name__, any(descriptor["setting"], "None"))
    if setting[0][0] == '@': # Applet setting.
        settings = get_applet_settings(setting[0][1:])
    else:   # Global setting.
        settings = get_settings(setting[0])
    return (settings, setting[1])

