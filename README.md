# Clarity

A modern desktop application for converting various document formats to Markdown.

## Features

- Convert documents to Markdown format
- Support for multiple formats: DOCX, PDF, PPTX, XLSX, HTML, and more
- Modern and adaptive user interface built with GTK 4 and Libadwaita
- Powered by Microsoft's markitdown library

## Requirements

- Python 3
- GTK 4
- Libadwaita
- PyGObject
- markitdown library

## Installation

### Running from source

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make main.py executable:
```bash
chmod +x main.py
```

3. Run the application:
```bash
./main.py
```

### Building with Flatpak

1. Install flatpak-builder:
```bash
# On Ubuntu/Debian
sudo apt install flatpak-builder

# On Fedora
sudo dnf install flatpak-builder
```

2. Build the Flatpak:
```bash
flatpak-builder --force-clean --install --user build-dir top.suhasdissa.Clarity.yml
```

3. Run the Flatpak:
```bash
flatpak run top.suhasdissa.Clarity
```

## Usage

1. Click "Open a Document" to select a file
2. Choose the document you want to convert
3. Click "Convert to Markdown"
4. Choose where to save the converted Markdown file

## License

GPL-3.0-or-later

## Credits

- Built with GTK 4 and Libadwaita
- Conversion powered by [markitdown](https://github.com/microsoft/markitdown)
