#!/usr/bin/env python3
# pages/welcome_page.py - Welcome page component

import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw


def create_welcome_page(on_open_clicked, on_url_clicked):
    """
    Create the welcome/status page.

    Args:
        on_open_clicked: Callback function for open button click
        on_url_clicked: Callback function for "convert from URL" button click

    Returns:
        Adw.StatusPage: The configured welcome page
    """
    welcome_page = Adw.StatusPage()
    welcome_page.set_title("Clarity")
    welcome_page.set_description(
        "Convert documents, spreadsheets, presentations, images, "
        "audio, web pages and more to Markdown"
    )
    welcome_page.set_icon_name("document-open-symbolic")

    # Button container
    button_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    button_box.set_spacing(10)
    button_box.set_halign(Gtk.Align.CENTER)

    # Create open button
    open_button = Gtk.Button(label="Open a Document")
    open_button.add_css_class("pill")
    open_button.add_css_class("suggested-action")
    open_button.connect("clicked", on_open_clicked)
    button_box.append(open_button)

    # Create "convert from URL" button (YouTube videos, web pages, ...)
    url_button = Gtk.Button(label="Convert from URL")
    url_button.add_css_class("pill")
    url_button.connect("clicked", on_url_clicked)
    button_box.append(url_button)

    welcome_page.set_child(button_box)

    return welcome_page
