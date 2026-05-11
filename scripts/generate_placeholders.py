#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write small PNG placeholders into static/img/ (stdlib only)."""

from __future__ import annotations

import base64
from pathlib import Path

# 1x1 transparent PNG
TINY_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMB/6X9n2kAAAAASUVORK5CYII="
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "static" / "img"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name in (
        "hero-stackforge.png",
        "card-flask.png",
        "card-nginx.png",
        "card-mysql.png",
    ):
        path = OUT / name
        path.write_bytes(TINY_PNG)
        print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
