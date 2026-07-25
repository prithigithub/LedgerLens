from PIL import Image, ImageDraw, ImageFont


def add_watermark(image_path: str, text: str = "LedgerLens AI"):
    image = Image.open(image_path).convert("RGBA")
    draw = ImageDraw.Draw(image)
    width, height = image.size

    try:
        font = ImageFont.truetype("Arial.ttf", max(20, width // 35))
    except OSError:
        font = ImageFont.load_default()

    draw.text(
        (30, max(10, height - 70)),
        text,
        fill=(255, 0, 0, 200),
        font=font,
    )

    image.convert("RGB").save(image_path)
    return image_path
