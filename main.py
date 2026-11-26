#!/usr/bin/env python3
"""Copy the pre-rendered front page (entry.png) into the grader's output
directory and prove the copy is whole.

Only the Python standard library is used. The checks are:

* the file starts with the PNG magic bytes;
* the first chunk is IHDR and declares 1024x1024;
* every chunk's CRC (over type + data) is valid, up to and including IEND;
* the file is smaller than 1 MiB;
* the SHA-256 of the copied file matches the SHA-256 of the source.

Any failure prints an error and exits non-zero.
"""

import hashlib
import os
import struct
import sys
import zlib
from pathlib import Path

EXPECTED_SHA256 = "71bc29914e48f771010e286caffd92e689681549c2b59102639065cf12cb3a9d"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_BYTES = 1024 * 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def die(message):
    print("main.py: error: " + message, file=sys.stderr)
    raise SystemExit(1)


def hash_bytes(data):
    return hashlib.sha256(data).hexdigest()


def check_png_bytes(data):
    """Walk the PNG chunk by chunk and validate structure and CRCs."""
    if len(data) < len(PNG_MAGIC) + 25:
        die("file too small to be a PNG")
    if data[:8] != PNG_MAGIC:
        die("missing PNG magic bytes")
    pos = 8
    first = True
    seen_iend = False
    while pos + 8 <= len(data):
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        chunk_type = data[pos + 4:pos + 8]
        body_start = pos + 8
        body_end = body_start + length
        if body_end + 4 > len(data):
            die("truncated chunk %r" % chunk_type)
        body = data[body_start:body_end]
        (stored_crc,) = struct.unpack(">I", data[body_end:body_end + 4])
        actual_crc = zlib.crc32(chunk_type + body) & 0xFFFFFFFF
        if actual_crc != stored_crc:
            die("bad CRC in chunk %r" % chunk_type)
        if first:
            if chunk_type != b"IHDR":
                die("first chunk is not IHDR")
            (width, height) = struct.unpack(">II", body[:8])
            if width != EXPECTED_WIDTH or height != EXPECTED_HEIGHT:
                die("IHDR is %dx%d, expected %dx%d"
                    % (width, height, EXPECTED_WIDTH, EXPECTED_HEIGHT))
            first = False
        if chunk_type == b"IEND":
            seen_iend = True
            pos = body_end + 4
            break
        pos = body_end + 4
    if not seen_iend:
        die("no IEND chunk found")
    if pos != len(data):
        die("trailing bytes after IEND")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        die("MAKEFUN_OUTPUT_DIR is not set")
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        die("entry.png not found next to main.py")
    data = source.read_bytes()
    if len(data) >= MAX_BYTES:
        die("entry.png is %d bytes, over the 1 MiB limit" % len(data))
    if hash_bytes(data) != EXPECTED_SHA256:
        die("entry.png SHA-256 does not match the expected value")
    check_png_bytes(data)
    target_dir = Path(out_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"
    if target.resolve() == source.resolve():
        die("output directory is the same as the source directory; "
            "refusing to copy entry.png onto itself")
    target.write_bytes(data)
    copied = target.read_bytes()
    if hash_bytes(copied) != EXPECTED_SHA256:
        die("copied file SHA-256 does not match the source")
    print("OK: entry.png copied to %s (%d bytes, sha256 %s)"
          % (target, len(copied), EXPECTED_SHA256))


if __name__ == "__main__":
    main()
