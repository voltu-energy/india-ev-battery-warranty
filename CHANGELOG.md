# Changelog

## 1.1.2, 29 September 2026

The Mahindra XUV400 closed, and it is a better fact than the absence it replaces. Tata's own warranty page read properly.

### Added
- **Six clauses from `ev.tata.cars/service/warranty.html`**, and the page itself as a source. The
  terms sit behind accordions that open one at a time, so every earlier automated read returned the
  headings and not the clauses. Read in a browser with all panels forced open.
  - The 70 percent SOH threshold, on a page a buyer is directed to, and the 80 percent restore
    ceiling.
  - Ordinary ageing above the threshold is outside cover, in terms.
  - "Lifetime" defined as fifteen years from first registration.
  - "Unlimited kilometres" excludes display, demonstration, test drives, courtesy, commercial
    operations, fleet management and taxi use, which drop to 8 or 10 years and a kilometre cap.
  - The lifetime warranty does not pass to a second owner unless that owner notifies Tata.
- **`ev.tata.cars/service/ew-details.html` as an absence we checked.** The extended warranty lists
  nine covered systems and the HV battery is not one of them. It points at a Digital Extended
  Warranty Booklet available only from a workshop, which Tata does not publish.

### Changed
- **The XUV400 row carries terms now.** It had `NOT_FOUND` across the board with a note saying no
  warranty guide is published. That was true and incomplete. Mahindra publishes the terms in one
  place: two rows at the foot of the specification table on page 8 of the Pro Range brochure,
  "BATTERY PACK AND MOTOR WARRANTY: 8 YEARS OR 1,60,000 KM" and "VEHICLE WARRANTY: 3 YEARS OR
  UNLIMITED KM", footnoted "whichever is earlier". The row now reads 8 years, 1,60,000 km, with
  `NOT_STATED` for the state of health floor and the measuring party, because all eight pages were
  read and none of that is in the document.
- The brochure has no embedded fonts and is entirely scanned images, so no text tool can read it. It
  was read by looking at the pages, and the source row says so.

### Notes
- The comparison that matters is inside Mahindra rather than across makers. Its warranty guides for
  the XEV 9e, BE 6, XEV 9S and BE 6 FE all carry an 85/75/70 tiered floor and charging exclusions.
  The XUV400 gets a line item in a brochure.
- The warranty page lists six models. The Tigor.ev, XPRES-T EV, Nexon.ev 30, Tiago.ev 19.2 and
  Punch.ev 35 do not appear on it. Recorded with the date, because a page can change.
- The owner manual index at `ev.tata.cars/support/owner-manual.html` carries eight PDFs and has no
  separate manual for the three smaller packs. Those variants are covered by the larger variant's
  manual, so they are a scope note rather than a gap in our reading, and the wording that called them
  unpublished has been corrected.

56 sources, 67 models, 71 clauses.

## 1.1.1, 29 September 2026

Two corrections to 1.1.0 and one source closed. No warranty value changed.

### Changed
- **The Tata XPRES-T EV source row now cites the manual itself.** It had pointed at the
  `ev.tata.cars` homepage rather than a document, with no `sha256` and no `archive_url`, which made it
  the only PDF-typed source in the set with no checksum. It now carries the manual's own URL on
  `xprest.tatamotors.com`, its hash and a read date. **25 of 25 PDF sources are hashed.** That row
  matters more than most: it is the one behind the shortest battery term in the dataset, 3 years or
  1,25,000 km on the fleet and taxi variant.

### Fixed
- **1.1.0's own entry for the `sha256` column was stale on release.** It said four rows were populated
  and twenty remained, which was true while it was being drafted and not by the time it shipped; the
  commit message said all 24. Corrected here rather than rewritten there, because 1.1.0 is tagged and
  pushed. The released state was 24 of 24 hashed and 34 rows carrying an archive capture.
- **The README overstated the dispute finding.** It said `owner_can_dispute` is an absence code in
  every row but two. The column reads `NOT_ADDRESSED` in 60 rows and `PARTIAL` in seven: six
  Mercedes-Benz rows and the Altigreen neEV TEZ. The seven support the finding rather than qualify it,
  and the README now says so and names them. It also now says dispute rather than verify, because a
  Mercedes-Benz owner can obtain the baseline, so "cannot verify" is the wrong word for that row.

## 1.1.0, 29 September 2026

### Added
- `scripts/freeze-sources.py`. Fills in `sha256` for every PDF source and `archive_url` for every row,
  and on a re-run verifies rather than overwrites: a hash that no longer matches is reported as a
  document changed under us, not silently rewritten. `--check` mode writes nothing and is meant for
  CI. Needs ordinary outbound internet; it will not run inside a sandbox with an egress allowlist.
- An `archive_url` column in `sources.csv`. For a web page a byte hash is noise, because the page
  changes on every render. A dated Internet Archive capture is the right artefact, and for two of the
  BYD documents it is now the only first-party copy that serves.
- A `sha256` column in `sources.csv`. A dataset whose claim is that every value can be checked at the
  source has an exposure that was never written down: the source can stop serving. Recording the hash
  of the document we read lets anyone who obtains a copy by any route prove it is the same document.
  Populated for the four BYD rows. The remaining 20 PDF rows are a one-command backfill with
  `freeze-sources.py`, run from a machine with normal internet. The other 30 rows are web pages and
  take `archive_url` instead of a hash.

### Changed
- The three BYD warranty policy source rows now carry BYD's own asset host as the document URL rather
  than a dealer URL or the site homepage.

### Notes
- On 29 September 2026, checked from outside India, `bydautoindia.com` served only a JavaScript shell
  and four of five BYD India asset URLs that search engines had indexed returned HTTP 403, including
  all three warranty policies tested. One brochure still served, so this is recorded as an
  availability observation with a date and a method, not as a withdrawal. Every BYD value was re-read
  at the document itself the same day and none changed.

54 sources, 67 models, 63 verbatim clauses.

Six makers that the 22 September audit had read were missing from 1.0.0 entirely: Ultraviolette,
PMV Electric, Audi India, Euler Motors, Strom Motors and Hero Electric. Seven rows added, one per
model, each read at the maker's own site on 28 September 2026. Strom Motors and Hero Electric serve
no warranty document; both were confirmed by a browser pass after automated retrieval failed.

The published counts were also wrong. 1.0.0 claimed 25 makers; the maker column held 24. The figures
are counted from `data/` by script and by a second independent pass, and as released 1.1.0 is
**67 models, 31 makers, 54 source documents and 63 verbatim clauses**. The counts moved twice more
after this entry was first drafted, as BYD, Tesla India and the model-level recheck landed, which is
the reason the figure is now generated rather than typed.

**BYD India's warranty policy was read in full on 29 September** and produced the sharpest finding in
the dataset: an 8 year / 160,000 km traction battery warranty that excludes "the normal attenuation of
battery capacity" in terms, with no state of health floor stated anywhere in the document. Six clauses
added. A new result code, `EXCLUDED`, was added for it: stronger than NOT_STATED and the opposite of a
gap, because the document addresses the thing and puts it outside cover.

A model-level check against the audit then found more. **Tesla India** was absent altogether. Five
**Mercedes-Benz** models were absent whose terms differ from the row that did ship, including the
longest warranty in the dataset at 10 years and unlimited km. The pattern was the same each time: a
maker's base tier was kept and its other tiers dropped.

**Hero Electric** was first recorded as serving no document. That was wrong. Its own Startup Guide
for lithium-ion variants exists and carries a full warranty policy; the canonical URL printed inside
the document, `heroelectric.in/PDF/li.pdf`, no longer resolves, so it was read from a mirrored copy of
the manufacturer's booklet and that is stated in `access_notes`. Three rows added. The policy
conditions cover on daily depth of discharge and states replacement thresholds in amp-hours at a C5
discharge rate, which is flagged against the "one model discloses a method" claim rather than
silently folded into it.

Not fixed: **BYD Seal, eMAX 7 and Sealion 7**, read by the audit at the Atto 3's terms but with no
citable per-model source, because `bydautoindia.com` does not serve to European networks. **Strom Motors** is closed: its site was retrieved
successfully from a third network on 29 September and publishes no warranty document of any kind, so
the absence rests on a successful read rather than a failed one. No `none_located` rows remain; every
row cites a document that was retrieved.

Schema: two document types added, `official_faq_page` and `none_located`, so that a maker who
publishes nothing can be recorded rather than dropped. No existing row changed. `clauses.csv`
unchanged.

`scripts/validate.py`: the sourcing rule it claimed to enforce was dead code, testing a condition the
check above it already caught. It now enforces what the rule means: a stated value may not cite a
`none_located` source. Verified by planting a defect and watching it fail.

Still missing, and carried forward openly: **Tata XPRES-T EV**. The 1.0.0 changelog said it was
recorded as NOT_FOUND. It was not; no row exists. Its owner manual's warranty chapter begins past
page 145 and has not been reached. It is the same class of omission 1.1.0 exists to fix and it is not
fixed here.

## 1.0.0, 23 September 2026

First publication. 41 source documents, 47 models, 46 verbatim clauses.

Read at the primary document over 22 September 2026. Three documents were
disallowed to automated retrieval by robots.txt and were read in a browser
instead: Tata's owner manuals, Kia's EV6 owner manual and Citroen's warranty
booklet. That is recorded per source in `access_notes`.

Known gaps at first publication, each recorded as NOT_FOUND with the reason:

- Tata Nexon.ev 30, Tiago.ev 19.2 and Punch.ev 35. The smaller packs. Terms
  appear on no page found.
- Tata XPRES-T EV. The owner manual's warranty chapter begins past page 145 and
  was not reached.
- Mahindra XUV400 and XUV 3XO EV. No warranty guide is published for either.
  The XUV400 manual exists as HTML behind a JavaScript portal with no citable URL.
- Volvo India. Publishes no battery warranty term for India, though Volvo
  publishes one in other markets.
