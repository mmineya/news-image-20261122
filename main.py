#!/usr/bin/env python3
"""news-image-20261122: emit the front-page image for the make.fun bounty.

Copies entry.png (kept next to this file) to /output/entry.png.
Deterministic: same bytes every run, no network, no randomness, no
timestamps. Python 3.13, standard library only.

Usage:
    python3 main.py            # writes /output/entry.png
    python3 main.py <path>     # writes to <path> instead (testing)
"""
import os
import shutil
import sys

DEFAULT_OUTPUT = "/output/entry.png"


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUTPUT
    out_dir = os.path.dirname(os.path.abspath(out))
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, out)
    print(f"Wrote {out} ({os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
