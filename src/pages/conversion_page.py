#!/usr/bin/env python3
# pages/conversion_page.py - Conversion page component

import os
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw


class ConversionPage(Gtk.Box):
    """Conversion page with file info and convert button."""

    def __init__(self, on_convert_clicked, on_open_another_clicked):
        """
        Initialize conversion page.

        Args:
            on_convert_clicked: Callback function for convert button click
            on_open_another_clicked: Callback function for open another file button click
        """
        super().__init__(orientation=Gtk.Orientation.VERTICAL)

        self.set_valign(Gtk.Align.CENTER)
        self.set_halign(Gtk.Align.FILL)
        self.set_margin_top(20)
        self.set_margin_bottom(20)
        self.set_margin_start(20)
        self.set_margin_end(20)
        self.set_spacing(20)

        # Create preferences group for file info
        self.file_group = Adw.PreferencesGroup()
        self.file_group.set_title("Selected File")

        self.file_row = Adw.ActionRow()
        self.file_row.set_title("No file selected")
        self.file_group.add(self.file_row)

        self.append(self.file_group)

        # Create button box
        button_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        button_box.set_spacing(10)
        button_box.set_halign(Gtk.Align.CENTER)

        # Create convert button
        self.convert_button = Gtk.Button(label="Convert & Preview")
        self.convert_button.add_css_class("pill")
        self.convert_button.add_css_class("suggested-action")
        self.convert_button.connect("clicked", on_convert_clicked)
        button_box.append(self.convert_button)

        # Create spinner
        self.spinner = Gtk.Spinner()
        self.spinner.set_size_request(32, 32)
        self.spinner.set_visible(False)
        button_box.append(self.spinner)

        # Create "Open Another File" button
        another_file_button = Gtk.Button(label="Open Another File")
        another_file_button.add_css_class("pill")
        another_file_button.connect("clicked", on_open_another_clicked)
        button_box.append(another_file_button)

        self.append(button_box)

    def update_file_info(self, file_path):
        """
        Update the displayed file information.

        Args:
            file_path: Path to the selected file
        """
        if file_path:
            self.file_row.set_title(os.path.basename(file_path))
            self.file_row.set_subtitle(file_path)

    def set_converting(self, is_converting):
        """
        Set the converting state (show/hide spinner, enable/disable button).

        Args:
            is_converting: True if conversion is in progress
        """
        if is_converting:
            self.spinner.set_visible(True)
            self.spinner.start()
            self.convert_button.set_sensitive(False)
        else:
            self.spinner.stop()
            self.spinner.set_visible(False)
            self.convert_button.set_sensitive(True)
