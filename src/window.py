# window.py
#
# Copyright 2023 Kónya Márton
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import Gtk, Gdk

@Gtk.Template(resource_path='/com/github/koma52/cubetimer/window.ui')
class CubetimerWindow(Adw.Window):
    __gtype_name__ = 'CubetimerWindow'

    timer_text = Gtk.Template.Child()
    scramble_text = Gtk.Template.Child()
    puzzle_types = Gtk.Template.Child()
    puzzle_type = Gtk.Template.Child()
    puzzle_types_renderer = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        css_widgets = Gtk.CssProvider()
        css_widgets.load_from_resource('/com/github/koma52/cubetimer/gtk/style.css')
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_widgets, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.timer_text.get_style_context().add_class("timer_text")

        #self.puzzle_type.pack_start(self.puzzle_types_renderer, True)
        self.puzzle_type.add_attribute(self.puzzle_types_renderer, 'text', 0)

        #self.puzzle_types.append(["Item 2"])

        #self.asd.set_label("New Label")

