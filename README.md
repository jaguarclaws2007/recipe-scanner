# Recipe Scanner

A simple desktop application for scanning, organizing, and saving recipes as PDFs. Built with Python, Tkinter, and FPDF.

## Features
- Scan single or double-sided recipe sheets using a TWAIN-compatible scanner
- Organize recipes by category (Cake, Cookie, Bread, etc.)
- Save scanned recipes as PDFs
- Browse and open saved recipes from the app
- Remembers your last used folder

## Requirements
- Python 3.7+
- Windows OS (TWAIN scanning)
- TWAIN-compatible scanner (I am using the [Epson ES-50](https://epson.com/For-Home/Scanners/Document-Scanners/WorkForce-ES-50-Portable-Document-Scanner/p/B11B252201))
- [Python packages](#installation)

## Installation
1. **Clone the repository:**
   ```sh
   git clone https://github.com/jaguarclaws2007/recipes_app.git
   cd recipes_app
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Ensure your Python installation includes Tkinter.**
   - On Windows, install Python with the "tcl/tk and IDLE" option enabled.

## Usage
Run the app with:
```sh
python recipe_scanner.py
```

- Click **Browse** to select or create a folder for your recipes.
- Click **New Recipe** to scan and save a new recipe.
- Double-click files in the browser to open them.


## Packaging for Windows
To create a standalone executable (optional):
```sh
pip install pyinstaller
pyinstaller --onefile recipe_scanner.py
```
The executable will be in the `dist/` folder.

## File Structure
```
recipes_app/
├── recipe_scanner.py
├── requirements.txt
├── README.md
```

## License
# MIT License

**Copyright (c) 2025 Corbin Mounteer**

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
