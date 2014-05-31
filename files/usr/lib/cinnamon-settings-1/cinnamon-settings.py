#!/usr/bin/env python

try:
    # i18n
    import gettext
    gettext.install("cinnamon", "/usr/share/cinnamon/locale")

    from gi.repository import Gdk, Gtk

    import CinnamonSettingsWidgets as CSW

    import sys
    import glob
    # Load modules.
    sys.path.append('./modules')
    mod_files = glob.glob('./modules/*.py')
    mod_files.sort()
    if len(mod_files) is 0:
        raise Exception("No settings modules found!!")
    for i in range(len(mod_files)):
        mod_files[i] = mod_files[i].split('/')[-1]
        mod_files[i] = mod_files[i].split('.')[0]
        if mod_files[i][0:3] != "cs_":
            raise Exception("Settings modules must have a prefix of 'cs_' !!")
    modules = map(__import__, mod_files)
except Exception, e:
    print e

CATEGORIES = [
#        Display name                         ID                    Icon
    {"label": _("Appearance"),            "id": "appear",     "icon": "cs-cat-appearance"},
    {"label": _("Preferences"),           "id": "prefs",      "icon": "cs-cat-prefs"},
    {"label": _("Hardware"),              "id": "hardware",   "icon": "cs-cat-hardware"},
    {"label": _("Administration"),        "id": "admin",      "icon": "cs-cat-admin"}
]

WIN_WIDTH = 800
WIN_HEIGHT = 600
WIN_H_PADDING = 20

MIN_LABEL_WIDTH = 16
MAX_LABEL_WIDTH = 25
MIN_PIX_WIDTH = 100
MAX_PIX_WIDTH = 160

class MainWindow:
    categories = {} # Dictionary of all categories, indexed by category ID.

    def __init__(self):
        # Build Settings UI frame.
        builder = Gtk.Builder()
        builder.add_from_file("./cinnamon-settings.ui")
        # Store references to UI components.
        self.window = builder.get_object("main_window")
        self.top_bar = builder.get_object("top_bar")
        self.category_box = builder.get_object("category_box")
        self.category_sw = builder.get_object("category_sw")
        self.category_sw.show_all()
        self.module_box = builder.get_object("module_box")
        self.module_sw = builder.get_object("module_sw")
        self.button_back = builder.get_object("button_back")
        self.button_back.set_label(_("All Settings"))
        self.button_back.hide()

        # Connect search entry.
        self.search_entry = builder.get_object("search_box")
        self.search_entry.connect("changed", self.on_search_entry_changed)
        self.search_entry.connect("icon-press", self.on_search_entry_icon_press)

        # Connect back button.
        self.button_back.connect('clicked', self.on_button_back_clicked)

        # Connect window events.
        self.window.connect("destroy", self.quit)
        self.window.connect("key-press-event", self.on_keypress_event)

        self.window.set_title(_("System Settings"))
        self.window.show()

        builder.connect_signals(self)
        self.window.set_has_resize_grip(False)

#       self.current_sidepage = None
#       self.c_manager = capi.CManager()
#       self.module_box.c_manager = self.c_manager
#       self.bar_heights = 0

        # FIX
        self.min_pix_length = 0
        self.min_label_length = 0

#        for key in self.store.keys():
#            char, pix = self.get_label_min_width(self.store[key])
#            self.min_label_length = max(char, self.min_label_length)
#            self.min_pix_length = max(pix, self.min_pix_length)
#            self.storeFilter[key] = self.store[key].filter_new()
#            self.storeFilter[key].set_visible_func(self.filter_visible_function)

        self.min_label_length += 2
        self.min_pix_length += 4

        self.min_label_length = max(self.min_label_length, MIN_LABEL_WIDTH)
        self.min_pix_length = max(self.min_pix_length, MIN_PIX_WIDTH)

        self.min_label_length = min(self.min_label_length, MAX_LABEL_WIDTH)
        self.min_pix_length = min(self.min_pix_length, MAX_PIX_WIDTH)

        self.create_categories()
        self.create_modules()
        self.update_visibility()

    # Initialisation
    def create_categories(self):
        prev_category = None

        for descriptor in CATEGORIES:
            category = CSW.Category(descriptor, bool(prev_category), self.min_pix_length, self.min_label_length)
            self.category_box.pack_start(category, False, False, 0)
            self.categories[descriptor["id"]] = category

            category.prev = prev_category
            if prev_category:   # Identifies this as the first category.
                prev_category.next = category
                self.current_icon_view = category.gtk_icon_view
            prev_category = category

            # Connect icon_view navigation signals.
            category.gtk_icon_view.connect("item-activated",       self.on_item_activated,       category)
            category.gtk_icon_view.connect("button-release-event", self.on_button_release_event, category)
            category.gtk_icon_view.connect("keynav-failed",        self.on_keynav_failed,        category)
            category.gtk_icon_view.connect("selection-changed",    self.on_selection_changed,    category)

        category.next = None    # Fix last category's list pointers.

        self.category_box.show_all()
    def create_modules(self):
        for i in range(len(modules)):
            try:
                module = modules[i].Module()
            except Exception, e:
                print "Failed to load module %s" % modules[i]
                print e
            module = modules[i].Module()
            if not hasattr(module, "load_check") or module.load_check():
                module.iterator = self.categories[module.category].store.append((module.name, module.icon, module.tooltip, True, module))

    # Helper Methods
    def load_module(self, category, module):    # Load a settings module into the window.
        module = category.store[module][4]
        if not module.stand_alone:
            self.window.set_title(module.name)
            # Hide category interface.
            self.category_sw.hide()
            self.search_entry.hide()
            # First time initialisation?
            if (module.loaded == False):
                print "Loading "+module.name+" module"
                module.widgets = []
                # Construct module's container.
                if hasattr(module, "tabs"):
                    tabs = module.tabs
                    module.tabs = {}
                    notebook = Gtk.Notebook()
                    module.add_widget(notebook)
                    for i in range(len(tabs)):
                        tab = tabs[i]
                        viewport = Gtk.Viewport()
                        scroll_window = Gtk.ScrolledWindow()
                        notebook.append_page(scroll_window, Gtk.Label.new(tab["title"]))
                        scroll_window.add_with_viewport(viewport)
                        module.tabs[tab["id"]] = viewport
                    notebook.expand = True
                else:
                    module.gtk_box = CSW.VBox(indent_children=False)
                    if hasattr(module, "no_background"):
                        background = module.gtk_box
                    else:
                        background = CSW.Background()
                        background.add(module.gtk_box)
                    module.add_widget(background)
                # Call unique module initialisation.
                module.on_module_selected()
                module.loaded = True
            # Fill the module box with the module's widgets.
            for widget in module.widgets:
                self.module_box.add(widget)
            # Show the module interface.
            self.module_box.show_all()
            self.module_sw.show()
            self.button_back.show()
            # Resize?
            m, n = self.module_box.get_preferred_size()
            width = n.width if n.width > WIN_WIDTH else WIN_WIDTH
            bar_height = self.top_bar.get_preferred_size()[1].height
            if hasattr(module, "height"):
                self.window.resize(width, module.height + bar_height + WIN_H_PADDING)
            else:
                self.window.resize(width, n.height + bar_height + WIN_H_PADDING)
        else:
            sidePage.build()
    def close_module(self):                     # Close the current settings module and return to icon view.
        # Reset window.
        self.window.set_title(_("System Settings"))
        self.window.resize(WIN_WIDTH, WIN_HEIGHT)
        self.module_sw.hide()
        # Remove the module interface.
        children = self.module_box.get_children()
        for child in children:
            self.module_box.remove(child)
#           if child.get_name() == "c_box":
#               c_widgets = child.get_children()
#               for c_widget in c_widgets:
#                   c_widget.hide()
        self.button_back.hide()
        # Show category interface.
        self.category_sw.show()
        self.search_entry.show()
        self.search_entry.grab_focus()
    def scroll_to_icon_view(self, icon_view):   # Scroll System Settings to view the current icon_view.
        sel = icon_view.get_selected_items()
        if sel:
            path = sel[0]
            found, rect = icon_view.get_cell_rect(path, None)

            cw = self.category_box.get_window()
            cw_x, cw_y = cw.get_position()

            ivw = icon_view.get_window()
            iv_x, iv_y = ivw.get_position()

            final_y = rect.y + (rect.height / 2) + cw_y + iv_y

            adj = self.category_sw.get_vadjustment()
            page = adj.get_page_size()
            current_pos = adj.get_value()

            if final_y > current_pos + page:
                adj.set_value(iv_y + rect.y)
            elif final_y < current_pos:
                adj.set_value(iv_y + rect.y)
    def update_visibility(self):                # Update the visibility of all categories and modules (matches vs search string).
        text = self.search_entry.get_text().lower()
        for category_id in self.categories:
            category = self.categories[category_id]
            category.visible = False
            # Update visibility flag in store.
            for module in category.store:
                # Does module name or keywords match search string?
                if module[4].name.lower().find(text) > -1 or module[4].keywords.lower().find(text) > -1:
                    module[3] = True
                    category.visible = True
                else:
                    module[3] = False
            # Show this category if any modules match.
            category.show() if category.visible else category.hide()

    # General Navigation
    def on_button_back_clicked(self, widget):                       # Hook back button to return to System Settings.
        self.close_module()
    def on_keypress_event(self, widget, event):                     # Hook backspace to return to System Settings.
        if event.keyval == Gdk.KEY_BackSpace:
            t = type(self.window.get_focus())
            # Ignore all keyboard input widgets.
            if t != Gtk.Entry and t != Gtk.SpinButton and t != Gtk.TreeView:
                self.close_module()
                return True
        return False    
    # Category Navigation
    def on_button_release_event(self, icon_view, event, category):  # Open a module when item is clicked.
        print "button_press()"
        if event.button == 1:
            self.on_item_activated(icon_view, None, category)
    def on_item_activated(self, icon_view, path, category):         # Open a module when item is activated.
        print "on_item_activated()"
        selected_items = icon_view.get_selected_items()
        if len(selected_items) > 0:
            icon_view.unselect_all()
            self.load_module(category, selected_items[0])
    def on_keynav_failed(self, icon_view, direction, category):     # Jump to the previous/next category.
        print "on_keynav_failed()"

        # Search for the first visible .next or .prev category.
        new_category = None
        if direction == Gtk.DirectionType.DOWN:
            new_category = category.next
            while new_category:
                if new_category.visible:
                    break
                new_category = new_category.next
        elif direction == Gtk.DirectionType.UP:
            new_category = category.prev
            while new_category:
                if new_category.visible:
                    break
                new_category = new_category.prev

        if not new_category:
            return False

        dist = 1000
        sel = None

        col = category.get_current_column()
        icon_view = new_category.gtk_icon_view
        model = icon_view.get_model()
        iter = model.get_iter_first()
        if direction == Gtk.DirectionType.DOWN:
            while iter is not None:
                path = model.get_path(iter)
                d = abs(icon_view.get_item_column(path) - col)
                if d < dist:
                    sel = path
                    dist = d
                iter = model.iter_next(iter)
        else:
            while iter is not None:
                path = model.get_path(iter)
                d = abs(icon_view.get_item_column(path) - col)
                if d <= dist:
                    sel = path
                    dist = d
                iter = model.iter_next(iter)

        new_category.select_item(sel)

        return True
    def on_selection_changed(self, icon_view, category):            # Clear previous selection, update current category.
        if self.current_icon_view != icon_view:
            self.current_icon_view.unselect_all()
            self.current_icon_view = icon_view
            self.scroll_to_icon_view(icon_view)

    # Search
    def on_search_entry_changed(self, widget):                      # Update category/module visibility to reflect change in search string.
        self.update_visibility()
    def on_search_entry_icon_press(self, widget, position, event):  # Clear search text.
        if position == Gtk.EntryIconPosition.SECONDARY:
            self.search_entry.set_text("")

    # Gtk.main
    def main(self):
        Gtk.main()
    def quit(self, *args):
        Gtk.main_quit()
    def delete_event(self, widget, event, data=None):
        return False

if __name__ == "__main__":
    import signal
    signal.signal(signal.SIGINT, MainWindow().quit)
    Gtk.main()

