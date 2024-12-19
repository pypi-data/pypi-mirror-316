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

import io
import xml.sax as sax
import signal
import sys

from .parser import GtkStreamXMLHandler
from . import GLib

class GtkStreamErrorHandler(sax.handler.ErrorHandler):
    def error(self, exc):
        print("Error", file=sys.stderr)
        raise exc
    def fatalError(self, exc):
        print("Fatal error", file=sys.stderr)
        raise exc

def main():
    handler = GtkStreamXMLHandler()
    errHandler = GtkStreamErrorHandler()
    parser = sax.make_parser()
    parser.setContentHandler(handler)
    parser.setErrorHandler(errHandler)
    try:
        parser.parse(io.FileIO(0, 'r', closefd=False))
    except Exception as e:
        def quit():
            handler.app.quit()
        GLib.idle_add(quit)
        print(f"Done with exception : {e}\n", file=sys.stderr)
