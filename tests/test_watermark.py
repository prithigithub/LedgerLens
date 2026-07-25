from PIL import Image

from backend.services.watermark import add_watermark


def test_watermark_creation(tmp_path):
    image_path = tmp_path / "invoice.png"

    image = Image.new(
        "RGB",
        (500, 500),
        "black",
    )

    image.save(image_path)

    result = add_watermark(
        str(image_path)
    )

    assert result == str(image_path)

    assert image_path.exists()