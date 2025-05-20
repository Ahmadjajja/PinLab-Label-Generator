from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

def parse_label_file(filepath): # this function is perfect
    with open(filepath, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip() != ""]

    max_width = int(lines[0])
    label_blocks = []
    current_block = []
    i = 1  # start after max width
    count = -1
    ERROR = False

    while i < len(lines):
        if lines[i].isdigit():
            if current_block:
                if count == -1:
                    return max_width, label_blocks
                label_blocks.append({
                    "lines": current_block,
                    "count": count
                })
                current_block = []
            count = int(lines[i])
        else:
            current_block.append(lines[i])
        i += 1
    if current_block:
        label_blocks.append({
            "lines": current_block,
            "count": count
        })
        current_block = []
    return max_width, label_blocks

def generate_label_pdf(output_path, max_width, label_blocks):
    font_size = 6.5
    line_spacing = font_size + 1
    column_width = max_width * (font_size * 0.6) + 10

    page_width, page_height = A4
    top_margin = 20 * mm
    bottom_margin = 10 * mm
    left_margin = 15 * mm

    usable_height = page_height - top_margin - bottom_margin
    lines_per_label = max(len(block["lines"]) for block in label_blocks)
    height_per_label = lines_per_label * line_spacing + line_spacing
    labels_per_column = int(usable_height // height_per_label)
    num_columns = int((page_width - left_margin) // column_width)

    c = canvas.Canvas(output_path, pagesize=A4)
    c.setFont("Courier", font_size)

    current_x = left_margin
    current_y = page_height - top_margin
    column = 0
    label_counter = 0

    def draw_label(label_lines, x, y):
        for i, line in enumerate(label_lines):
            c.drawString(x, y - i * line_spacing, line)

    for block in label_blocks:
        for _ in range(block["count"]):
            if label_counter >= labels_per_column:
                column += 1
                current_x = left_margin + column * column_width
                current_y = page_height - top_margin
                label_counter = 0

                if column >= num_columns:
                    c.showPage()
                    c.setFont("Courier", font_size)
                    column = 0
                    current_x = left_margin
                    current_y = page_height - top_margin

            draw_label(block["lines"], current_x, current_y - label_counter * height_per_label)
            label_counter += 1

    c.save()

if __name__ == "__main__":
    filepath = "Part 2 Summer Labels E - Copy.txt"  # Replace with your real input file name
    max_width, label_blocks = parse_label_file(filepath)
    if not label_blocks:
        print("ERROR: width or count label is missing!")
    else:
        print("Max label width:", max_width)
        print("Total blocks:", len(label_blocks))
        for i, block in enumerate(label_blocks):
            print(f"\nLabel {i+1} (repeat {block['count']} times):")
            for line in block['lines']:
                print(line)

        output_path = "Part 2 Summer Labels E_output_labels.pdf"
        generate_label_pdf(output_path, max_width, label_blocks)
        # print(f"\nPDF created: {output_path}")