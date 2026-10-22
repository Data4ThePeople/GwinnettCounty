"""Instagram carousel: the post's charts centered on 1080x1350 (4:5) slides in the chart background color, so the
padding blends into each chart. Nothing is redrawn; each slide is the published image, scaled to fit.
Output: posts/gwinnett-county-rents/social/instagram-01.png onward."""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from plot_style import SURFACE  # noqa: E402

POST = ROOT / "posts" / "gwinnett-county-rents"
SLIDES = ["01-atlanta-map.png", "04-income-vs-rent.png", "06-older-apartment-rents.png", "07-renter-pay.png"]
W, H = 1080, 1350


def slide(src, dst):
    im = Image.open(src).convert("RGB")
    scale = min(W / im.width, H / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    canvas = Image.new("RGB", (W, H), SURFACE)
    canvas.paste(im, ((W - im.width) // 2, (H - im.height) // 2))
    canvas.save(dst)
    print(f"wrote {dst.relative_to(ROOT)} from {src.name}")


if __name__ == "__main__":
    out = POST / "social"
    out.mkdir(exist_ok=True)
    for i, name in enumerate(SLIDES, 1):
        slide(POST / "images" / name, out / f"instagram-{i:02d}.png")
