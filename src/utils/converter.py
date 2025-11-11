#!/usr/bin/env python3
# utils/converter.py - Document conversion utility

import threading
from gi.repository import GLib


class DocumentConverter:
    """Utility class for converting documents to Markdown."""

    @staticmethod
    def convert_async(file_path, on_success, on_error):
        """
        Convert a document to Markdown asynchronously.

        Args:
            file_path: Path to the file to convert
            on_success: Callback function(markdown_content) called on success
            on_error: Callback function(error_message) called on error
        """
        def convert_thread():
            """Run conversion in a separate thread."""
            try:
                # Import markitdown
                from markitdown import MarkItDown

                # Initialize converter
                md = MarkItDown()

                # Convert file
                result = md.convert(file_path)
                markdown_content = result.text_content

                # Schedule success callback on main thread
                GLib.idle_add(on_success, markdown_content)

            except Exception as e:
                # Schedule error callback on main thread
                GLib.idle_add(on_error, str(e))

        # Run conversion in a separate thread
        thread = threading.Thread(target=convert_thread)
        thread.daemon = True
        thread.start()
