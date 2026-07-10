"""Compose Chrome Web Store screenshots (1280x800) from raw captures.

Raw 1600w JPEG capture -> single Lanczos downscale into a dark brand canvas with a
rounded-corner frame and a caption rendered at 4x for crispness. PNG out (no lossy step).
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path("/Users/victorbejas/projects/local-resumer")
SRC = ROOT / "docs" / "captures"
OUT = ROOT / "docs" / "store" / "screenshots"

W, H = 1280, 800
BG = (13, 13, 15)
ACCENT = (110, 168, 254)  # --primary #6ea8fe
CAPTION_COLOR = (235, 237, 240)
SUB_COLOR = (140, 145, 155)

FONT = "/System/Library/Fonts/Helvetica.ttc"

SHOTS = [
    ("3.jpeg", "1-hero.png", "Any article, summarized: title, TL;DR & key points"),
    ("1.jpeg", "2-local.png", "Runs 100% on your device — nothing leaves your machine"),
    ("4.jpeg", "3-cloud.png", "Or bring your own key — OpenAI, Anthropic, OpenRouter"),
    ("2.jpeg", "4-progress.png", "Local inference on your GPU — live progress, cancel anytime"),
]

CAPTION_BAND = 128  # px reserved at the top
MARGIN_X = 50


def rounded(im: Image.Image, radius: int) -> Image.Image:
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, im.width - 1, im.height - 1), radius=radius, fill=255
    )
    im = im.convert("RGBA")
    im.putalpha(mask)
    return im


def caption_layer(text: str) -> Image.Image:
    """Render the caption at 4x and downscale — crisp text without a 4x screenshot."""
    s = 4
    layer = Image.new("RGBA", (W * s, CAPTION_BAND * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    font = ImageFont.truetype(FONT, 34 * s)
    # accent tick + text, horizontally centered as a unit
    tw = d.textlength(text, font=font)
    tick_w, gap = 10 * s, 18 * s
    total = tick_w + gap + tw
    x = (W * s - total) / 2
    y = (CAPTION_BAND * s) / 2
    d.rounded_rectangle(
        (x, y - 17 * s, x + tick_w, y + 17 * s), radius=4 * s, fill=(*ACCENT, 255)
    )
    d.text((x + tick_w + gap, y), text, font=font, fill=(*CAPTION_COLOR, 255), anchor="lm")
    return layer.resize((W, CAPTION_BAND), Image.LANCZOS)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for src_name, out_name, caption in SHOTS:
        shot = Image.open(SRC / src_name).convert("RGB")

        # Fit inside the canvas below the caption band, keeping aspect (single downscale).
        max_w = W - 2 * MARGIN_X
        max_h = H - CAPTION_BAND - 40  # bottom margin
        scale = min(max_w / shot.width, max_h / shot.height)
        shot = shot.resize(
            (round(shot.width * scale), round(shot.height * scale)), Image.LANCZOS
        )
        shot = rounded(shot, radius=14)

        canvas = Image.new("RGBA", (W, H), (*BG, 255))

        # Soft glow behind the frame so it separates from the background.
        x = (W - shot.width) // 2
        y = CAPTION_BAND + (H - CAPTION_BAND - 40 - shot.height) // 2
        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(glow).rounded_rectangle(
            (x - 2, y - 2, x + shot.width + 2, y + shot.height + 2),
            radius=16,
            fill=(*ACCENT, 70),
        )
        canvas.alpha_composite(glow.filter(ImageFilter.GaussianBlur(12)))

        canvas.alpha_composite(shot, (x, y))
        canvas.alpha_composite(caption_layer(caption), (0, 0))

        canvas.convert("RGB").save(OUT / out_name, "PNG")
        print(out_name, "ok")


if __name__ == "__main__":
    main()
