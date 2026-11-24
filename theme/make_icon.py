"""Genera `assets/icon.ico` e `assets/icon.png` a partir del diseño de `icon.svg`.

Uso (requiere Pillow, solo para este paso):

    pip install pillow
    python -m theme.make_icon

Si prefieres un icono propio, no hace falta este script: coloca tu `icon.ico`
(y opcionalmente `icon.png` / `icon.svg`) en `theme/assets/`.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

ASSETS_DIR = Path(__file__).parent / "assets"
SCALE = 4                      # supersampling para bordes suaves
SIZE = 256 * SCALE
CENTER = (128, 128)
OUTER = [(70, 70), (186, 70), (70, 186), (186, 186)]


def _gradient(top: tuple[int, int, int], bottom: tuple[int, int, int]) -> Image.Image:
    """Degradado diagonal sencillo (mismos colores que el SVG)."""
    data = []
    for y in range(SIZE):
        for x in range(SIZE):
            t = (x + y) / (2 * SIZE)
            data.append(tuple(int(a + (b - a) * t) for a, b in zip(top, bottom)))
    img = Image.new("RGB", (SIZE, SIZE))
    img.putdata(data)
    return img


def render() -> Image.Image:
    s = SCALE
    background = _gradient((0x3B, 0x82, 0xF6), (0x1E, 0x40, 0xAF))
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, SIZE - 1, SIZE - 1), radius=56 * s, fill=255)
    icon = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    icon.paste(background, (0, 0), mask)

    draw = ImageDraw.Draw(icon)
    white = (255, 255, 255, 255)
    for x, y in OUTER:
        draw.line((CENTER[0] * s, CENTER[1] * s, x * s, y * s), fill=white, width=10 * s)

    def dot(cx: int, cy: int, r: int) -> None:
        draw.ellipse(((cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s), fill=white)

    dot(*CENTER, 26)
    for x, y in OUTER:
        dot(x, y, 18)
    return icon.resize((256, 256), Image.Resampling.LANCZOS)


if __name__ == "__main__":
    image = render()
    image.save(ASSETS_DIR / "icon.png")
    image.save(ASSETS_DIR / "icon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print(f"Iconos generados en {ASSETS_DIR}")
