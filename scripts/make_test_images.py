from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path("test_images")
OUT.mkdir(exist_ok=True)
cases = {
    "us_plate.png": "8ABC123",
    "work_sign.png": "ROAD\nWORK\nAHEAD",
    "speed_plaque.png": "35 MPH"
}
for name, text in cases.items():
    img = Image.new("RGB", (900, 360), "white")
    d = ImageDraw.Draw(img)
    font = ImageFont.load_default(size=64)
    d.multiline_text((60, 80), text, fill="black", font=font, spacing=24)
    img.save(OUT / name)
print(OUT)
