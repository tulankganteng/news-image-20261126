#!/usr/bin/env python3
"""news-image-20261126 entry runner.

The picture itself is pre-rendered and stored next to this file as
``entry.png``.  All this program does is place an exact copy of it in
the output directory and prove the copy is whole, using only the
standard library: no network, no clock, no image libraries.
"""
import hashlib
import os
import struct
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
WANTED_WIDTH = 1024
WANTED_HEIGHT = 1024
MAX_BYTES = 1048576


def die(message):
    sys.stderr.write("error: %s\n" % message)
    raise SystemExit(1)


def digest(blob):
    return hashlib.sha256(blob).hexdigest()


def dimensions(blob):
    """Pull width and height out of the PNG IHDR chunk."""
    if len(blob) < 24:
        die("file too short to hold a PNG header")
    if blob[:8] != PNG_MAGIC:
        die("not a PNG file (bad magic bytes)")
    if blob[12:16] != b"IHDR":
        die("first PNG chunk is not IHDR")
    width, height = struct.unpack(">II", blob[16:24])
    return width, height


def check_chunks(blob):
    """Walk every PNG chunk, checking lengths and CRCs, until IEND.

    The gate rejects a truncated or corrupt image, so the copy must be
    a whole PNG, not just a file with the right header and size.
    """
    import zlib

    pos = 8
    seen_iend = False
    while pos + 8 <= len(blob):
        length = struct.unpack(">I", blob[pos:pos + 4])[0]
        ctype = blob[pos + 4:pos + 8]
        end = pos + 8 + length + 4
        if end > len(blob):
            die("chunk %r runs past the end of the file" % ctype)
        stored_crc = struct.unpack(">I", blob[end - 4:end])[0]
        actual_crc = zlib.crc32(ctype + blob[pos + 8:pos + 8 + length])
        if stored_crc != (actual_crc & 0xFFFFFFFF):
            die("chunk %r has a bad CRC" % ctype)
        if ctype == b"IEND":
            if end != len(blob):
                die("trailing bytes after IEND chunk")
            seen_iend = True
            break
        pos = end
    if not seen_iend:
        die("no IEND chunk found: PNG is truncated")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    try:
        with open(source, "rb") as handle:
            blob = handle.read()
    except OSError as exc:
        die("cannot read entry.png: %s" % exc)

    width, height = dimensions(blob)
    if (width, height) != (WANTED_WIDTH, WANTED_HEIGHT):
        die("entry.png is %dx%d, expected %dx%d"
            % (width, height, WANTED_WIDTH, WANTED_HEIGHT))
    check_chunks(blob)
    if len(blob) > MAX_BYTES:
        die("entry.png is %d bytes, over the 1 MiB limit" % len(blob))

    wanted = digest(blob)
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(outdir, exist_ok=True)
    except OSError as exc:
        die("cannot create output dir %s: %s" % (outdir, exc))
    target = os.path.join(outdir, "entry.png")
    try:
        with open(target, "wb") as handle:
            handle.write(blob)
        with open(target, "rb") as handle:
            copied = handle.read()
    except OSError as exc:
        die("cannot write %s: %s" % (target, exc))

    if digest(copied) != wanted:
        die("copy mismatch: SHA-256 of output differs from entry.png")
    if len(copied) != len(blob):
        die("copy mismatch: output is %d bytes, expected %d"
            % (len(copied), len(blob)))
    print("wrote %s (%d bytes, %dx%d, sha256 %s)"
          % (target, len(copied), width, height, wanted))


if __name__ == "__main__":
    main()
