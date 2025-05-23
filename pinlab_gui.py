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
import win32api
import win32print
import winreg  # Add at the top if not already imported

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
btn_edit = tk.Button(btn_frame, text="📝 View/Edit", state=tk.DISABLED, **btn_style)
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
    center_window(win, 520, 300)
    tk.Label(win, text=message, font=("Segoe UI", 11), bg="white", wraplength=450, justify="left").pack(pady=20)
    tk.Button(win, text="OK", font=("Segoe UI", 10, "bold"), command=win.destroy, bg="#0a2036", fg="white", relief=tk.FLAT, padx=10, pady=5).pack()

def show_help():
    import webbrowser

    win = tk.Toplevel(app)
    win.title("Help - How to Use")
    center_window(win, 640, 450)
    win.configure(bg="white")

    txt = scrolledtext.ScrolledText(win, wrap=tk.WORD, font=("Segoe UI", 10), bg="white", fg="#222222", cursor="arrow")
    txt.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    content = """
HOW TO USE PINLAB LABEL GENERATOR

1. 📂 Open File
   - Click to select a `.txt` file formatted as:
     - Line 1 → Maximum character width (e.g., 25)
     - Line 2 → Number of times to repeat the label block (e.g., 30)
     - Following lines → Label content
     - A new number → begins a new label block

2. 📝 View/Edit
   - This opens the selected file in Notepad.
   - After editing and saving, the file is automatically reloaded in the app.

3. ⚙️ Process
   - Validates the content:
     - Checks for overly long lines
     - Ensures label blocks are correctly formatted
   - You'll see an error if there's any formatting issue, or a success message if it's clean.

4. 📄 Generate PDF
   - Saves your processed labels in a PDF format.
   - You’ll be asked where to save the file.
   - Great for previewing or sharing your labels.

5. \U0001F5A8 Print
   - Sends labels directly to your **default connected printer**.
   - To use this successfully:
     - Ensure your printer is **connected and set as default**.
     - Install **Adobe Acrobat Reader** and set it as the **default PDF viewer**.
   - If something is missing, the app will guide you with an error message.

6. ℹ️ About
   - Shows you the history of the software:
     - Original version 1.0 built around 20 years ago by Daniel L. Gustafson, Ph.D.
     - This new version 2.0 redesigned in Python in 2025 by Ahmad Jajja.

7. ❓ Help
   - Displays this guide any time you need it.

8. ❌ Exit
   - Closes the app.

💡 Tip: Avoid blank lines in your input file. Keep formatting consistent for best results.
"""

    txt.insert(tk.END, content)
    
    # Add link tags
    def make_hyperlink(tag_name, text_to_find, url):
        start = content.find(text_to_find)
        end = start + len(text_to_find)
        txt.tag_add(tag_name, f"1.0+{start}c", f"1.0+{end}c")
        txt.tag_config(tag_name, foreground="blue", underline=True)
        txt.tag_bind(tag_name, "<Button-1>", lambda e: webbrowser.open_new(url))

        # Simulate hover cursor manually
        def on_enter(event): txt.config(cursor="hand2")
        def on_leave(event): txt.config(cursor="arrow")
        txt.tag_bind(tag_name, "<Enter>", on_enter)
        txt.tag_bind(tag_name, "<Leave>", on_leave)

    make_hyperlink("ahmad", "Ahmad Jajja", "https://linkedin.com/in/ahmad-jajja")

    txt.config(state=tk.DISABLED)

def show_about():
    import webbrowser

    win = tk.Toplevel(app)
    win.title("About PinLab")
    center_window(win, 640, 450)
    win.configure(bg="white")

    txt = scrolledtext.ScrolledText(win, wrap=tk.WORD, font=("Segoe UI", 10), bg="white", fg="#222222", cursor="arrow")
    txt.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    content = """
🔹 PinLab Label Generator – Version 2.0

Version 1.0 (2004)

Originally developed by **Daniel L. Gustafson, Ph.D. Montana State University, Bozeman, MT.**, this version was written in **Fortran** using the **WINTERACTER** GUI toolkit. It was designed specifically for generating entomology labels.

Limitations of the old version:
- Only supported specific printer hardware
- Output was limited to `.plt` files (PCL)
- No PDF export support
- Rigid formatting and font limitations

Version 2.0 (2025)

To preserve and modernize the original concept, Ahmad Jajja rebuilt the software from scratch with updated technologies for today’s users.

This version:

- Is written in Python using Tkinter for GUI and ReportLab for PDF generation
- Supports monospaced Unicode fonts for scientific accuracy
- Allows direct PDF printing and label generation
- Features a modern, user-friendly interface
- Works across modern Windows systems without needing complex dependencies

Benefits of Version 2.0:

- Print-ready without old printer constraints
- Export to PDF directly
- Lightweight, portable .exe for offline use
- Editable and transparent input format
- Great for labs, museums, research, and fieldwork printing

Developer Links:

- GitHub: Ahmad Jajja
- LinkedIn: Ahmad Jajja
- Website: ahmad-jajja.com

Source Code:

Available on GitHub: PinLab Label Generator Repository

Acknowledgments

Special thanks to **Daniel L. Gustafson, Ph.D.** for the original PinLab concept and vision that inspired this modern implementation.

Built with \u2764 for the scientific research community
"""
    txt.insert(tk.END, content)

    # Helper for hyperlink styling
    def make_hyperlink(tag_name, text_to_find, url):
        start = content.find(text_to_find)
        end = start + len(text_to_find)
        txt.tag_add(tag_name, f"1.0+{start}c", f"1.0+{end}c")
        txt.tag_config(tag_name, foreground="blue", underline=True)
        txt.tag_bind(tag_name, "<Button-1>", lambda e: webbrowser.open_new(url))

        def on_enter(event): txt.config(cursor="hand2")
        def on_leave(event): txt.config(cursor="arrow")
        txt.tag_bind(tag_name, "<Enter>", on_enter)
        txt.tag_bind(tag_name, "<Leave>", on_leave)

    # Create clickable tags
    make_hyperlink("github", "GitHub: Ahmad Jajja", "https://github.com/Ahmadjajja")
    make_hyperlink("linkedin", "LinkedIn: Ahmad Jajja", "https://linkedin.com/in/ahmad-jajja")
    make_hyperlink("website", "Website: ahmad-jajja.com", "https://ahmad-jajja.com")
    make_hyperlink("repo", "PinLab Label Generator Repository", "https://github.com/Ahmadjajja/PinLab-Label-Generator")

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


# def print_pdf_file():
#     try:

#         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
#             generate_label_pdf(temp_pdf.name, max_width, label_blocks)

#         # Open the default PDF viewer's print dialog
#         os.startfile(temp_pdf.name, "print")

#     except Exception as e:
#         show_popup(
#             "Printer Error",
#             "⚠️ Printing Failed.\n\n"
#             "Please follow these steps to fix the issue:\n\n"
#             "1. Make sure your printer is connected and set as the default printer.\n"
#             "2. Ensure that Adobe Acrobat Reader is installed and set as the default app for opening PDF files.\n\n"
#             "Once both are configured correctly, try printing again."
#         )

# ---------------- Second working print function---------------------------

import subprocess
import tempfile
import threading
import win32print
import os

def find_adobe_executable():
    possible_paths = [
        r"C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe",
        r"C:\Program Files\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe",
        r"C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe",
        r"C:\Program Files (x86)\Adobe\Acrobat DC\Acrobat\Acrobat.exe",
        r"C:\Program Files\Adobe\Acrobat Pro\Acrobat\Acrobat.exe",
        r"C:\Program Files (x86)\Adobe\Acrobat Pro\Acrobat\Acrobat.exe"
    ]
    for path in possible_paths:
        if os.path.isfile(path):
            return path
    return None

# def is_default_printer_ready():
#     try:
#         printer_name = win32print.GetDefaultPrinter()
#         hPrinter = win32print.OpenPrinter(printer_name)
#         info = win32print.GetPrinter(hPrinter, 2)
#         win32print.ClosePrinter(hPrinter)

#         status = info["Status"]

#         # Check for common "not ready" states
#         PRINTER_STATUS_OFFLINE = 0x00000080
#         PRINTER_STATUS_PAUSED = 0x00000001
#         PRINTER_STATUS_ERROR = 0x00000002

#         if status & (PRINTER_STATUS_OFFLINE | PRINTER_STATUS_PAUSED | PRINTER_STATUS_ERROR):
#             return False

#         return True
#     except Exception:
#         return False

def print_pdf_file():
    def do_print():
        try:
            printer_name = win32print.GetDefaultPrinter()
            hPrinter = win32print.OpenPrinter(printer_name)
            info = win32print.GetPrinter(hPrinter, 2)
            win32print.ClosePrinter(hPrinter)

            # Check status
            status = info["Status"]
            PRINTER_STATUS_OFFLINE = 0x00000080
            PRINTER_STATUS_ERROR = 0x00000002
            PRINTER_STATUS_PAUSED = 0x00000001

            if status & (PRINTER_STATUS_OFFLINE | PRINTER_STATUS_ERROR | PRINTER_STATUS_PAUSED):
                raise Exception(f"Printer '{printer_name}' is not ready (paused, offline, or error state).")

            adobe_path = find_adobe_executable()
            if not adobe_path:
                raise Exception("Adobe Reader or Acrobat not found in known locations.")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                generate_label_pdf(temp_pdf.name, max_width, label_blocks)

            subprocess.run([adobe_path, "/p", "/h", temp_pdf.name], check=False)

            show_popup(
                "Sent to Printer",
                f"Print command sent to: {printer_name}\nPlease check the printer output or print queue manually."
            )

        except Exception as e:
            show_popup(
                "Printer Error",
                f"""Printing Failed!

Steps to fix:
1. Select the correct printer as your default printer.
2. If the printer is online, the document will print immediately.
3. If the printer is offline, the document will be queued. It will automatically print once the printer comes online.
4. Ensure Adobe Acrobat/Reader is installed and set as the default PDF app.

(Error: {str(e)})
"""
            )

    threading.Thread(target=do_print, daemon=True).start()



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




# pyinstaller --onefile --add-data "LiberationMono-Regular.ttf;." pinlab_gui.py
