#!/usr/bin/env python3
# pages/preview_page.py - Preview page component

import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw


class PreviewPage(Gtk.Box):
    """Markdown preview page."""

    def __init__(self, on_back_clicked, on_save_clicked):
        """
        Initialize preview page.

        Args:
            on_back_clicked: Callback function for back button click
            on_save_clicked: Callback function for save button click
        """
        super().__init__(orientation=Gtk.Orientation.VERTICAL)

        self.set_spacing(0)

        # Create toolbar for preview page
        preview_toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        preview_toolbar.set_spacing(10)
        preview_toolbar.set_margin_top(10)
        preview_toolbar.set_margin_bottom(10)
        preview_toolbar.set_margin_start(10)
        preview_toolbar.set_margin_end(10)

        # Back button
        back_button = Gtk.Button()
        back_button.set_icon_name("go-previous-symbolic")
        back_button.set_tooltip_text("Back to conversion")
        back_button.connect("clicked", on_back_clicked)
        preview_toolbar.append(back_button)

        # Spacer
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        preview_toolbar.append(spacer)

        # Save button
        save_button = Gtk.Button(label="Save")
        save_button.add_css_class("suggested-action")
        save_button.connect("clicked", on_save_clicked)
        preview_toolbar.append(save_button)

        self.append(preview_toolbar)

        # Create scrolled window for markdown content
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_hexpand(True)

        # Create text view for markdown
        self.preview_text = Gtk.TextView()
        self.preview_text.set_editable(False)
        self.preview_text.set_cursor_visible(False)
        self.preview_text.set_wrap_mode(Gtk.WrapMode.WORD)
        self.preview_text.set_margin_top(10)
        self.preview_text.set_margin_bottom(10)
        self.preview_text.set_margin_start(10)
        self.preview_text.set_margin_end(10)

        # Set monospace font for markdown
        self.preview_text.add_css_class("monospace")

        scrolled.set_child(self.preview_text)
        self.append(scrolled)

    def set_content(self, markdown_content):
        """
        Set the markdown content to display.

        Args:
            markdown_content: The markdown text to display
        """
        if markdown_content:
            buffer = self.preview_text.get_buffer()
            buffer.set_text(markdown_content)
