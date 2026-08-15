from __future__ import annotations

import io

from PIL import Image


DARK_COOL = ((8, 12, 28), (28, 40, 72))
BRIGHT_WARM = ((250, 225, 180), (235, 190, 120))


def gradient_bytes(
    top: tuple[int, int, int] = DARK_COOL[0],
    bottom: tuple[int, int, int] = DARK_COOL[1],
    size: tuple[int, int] = (1280, 720),
    image_format: str = "JPEG",
) -> bytes:
    """Build a vertical two-tone gradient so mood metrics have real variation."""
    small = Image.new("RGB", (32, 32))
    small.putdata(
        [
            tuple(round(top[band] + (bottom[band] - top[band]) * (y / 31)) for band in range(3))
            for y in range(32)
            for _ in range(32)
        ]
    )
    buffer = io.BytesIO()
    small.resize(size, Image.Resampling.BILINEAR).save(buffer, image_format)
    return buffer.getvalue()


def dark_thumbnail() -> bytes:
    return gradient_bytes(*DARK_COOL)


def bright_thumbnail() -> bytes:
    return gradient_bytes(*BRIGHT_WARM)
