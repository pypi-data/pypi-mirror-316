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

from ... import Gtk
from ...common import printEvent
from .. import Document

class Button(Document):
    __g_class__ = Gtk.Button
    def __init__(self, app, id, **kwargs):
        super().__init__(app, id = id, **kwargs)
    def render_raw(self):
        button = Gtk.Button()
        button.connect('clicked', printEvent(self.app.logger, 'clicked', self.id))
        return button
    def insert_child(self, w, d):
        w.set_child(d.render())

class LinkButton(Button):
    __g_class__ = Gtk.LinkButton
    def __init__(self, app, id, **kwargs):
        super().__init__(app, id=id, **kwargs)
    def render_raw(self):
        button = Gtk.LinkButton()
        button.connect('activate-link', printEvent(self.app.logger, 'clicked', self.id, True))
        return button
    def insert_child(self, w, d):
        w.set_child(d.render())
