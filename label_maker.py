from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm


def parse_label_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip() != ""]

    max_width = int(lines[0])
    label_blocks = []
    current_block = []
    i = 1  # start after max width

    while i < len(lines):
        if lines[i].isdigit():
            count = int(lines[i])
            if current_block:
                label_blocks.append({
                    "lines": current_block,
                    "count": count
                })
                current_block = []
        else:
            current_block.append(lines[i])
        i += 1

    return max_width, label_blocks


def generate_label_pdf(output_path, max_width, label_blocks):
    font_size = 7.2
    line_spacing = font_size + 1.0

    page_width, page_height = A4
    top_margin = 20 * mm
    bottom_margin = 10 * mm
    left_margin = 10 * mm
    right_margin = 10 * mm
    column_spacing = 3 * mm
    num_columns = 11

    column_width = (page_width - left_margin - right_margin - (num_columns - 1) * column_spacing) / num_columns

    usable_height = page_height - top_margin - bottom_margin
    lines_per_label = max(len(block["lines"]) for block in label_blocks)
    height_per_label = lines_per_label * line_spacing + 1.5 * mm  # Small vertical gap between labels
    labels_per_column = int(usable_height // height_per_label)

    c = canvas.Canvas(output_path, pagesize=A4)
    c.setFont("Courier", font_size)

    current_x = left_margin
    current_y = page_height - top_margin
    column = 0
    label_counter = 0

    def draw_label(label_lines, x, y):
        for i, line in enumerate(label_lines):
            trimmed_line = line[:max_width]  # Enforce max character width
            c.drawString(x, y - i * line_spacing, trimmed_line)

    for block in label_blocks:
        for _ in range(block["count"]):
            if label_counter >= labels_per_column:
                column += 1
                current_x = left_margin + column * (column_width + column_spacing)
                current_y = page_height - top_margin
                label_counter = 0

                if column >= num_columns:
                    c.showPage()
                    c.setFont("Courier", font_size)
                    column = 0
                    current_x = left_margin
                    current_y = page_height - top_margin

            y_position = current_y - label_counter * height_per_label
            draw_label(block["lines"], current_x, y_position)
            label_counter += 1

    c.save()


if __name__ == "__main__":
    filepath = "Part 2 Summer Labels E.txt"  # Replace this with your actual input file path
    output_path = "output_labels3.pdf"

    max_width, label_blocks = parse_label_file(filepath)

    print("Max label width:", max_width)
    print("Total blocks:", len(label_blocks))
    for i, block in enumerate(label_blocks):
        print(f"\nLabel {i+1} (repeat {block['count']} times):")
        for line in block['lines']:
            print(line)

    generate_label_pdf(output_path, max_width, label_blocks)
    print(f"PDF created: {output_path}")