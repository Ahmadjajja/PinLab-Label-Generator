# _______________________________________________
# _______________________________________________
# _______________________________________________
# _______________________________________________
# _______________________________________________

import tkinter as tk
from tkinter import filedialog, scrolledtext
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import sys
import os
import tempfile

# Helper to support PyInstaller font packaging
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Register font
pdfmetrics.registerFont(TTFont("LiberationMonoRegular", resource_path("LiberationMono-Regular.ttf")))

# Globals
selected_file = None
label_blocks = []
max_width = 0
error_line = -1

# ---------- Utility ----------
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x}+{y}")

def parse_label_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip() != ""]

    max_width = int(lines[0])
    label_blocks = []
    current_block = []
    i = 1
    count = -1

    while i < len(lines):
        if lines[i].isdigit():
            if current_block:
                label_blocks.append({"lines": current_block, "count": count})
                current_block = []
            count = int(lines[i])
        else:
            if count == -1:
                return max_width, label_blocks, 1
            if len(lines[i]) > max_width:
                return max_width, label_blocks, i + 1
            current_block.append(lines[i])
        i += 1

    if current_block:
        label_blocks.append({"lines": current_block, "count": count})
    return max_width, label_blocks, -1

def generate_label_pdf(output_path, max_width, label_blocks):
    font_size = 2.9
    line_spacing = font_size + 0.6
    column_width = max_width * (font_size * 0.6) + 10
    page_width, page_height = A4
    top_margin = 10.3 * mm
    bottom_margin = 11.3 * mm
    left_margin = 0 * mm
    usable_height = page_height - top_margin - bottom_margin
    lines_per_label = max(len(block["lines"]) for block in label_blocks)
    height_per_label = lines_per_label * line_spacing + 2.5
    labels_per_column = int(usable_height // height_per_label)
    num_columns = int((page_width - left_margin) // column_width)

    c = canvas.Canvas(output_path, pagesize=A4)
    c.setFont("LiberationMonoRegular", font_size + 0.5)

    current_x = left_margin
    current_y = page_height - top_margin
    column = 0
    label_counter = 0

    def draw_label(label_lines, x, y):
        for i, line in enumerate(label_lines):
            c.saveState()
            c.translate(x, y - i * line_spacing)
            c.scale(1.0, 1.3)
            c.drawString(0, 0, line)
            c.restoreState()

    for block in label_blocks:
        for _ in range(block["count"]):
            if label_counter >= labels_per_column:
                column += 1
                current_x = left_margin + column * column_width
                current_y = page_height - top_margin
                label_counter = 0
                if column >= num_columns:
                    c.showPage()
                    c.setFont("LiberationMonoRegular", font_size + 0.5)
                    column = 0
                    current_x = left_margin
                    current_y = page_height - top_margin
            draw_label(block["lines"], current_x, current_y - label_counter * height_per_label)
            label_counter += 1
    c.save()

# ---------- GUI ----------
app = tk.Tk()
app.title("PinLab Label Generator")
app.configure(bg="#f4f6f9")
center_window(app, 800, 550)

header = tk.Label(app, text="PinLab Label Generator", font=("Segoe UI", 16, "bold"), bg="#0a2036", fg="white", pady=10)
header.pack(fill=tk.X)

text_display = scrolledtext.ScrolledText(app, wrap=tk.WORD, height=20, state=tk.DISABLED, font=("Consolas", 10))
text_display.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

btn_frame = tk.Frame(app, bg="#f4f6f9")
btn_frame.pack(pady=10)

btn_style = {
    "font": ("Segoe UI", 10, "bold"),
    "bg": "#0a2036",
    "fg": "white",
    "activebackground": "#0a2036",
    "activeforeground": "white",
    "relief": tk.FLAT,
    "width": 14,
    "padx": 5,
    "pady": 5
}

btn_open = tk.Button(btn_frame, text="📂 Open File", **btn_style)
btn_edit = tk.Button(btn_frame, text="📝 Edit", state=tk.DISABLED, **btn_style)
btn_process = tk.Button(btn_frame, text="⚙️ Process", state=tk.DISABLED, **btn_style)
btn_generate = tk.Button(btn_frame, text="📄 Generate PDF", state=tk.DISABLED, **btn_style)
btn_print = tk.Button(btn_frame, text="🖨️ Print", state=tk.DISABLED, **btn_style)
btn_help = tk.Button(btn_frame, text="❓ Help", **btn_style)
btn_about = tk.Button(btn_frame, text="ℹ️ About", **btn_style)
btn_exit = tk.Button(btn_frame, text="❌ Exit", command=app.quit, **btn_style)

btn_open.grid(row=0, column=0, padx=5)
btn_edit.grid(row=0, column=1, padx=5)
btn_process.grid(row=0, column=2, padx=5)
btn_generate.grid(row=0, column=3, padx=5)
btn_print.grid(row=0, column=4, padx=5)
btn_about.grid(row=0, column=5, padx=5)
btn_help.grid(row=0, column=6, padx=5)
btn_exit.grid(row=0, column=7, padx=5)

# Hover
def on_enter(e): e.widget["background"] = "#444444"
def on_leave(e): e.widget["background"] = "#0a2036"
for b in [btn_open, btn_edit, btn_process, btn_generate, btn_print, btn_help, btn_about, btn_exit]:
    b.bind("<Enter>", on_enter)
    b.bind("<Leave>", on_leave)

# ---------- Popups ----------
def show_popup(title, message):
    win = tk.Toplevel(app)
    win.title(title)
    win.configure(bg="white")
    center_window(win, 420, 180)
    tk.Label(win, text=message, font=("Segoe UI", 11), bg="white", wraplength=380, justify="left").pack(pady=20)
    tk.Button(win, text="OK", font=("Segoe UI", 10, "bold"), command=win.destroy, bg="#0a2036", fg="white", relief=tk.FLAT, padx=10, pady=5).pack()

def show_help():
    win = tk.Toplevel(app)
    win.title("Help - How to Use")
    center_window(win, 640, 450)
    win.configure(bg="white")
    txt = scrolledtext.ScrolledText(win, wrap=tk.WORD, font=("Segoe UI", 10), bg="white", fg="#222222")
    txt.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    txt.insert(tk.END, """
📘 HOW TO USE PINLAB LABEL GENERATOR:

1. 📂 Open File
   - Select a `.txt` label input file formatted as:
     > Line 1: Max width (e.g., 25)
     > Line 2: Repetition count (e.g., 52)
     > Next lines: Label block
     > Then new number → new block, and so on

2. 📝 Edit
   - Opens in Notepad, edit it
   - Save and close, it reloads into app

3. ⚙️ Process
   - Validates file, checks line length, errors

4. 📄 Generate PDF
   - Outputs label layout in PDF format

5. ❌ Exit
   - Close the software

ℹ️ Tip: Don’t leave blank lines in the input file.
    """)
    txt.config(state=tk.DISABLED)

def show_about():
    win = tk.Toplevel(app)
    win.title("About PinLab")
    center_window(win, 640, 450)
    win.configure(bg="white")
    txt = scrolledtext.ScrolledText(win, wrap=tk.WORD, font=("Segoe UI", 10), bg="white", fg="#222222")
    txt.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    txt.insert(tk.END, """
🔹 PinLab Software - Version History 🔹

📌 Version 1.0 (2004)
- Developed by DLG using Fortran + WINTERACTER
- Outputs: PCL plot files (.plt)
- Limitations: no PDF, limited characters

🚀 Version 2.0 (2024)
- Rewritten by Ahmad Sultan in Python
- Uses: Tkinter + ReportLab
- Output: PDF
- Supports: ASCII/Unicode, modern fonts, dynamic scaling

🔗 Developer:
- GitHub: https://github.com/ahmadcodes
- LinkedIn: https://linkedin.com/in/ahmadcodes
- Website: https://ahmad.codes

📁 Repo:
https://github.com/ahmadcodes/pinlab-label-generator
    """)
    txt.config(state=tk.DISABLED)

# ---------- Actions ----------
def open_file():
    global selected_file
    selected_file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if selected_file:
        btn_edit.config(state=tk.NORMAL)
        btn_process.config(state=tk.NORMAL)
        btn_generate.config(state=tk.DISABLED)
        btn_print.config(state=tk.DISABLED)
        text_display.config(state=tk.NORMAL)
        text_display.delete("1.0", tk.END)
        with open(selected_file, "r", encoding="utf-8") as f:
            text_display.insert(tk.END, f.read())
        text_display.config(state=tk.DISABLED)

def process_file():
    global max_width, label_blocks, error_line
    max_width, label_blocks, error_line = parse_label_file(selected_file)
    text_display.config(state=tk.NORMAL)
    text_display.delete("1.0", tk.END)
    if error_line != -1:
        text_display.insert(tk.END, f"❌ ERROR: Check line {error_line} in input file.\n")
        btn_generate.config(state=tk.DISABLED)
        btn_print.config(state=tk.DISABLED)
    else:
        text_display.insert(tk.END, f"✅ No errors found. Ready to generate PDF or print.\n")
        btn_generate.config(state=tk.NORMAL)
        btn_print.config(state=tk.NORMAL)
    text_display.config(state=tk.DISABLED)

def generate_pdf_file():
    if not selected_file:
        return
    base_name = os.path.splitext(os.path.basename(selected_file))[0]
    output_file = filedialog.asksaveasfilename(
        initialfile=f"{base_name}_output.pdf",
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")]
    )
    if output_file:
        generate_label_pdf(output_file, max_width, label_blocks)
        show_popup("Success", f"✅ PDF saved to:\n{output_file}")

def print_pdf_file():
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            generate_label_pdf(temp_pdf.name, max_width, label_blocks)
            os.startfile(temp_pdf.name, "print")
    except Exception:
        show_popup("Printer Error", "⚠️ No printer found or unable to print.")

def edit_file():
    if not selected_file: return
    os.system(f'notepad "{selected_file}"')
    text_display.config(state=tk.NORMAL)
    text_display.delete("1.0", tk.END)
    with open(selected_file, "r", encoding="utf-8") as f:
        text_display.insert(tk.END, f.read())
    text_display.config(state=tk.DISABLED)

# ---------- Bind ----------
btn_open.config(command=open_file)
btn_edit.config(command=edit_file)
btn_process.config(command=process_file)
btn_generate.config(command=generate_pdf_file)
btn_print.config(command=print_pdf_file)
btn_help.config(command=show_help)
btn_about.config(command=show_about)

# ---------- Start ----------
app.mainloop()
