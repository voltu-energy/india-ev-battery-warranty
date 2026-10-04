#!/usr/bin/env python3
"""Decode the text layer of the Hyundai Creta Electric owner's manual.

The PDF Hyundai publishes at
  https://www.hyundai.com/content/dam/hyundai/in/en/data/connect-to-service/owners-manual/pc/cretaev.pdf
embeds its fonts as subsets with custom encodings, so `pdftotext` returns
mojibake and a reader concludes the document is unreadable. It is not.

There are two subset fonts and they shift in opposite directions:

  * most of the manual is ASCII shifted DOWN by 29, so 0x03 is a space,
    0x11 a full stop, 'H' an 'e' and '3' a 'P'
  * the warranty pages near the front are ASCII shifted UP by 29, so 'e' is
    an 'H', '_' a 'B' and 'K' a full stop
  * in both, digits are moved out to U+0238..U+0241, in the order 1..9 then 0

Digits are the part that matters. The two figures that carry the most weight in
that manual, the 10 percent floor and the 20 percent full-charge trigger, are
digits, and digits are exactly what the encoding hides. Anyone quoting this
manual from a rendered page is reading pixels. This reads the file.

Direction is chosen per page by counting common English words in each
candidate, because the two fonts are mixed within one document.

Verification, which runs every time: the manual prints a chapter-page marker on
nearly every page. Decoded, those run in order from 1-3 to 9-55 across 471
pages. A wrong map does not produce an ordered sequence, so the check is the
proof, and the script withholds output if it fails.

Usage:
    pdftotext cretaev.pdf cretaev.txt
    python3 scripts/decode-hyundai-creta.py cretaev.txt > cretaev.decoded.txt
"""
import re
import sys

DIGITS = {0x238 + i: str(i + 1) for i in range(9)}
DIGITS[0x241] = "0"
SHIFT = 29
# Whitespace is emitted by the text extractor, not by the font, so it is never
# encoded and must survive untouched. Shifting a newline turns it into an
# apostrophe and silently welds every line of the page together.
LITERAL = set("\t\n\r\f ")
COMMON = re.compile(
    r"\b(the|and|warranty|battery|vehicle|charging|of|to|is|for|shall|this|not)\b", re.I
)


def _shift(text, delta):
    out = []
    for ch in text:
        if ch in LITERAL:
            out.append(ch)
            continue
        c = ord(ch)
        if c in DIGITS:
            out.append(DIGITS[c])
            continue
        n = c + delta
        out.append(chr(n) if 0x20 <= n <= 0x7E else ch)
    return "".join(out)


def decode_page(page):
    """Try both fonts and keep whichever reads as English."""
    down, up = _shift(page, SHIFT), _shift(page, -SHIFT)
    return down if len(COMMON.findall(down)) >= len(COMMON.findall(up)) else up


def verify(pages):
    seen = []
    for p in pages:
        m = re.findall(r"\b(\d)-(\d{1,3})\b", p)
        if m:
            seen.append((int(m[-1][0]), int(m[-1][1])))
    if len(seen) < 100:
        return False, f"only {len(seen)} page markers decoded, expected hundreds"
    falls = sum(1 for a, b in zip(seen, seen[1:]) if b < a)
    if falls > len(seen) * 0.08:
        return False, f"page markers are not ordered ({falls} steps backwards)"
    return True, f"{len(seen)} page markers in order, {seen[0]} to {seen[-1]}"


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    raw = open(sys.argv[1], encoding="utf-8", errors="replace").read()
    pages = [decode_page(p) for p in raw.split("\f")]
    ok, msg = verify(pages)
    print(f"verification: {msg}", file=sys.stderr)
    if not ok:
        sys.exit("decode failed its own check, output withheld")
    sys.stdout.write("\f".join(pages))


if __name__ == "__main__":
    main()
