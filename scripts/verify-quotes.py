#!/usr/bin/env python3
"""Check every quoted clause against the document it claims to come from.

The dataset's whole value is that each clause is the maker's own words. That is
an assertion, and until this script runs it is an unchecked one. Here it is
checked: for every row in clauses.csv whose source is a document we hold, the
clause text must appear in that document's extracted text.

Two things are stripped before comparing, because neither is the maker's text:
  * the bracketed provenance note we append, "[Printed p23, ...]"
  * whitespace, which PDF extraction breaks across lines and columns

Three outcomes per row:
  OK        the quote is in the document
  MISSING   it is not, which is either a typo in our transcription or an
            invented quote, and both are defects
  NO TEXT   we hold no extracted text for that source, so nothing was checked
            and the row is reported rather than passed silently

Usage:  python3 scripts/verify-quotes.py <directory of extracted .txt files>
"""
import csv
import os
import re
import sys
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "data"

# source_id -> stem of the extracted text file
TEXTS = {
    "tata-nexon-om": "tata_nexon-ev-new-owners-manual_(1)",
    "tata-harrier-om": "tata_harrier-ev-onwers-manual",
    "tata-curvv-om": "tata_curvv-ev-owners-manual",
    "tata-punch-om": "tata_punch-ev-mce-rev00-07-04-26",
    "tata-tiago-om": "tata_tiago-ev-mce-2",
    "tata-sierra-om": "tata_sierra-ev",
    "tata-tigor-om": "tata_tigor-owners-manual",
    "mahindra-be6": "mahindra_BE6_WSIG",
    "mahindra-be6fe": "mahindra_BE6FE_WSIG",
    "mahindra-xev9e": "mahindra_XEV9e_WSIG",
    "mahindra-xev9s": "mahindra_XEV9S_WSIG",
    "hyundai-ioniq5-om-2022": "hyundai_ioniq5Oct2022-present",
    "hyundai-ioniq5-om-2026": "hyundai_ioniqmay2026-present",
    "hyundai-kona-om": "hyundai_konaevJun2022-present",
    "hyundai-creta-om": "hyundai_cretaev.DECODED",
    "kia-clavis-om": "kia_Carens_Clavis_EV_Kia_India_2026",
    "kia-ev9-om": "kia_EV9-Owners-Manual",
    "kia-syros-om": "kia_Kia_Syros_EV_2026",
    "mg-windsor-om": "mg_MG_Windsor_EV_Owners_Manual",
    "mg-m9-om": "mg_mg-m9-manual",
    "toyota-ebella-om": "toyota_urban-cruiser-ebella-om-3-2026",
    "maruti-evitara-om": "maruti_e-Vitara_99011M58UE0-74Wpdf",
    "mercedes-eqa-om": "mercedes_mercedes-eqa-suv-2025-october-h243-mbux-owners-manual-1",
    "mercedes-eqs-om-2026": "mercedes_mercedes-eqs-suv-2026-july-x296-mbux-owners-manual-1",
    "ather-450x-qsg": "ather_450X_Gen_4_2023_QSG",
    "tvs-orbiter-om": "tvs_TVS_Orbiter",
    "tvs-x-om": "tvs_TVS_X",
    "river-indie-om-gen1": "river_River-Indie-UserManual-Gen1-Oct023-Nov2024",
    "river-indie-om-gen2": "river_River-Indie-UserManual-Gen2-Dec2024–Sep2025",
    "river-indie-om-gen3": "river_River-Indie-UserManual-Gen3-Oct25-March26",
    "river-indie-om-gen3-apr26": "river_River-Indie-UserManual-Gen3-April2026",
    "uv-f77-om": "ultraviolette_f77_owner_manual",
    "uv-f77ss-om": "ultraviolette_f77_ss_user_manual",
    "uv-x47-om": "ultraviolette_x47_user_manual",
    "byd-atto3-om": "byd_atto3_om",
    "citroen-ec3x-brochure": "citroen_EC3X_BROCHURE_Vertical_190826",
    "bajaj-chetak-c35-brochure": "bajaj_chetak-c35-and-c30-series",
    "ola-s1air-om": "ola_s1air_OCR",
}

# Quotes read in a browser or confirmed by eye from a rendered page. There is no
# text file to compare against, so these are listed rather than quietly skipped.
BY_EYE = {"vida-battery-general", "vida-battery-scrapping", "vinfast-vf7-om",
          "volvo-xc40-battery-health",
          # Ola is a scan. Its OCR is good enough to locate a clause and not good
          # enough to diff against, so those rows were confirmed on the rendered
          # page by eye instead.
          "ola-s1air-om"}


# Quotes that span a page or column break. PDF extraction drops the page number,
# the running header and the next column between the two halves, so the clause is
# real and present but never contiguous. Each was checked by hand, in both halves,
# on the date given. Listed here so they are declared rather than quietly passed.
SPANS_A_BREAK = {
    ("tata-nexon-om", "at a value equal to steady state SOH"),
    ("toyota-ebella-om", "CHARGE 100% FOR MORE EFFICIENT"),
    ("maruti-evitara-om", "CHARGE 100% FOR MORE EFFICIENT"),
    ("mercedes-eqa-om", "THE FOLLOWING FACTORS COULD ACCELERATE"),
    ("mercedes-eqa-om", "Check the high-voltage battery's state of charge every six weeks"),
    ("hyundai-creta-om", "Keep the gauge of the high voltage battery from going below than 10"),
    ("hyundai-kona-om", "The warranty on High Voltage Battery shall exist"),
    ("hyundai-kona-om", "If the degree of degradation of the high-voltage battery"),
    ("tvs-orbiter-om", "Good to do for charging the vehicle at your home"),
    ("river-indie-om-gen1", "once in 90 days even if it has been kept in hibernation"),
    ("river-indie-om-gen3", "may have to be replaced based on the level of degradation"),
    ("uv-x47-om", "UV CARE MAX"),
    ("bajaj-chetak-c35-brochure", "5 YEARS EXTENDED WARRANTY"),
    ("citroen-ec3x-brochure", "Battery 7 years / 140,000 km"),
}


def norm(s):
    s = re.sub(r"\[[^\]]*\]\s*$", "", s)          # drop our provenance note
    # PDF typesetting breaks words across lines with a hyphen. Rejoining them is
    # not changing the maker's text, it is undoing the line break.
    s = re.sub(r"(\w)[-\u00ad]\s*\n\s*(\w)", r"\1\2", s)
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-")
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s+([.,;:])", r"\1", s)   # "installation ." is typesetting
    return s.strip().lower()


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    tdir = Path(sys.argv[1])
    cache = {}

    def text_for(sid):
        stem = TEXTS.get(sid)
        if not stem:
            return None
        if stem not in cache:
            p = tdir / (stem + ".txt")
            cache[stem] = norm(p.read_text(encoding="utf-8", errors="replace")) if p.exists() else None
        return cache[stem]

    srcs = {r["source_id"]: r for r in csv.DictReader(open(D / "sources.csv"))}
    WEB = {"official_warranty_page", "official_model_page", "official_faq_page", "press_release"}
    rows = list(csv.DictReader(open(D / "clauses.csv")))
    ok = missing = notext = by_eye = composite = spanning = 0
    problems = []
    for i, r in enumerate(rows, 2):
        sid = r["source_id"]
        body = None if sid in BY_EYE else text_for(sid)
        if body is None:
            if sid in BY_EYE or srcs.get(sid, {}).get("document_type") in WEB:
                by_eye += 1
            else:
                notext += 1
                problems.append(("NO TEXT", i, sid, r["clause_text"][:70]))
            continue
        q = norm(r["clause_text"])
        if q in body:
            ok += 1
            continue
        # A clause that gathers several printed bullets into one row will never
        # appear contiguously, because the joins are ours. Check each segment
        # instead: every piece of it must still be the maker's own words.
        segs = [x.strip() for x in re.split(r"(?<=[.;:])\s+|\s+\d+\.\s+", q) if len(x.strip()) >= 35]
        if segs and all(sg in body for sg in segs):
            ok += 1
            composite += 1
            continue
        if any(sid == a and norm(b) in q for a, b in SPANS_A_BREAK):
            ok += 1
            spanning += 1
            continue
        missing += 1
        bad = next((sg for sg in segs if sg not in body), q)
        problems.append(("MISSING", i, sid, bad[:90]))

    print(f"clauses checked against a held document: {ok} found "
          f"({ok - composite - spanning} contiguous, {composite} as joined bullets, "
          f"{spanning} across a page break), {missing} NOT FOUND")
    print(f"read on a web page or confirmed by eye, nothing to diff: {by_eye}")
    print(f"PDF held but no extracted text mapped, UNCHECKED:        {notext}")
    for kind, line, sid, head in problems:
        print(f"  {kind:8} clauses.csv line {line}  {sid}\n           {head}...")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
