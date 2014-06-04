#!/usr/bin/env python

# Media app chooser widget.

# Cinnamon maintains three string arrays containing x-content types.
# 'autorun-x-content-start-app' contains a list of media types that have
# an associated default application, 'autorun-x-content-ignore' contains
# a list of media types that should be ignored, and 'autorun-x-content-
# open-folder' contains a list of media types that should automatically
# open in Nemo.

from gi.repository import Gio
from AppChooserButton import AppChooserButton
import Settings

PREF_MEDIA_AUTORUN_NEVER = "autorun-never"
PREF_MEDIA_AUTORUN_X_CONTENT_START_APP = "autorun-x-content-start-app"
PREF_MEDIA_AUTORUN_X_CONTENT_IGNORE = "autorun-x-content-ignore"
PREF_MEDIA_AUTORUN_X_CONTENT_OPEN_FOLDER = "autorun-x-content-open-folder"

CUSTOM_ITEM_ASK = "cc-item-ask"
CUSTOM_ITEM_DO_NOTHING = "cc-item-do-nothing"
CUSTOM_ITEM_OPEN_FOLDER = "cc-item-open-folder"

settings = Settings.get_settings("org.cinnamon.desktop.media-handling")

class MediaAppChooserButton(AppChooserButton):
    def __init__(self, **descriptor):
        descriptor["default"] = descriptor.get("default", False)
        descriptor["dialog"] = descriptor.get("dialog", True)
        # Build extra menu options.
        descriptor["options"] = descriptor.get("options", []) + [
            [CUSTOM_ITEM_ASK,         _("Ask what to do"), "gtk-dialog-question"],
            [CUSTOM_ITEM_OPEN_FOLDER, _("Open folder"),    "gtk-directory"],
            [CUSTOM_ITEM_DO_NOTHING,  _("Do nothing"),     "gtk-cancel"]
        ]

        AppChooserButton.__init__(self, **descriptor)

        # Fetch preferences for this content type.
        pref_start_app   = self.get_preference(PREF_MEDIA_AUTORUN_X_CONTENT_START_APP)
        pref_ignore      = self.get_preference(PREF_MEDIA_AUTORUN_X_CONTENT_IGNORE)
        pref_open_folder = self.get_preference(PREF_MEDIA_AUTORUN_X_CONTENT_OPEN_FOLDER)
        # If none of the other options are chosen, fallback to asking the user.
        pref_ask = not pref_start_app and not pref_ignore and not pref_open_folder

        if pref_ask:
            self.set_active_custom_item(CUSTOM_ITEM_ASK)
        elif pref_ignore:
            self.set_active_custom_item(CUSTOM_ITEM_DO_NOTHING)
        elif pref_open_folder:
            self.set_active_custom_item(CUSTOM_ITEM_OPEN_FOLDER)

        self.connect("changed", self.on_changed)
        self.connect("custom-item-activated", self.on_custom_item_activated)

    def on_changed(self, button):
        info = button.get_app_info()
        if info:
            self.set_preferences(True, False, False)
            info.set_as_default_for_type(self.get_content_type())

    def on_custom_item_activated(self, button, item):
        if item == CUSTOM_ITEM_ASK:
            self.set_preferences(False, False, False)
        elif item == CUSTOM_ITEM_OPEN_FOLDER:
            self.set_preferences(False, False, True)
        elif item == CUSTOM_ITEM_DO_NOTHING:
            self.set_preferences(False, True, False)

    # Check for existence of this content_type in an autorun-x-content list.
    def get_preference(self, settings_key):
        strv = settings.get_strv(settings_key)
        return strv != None and self.get_content_type() in strv
    # Update an autorun-x-content list to include or not include this content_type.
    def set_preference(self, pref_value, settings_key):
        array = settings.get_strv(settings_key)
        content_type = self.get_content_type()
        array = [ v for v in array if v != content_type ]
        if pref_value:
            array.append(content_type)
        settings.set_strv(settings_key, array)
    # Update all autorun-x-content lists for this content_type.
    def set_preferences(self, pref_start_app, pref_ignore, pref_open_folder):
        self.set_preference(pref_start_app,   PREF_MEDIA_AUTORUN_X_CONTENT_START_APP)
        self.set_preference(pref_ignore,      PREF_MEDIA_AUTORUN_X_CONTENT_IGNORE)
        self.set_preference(pref_open_folder, PREF_MEDIA_AUTORUN_X_CONTENT_OPEN_FOLDER)
