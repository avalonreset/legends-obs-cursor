from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SCREENSHOTS = ASSETS / "screenshots"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def add_linear_gradient(img: Image.Image) -> Image.Image:
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    pixels = overlay.load()
    width, height = img.size
    for x in range(width):
        alpha = int(188 * max(0.0, 1.0 - x / (width * 0.72)))
        for y in range(height):
            pixels[x, y] = (3, 8, 10, alpha)
    return Image.alpha_composite(img.convert("RGBA"), overlay)


def fit_cover(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_w, target_h = size
    src_w, src_h = img.size
    scale = max(target_w / src_w, target_h / src_h)
    resized = img.resize((int(src_w * scale), int(src_h * scale)), Image.Resampling.LANCZOS)
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def render_banner() -> None:
    source = ASSETS / "banner-source.png"
    if source.exists():
        img = fit_cover(Image.open(source).convert("RGBA"), (1792, 768))
    else:
        img = Image.new("RGBA", (1792, 768), (5, 10, 13, 255))

    img = add_linear_gradient(img)
    draw = ImageDraw.Draw(img)

    title_font = font(86, bold=True)
    tag_font = font(33)
    small_font = font(24)

    draw.text((92, 214), "Legends OBS Cursor", fill=(238, 255, 248, 255), font=title_font)
    draw.text(
        (98, 326),
        "Momentum cursor overlay for OBS Studio",
        fill=(142, 242, 213, 255),
        font=tag_font,
    )
    draw.text(
        (100, 384),
        "Rotating ticks. Distinct click art. Optional floaty follow.",
        fill=(207, 218, 222, 235),
        font=small_font,
    )

    accent = Image.new("RGBA", img.size, (0, 0, 0, 0))
    adraw = ImageDraw.Draw(accent)
    adraw.rounded_rectangle((96, 478, 515, 538), radius=18, outline=(0, 255, 164, 210), width=3)
    adraw.text((128, 493), "OBS Lua filter", fill=(235, 255, 249, 255), font=small_font)
    adraw.rounded_rectangle((540, 478, 930, 538), radius=18, outline=(255, 76, 205, 190), width=3)
    adraw.text((572, 493), "Backup-first installer", fill=(235, 255, 249, 255), font=small_font)
    img = Image.alpha_composite(img, accent)

    img.convert("RGB").save(ASSETS / "banner.webp", "WEBP", quality=84, method=6)
    img.convert("RGB").resize((1280, 640), Image.Resampling.LANCZOS).save(
        ASSETS / "social-preview.jpg", "JPEG", quality=86, optimize=True
    )


def glow_layer(size: tuple[int, int], center: tuple[float, float], radius: float, color: tuple[int, int, int]) -> Image.Image:
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for i in range(22, 0, -1):
        a = int(6 * i)
        r = radius + i * 5
        draw.ellipse(
            (center[0] - r, center[1] - r, center[0] + r, center[1] + r),
            outline=(*color, a),
            width=3,
        )
    return layer.filter(ImageFilter.GaussianBlur(3.0))


def draw_cursor_art(
    img: Image.Image,
    center: tuple[float, float],
    velocity: tuple[float, float],
    right_click: bool = False,
) -> None:
    draw = ImageDraw.Draw(img)
    main = (0, 255, 120)
    cyan = (58, 209, 255)
    magenta = (255, 46, 199)
    white = (245, 255, 252)

    img.alpha_composite(glow_layer(img.size, center, 82, main))

    vx, vy = velocity
    angle = math.atan2(vy, vx) if vx or vy else -0.7
    speed = min(math.hypot(vx, vy) / 18.0, 1.0)

    for i in range(8):
        age = i / 8.0
        x = center[0] - vx * age * 0.22
        y = center[1] - vy * age * 0.22
        r = 24 + age * 24
        a = int(120 * (1.0 - age))
        draw.ellipse((x - r, y - r, x + r, y + r), outline=(0, 255, 138, a), width=3)

    radius = 82
    draw.ellipse(
        (center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius),
        outline=(*main, 235),
        width=12,
    )
    draw.arc(
        (center[0] - 114, center[1] - 114, center[0] + 114, center[1] + 114),
        start=math.degrees(angle) - 34,
        end=math.degrees(angle) + 34,
        fill=(*cyan, 225),
        width=7,
    )

    tick_count = 10
    spin = -angle + speed * 1.6
    for i in range(tick_count):
        theta = spin + i * math.tau / tick_count
        tx = center[0] + math.cos(theta) * 122
        ty = center[1] + math.sin(theta) * 122
        dot_r = 7 + (i % 3) * 1.6
        draw.ellipse((tx - dot_r, ty - dot_r, tx + dot_r, ty + dot_r), fill=(*main, 220))

    pointer = [
        (center[0] - 12, center[1] - 48),
        (center[0] + 34, center[1] + 36),
        (center[0] + 4, center[1] + 30),
        (center[0] - 22, center[1] + 60),
    ]
    draw.polygon(pointer, fill=(12, 20, 20, 235), outline=white)
    draw.line(pointer + [pointer[0]], fill=white, width=4)

    if right_click:
        diamond_r = 150
        diamond = [
            (center[0], center[1] - diamond_r),
            (center[0] + diamond_r, center[1]),
            (center[0], center[1] + diamond_r),
            (center[0] - diamond_r, center[1]),
        ]
        draw.line(diamond + [diamond[0]], fill=(*magenta, 230), width=8)
        draw.ellipse(
            (center[0] - 42, center[1] - 42, center[0] + 42, center[1] + 42),
            outline=(*magenta, 255),
            width=8,
        )


def render_screenshot(path: Path, title: str, subtitle: str, center: tuple[int, int], velocity: tuple[int, int], right_click: bool = False) -> None:
    size = (1600, 900)
    img = Image.new("RGBA", size, (5, 7, 9, 255))
    draw = ImageDraw.Draw(img)

    for x in range(0, size[0], 80):
        draw.line((x, 0, x, size[1]), fill=(16, 24, 27, 120), width=1)
    for y in range(0, size[1], 80):
        draw.line((0, y, size[0], y), fill=(16, 24, 27, 120), width=1)

    draw_cursor_art(img, center, velocity, right_click=right_click)

    panel = Image.new("RGBA", size, (0, 0, 0, 0))
    pdraw = ImageDraw.Draw(panel)
    pdraw.rounded_rectangle((64, 642, 815, 812), radius=22, fill=(4, 10, 12, 215), outline=(44, 72, 76, 200), width=2)
    pdraw.text((98, 680), title, fill=(238, 255, 248, 255), font=font(46, bold=True))
    pdraw.text((100, 744), subtitle, fill=(185, 211, 213, 245), font=font(28))
    img = Image.alpha_composite(img, panel)

    img.convert("RGB").save(path, "PNG", optimize=True)


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    SCREENSHOTS.mkdir(exist_ok=True)
    render_banner()
    render_screenshot(
        SCREENSHOTS / "momentum-ticks.png",
        "Momentum ticks",
        "Orbiting dots rotate against movement with floaty follow.",
        center=(1060, 390),
        velocity=(380, -120),
    )
    render_screenshot(
        SCREENSHOTS / "right-click-diamond.png",
        "Distinct right-click art",
        "Magenta diamond burst keeps click feedback readable on stream.",
        center=(1030, 410),
        velocity=(-220, 70),
        right_click=True,
    )


if __name__ == "__main__":
    main()

