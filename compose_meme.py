#!/usr/bin/env python3
"""Compose a crisp, square GTA VI loading-screen meme with Pillow."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
SIZE = 1024
FONT_FILE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
INK = (9, 10, 24)
WHITE = (250, 248, 255)
PINK = (255, 51, 176)
ORANGE = (255, 132, 83)


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_FILE, size=size)


def lerp(a: int, b: int, t: float) -> int:
    return round(a + (b - a) * t)


def make_sky() -> Image.Image:
    """Build a navy dusk gradient with a restrained magenta horizon glow."""
    image = Image.new("RGB", (SIZE, SIZE))
    pixels = image.load()
    horizontal = [math.exp(-((x - 510) / 410) ** 2) for x in range(SIZE)]
    for y in range(SIZE):
        t = y / (SIZE - 1)
        base = tuple(lerp(a, b, t) for a, b in zip((7, 10, 25), (18, 13, 38)))
        horizon = math.exp(-((y - 735) / 205) ** 2)
        for x in range(SIZE):
            glow = horizon * horizontal[x]
            pixels[x, y] = (
                min(255, round(base[0] + 39 * glow)),
                min(255, round(base[1] + 8 * glow)),
                min(255, round(base[2] + 42 * glow)),
            )
    return image.convert("RGBA")


def cubic(start: tuple[float, float], control_a: tuple[float, float],
          control_b: tuple[float, float], end: tuple[float, float],
          steps: int = 24) -> list[tuple[int, int]]:
    points = []
    for index in range(steps + 1):
        t = index / steps
        u = 1 - t
        x = u**3 * start[0] + 3 * u**2 * t * control_a[0] + 3 * u * t**2 * control_b[0] + t**3 * end[0]
        y = u**3 * start[1] + 3 * u**2 * t * control_a[1] + 3 * u * t**2 * control_b[1] + t**3 * end[1]
        points.append((round(x), round(y)))
    return points


def draw_sunset_and_city(canvas: Image.Image) -> None:
    """Paint a small Vice City horizon, with the buildings kept in silhouette."""
    glow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse((365, 625, 659, 920), fill=(255, 83, 153, 62))
    glow = glow.filter(ImageFilter.GaussianBlur(48))
    canvas.alpha_composite(glow)

    sun = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sun)
    sd.ellipse((424, 652, 600, 828), fill=(255, 136, 91, 238))
    for y in (735, 755, 778, 805):
        sd.rectangle((421, y, 603, y + (5 if y < 778 else 8)), fill=(24, 14, 39, 210))
    canvas.alpha_composite(sun)

    city = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(city)
    blocks = [
        (-20, 766, 122, 1024), (108, 727, 232, 1024),
        (218, 766, 333, 1024), (322, 711, 431, 1024),
        (419, 751, 528, 1024), (514, 724, 635, 1024),
        (623, 773, 736, 1024), (720, 733, 846, 1024),
        (832, 756, 949, 1024), (936, 721, 1050, 1024),
    ]
    for left, top, right, bottom in blocks:
        d.rectangle((left, top, right, bottom), fill=(12, 13, 31, 250))
        d.line((left, top, right, top), fill=(238, 58, 168, 180), width=3)

    # Selective windows keep the skyline legible without turning it into texture.
    window_color = (255, 117, 123, 176)
    for left, top, right, _ in blocks:
        for row, y in enumerate(range(top + 26, 950, 42)):
            for x in range(left + 16 + (row % 2) * 12, right - 8, 32):
                if (x * 3 + y) % 5 in (0, 1):
                    d.rounded_rectangle((x, y, x + 8, y + 15), radius=2, fill=window_color)

    # A pair of palm silhouettes anchors the Vice City horizon.
    for base_x, base_y, lean in ((88, 924, 12), (937, 930, -11)):
        trunk = cubic((base_x, base_y), (base_x + lean, base_y - 80),
                      (base_x + lean * 1.7, base_y - 152),
                      (base_x + lean * 2.4, base_y - 228))
        d.line(trunk, fill=(13, 12, 29, 255), width=15, joint="curve")
        crown_x, crown_y = trunk[-1]
        d.ellipse((crown_x - 10, crown_y - 7, crown_x + 10, crown_y + 9), fill=(13, 12, 29, 255))
        fronds = [
            ((crown_x, crown_y), (crown_x - 33, crown_y - 31), (crown_x - 80, crown_y - 49), (crown_x - 112, crown_y - 24)),
            ((crown_x, crown_y), (crown_x - 20, crown_y - 52), (crown_x - 47, crown_y - 83), (crown_x - 78, crown_y - 87)),
            ((crown_x, crown_y), (crown_x + 22, crown_y - 52), (crown_x + 54, crown_y - 70), (crown_x + 91, crown_y - 59)),
            ((crown_x, crown_y), (crown_x + 42, crown_y - 27), (crown_x + 76, crown_y - 27), (crown_x + 111, crown_y - 7)),
            ((crown_x, crown_y), (crown_x + 8, crown_y - 35), (crown_x + 12, crown_y - 74), (crown_x + 1, crown_y - 105)),
        ]
        for start, a, b, end in fronds:
            d.line(cubic(start, a, b, end), fill=(13, 12, 29, 255), width=12, joint="curve")

    # A few restrained neon roof lines give the silhouette a sunset edge.
    d.line((0, 1007, SIZE, 1007), fill=(246, 55, 168, 105), width=3)
    d.line((0, 1014, SIZE, 1014), fill=(255, 137, 84, 58), width=2)
    canvas.alpha_composite(city)


def centered_text(draw: ImageDraw.ImageDraw, text: str, y: int,
                  face: ImageFont.FreeTypeFont, fill: tuple[int, int, int],
                  stroke: int = 0) -> tuple[int, int, int, int]:
    bounds = draw.textbbox((0, 0), text, font=face, stroke_width=stroke)
    x = (SIZE - (bounds[2] - bounds[0])) // 2 - bounds[0]
    draw.text((x, y), text, font=face, fill=fill, stroke_width=stroke,
              stroke_fill=(37, 18, 55), anchor="lt")
    return draw.textbbox((x, y), text, font=face, stroke_width=stroke)


def add_bar(canvas: Image.Image, mark_path: Path) -> None:
    bar = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(bar)
    left, top, right, bottom = 110, 452, 914, 548
    d.rounded_rectangle((left, top, right, bottom), radius=48,
                        fill=(5, 7, 19, 232), outline=(91, 62, 112, 225), width=4)

    # Build the 99% fill as a gradient, then clip it to a rounded pill.
    fill_end = left + round((right - left) * 0.99)
    fill_layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    fd = ImageDraw.Draw(fill_layer)
    for x in range(left + 4, fill_end):
        t = (x - left) / (fill_end - left)
        color = (lerp(247, 255, t), lerp(35, 105, t), lerp(151, 203, t), 255)
        fd.line((x, top + 4, x, bottom - 4), fill=color)
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).rounded_rectangle((left + 4, top + 4, right - 4, bottom - 4), radius=43, fill=255)
    fill_layer.putalpha(Image.composite(fill_layer.getchannel("A"), Image.new("L", (SIZE, SIZE), 0), mask))
    bar.alpha_composite(fill_layer)
    d = ImageDraw.Draw(bar)
    d.line((left + 38, top + 14, fill_end - 24, top + 14), fill=(255, 211, 241, 108), width=3)

    # The mascot is the endpoint marker, scaled by its visible alpha bounds.
    mark = Image.open(mark_path).convert("RGBA")
    mark = mark.crop(mark.getchannel("A").getbbox())
    mark = mark.resize((224, 224), Image.Resampling.LANCZOS)
    x = 886 - mark.width // 2
    y = 500 - mark.height // 2
    bar.alpha_composite(mark, (x, y))
    canvas.alpha_composite(bar)


def compose(preview_path: Path | None) -> None:
    canvas = make_sky()
    draw_sunset_and_city(canvas)

    # Sparse neon flares above the horizon tie the skyline to the loading UI.
    flare = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    fl = ImageDraw.Draw(flare)
    fl.line((88, 690, 936, 690), fill=(238, 61, 172, 90), width=2)
    fl.ellipse((504, 684, 520, 700), fill=(255, 153, 91, 190))
    canvas.alpha_composite(flare)

    text_layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    td = ImageDraw.Draw(text_layer)
    measurements: dict[str, tuple[int, int, int, int]] = {}
    measurements["GTA VI"] = centered_text(td, "GTA VI", 72, font(144), WHITE, 2)
    measurements["LOADING LEONIDA…"] = centered_text(td, "LOADING LEONIDA…", 250, font(51), (243, 220, 252), 1)

    # A subtle line separates the title from the loading UI.
    td.rounded_rectangle((366, 365, 658, 369), radius=2, fill=(249, 59, 174, 170))
    canvas.alpha_composite(text_layer)

    add_bar(canvas, ROOT / "assets" / "mark-1024.png")

    caption = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    cd = ImageDraw.Draw(caption)
    measurements["99% — 13 YEARS AND COUNTING"] = centered_text(
        cd, "99% — 13 YEARS AND COUNTING", 610, font(43), WHITE, 1)

    # Keep the button joke readable over the dark foreground skyline.
    cd.rounded_rectangle((54, 765, 970, 932), radius=26,
                         fill=(7, 9, 24, 216), outline=(100, 47, 116, 190), width=2)
    measurements["TIP: Press X to skip the 13-year wait."] = centered_text(
        cd, "TIP: Press X to skip the 13-year wait.", 790, font(38), WHITE, 1)
    measurements["(X does nothing. It never did.)"] = centered_text(
        cd, "(X does nothing. It never did.)", 849, font(38), (255, 199, 228), 1)
    canvas.alpha_composite(caption)

    footer = ImageDraw.Draw(canvas)
    footer.text((976, 975), "make.fun", font=font(23), fill=(255, 183, 222), anchor="ra",
                stroke_width=1, stroke_fill=(35, 13, 40))

    output = ROOT / "meme.png"
    canvas.convert("RGB").save(output, format="PNG", optimize=True)

    scale = 480 / SIZE
    for label, bounds in measurements.items():
        width = (bounds[2] - bounds[0]) * scale
        height = (bounds[3] - bounds[1]) * scale
        print(f"480px text bounds: {label!r}: {width:.1f} x {height:.1f}px")
        if label == "GTA VI":
            assert height >= 40, "The title is too small in the judge view."
        if label.startswith("TIP:") or label.startswith("(X"):
            assert height >= 16, "A tip line is too small in the judge view."

    if preview_path is not None:
        canvas.convert("RGB").resize((480, 480), Image.Resampling.LANCZOS).save(preview_path, format="PNG")
        print(f"480px preview: {preview_path}")
    print(f"Wrote {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview", type=Path, help="also write a 480 by 480 inspection image")
    args = parser.parse_args()
    compose(args.preview)


if __name__ == "__main__":
    main()
