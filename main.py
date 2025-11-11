#!/usr/bin/env python3
# main.py - Entry point for Clarity application

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from src.application import ClarityApplication


def main():
    """Run the application."""
    app = ClarityApplication()
    return app.run(sys.argv)


if __name__ == '__main__':
    sys.exit(main())
