import os
import json
from io import BytesIO
import twain # pyright: ignore[reportMissingImports]
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
from fpdf import FPDF # pyright: ignore[reportMissingModuleSource]
import PIL.Image
from PIL import Image
import PIL.ImageTk

class RecipeScannerApp:
    CONFIG_FILE = os.path.expanduser("~/.recipe_scanner_config.json")

    def __init__(self, root):
        self.root = root
        self.root.title("Recipe Scanner")
        self.root.geometry("600x400")
        self.save_path = self.load_last_path() or os.path.abspath("Recipes")
        self.setup_home()

        self.selected_source_name = None  # store the scanner source name

    def load_last_path(self):
        try:
            with open(self.CONFIG_FILE, "r") as f:
                data = json.load(f)
            path = data.get("last_path")
            if path and os.path.exists(path):
                return path
        except Exception:
            pass
        return None

    def save_last_path(self, path):
        try:
            with open(self.CONFIG_FILE, "w") as f:
                json.dump({"last_path": path}, f)
        except Exception:
            pass

    def setup_home(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Path selection
        path_frame = tk.Frame(self.root)
        path_frame.pack(fill=tk.X, pady=10, padx=10)
        tk.Label(path_frame, text="Save/View Path:").pack(side=tk.LEFT)
        self.path_var = tk.StringVar(value=self.save_path)
        path_entry = tk.Entry(path_frame, textvariable=self.path_var, width=50)
        path_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(path_frame, text="Browse", command=self.browse_path).pack(side=tk.LEFT)

        # File browser
        browser_frame = tk.LabelFrame(self.root, text="Recipes in Path")
        browser_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


        self.tree = ttk.Treeview(browser_frame)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.heading("#0", text="Files/Folders", anchor=tk.W)
        self.tree.bind("<Double-1>", self.on_tree_double_click)
        self.populate_tree()

        # New Recipe button
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="New Recipe", font=("Arial", 14), command=self.start_new_recipe).pack()

    def browse_path(self):
        path = filedialog.askdirectory(initialdir=self.save_path, title="Select Recipe Folder")
        if path:
            self.save_path = path
            self.path_var.set(path)
            self.save_last_path(path)
            self.populate_tree()


    def populate_tree(self):
        self.tree.delete(*self.tree.get_children())
        path = self.path_var.get()
        if not os.path.exists(path):
            os.makedirs(path)
        self._insert_tree_items('', path)

    def _insert_tree_items(self, parent, path):
        # Insert folders first, then files, sorted alphabetically
        items = sorted(os.listdir(path))
        for item in items:
            abspath = os.path.join(path, item)
            if os.path.isdir(abspath):
                node = self.tree.insert(parent, 'end', text=f"📁 {item}", open=False, values=[abspath])
                # Insert a dummy child to show expand arrow
                if os.listdir(abspath):
                    self.tree.insert(node, 'end')
            else:
                self.tree.insert(parent, 'end', text=f"📄 {item}", values=[abspath])

    def on_tree_double_click(self, event):
        item_id = self.tree.focus()
        if not item_id:
            return
        abspath = self.tree.item(item_id, 'values')
        if not abspath:
            return
        abspath = abspath[0]
        if os.path.isdir(abspath):
            # Expand/collapse folder
            if self.tree.item(item_id, 'open'):
                self.tree.item(item_id, open=False)
                self.tree.delete(*self.tree.get_children(item_id))
                # Re-insert dummy if needed
                if os.listdir(abspath):
                    self.tree.insert(item_id, 'end')
            else:
                self.tree.item(item_id, open=True)
                self.tree.delete(*self.tree.get_children(item_id))
                self._insert_tree_items(item_id, abspath)
        else:
            try:
                os.startfile(abspath)
            except Exception as e:
                messagebox.showerror("Open File", f"Could not open file:\n{abspath}\n\n{e}")

    def start_new_recipe(self):
        # If scanner not selected, prompt for it once per session
        if not self.selected_source_name:
            try:
                import twain
                with twain.SourceManager() as sm:
                    src = sm.open_source()  # show selection dialog
                    if src:
                        self.selected_source_name = src.GetSourceName()
            except Exception as e:
                messagebox.showerror("Scanner Error", f"Could not select scanner: {e}")
                return
        RecipeDialog(self.root, self.save_path, on_done=self.on_recipe_done, selected_source_name=self.selected_source_name)

    def on_recipe_done(self):
        self.populate_tree()

class RecipeDialog:
    def show_scan_preview(self, image_path, side_label="Scanned Image"):
        preview = tk.Toplevel(self.win)
        preview.title(f"Preview - {side_label}")
        preview.geometry("600x800")
        preview.grab_set()

        img = Image.open(image_path)
        # Resize for preview window if needed
        max_w, max_h = 550, 700
        w, h = img.size
        scale = min(max_w / w, max_h / h, 1.0)
        img_disp = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
        tk_img = PIL.ImageTk.PhotoImage(img_disp)

        label = tk.Label(preview, image=tk_img)
        label.image = tk_img
        label.pack(pady=10)

        btn_frame = tk.Frame(preview)
        btn_frame.pack(pady=10)
        result = {"action": None}

        def do_continue():
            result["action"] = "continue"
            preview.destroy()

        def do_rescan():
            result["action"] = "rescan"
            preview.destroy()

        tk.Button(btn_frame, text="Continue", width=15, command=do_continue).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Rescan", width=15, command=do_rescan).pack(side=tk.LEFT, padx=10)

        preview.wait_window()
        return result["action"]
    def __init__(self, parent, base_dir, on_done, selected_source_name=None):
        self.base_dir = base_dir
        self.on_done = on_done
        self.win = tk.Toplevel(parent)
        self.win.title("New Recipe")
        self.win.geometry("400x300")
        self.win.grab_set()

        self.selected_source_name = selected_source_name  # store the scanner source name

        # Recipe info form
        tk.Label(self.win, text="Recipe Name:").pack(pady=5)
        self.title_var = tk.StringVar()
        tk.Entry(self.win, textvariable=self.title_var).pack(fill=tk.X, padx=20)


        tk.Label(self.win, text="Type:").pack(pady=5)
        self.cat_var = tk.StringVar()
        self.type_options = ["Cake", "Cookie", "Bread", "Soup", "Pie", "Muffin", "Salad", "Other"]
        self.type_combo = ttk.Combobox(self.win, textvariable=self.cat_var, values=self.type_options, state="readonly")
        self.type_combo.pack(fill=tk.X, padx=20)
        self.type_combo.bind("<<ComboboxSelected>>", self.on_type_selected)

        self.other_type_var = tk.StringVar()
        self.other_type_entry = tk.Entry(self.win, textvariable=self.other_type_var)
        self.other_type_entry.pack(fill=tk.X, padx=20, pady=(2,0))
        self.other_type_entry.pack_forget()

        self.double_var = tk.BooleanVar()
        tk.Checkbutton(self.win, text="Double-sided?", variable=self.double_var).pack(pady=10)

        tk.Button(self.win, text="Start Scanning", command=self.scan_recipe).pack(pady=10)

    def on_type_selected(self, event=None):
        if self.cat_var.get() == "Other":
            self.other_type_entry.pack(fill=tk.X, padx=20, pady=(2,0))
        else:
            self.other_type_entry.pack_forget()

    def scan_recipe(self):
        title = self.title_var.get().strip()
        category = self.cat_var.get().strip()
        if category == "Other":
            category = self.other_type_var.get().strip()
        double_sided = self.double_var.get()
        if not title or not category:
            messagebox.showerror("Missing Info", "Please enter both recipe name and type.")
            return

        folder = os.path.join(self.base_dir, category)
        os.makedirs(folder, exist_ok=True)
        images = []

        # Scan front (with preview/rescan loop)
        front_img = os.path.join(folder, "front_temp.jpg")
        while True:
            if not self.do_scan(front_img, "Scan the FRONT of the recipe sheet."):
                return
            action = self.show_scan_preview(front_img, "Front")
            if action == "continue":
                break
            elif action == "rescan":
                continue
            else:
                return
        images.append(front_img)

        # If double-sided
        if double_sided:
            if not messagebox.askokcancel("Flip Sheet", "Flip the recipe sheet, then click OK to scan the back..."):
                self.cleanup(images)
                return
            back_img = os.path.join(folder, "back_temp.jpg")
            while True:
                if not self.do_scan(back_img, "Scan the BACK of the recipe sheet."):
                    self.cleanup(images)
                    return
                action = self.show_scan_preview(back_img, "Back")
                if action == "continue":
                    break
                elif action == "rescan":
                    continue
                else:
                    self.cleanup(images)
                    return
            images.append(back_img)

        # Save as PDF
        safe_title = title.replace(" ", "_")
        output_file = os.path.join(folder, f"{safe_title}.pdf")
        try:
            base, ext = os.path.splitext(output_file)
            counter = 1
            while os.path.exists(output_file):
                output_file = f"{base} ({counter}){ext}"
                counter += 1
            save_as_pdf(images, output_file)
            messagebox.showinfo("Success", f"Saved recipe to {output_file}")
        except Exception as e:
            print(f"Error saving PDF: {e}")
            messagebox.showerror("Error", f"Failed to save PDF: {e}")
        self.cleanup(images)
        self.win.destroy()
        if self.on_done:
            self.on_done()

    def do_scan(self, output_file, prompt):
        if not messagebox.askokcancel("Ready to Scan", prompt):
            return False
        try:
            with twain.SourceManager() as sm:
                src = sm.open_source(self.selected_source_name) if self.selected_source_name else None
                if src:
                    src.request_acquire(show_ui=False, modal_ui=False)
                    (handle, remaining_count) = src.xfer_image_natively()
                    bmp_bytes = twain.dib_to_bm_file(handle)

                    img = PIL.Image.open(BytesIO(bmp_bytes), formats=["bmp"])

                    width, height = img.size
                    factor = 600.0 / width

                    img2 = img.resize((int(width * factor), int(height * factor)), PIL.Image.LANCZOS)
                    img2.convert("RGB").save(output_file, "JPEG")

            return True
        except Exception as e:
            print(f"Error during scanning: {e}")
            messagebox.showerror("Scan Error", f"Failed to scan: {e}")
            return False



    def cleanup(self, images):
        for img in images:
            if os.path.exists(img):
                try:
                    os.remove(img)
                except Exception:
                    pass

def save_as_pdf(images, output_file):
    # Find largest width and height among all images (in pixels)
    max_width, max_height = 0, 0
    img_sizes = []
    for img in images:
        im = Image.open(img)
        img_sizes.append(im.size)
        if im.size[0] > max_width:
            max_width = im.size[0]
        if im.size[1] > max_height:
            max_height = im.size[1]

    # Convert to mm at 300 dpi
    max_width_mm = max_width * 25.4 / 300
    max_height_mm = max_height * 25.4 / 300

    pdf = FPDF(unit="mm", format=(max_width_mm, max_height_mm))
    for img, (width, height) in zip(images, img_sizes):
        width_mm = width * 25.4 / 300
        height_mm = height * 25.4 / 300
        pdf.add_page()
        # Center the image on the page
        x = (max_width_mm - width_mm) / 2
        y = (max_height_mm - height_mm) / 2
        pdf.image(img, x, y, width_mm, height_mm)
    
    # Save the PDF
    pdf.output(output_file)

def main():
    root = tk.Tk()
    app = RecipeScannerApp(root)
    root.protocol("WM_DELETE_WINDOW", root.quit)
    root.mainloop()

if __name__ == "__main__":
    main()
    