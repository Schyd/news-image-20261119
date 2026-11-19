"""news-image-20261119 entry: write the 19 November 2026 world-news summary
image to /output/entry.png.

The image itself is drawn by build_image.py (Pillow + DejaVu, run at build
time) and shipped in this repository as news.png; this program copies it to
the output path. Copying a repository-held image is the simplest entry the
bounty rules describe, and it is deterministic: two runs write the same
bytes, with no network.

Run locally:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
SOURCE = HERE / "news.png"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, OUTPUT_DIR / "entry.png")


if __name__ == "__main__":
    main()
