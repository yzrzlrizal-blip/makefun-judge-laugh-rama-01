#!/usr/bin/env python3
"""make.fun entry for "Make the AI Judge Laugh"
(u-rama-melon-make-the-ai-judge-laugh-302d0825).

Reads the one-line office joke shipped in entry.txt next to this file and
writes it verbatim to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output).
Pure standard library; no network, no secrets, nothing read from outside
this repository.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

MAX_CHARS = 200


def load_joke() -> str:
    here = Path(__file__).resolve().parent
    text = (here / "entry.txt").read_text(encoding="utf-8")
    line = text.rstrip("\n")
    if not line or line.isspace():
        raise ValueError("entry.txt is empty")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError(f"entry is {len(line)} chars, over the {MAX_CHARS} limit")
    if any(ord(ch) < 0x20 for ch in line):
        raise ValueError("entry holds a control character")
    return line


def main() -> int:
    joke = load_joke()
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_text(joke, encoding="utf-8")
    # Verify on write: the bytes on disk must be exactly the joke.
    if target.read_text(encoding="utf-8") != joke:
        raise ValueError("verify failed: entry.txt on disk differs from the joke")
    print(f"wrote {len(joke)} characters to {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
