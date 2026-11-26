"""News-image entrypoint (Python 3.13, standard library only).

The front page is drawn deterministically by draw.py and shipped in this
repository as entry.png; this program copies it to the output directory,
so both grader runs write byte-identical output.

Run outside the grader with:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import hashlib
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
OUTPUT_NAME = "entry.png"


def output_dir():
    """Grader output directory: $MAKEFUN_OUTPUT_DIR, else /output."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def sha256_of(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if not SOURCE.is_file():
        print(f"missing shipped image: {SOURCE}", file=sys.stderr)
        return 1
    out = output_dir()
    out.mkdir(parents=True, exist_ok=True)
    target = out / OUTPUT_NAME
    shutil.copyfile(SOURCE, target)
    if sha256_of(target) != sha256_of(SOURCE):
        print("copied image does not match shipped image", file=sys.stderr)
        return 1
    print(f"wrote {target} sha256={sha256_of(target)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
