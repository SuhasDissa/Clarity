#!/usr/bin/env python3
# pages/welcome_page.py - Welcome page component

import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw


def create_welcome_page(on_open_clicked):
    """
    Create the welcome/status page.

    Args:
        on_open_clicked: Callback function for open button click

    Returns:
        Adw.StatusPage: The configured welcome page
    """
    welcome_page = Adw.StatusPage()
    welcome_page.set_title("Clarity")
    welcome_page.set_description("Convert documents to Markdown format")
    welcome_page.set_icon_name("document-open-symbolic")

    # Create open button
    open_button = Gtk.Button(label="Open a Document")
    open_button.add_css_class("pill")
    open_button.add_css_class("suggested-action")
    open_button.connect("clicked", on_open_clicked)

    welcome_page.set_child(open_button)

    return welcome_page
