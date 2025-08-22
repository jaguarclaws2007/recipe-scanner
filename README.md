# recipes_app

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
- TWAIN-compatible scanner
- [Python packages](#installation)

## Installation
1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/recipes_app.git
   cd recipes_app
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
   - If you plan to run tests:
     ```sh
     pip install pytest
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

## Testing
Run tests with:
```sh
pytest test_recipe_scanner.py
```

> **Note:** Some tests require a working Tkinter installation and may not run in headless environments.

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
├── __init__.py
├── recipe_scanner.py
├── test_recipe_scanner.py
├── requirements.txt
├── README.md
```

## License
MIT License

---

**Created by [Your Name]**
