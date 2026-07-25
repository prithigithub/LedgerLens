from io import BytesIO
import base64
import logging

from PIL import Image

logger = logging.getLogger(__name__)


def preprocess_image(image_path: str) -> str:
    """
    Opens an image, converts it to JPEG,
    compresses it, and returns a Base64 string.
    """

    try:
        logger.info("Opening image: %s", image_path)

        image = Image.open(image_path)

        image = image.convert("RGB")

        image.thumbnail((2000, 2000))

        buffer = BytesIO()

        image.save(
            buffer,
            format="JPEG",
            quality=85,
            optimize=True,
        )

        encoded = base64.b64encode(
            buffer.getvalue()
        ).decode("utf-8")

        logger.info("Image preprocessing completed.")

        return encoded

    except FileNotFoundError:
        logger.exception("Image file not found.")
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    except Exception as e:
        logger.exception("Image preprocessing failed.")
        raise RuntimeError(
            f"Failed to preprocess image: {e}"
        )