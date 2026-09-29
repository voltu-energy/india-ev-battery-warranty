#!/usr/bin/env python3
"""Record what each source document was, so a value stays checkable after its host stops serving it.

Why this exists. On 29 September 2026, four of five BYD India asset URLs that search engines had
indexed stopped serving, inside about a week, including all three warranty policies. The BYD rows
survived only because the files had been saved by hand. A dataset whose whole claim is that every
value can be checked at the source needs an answer for the source going away, and it did not have
one.

Two artefacts, because there are two different problems.

  sha256      For a PDF, which is a fixed document. The hash does not bring the file back. It lets
              anyone who obtains a copy by any route prove it is the document we read.
  archive_url An Internet Archive snapshot, which is the right artefact for a web page. Hashing an
              HTML page is noise: it changes on every render. A dated capture freezes what the page
              said.

Re-running is the point. A hash that no longer matches is not an error to be written over, it is a
finding: a maker has edited a document under us. This script never overwrites a recorded hash. It
reports the mismatch and exits non-zero.

    python3 scripts/freeze-sources.py            # fill in what is missing
    python3 scripts/freeze-sources.py --check    # verify only, write nothing. For CI
    python3 scripts/freeze-sources.py --only tata   # limit to source_ids containing a string

Needs ordinary outbound internet. It will not run inside a sandbox with an egress allowlist; every
manufacturer host returns a proxy 403 there.
"""
import argparse, csv, hashlib, io, json, sys, time, urllib.parse, urllib.request

CSV = "data/sources.csv"
UA = {"User-Agent": "Mozilla/5.0 (compatible; india-ev-battery-warranty/1.1; +https://github.com/voltu-energy/india-ev-battery-warranty)"}
AVAIL = "https://archive.org/wayback/available?url="


def get(url, timeout=45):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout)


def is_pdf(url):
    return url.lower().split("?")[0].endswith(".pdf")


def snapshot(url):
    """Closest Internet Archive capture, or None. Never invents one."""
    try:
        d = json.loads(get(AVAIL + urllib.parse.quote(url, safe=""), timeout=30).read())
        s = d.get("archived_snapshots", {}).get("closest") or {}
        return (s.get("url"), s.get("timestamp")) if s.get("available") else (None, None)
    except Exception:
        return (None, None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="verify recorded hashes, write nothing")
    ap.add_argument("--only", default="", help="limit to source_ids containing this string")
    a = ap.parse_args()

    rows = list(csv.DictReader(io.open(CSV, encoding="utf-8")))
    fields = list(rows[0].keys())
    for c in ("sha256", "archive_url"):
        if c not in fields:
            fields.append(c)

    hashed = archived = skipped = 0
    mismatches, unreachable = [], []

    for r in rows:
        for c in ("sha256", "archive_url"):
            r.setdefault(r.get(c) and c or c, r.get(c, "") or "")
        sid, url = r["source_id"], r["url"]
        if a.only and a.only not in sid:
            continue

        if is_pdf(url) and (not r["sha256"] or a.check):
            try:
                body = get(url).read()
                h = hashlib.sha256(body).hexdigest()
                if r["sha256"] and r["sha256"] != h:
                    mismatches.append((sid, r["sha256"], h, len(body)))
                    print(f"  CHANGED  {sid}\n           recorded {r['sha256']}\n           now      {h}  ({len(body)} bytes)")
                elif not r["sha256"]:
                    if not a.check:
                        r["sha256"] = h
                    hashed += 1
                    print(f"  hashed   {sid}  {h[:16]}…  {len(body)} bytes")
            except Exception as e:
                unreachable.append((sid, url, str(e)[:90]))
                print(f"  NOFETCH  {sid}  {str(e)[:70]}")
            time.sleep(0.4)
        elif not is_pdf(url):
            skipped += 1

        if not r["archive_url"] and not a.check:
            su, ts = snapshot(url)
            if su:
                r["archive_url"] = su
                archived += 1
                print(f"  archive  {sid}  {ts}")
            time.sleep(0.4)

    if not a.check:
        with io.open(CSV, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)

    print(f"\n{hashed} hashed, {archived} archive urls found, {skipped} html rows skipped "
          f"(a byte hash of a web page is noise; those get archive_url instead)")
    if unreachable:
        print(f"\n{len(unreachable)} could not be fetched. Each one is a row whose source may already be gone:")
        for sid, url, err in unreachable:
            print(f"  {sid}\n    {url}\n    {err}")
    if mismatches:
        print(f"\n{len(mismatches)} DOCUMENT(S) CHANGED SINCE WE READ THEM. Nothing was overwritten.")
        print("Re-read the document, update the row and the dependent values, and record the change.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
