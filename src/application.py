#!/usr/bin/env python3
# application.py - Main application class

import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw
from src.window import ClarityWindow


class ClarityApplication(Adw.Application):
    """Main application class for Clarity."""

    def __init__(self):
        super().__init__(
            application_id='top.suhasdissa.Clarity',
            flags=0
        )

    def do_activate(self):
        """Called when the application is activated."""
        win = self.props.active_window
        if not win:
            win = ClarityWindow(application=self)
        win.present()
