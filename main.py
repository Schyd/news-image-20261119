#!/usr/bin/env python3
"""Ship the entry image.

Copies the news.png sitting next to this file into the make.fun output
directory as entry.png. The output directory comes from the
MAKEFUN_OUTPUT_DIR environment variable and defaults to /output.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path


def main() -> None:
    here = Path(__file__).resolve().parent
    source = here / "news.png"
    if not source.is_file():
        raise SystemExit(f"missing input image: {source}")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(source, target)
    print(f"copied {source} -> {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
