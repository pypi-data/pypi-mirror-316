# Gtk-Stream : A stream-based GUI protocol
# Copyright (C) 2024  Marc Coiffier
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
from . import Gtk, GLib, Gdk
from .common import printEvent
from .properties import parse_property, get_prop_type

class GtkStreamApp(Gtk.Application):
    def __init__(self, logger, name = None, **kwargs):
        super().__init__(**kwargs)
        self.logger = logger
        if name != None:
            GLib.set_application_name(name)
        self.namedWidgets = { }
        self.namedWindows = { }
        
        self.callback_queue = []

        def run_when_idle_before_startup(cb):
            self.callback_queue.append(cb)
        self.run_when_idle = run_when_idle_before_startup
        
        def on_startup(_):
            for cb in self.callback_queue:
                GLib.idle_add(cb)
            self.run_when_idle = GLib.idle_add
        self.connect('startup', on_startup)
        
    def nameWidget(self, id, w):
        if id is not None:
            self.namedWidgets[id] = w

    def openFileDialog(self, id, parent):
        def cb():
            dialog = Gtk.FileDialog()
            dialog.props.modal = True
            def on_choose(_, b):
                try:
                    file = dialog.open_finish(b)
                    print(f"{id}:selected:{file.get_path()}")
                    sys.stdout.flush()
                except GLib.GError as e:
                    print(f"{id}:none-selected")
                    sys.stdout.flush()
                    
            dialog.open(parent = self.namedWindows[parent], callback = on_choose)
        self.run_when_idle(cb)
    def newWindow(self, document, id, title = "Window", width = None, height = None):
        def cb():
            win = Gtk.Window(application=self)
            win.set_title(title)
            if width != None and height != None:
                win.set_default_size(int(width), int(height))
            self.namedWindows[id] = win
            win.set_child(document.render())
            win.connect('close-request', printEvent(self.logger, 'close-request', id))
            win.present()
            return False
        self.run_when_idle(cb)
    def addStyle(self, style):
        def cb():
            provider = Gtk.CssProvider()
            provider.load_from_data(style)
            Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.run_when_idle(cb)
    def closeWindow(self, id):
        def cb():
            self.namedWindows[id].close()
        self.run_when_idle(cb)
    def removeWidget(self, id):
        def cb():
            w = self.namedWidgets[id]
            w.get_parent().remove(w)
        self.run_when_idle(cb)
    def insertWidget(self, to, document):
        def cb():
            if to in self.namedWidgets:
                w = self.namedWidgets[to]
                w.insert_child(document)
            else:
                raise Exception(f"Error: unknown widget id '{to}'")
        self.run_when_idle(cb)
    def setProp(self, id, name, value):
        def cb():
            w = self.namedWidgets[id]
            w.set_property(name, parse_property(get_prop_type(w.__class__, name), value)(self))
        self.run_when_idle(cb)
