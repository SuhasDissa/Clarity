#!/usr/bin/env python3
# window.py - Main application window

from pathlib import Path
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw

from src.pages import create_welcome_page, ConversionPage, PreviewPage
from src.utils import DocumentConverter


class ClarityWindow(Adw.ApplicationWindow):
    """Main application window for Clarity."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.selected_file = None
        self.markdown_content = None

        # Set window properties
        self.set_title("Clarity")
        self.set_default_size(600, 400)

        # Create main box
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # Create header bar
        self.header_bar = Adw.HeaderBar()
        self.main_box.append(self.header_bar)

        # Create main content area
        self.content_stack = Gtk.Stack()
        self.content_stack.set_vexpand(True)
        self.main_box.append(self.content_stack)

        # Create pages
        self._create_pages()

        # Show welcome page initially
        self.content_stack.set_visible_child_name("welcome")

        # Create toast overlay and set as window content
        self.toast_overlay = Adw.ToastOverlay()
        self.toast_overlay.set_child(self.main_box)
        self.set_content(self.toast_overlay)

    def _create_pages(self):
        """Create all pages and add them to the stack."""
        # Create welcome page
        self.welcome_page = create_welcome_page(on_open_clicked=self.on_open_file_clicked)
        self.content_stack.add_named(self.welcome_page, "welcome")

        # Create conversion page
        self.conversion_page = ConversionPage(
            on_convert_clicked=self.on_convert_clicked,
            on_open_another_clicked=self.on_open_file_clicked
        )
        self.content_stack.add_named(self.conversion_page, "conversion")

        # Create preview page
        self.preview_page = PreviewPage(
            on_back_clicked=self.on_back_from_preview,
            on_save_clicked=lambda btn: self.open_save_dialog()
        )
        self.content_stack.add_named(self.preview_page, "preview")

    def on_open_file_clicked(self, button):
        """Handle open file button click."""
        dialog = Gtk.FileChooserDialog(
            title="Open a Document",
            action=Gtk.FileChooserAction.OPEN,
            transient_for=self,
            modal=True
        )

        dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("_Open", Gtk.ResponseType.ACCEPT)

        # Add file filters
        filter_all = Gtk.FileFilter()
        filter_all.set_name("All Supported Documents")
        filter_all.add_pattern("*.docx")
        filter_all.add_pattern("*.pdf")
        filter_all.add_pattern("*.pptx")
        filter_all.add_pattern("*.xlsx")
        filter_all.add_pattern("*.html")
        filter_all.add_pattern("*.txt")
        dialog.add_filter(filter_all)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("All Files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

        dialog.connect("response", self.on_open_response)
        dialog.show()

    def on_open_response(self, dialog, response):
        """Handle file chooser response."""
        if response == Gtk.ResponseType.ACCEPT:
            file = dialog.get_file()
            if file:
                self.selected_file = file.get_path()
                self.conversion_page.update_file_info(self.selected_file)
                self.content_stack.set_visible_child_name("conversion")

        dialog.destroy()

    def on_convert_clicked(self, button):
        """Handle convert button click."""
        if not self.selected_file:
            self.show_toast("No file selected")
            return

        # Show spinner and disable button
        self.conversion_page.set_converting(True)

        # Run conversion asynchronously
        DocumentConverter.convert_async(
            self.selected_file,
            on_success=self.on_conversion_success,
            on_error=self.on_conversion_error
        )

    def on_conversion_success(self, markdown_content):
        """
        Handle successful conversion (runs on main thread).

        Args:
            markdown_content: The converted markdown text
        """
        # Store the markdown content
        self.markdown_content = markdown_content

        # Hide spinner and enable button
        self.conversion_page.set_converting(False)

        # Show preview
        self.show_preview()

    def on_conversion_error(self, error_message):
        """
        Handle conversion error (runs on main thread).

        Args:
            error_message: The error message
        """
        # Hide spinner and enable button
        self.conversion_page.set_converting(False)

        # Show error toast
        self.show_toast(f"Conversion failed: {error_message}")

        # Show error dialog
        dialog = Adw.MessageDialog(
            transient_for=self,
            modal=True,
            heading="Conversion Failed",
            body=f"An error occurred during conversion:\n\n{error_message}"
        )
        dialog.add_response("ok", "OK")
        dialog.set_default_response("ok")
        dialog.show()

    def show_preview(self):
        """Show the markdown preview."""
        if self.markdown_content:
            # Set the content in the preview page
            self.preview_page.set_content(self.markdown_content)

            # Switch to preview page
            self.content_stack.set_visible_child_name("preview")

    def on_back_from_preview(self, button):
        """Handle back button from preview."""
        self.content_stack.set_visible_child_name("conversion")

    def open_save_dialog(self):
        """Open file save dialog."""
        dialog = Gtk.FileChooserDialog(
            title="Save Markdown File",
            action=Gtk.FileChooserAction.SAVE,
            transient_for=self,
            modal=True
        )

        dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("_Save", Gtk.ResponseType.ACCEPT)

        # Set default filename
        if self.selected_file:
            original_name = Path(self.selected_file).stem
            dialog.set_current_name(f"{original_name}.md")
        else:
            dialog.set_current_name("document.md")

        # Add markdown filter
        filter_md = Gtk.FileFilter()
        filter_md.set_name("Markdown Files")
        filter_md.add_pattern("*.md")
        dialog.add_filter(filter_md)

        dialog.connect("response", self.on_save_response)
        dialog.show()

    def on_save_response(self, dialog, response):
        """Handle save dialog response."""
        if response == Gtk.ResponseType.ACCEPT:
            file = dialog.get_file()
            if file and self.markdown_content:
                try:
                    save_path = file.get_path()
                    with open(save_path, 'w', encoding='utf-8') as f:
                        f.write(self.markdown_content)

                    self.show_toast("Conversion successful!")

                except Exception as e:
                    self.show_toast(f"Error saving file: {str(e)}")

        dialog.destroy()

    def show_toast(self, message):
        """Show a toast notification."""
        toast = Adw.Toast(title=message)
        toast.set_timeout(3)
        self.toast_overlay.add_toast(toast)
