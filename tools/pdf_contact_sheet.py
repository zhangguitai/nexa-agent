from pathlib import Path
import sys

from PIL import Image, ImageDraw


source = Path(sys.argv[1])
target = Path(sys.argv[2])
pages = sorted(source.glob("page-*.png"))
if not pages:
    raise SystemExit("No rendered pages found")

columns = 5
thumb_width = 280
thumb_height = 396
rows = (len(pages) + columns - 1) // columns
sheet = Image.new("RGB", (columns * thumb_width, rows * thumb_height), "white")
draw = ImageDraw.Draw(sheet)

for index, page in enumerate(pages):
    image = Image.open(page).convert("RGB").resize((thumb_width, thumb_height))
    x = (index % columns) * thumb_width
    y = (index // columns) * thumb_height
    sheet.paste(image, (x, y))
    draw.rectangle((x + 5, y + 5, x + 38, y + 26), fill="#0d9075")
    draw.text((x + 13, y + 9), str(index + 1), fill="white")

sheet.save(target)
print(target)
