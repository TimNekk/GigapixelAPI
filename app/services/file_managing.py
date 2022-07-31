import base64
import binascii
import io
from pathlib import Path

from PIL import Image
from loguru import logger


def encode_image_base64(image_path: Path) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def save_image_base64(image_b64: str, save_path: Path) -> None:
    with open(save_path, "wb") as f:
        f.write(base64.b64decode(image_b64))


def is_valid_base64_image(image_string):
    try:
        image = base64.b64decode(image_string)
        Image.open(io.BytesIO(image))
    except binascii.Error:
        return False
    return True


def delete_image(image_path: Path) -> None:
    logger.info(f"Deleting image: {image_path}")
    image_path.unlink()
