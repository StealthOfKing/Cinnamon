#!/usr/bin/env python

import CinnamonSettingsWidgets as CSW
from functools import partial
from gi.repository import Gio, Gtk
import subprocess   # Used to query alternatives to x-terminal-emulator.

PREF_CONTENT_TYPE = 0
PREF_GEN_CONTENT_TYPE = 1
PREF_LABEL = 2

DEF_CONTENT_TYPE = 0
DEF_LABEL = 1
DEF_HEADING = 2

#TODO: Add mnemonic once we are out of M16 release to preserve i18n for now
preferred_app_defs = [
    { "label" : _("_Mail"  ), "content_type" : "x-scheme-handler/mailto", "also" : ["x-scheme-handler/mailto"] },
    { "label" : _("Te_xt"  ), "content_type" : "text/plain",              "also" : ["text"                   ] },
    { "label" : _("M_usic" ), "content_type" : "audio/x-vorbis+ogg",      "also" : ["audio"                  ] },
    { "label" : _("_Video" ), "content_type" : "video/x-ogm+ogg",         "also" : ["video"                  ] },
    { "label" : _("_Photos"), "content_type" : "image/jpeg",              "also" : ["image"                  ] }
]

removable_media_defs = [
{ "label" : _("CD _audio"    ), "heading" : _("Select an application for audio CDs"                          ), "content_type" : "x-content/audio-cdda"    },
{ "label" : _("_DVD video"   ), "heading" : _("Select an application for video DVDs"                         ), "content_type" : "x-content/video-dvd"     },
{ "label" : _("_Music player"), "heading" : _("Select an application to run when a music player is connected"), "content_type" : "x-content/audio-player"  },
{ "label" : _("_Photos"      ), "heading" : _("Select an application to run when a camera is connected"      ), "content_type" : "x-content/image-dcf"     },
{ "label" : _("_Software"    ), "heading" : _("Select an application for software CDs"                       ), "content_type" : "x-content/unix-software" }
]

# Some terminal emulators are designed to be launched via a wrapper (for
# example, gnome-terminal reports its primary installation path as
# "/usr/bin/gnome-terminal.wrapper"). This list is not that specific,
# the TerminalChooserButton strips /usr/bin/ and .wrapper when
# identifying x-terminal-emulators.
terminal_defs = {
    # gnome-terminal
    "gnome-terminal" : { "label" : "GNOME Terminal",  "icon" : "utilities-terminal" },
    #lxterminal
    "lxterminal"     : { "label" : "LXTerminal",      "icon" : "lxterminal"         },
    # uxterm
    "uxterm"         : { "label" : "XTerm (Unicode)", "icon" : "xterm-color"        },
    "koi8rxterm"     : { "label" : "XTerm (Russian)", "icon" : "xterm-color"        },
    "lxterm"         : { "label" : "XTerm (any)",     "icon" : "xterm-color"        },
    "xterm"          : { "label" : "XTerm",           "icon" : "xterm-color"        }
}

other_defs = {
    # translators: these strings are duplicates of shared-mime-info
    # strings, just here to fix capitalization of the English originals.
    # If the shared-mime-info translation works for your language,
    # simply leave these untranslated.
    "x-content/audio-dvd"       : _("audio DVD"),
    "x-content/blank-bd"        : _("blank Blu-ray disc"),
    "x-content/blank-cd"        : _("blank CD disc"),
    "x-content/blank-dvd"       : _("blank DVD disc"),
    "x-content/blank-hddvd"     : _("blank HD DVD disc"),
    "x-content/video-bluray"    : _("Blu-ray video disc"),
    "x-content/ebook-reader"    : _("e-book reader"),
    "x-content/video-hddvd"     : _("HD DVD video disc"),
    "x-content/image-picturecd" : _("Picture CD"),
    "x-content/video-svcd"      : _("Super Video CD"),
    "x-content/video-vcd"       : _("Video CD"),
    "x-content/win32-software"  : _("Windows software"),
    "x-content/software"        : _("Software")
}

class Module(CSW.Module):
    id = "default"
    name = _("Preferred Applications")
    tooltip = _("Preferred Applications")
    keywords = _("media, defaults, applications, programs, removable, browser, email, calendar, music, videos, photos, images, cd, autostart, autoplay")
    icon = "cs-default-applications"
    category = "prefs"
    height = 300
    tabs = [
        { "id":"preferred",       "title":_("Preferred Applications") },
        { "id":"removable_media", "title":_("Removable Media") }
    ]

    def on_module_selected(self):
        self.tabs["preferred"].add(
            CSW.Section(
                CSW.Label(
                    markup = "<b>%s</b>" % _("Select preferred applications for file types"),
                    align  = [0.5,0.5],
                    margin = [0,0,8,0]
                ),
                align           = [0.5,0],
                indent_children = False
            ).add(
                # For web, we need to support text/html, application/xhtml+xml and x-scheme-handler/https...
                CSW.VBox(lock_widths=2).add(
                    *[ CSW.AppChooserButton(
                        label        = app_def["label"],
                        content_type = app_def["content_type"],
                        also         = app_def["also"]
                    ) for app_def in preferred_app_defs ]
                ).add(
                    TerminalChooserButton(
                        label   = _("_Terminal"),
                        setting = "org.cinnamon.desktop.default-applications.terminal/exec",
                        heading = _("Select a terminal emulator")
                    )
                )
            )
        )
        self.tabs["removable_media"].add(
            CSW.Section(
                CSW.Label(
                    markup = "<b>%s</b>" % _("Select how media should be handled"),
                    align  = [0.5,0.5],
                    margin = [0,0,8,0]
                ),
                lock_widths     = 0,
                indent_children = False
            ).add(
                CSW.VBox(
                    depends     = ["!org.cinnamon.desktop.media-handling/autorun-never"],
                    align       = [0.5,0],
                    lock_widths = 2
                ).add(
                    *[ CSW.MediaAppChooserButton(
                        label        = media_def["label"],
                        heading      = media_def["heading"],
                        content_type = media_def["content_type"]
                    ) for media_def in removable_media_defs ]
                ).add(
                    CSW.Button(
                        text    = _("_Other Media..."),
                        clicked = self.on_other_media_clicked
                    )
                ),
                CSW.CheckButton(
                    setting = "org.cinnamon.desktop.media-handling/autorun-never",
                    label   = _("_Never prompt or start programs on media insertion")
                )
            )
        )

    def on_other_media_clicked(self, button, widget):
        if not hasattr(self, "other_type_dialog"):
            self.other_type_dialog = OtherTypeDialog()
        self.other_type_dialog.open(widget.get_toplevel())

class TerminalChooserButton(CSW.AppChooserButton):
    def __init__(self, **descriptor):
        # Setup terminal chooser...
        terminals = subprocess.check_output(["update-alternatives", "--list", "x-terminal-emulator"]).split('\n')[:-1]  # Find which terminal packages are installed.
        # Build terminal chooser's options.
        found_def = False
        for i in range(len(terminals)):
            terminal = terminals[i]
            name = terminal.split('/')[-1].split('.')[0]    # Strip /usr/bin/ .wrapper.
            if name in terminal_defs:   # Look for terminal definition.
                terminal_def = terminal_defs[name]
                terminals[i] = [terminal, terminal_def["label"], terminal_def["icon"]]
            else:   # Unknown terminal, warn + fallback.
                print "unknown terminal emulator {0} ({1})".format(terminal, name)
                terminals[i] = [terminal, name, "utilities-terminal"]

        descriptor["options"] = terminals

        CSW.AppChooserButton.__init__(self, **descriptor)

    def set_value(self, value):
        value = value.split('/')[-1].split('.')[0]
        model = self.gtk_widget.get_model()
        for row in model:
            if value == row[1].split('/')[-1].split('.')[0]:
                self.gtk_widget.set_active_custom_item(row[1])
                return

class OtherTypeDialog(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self,
            title = _("Other Media"),
            transient_for = None,
            flags = 0
        )
        self.add_button(_("Close"), Gtk.ResponseType.OK)
        self.set_default_size(350, 100)

        self.section = CSW.Section(
            CSW.Label(
                markup      = "<b>%s</b>" % _("Select how other media should be handled"),
                align       = [0.5,0.5],
                margin      = [0,0,8,0]
            ),
            align       = [0.5,0.5],
            lock_widths = 2
        )
        # Type combo box for choosing the removable media type to configure.
        self.type_combo_box = CSW.ComboBox(
            label   = _("_Type"),
            options = [
                [content_type, self.get_description(content_type)]
                for content_type in Gio.content_types_get_registered()
                if self.accept_content_type(content_type)
            ],
            alphabetical = True,
            changed      = self.on_type_changed
        )
        self.section.add(self.type_combo_box)
        self.get_content_area().add(self.section)
        # Placeholder for combo box.
        class Pass: pass
        self.application_combo_box = Pass()
        # on_type_changed() needs application_combo_box.destroy().
        self.application_combo_box.destroy = lambda:None
        self.type_combo_box.gtk_widget.set_active(0)

    def accept_content_type(self, content_type):    # Include this content_type in dialog?
        if not content_type.startswith("x-content/"):
            return False
        for media_def in removable_media_defs:  
            if Gio.content_type_is_a(content_type, media_def["content_type"]):
                return False
        return True
    def get_description(self, content_type):    # Fetch description for content_type (with maintenance error check).
        if content_type in other_defs:
            return other_defs[content_type]
        else:
            print "Content type '%s' is missing from the info panel" % content_type

    def open(self, topLevel):
        self.set_transient_for(topLevel)
        self.set_modal(True)
        self.connect("response", self.on_response)
        self.present()
        self.show_all()

    def on_response(self, dialog, response):
        self.hide()

    def on_type_changed(self, combo_box, widget):
        content_type = combo_box.get_value()

        # There is no set_content_type for Gtk.AppChooserButton, so we
        # cannot reuse this widget.
        self.application_combo_box.destroy()
        self.application_combo_box = CSW.MediaAppChooserButton(
            label        = _("_Action:"),
            content_type = content_type,
            heading      = other_defs[content_type]
        )
        self.application_combo_box.show_all()

        self.section.add(self.application_combo_box)

