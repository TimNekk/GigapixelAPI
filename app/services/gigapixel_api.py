import os
from pathlib import Path

from gigapixel import Gigapixel, Scale, Mode

from app.config import GIGAPIXEL_EXECUTABLE_PATH, OUTPUT_SUFFIX, OUTPUT_PATH
from app.services.file_managing import save_image_base64, delete_image

gigapixel = Gigapixel(
    executable_path=GIGAPIXEL_EXECUTABLE_PATH,
    output_suffix=OUTPUT_SUFFIX
)


def process_image(image_b64: str, unique_id: str, scale: str | None = None, mode: str | None = None) -> None:
    save_path = Path.cwd() / OUTPUT_PATH / f"{unique_id}.jpg"

    save_image_base64(image_b64, save_path)

    scale = Scale[scale] if scale else Scale.X2
    mode = Mode[mode] if mode else Mode.STANDARD
    gigapixel.process(save_path, scale, mode)

    delete_image(save_path)
