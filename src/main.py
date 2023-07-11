# main.py
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

import sys
import gi
import datetime

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw, GLib
from .window import CubetimerWindow
from cubescrambler import scrambler222, scrambler333, scrambler444


class CubetimerApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='com.github.koma52.cubetimer',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('export', self.on_export_action)
        self.create_action('start_timer', self.on_key_press_event, ['space'])
        #self.create_action('type_changed', self.on_type_changed)

        # Create a timer that updates the label every second
        self.timer_id = None
        self.start_time = None

        #self.builder = Gtk.Builder()
        #self.builder.add_from_resource('/com/github/koma52/cubetimer/window.ui')

    def generate_scramble(self, p_type):
        if p_type == "2x2x2":
            return scrambler222.get_WCA_scramble()
        elif p_type == "3x3x3":
            return scrambler333.get_WCA_scramble()
        elif p_type == "4x4x4":
            return scrambler444.get_random_state_scramble()

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = CubetimerWindow(application=self)
        win.present()

        self.timer_text = win.timer_text
        self.scramble_text = win.scramble_text
        self.puzzle_type = win.puzzle_type
        self.puzzle_type.connect("changed", self.on_type_changed)

        self.scramble_text.set_label(f"Scramble: {self.generate_scramble(str(self.get_active_type()))}")

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='Cube Timer',
                                application_icon='com.github.koma52.cubetimer',
                                developer_name='Kónya Márton',
                                version='0.1.0',
                                developers=['Kónya Márton'],
                                copyright='© 2023 Kónya Márton')
        about.present()

    def get_active_type(self):
        active_type_index = self.puzzle_type.get_active()
        if active_type_index != -1:
            active_type = self.puzzle_type.get_model()[active_type_index][0]
        else:
            return None

        return active_type

    def on_type_changed(self, widget):
        active_type = self.get_active_type()

        self.scramble_text.set_label(f"Scramble: {self.generate_scramble(str(active_type))}")

    def on_export_action(self, widget, _):
        """Callback for the app.preferences action."""
        print('app.export action activated')

    def start_timer(self):
        if self.timer_id is None:
            self.start_time = datetime.datetime.now()
            self.timer_id = GLib.timeout_add(10, self.update_label)

    def stop_timer(self):
        if self.timer_id is not None:
            GLib.source_remove(self.timer_id)
            self.timer_id = None
            self.start_time = None

    def update_label(self):
        elapsed_time = datetime.datetime.now() - self.start_time
        elapsed_time_str = (datetime.datetime(1900, 1, 1) + elapsed_time).strftime("%M:%S.%f")[:-3]
        self.timer_text.set_text(elapsed_time_str)
        return True

    def on_key_press_event(self, widget, event):
        if self.timer_id is None:
            self.start_timer()
        else:
            self.stop_timer()

            active_type = self.get_active_type()
            self.scramble_text.set_label(f"Scramble: {self.generate_scramble(str(active_type))}")

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = CubetimerApplication()
    return app.run(sys.argv)
