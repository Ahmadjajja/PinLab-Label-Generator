import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import sys
import os

# Helper for PyInstaller to find font
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS  # PyInstaller sets this
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Register font once globally
pdfmetrics.registerFont(TTFont("LiberationMonoBold", resource_path("LiberationMono-Bold.ttf")))


selected_file = None
label_blocks = []
max_width = 0
error_line = -1

# -- Utility Functions --
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
    font_size = 2.8
    line_spacing = font_size + 0.5
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
    c.setFont("LiberationMonoBold", font_size + 0.5)

    current_x = left_margin
    current_y = page_height - top_margin
    column = 0
    label_counter = 0

    def draw_label(label_lines, x, y):
        for i, line in enumerate(label_lines):
            c.saveState()
            c.translate(x, y - i * line_spacing)
            c.scale(1.0, 1.4)
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
                    c.setFont("LiberationMonoBold", font_size + 0.5)
                    column = 0
                    current_x = left_margin
                    current_y = page_height - top_margin

            draw_label(block["lines"], current_x, current_y - label_counter * height_per_label)
            label_counter += 1

    c.save()

# -- GUI Setup --
app = tk.Tk()
app.title("PinLab Label Generator")
app.geometry("800x550")
app.configure(bg="#f4f6f9")

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
    "width": 12,
    "padx": 5,
    "pady": 5
}

btn_open = tk.Button(btn_frame, text="📂 Open File", **btn_style)
btn_edit = tk.Button(btn_frame, text="📝 View/Edit", state=tk.DISABLED, **btn_style)
btn_process = tk.Button(btn_frame, text="⚙️ Process", state=tk.DISABLED, **btn_style)
btn_generate = tk.Button(btn_frame, text="📄 Generate PDF", state=tk.DISABLED, **btn_style)
btn_exit = tk.Button(btn_frame, text="❌ Exit", command=app.quit, **btn_style)

btn_open.grid(row=0, column=0, padx=10)
btn_edit.grid(row=0, column=1, padx=10)
btn_process.grid(row=0, column=2, padx=10)
btn_generate.grid(row=0, column=3, padx=10)
btn_exit.grid(row=0, column=4, padx=10)

# -- Hover Effects --
def on_enter(e):
    e.widget["background"] = "#444444"

def on_leave(e):
    e.widget["background"] = "#0a2036"

for b in [btn_open, btn_edit, btn_process, btn_generate, btn_exit]:
    b.bind("<Enter>", on_enter)
    b.bind("<Leave>", on_leave)

# -- Button Actions --
def open_file():
    global selected_file
    selected_file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if selected_file:
        btn_edit.config(state=tk.NORMAL)
        btn_process.config(state=tk.NORMAL)
        text_display.config(state=tk.NORMAL)
        text_display.delete("1.0", tk.END)
        with open(selected_file, "r", encoding="utf-8") as f:
            text_display.insert(tk.END, f.read())
        text_display.config(state=tk.DISABLED)
        btn_generate.config(state=tk.DISABLED)

def process_file():
    global max_width, label_blocks, error_line
    max_width, label_blocks, error_line = parse_label_file(selected_file)
    text_display.config(state=tk.NORMAL)
    text_display.delete("1.0", tk.END)
    if error_line != -1:
        text_display.insert(tk.END, f"❌ ERROR: Check line {error_line} in input file.\n")
        btn_generate.config(state=tk.DISABLED)
    else:
        text_display.insert(tk.END, f"✅ No errors found. Ready to generate PDF.\n")
        btn_generate.config(state=tk.NORMAL)
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
        messagebox.showinfo("Success", f"PDF saved to:\n{output_file}")

def edit_file():
    global selected_file
    if not selected_file:
        return

    # Open Notepad and wait until it's closed
    os.system(f'notepad "{selected_file}"')

    # After editing, reload content
    text_display.config(state=tk.NORMAL)
    text_display.delete("1.0", tk.END)
    with open(selected_file, "r", encoding="utf-8") as f:
        text_display.insert(tk.END, f.read())
    text_display.config(state=tk.DISABLED)


# -- Bind Buttons --
btn_open.config(command=open_file)
btn_edit.config(command=edit_file)
btn_process.config(command=process_file)
btn_generate.config(command=generate_pdf_file)

# -- Start App --
app.mainloop()
