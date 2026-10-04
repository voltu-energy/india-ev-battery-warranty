# Changelog

## 1.2.0, 4 October 2026

A minor version because of what is in it, not because of how long it took. Sources 56 to 89.
Clauses 71 to 198. Charging rules 0 to 133. Models 67 to 74. The charging-rules layer is new.

The manuals arrived. The day began with two owner's manuals held locally and the honest admission
that everything else had been read over a fetch tool. 54 maker documents were then downloaded, so
this is the first release where the charging layer rests on files we hold and hash.

### Three makers, one number

Tata, Mahindra and MG independently tell owners to do an AC charge to 100 percent after every
four DC charges. Three companies, no shared platform, the same number. Tata and MG even use the
same phrase, "opportunity charging".

    Tata      after a maximum of four DC / opportunity charging cycles, you must use AC charging
              to 100% State of Charge for the optimum performance of the high voltage battery pack
    Mahindra  Allow AC charging up to 100% State of Charging ("SOC") once in every 4 fast
              charge (DC) cycles
    MG        Slow AC charging till 100% SoC is recommended at least once a 15 Days or after
              every 4 fast DC/opportunity charging cycles whichever is earlier, for SoC
              calibration & cell balancing

Only MG names the mechanism. Tata offers a purpose, "for the optimum performance of the high
voltage battery pack", and Mahindra offers nothing. MG's sentence is the most useful in this
release:

    Cell balancing and equalization, as well as state of charge (SoC) calibration, occur during
    charging, particularly when the SoC is above 90%.

So the full charge is for the gauge and the cell balance. That is a different thing from cell
chemistry ageing, which is what the research on dwell time at high charge measures, and it is why
the two can both be true. The research is about how long a
pack sits at a high state of charge. The makers are asking for a brief visit to the top of the
range so the BMS can re-reference itself. Both can be true, and the tool should now say so
instead of flagging a conflict.

### Mahindra's care instructions are warranty conditions

The page 23 list is not advice. Page 22 closes the null-and-void list with:

    Vehicle missing any of Battery service requirements as specified or not adhering to the
    conditions set out above, or not adhering to conditions mentioned in the Vehicle Manual,
    will forfeit warranty on Battery.

So the 4-DC rule, the 5 percent floor, the two-month idle top-up and the six-month idle ceiling
all carry warranty weight. Mahindra also voids the battery warranty if a vehicle stopped by
over-discharge is not plugged in within 24 hours.

### Kia says 80, MG says 100

    Kia   If the HV battery is only charged to 80%, and you minimise the number of DC fast
          charging, you can keep the HV battery performance in optimal condition
    MG    It is recommended to charge the vehicle to 100%, whenever vehicle is being charged

Both sold in India, both in the owner's manual. Mercedes sits with Kia and is blunter, listing
"frequently fully charging (charge level 100%) the high-voltage battery, especially when this
process is not directly followed by a journey" as a cause of accelerated ageing.

### Scoping that only reading the files could produce

The Kia 80 percent sentence is in the Carens Clavis EV and EV9 manuals and is absent from the
Syros EV manual, so the rule is scoped to two models. The Mahindra XEV 9S guide says "once after
4 fast charge (DC) cycles" where the other three say "once in every 4". Both differences would
have been invisible to anything that read one document per maker.

### MG storage advice has a warranty consequence

    Failure to maintain the battery as recommended could lead to vehicle issues caused by
    over-discharge, which may not be covered under warranty.

### BYD closes the loop on why makers ask for a full charge

BYD was the gap worth closing, because the ATTO 3 is LFP and LFP guidance usually runs opposite
to the 80 percent advice. It does, and it says why, printed p159:

    To keep the power battery in optimal conditions, it should be fully charged and discharged
    regularly (once every 6 months or 72,000 km, whichever comes first) for self-calibration. A
    BYD authorized dealer or service provider may also be contacted to carry out capacity testing
    and calibration.

And p82:

    Battery balancing is enabled before charging is completed to improve service life. In such
    case, charging time may be prolonged.

Two makers state the mechanism. MG's Windsor EV manual names SoC calibration and cell balancing
and puts them above 90 percent. BYD's ATTO 3 manual names self-calibration and battery balancing,
asks for a full discharge as well as a full charge, and puts it on a six month or 72,000 km
interval.

Five more ask for the same periodic full charge without naming a mechanism. Tata gives a purpose
and not a reason, "for the optimum performance of the high voltage battery pack". Mahindra gives
the number and nothing else. Toyota and Maruti print the same sentence as each other about an
"automatic maintenance function" that works at full charge, without saying what the function
does. Hyundai asks for a full charge when the pack falls to 20 percent, monthly or more, with no
reason given.

So the mechanism is a reading of the two manuals that name it, extended to the five that do not.
That is worth stating as a reading rather than as something seven makers said.

The intervals disagree wildly, from weekly to six-monthly, but the underlying request is the
same: let the pack reach an extreme occasionally so the management system can re-reference
itself. That is a gauge and cell-balance problem, not a chemistry one, which is why it sits
alongside rather than against the ageing research on dwell time at high charge. The tool should
say this plainly instead of flagging a conflict between the maker and the science.

BYD is also the only maker here that offers capacity testing to the owner, and the only one
telling owners to arrive at a DC charger with a low state of charge and a warm pack because that
is what makes it fast.

### BYD classes ordinary Indian driving as harsh use

Printed p159, defining the conditions that shorten the maintenance interval:

    Driving in congested urban areas at temperatures above 32 degrees C for more than 50% of
    total driving time.

With "Use as taxi" on the same list. Congested city driving above 32 degrees for more than half
the time is simply what most Indian cities are. It sits beside VinFast's instruction not to store
the VF 7 above 35 degrees. Neither is a warranty exclusion: BYD's is a trigger that shortens the
maintenance interval and VinFast's is a storage instruction. Both are written against conditions
much of India exceeds.

A correction found while checking this entry. An earlier draft also cited a TVS iQube exclusion
for exposure above 25 degrees. No such clause exists in this dataset. It came from an agent's
summary and was repeated here without being read in the document, which is the exact failure this
project has a rule against. The TVS temperature clause we hold is the Orbiter's, above 60 degrees,
and it is an instruction rather than an exclusion.

### One manual for four cars

BYD India's owner's manual page builds its links from a serviceData array with exactly two
entries, ATTO 3 2022 and ATTO 3 2023, both pointing at the same file. BYD sells the ATTO 3,
eMAX 7, SEAL and SEALION 7 here and publishes a manual for the oldest only.

### The terms move under the owner, and one maker says so outright

Three documents read in this batch point the same way.

Ultraviolette, F77 owner's manual, printed p97, closing the Warranty Policy:

    Ultraviolette Automotive Private Limited reserves the right to change and withdraw any clause
    of Warranty policy without prior information or notification.

Ola, S1 Air owner's manual, printed p3:

    Refer to the latest version of Owner's manual in the Ola Electric app for information on
    latest features and technologies, as they are subject to change.

And River, where it already happened: the mandatory full-charge interval went from 90 days to 60
between the September and October 2025 manuals, with the warranty consequence attached
throughout.

So one maker reserves the right to rewrite the terms silently, one tells the owner the printed
manual is not the authoritative copy, and one has already changed a warranty-voiding obligation
without announcement. A dataset that records what makers publish, on the date it was read, with
a hash, is the only way any of this stays checkable. That is now the clearest argument for the
way this repository is built.

### Ultraviolette binds the whole manual into the warranty

    Ultraviolette warrants that motorcycles are free from defects in material and workmanship
    during the warranty coverage period, provided that the motorcycles are stored, used and
    maintained in accordance with the USER MANUAL.

That pulls the charging and storage pages into the warranty, the same move Mahindra makes on
page 22 of its warranty guide. Ultraviolette then says it again in the battery section: failure
to follow the charging guidelines "can void the warranty".

The F77 battery, motor and controller are covered for 5 years or 100,000 km. The X-47 manual
adds an optional UV Care Max plan at 8 years or 800,000 km, the highest distance figure anywhere
in this dataset. Neither states a retention percentage.

Ultraviolette is also the only maker here that names a daily charge limit and gives a reason
that has nothing to do with ageing: it recommends 90 percent so that regenerative braking keeps
working.

### Ola's manual does have charging rules, and the earlier sweep was wrong

An earlier pass concluded the Ola owner's manual had no charging chapter at all. That was read
off an S1 Pro manual. The S1 Air manual, printed page 3, carries a full set, including:

    Ensure that the battery is charged to 100% at least once in 30 days to maintain battery
    health.

On the same page Ola also says to charge it every week if the scooter is standing, so the manual
gives two different intervals eight lines apart.

This document is a scan with no text layer. It was OCRed, and then every clause recorded from it
was confirmed by reading the rendered page at 300 dpi by eye, because OCR output is not good
enough to quote from. The access note says so.

### Bajaj publishes brochures and nothing else

Five Chetak brochures were read. Not one carries a charging rule, a charging condition, or any
warranty term beyond the headline figures. "5 YEARS EXTENDED WARRANTY*" has one footnote, "T&C
Apply", and the terms appear nowhere in the document. Standard warranty is given as 3 years or
50,000 km with no conditions attached. That is the same asterisk-with-no-footnote pattern Piaggio
uses, now recorded as a held negative rather than silence.

### Vida tells you the date your battery stops working

The VIDA owner's manual, section 11.b, carries something no other maker in this dataset has:

    Battery electric output auto-stopping function | The battery is equipped with a function to
    prevent further use in case of excessive depletion. When eight years have passed post initial
    battery charging (at OEM end) and/or the accumulated charging amount reaches 14000 Ah, the
    traction battery will no longer be usable.

That is not a retention threshold and not a warranty term. It is a programmed end of life, and it
arrives on whichever comes first of a date and a throughput figure. The Vida battery warranty is
three years or 30,000 km, so the stop is five years past the end of cover.

The Ah figure is the part worth sitting with. It is the only usage-based end of life stated by any
maker here, and it is the one an owner could actually track, because accumulated charge is
countable. Vida does not publish the pack's Ah rating in any document we hold, so the owner cannot
convert 14,000 Ah into cycles or kilometres. A number you can only act on with a figure the maker
withholds is the same pattern as a retention threshold measured by a tool you cannot read.

### Vida also tells owners to store at a high state of charge, alone among the makers here

    Please keep your vehicle SOC > 80% when you intend to keep stored for long periods of time
    without using ... Failure to comply with above instructions will likely cause permanent damage
    the battery and void the warranty.

Every other maker in this dataset that names a storage level names a middling one. Mercedes says
30 to 50 percent, Volvo 40 to 60, Tesla 50, Mahindra 30 to 40, MG above 50 then 40 to 60, VinFast
80 then above 30. Vida says above 80 and attaches the warranty to it. An owner who follows the
ageing research and parks a Vida at half charge is departing from a printed warranty condition.

### River shortened a warranty-voiding obligation and did not say so

Four revisions of the River Indie manual are held, which is enough to date a change.

    Gen 1, Oct 2023 to Nov 2024:  charge your vehicle up to 100% once in 90 days
    Gen 2, Dec 2024 to Sep 2025:  charge your vehicle up to 100% once in 90 days
    Gen 3, Oct 2025 onward:       charge your vehicle up to 100% once in 60 days

In all four the sentence ends "Failing to do so may result in voiding your warranty." So the
consequence was always there and the obligation got a third tighter, somewhere between September
and October 2025. A Gen 1 owner going by the manual they were given is now 30 days out of step
with the current rule.

The Gen 3 manual also adds a warranty consequence to the low-charge storage notice. Gen 1 says
storing with insufficient charge may degrade the battery and require replacement. Gen 3 adds "In
such cases, warranty shall not be covered."

River is also the most specific maker in the dataset about the Indian grid: neutral to earth under
3V measured with a multimeter, a voltage protector, and the flat statement that "Any out-of-bound
surges or grid faults may result in irreparable damages to the charger."

### TVS gives two different numbers for the same rule

    Orbiter:  Vehicles should be charged to 30% SOC atleast once in 15 days
    TVS X:    Vehicles should be charged to 50% SOC atleast once in 15 days

Same maker, same sentence, same interval, different floor. The Orbiter manual also carries the
most practical home-wiring guidance of any document here, down to telling the owner to check the
socket with a multimeter and expect 230 plus or minus 5V, and to fit a surge protector.

### Hyundai does not omit a retention percentage, it refuses to publish one

The dataset recorded Hyundai's state of health floor as NOT_STATED, on the strength of a
brochure and a model page. That was a weak absence built on marketing material, and it was
weaker than the facts deserved.

The Kona Electric owner's manual prints HMIL's own India warranty policy on pdf pages 72 to 74.
It gives the high voltage battery term, 96 months or 160,000 km, and then says this:

    If the degree of degradation of the high-voltage battery is within the normal aging level
    according to the use of the vehicle.

    - The criterion for normal aging of high-voltage battery conforms to our internal quality
      standards.

So Hyundai states that a criterion exists, excludes everything on the right side of it, and
places the criterion inside the company. That is not an omission. It is a documented refusal,
and it is categorically different from a maker that simply never addressed the question.
soh_floor_pct for Hyundai moves from NOT_STATED to EXCLUDED, who_measures to maker.

The comparison that makes it worth publishing: Kia states 70 percent. Kia and Hyundai are the
same group. One brand gives the owner a number to hold the company to and the other says its
own quality standards decide.

HMIL also reserves "the right for the final decision in all warranty matters", so the owner has
no stated route to dispute a reading they cannot see in the first place.

Two smaller things fell out of the same pages. Hyundai's charging exclusion, "Use of improper
battery charger, fluids or lubricants", is word for word the clause JSW MG prints for the ZS EV,
Comet EV and Windsor EV, so at least two makers are working from a shared template. And the
warranty policy appears in the Kona manual only: the IONIQ 5 manuals, both editions, and the
Creta Electric manual were searched for the same text and do not carry it. An IONIQ 5 owner
reading their own manual cover to cover never encounters the battery warranty terms.

### The Hyundai Creta manual was not unreadable, it was encoded

1.2.0 first recorded the Creta Electric manual as held but not read, because pdftotext returns
mojibake from it. That was wrong, and the wrong conclusion was ours. Hyundai embeds the fonts
as a subset with a custom encoding. Letters, spaces and punctuation are ASCII shifted down by
29, and the digits are moved out to U+0238 to U+0241 in the order 1 to 9 then 0, which is
exactly why the earlier reading could make out the prose but not a single number.

scripts/decode-hyundai-creta.py decodes it and checks itself: the manual prints a chapter-page
marker on nearly every page, and decoded those run in order from 1-3 to 9-55 across 471 pages.
A wrong digit map does not produce an ordered sequence, so the check is the proof. The script
refuses to emit output if the check fails.

The two figures that could not be read are 10 and 20, and the Creta manual turns out to carry
the strongest Hyundai India wording of the four manuals held:

    Keep the gauge of the high voltage battery from going below than 10 %. Storing the vehicle
    whilst the battery level is low for a long time may damage the battery or reduce the
    battery's capacity, potentially causing the need for a battery replacement.

    Battery performance and life may deteriorate if the DC charger is used constantly. Use of
    DC charging should be minimised in order to help prolong high voltage battery life. Use AC
    charging unless DC charging is necessary.

That last sentence is absent from the IONIQ 5 and Kona manuals. Hyundai also states that
repeated use of V2L shortens pack life, which is the only place in this dataset where a maker
says using the car as a power source costs you battery.

The general point is worth keeping. A document that defeats text extraction is not a document
that cannot be read, and recording it as unreadable would have quietly dropped the most
specific numbers any Hyundai India manual publishes.

### VinFast does publish a manual, and Volvo publishes one per market

The earlier sweep recorded VinFast as publishing no owner documentation at all. That was wrong.
VinFast publishes a full India owner's manual at om.vinfastauto.com with an en_in locale and a
model and year selector. Two things hid it: the search looked at vinfastauto.in only, and the
manual body renders inside shadow DOM, so an ordinary page fetch returns the navigation and the
manual appears empty. It was read in a browser. The warranty-terms note has been corrected.

VinFast tells Indian owners the vehicle "should not be exposed to ambient temperatures exceeding
35°C" during storage, and says not adhering may cause permanent degradation. Most Indian cities
are above 35 degrees for a large part of the year. That sits beside the TVS iQube exclusion for
exposure above 25 degrees as a condition written for somewhere else.

VinFast also shows battery health, labelled SOCE, to the owner in the EV app on the infotainment
screen. Very few makers in this dataset show the owner any health number at all.

Volvo publishes its manual per market as support articles rather than a PDF. The India XC40
Recharge article was read and carries a full set of charging rules, including a recommendation
to set a target below 100 percent for everyday charging and 40 to 60 percent for parking over a
month.

### Schema

A source can now be held and cited by no row, when it corroborates another document word for
word, when it is held as a recorded negative, or when it cannot be read. access_notes has to say
which, and the validator prints them rather than hiding them. Seven documents are in that state.
hyundai-creta-om is one: its subsetted font renders every digit as a private use glyph, so not a
single figure has been taken from it.

### The sweep that found the charging layer was built on the wrong documents

A sweep for charging rules, after the realisation that the first two passes had looked in the
wrong document. Warranty booklets carry warranty clauses. Charging rules live in the owner's
manual, the charger guide and the home installation guide, and those were never read.

### Eight rules that were already in the data and had never been lifted

The charging-rules layer was built by hand and seven clauses sitting in clauses.csv never made
it across, plus one that was only half carried. Three of them belong to makers the
consumer tool was telling owners had no charging rule at all:

- Mahindra BE 6, BE 6 FE, XEV 9e and XEV 9S. A charger exclusion and, separately, an exclusion
  for any electricity surge, dip or fluctuation while charging.
- JSW MG ZS EV, Comet EV and Windsor EV. An improper-charger exclusion.
- Kia, all EV models. A charger exclusion that also reaches installation by an unauthorised
  electrician and damage from voltage fluctuation.
- Citroen eC3, a follow-the-procedure exclusion. Bajaj Chetak, supply above 250V rms and
  earthing faults. Tata Nexon.ev, improper charging as unusual stress.

This was a defect in the tool, not only in the dataset. A Mahindra owner was being shown the
ageing science with the line that their maker states no rule, while Mahindra excludes grid
damage in the warranty booklet we already held.

### Grid quality is now a rule type of its own

Three makers put the condition of the Indian supply on the owner: Mahindra, Kia and Bajaj. The
new grid_quality_excluded rule records that. It is the first rule in this dataset that is about
the house rather than the car.

### Two new sources, one vehicle, two badges

The Toyota Urban Cruiser Ebella and the Maruti Suzuki e VITARA are the same vehicle. Their
owner's manuals carry the same charging rules in the same order, differing only in whether the
pack is called the high voltage battery or the traction battery. Both are recorded, separately,
because an owner reads one or the other and never both.

What they say is the opposite of what every other maker in this dataset says:

    To maintain the high voltage battery performance, fully charge the battery once a week.
    However, if the vehicle is not used for an extended period of time, refrain from storing
    the high voltage battery fully charged to prevent deterioration.

A mandated weekly 100 percent charge, paired with an instruction not to sit at 100 percent.
Both manuals also tell the owner to avoid frequent DC charging and not to park at a full charge
in the sun.

### The warning the owner can actually see

Both manuals print a dashboard message, CHARGE 100% FOR MORE EFFICIENT HV BATTERY USAGE, shown
when the car has been used repeatedly without a full charge. That is worth putting beside the
Tata clause already in this dataset, which counts EV charging pattern warnings between services
and makes two of them a warranty condition, with no way for the owner to read the counter. Same
mechanism, opposite treatment: one maker shows it, the other scores you on it in private.

### Schema

sources.csv url now accepts NOT_PUBLISHED_ONLINE. The Maruti e VITARA owner's manual is handed
to registered owners through the Maruti Suzuki mobile application and appears nowhere on
marutisuzuki.com, so there is no link to record. A row with no URL must carry a sha256, because
the hash is then the only thing identifying the document. Guarded in validate.py.

### VinFast, and the charging-rules layer this release then rebuilt

VinFast added, a new owner-facing charging rules layer, and the published JSON fixed after it was
found disagreeing with itself.

**VinFast was missing entirely.** The company has a plant in Thoothukudi and is selling. Four
models added from brochures: VF 6, VF 7, VF MPV7 and Limo Green, all at 10 years or 2,00,000 km
on the battery and 7 years or 1,60,000 km on the vehicle.

Read them with the caveat attached. The terms come from a footnote on a specification spread, not
from a warranty document, because **no VinFast India warranty booklet or warranty page has been
located**. The retention floor, who measures it and the method are all `NOT_FOUND`. A maker
actively selling with no locatable warranty document is a finding, and it is recorded as one
rather than left as a blank row.

Also recorded: none of the four brochures states a capacity retention threshold. VinFast is the
only maker outside Mercedes-Benz to publish the usable capacity, which is the denominator every
other maker's threshold lacks, and it states no threshold to apply it to.

**New: `data/charging-rules.csv`.** The operational rules makers state about charging, pulled out
of `clauses.csv` into a layer an owner can act on. Fifteen rules, each carrying the maker's
verbatim clause and a `strength` of `warranty_exclusion`, `warranty_condition` or
`maker_instruction`, because the difference between those three is the whole point.

The rules contradict each other between makers, which is why no general charging advice can be
right in India:

- Ampere puts "unauthorized charging profiles and fast charging options" outside cover.
- Altigreen excludes a claim if the battery has not been charged to 100 percent at least once in
  seven days, which is the opposite of the advice every charging article gives.
- Tata instructs an AC charge to 100 percent after at most four DC charges, printed inside the
  list of conditions under which the Lifetime battery warranty applies, next to a condition that
  the vehicle carry no more than two EV charging pattern warnings between service intervals, read
  off telematics the owner cannot see.
- Mercedes requires a recharge within fourteen days of the pack reaching zero.
- Eight makers require an approved charger.

A validator guard enforces that every `clause_verbatim` in the new file is found inside a real
`clauses.csv` row, so the owner-facing wording can never drift from what the maker wrote. It
caught one of the first fifteen on its first run.

**`data/warranty.json` was wrong and is now generated.** At 1.1.3 its arrays held 54 sources and
63 clauses, its own `counts` field claimed 56 and 71, and the CSVs beside it held 56 and 71. A
published artifact that disagreed with itself and with its own source of truth. It is written by
`scripts/build-json.py` now, the validator regenerates and compares it on every run, and it
carries the maker count and the charging rules that were never in it.

**The README's opening line is checked.** It stated 67 models, 31 makers, 56 source documents and
71 verbatim clauses while the files held more of each. Any count in the live part of the README
is now compared against the files, and the release history below is exempt so that "Version 1.0.0
shipped 47 models" stays as written.

**Two Tata clauses gained their page context.** The four-DC instruction and the charging-pattern
warnings condition both sit on page 333 of the Nexon owner's manual, inside the list headed
"Applicability of Lifetime HV Battery Warranty ... exclusively applicable under the following
conditions". That context changes what the clauses are, so it is recorded in the clause text.

**The Tata Nexon owner's manual hash is settled**, read in a browser on 3 October 2026.

## 1.1.3, 1 October 2026

The XPRES-T manual changed a denominator two days ago. Three clause scopes and three lines of prose
in this repository never got the message. Fixed, and the validator now refuses to let it happen again.

### Changed
- **Every "of seven" became "of eight".** The Tata owner manual index carries eight PDFs and all eight
  were read on 29 September. The clause scopes in `data/clauses.csv` and `data/warranty.json` still
  said five of seven, three of seven and six of seven, and `README.md` said it twice in prose. The
  XPRES-T EV carries none of the three clauses, so every numerator is unchanged and every denominator
  was wrong.
  - DC charging cap: **5 of 8** manuals. Absent from Sierra.ev, Tigor.ev and XPRES-T EV.
  - Charging pattern warnings: **3 of 8** manuals.
  - Telematics requirement: **6 of 8** manuals. Absent from Tigor.ev and XPRES-T EV.

### Added
- **A denominator guard in `scripts/validate.py`.** Any clause scope of the form "N of M" must have M
  equal to the number of owner manuals `sources.csv` holds for that maker, and N no larger than it.
  The prose in `README.md` and `CHANGELOG.md` is checked the same way, in words. Add a manual without
  revisiting the scopes and the build fails.

### Notes
- Nothing here changes a warranty value, a source or a count of models, makers or documents. 67
  models, 31 makers, 56 documents, unchanged.
- The defect is worth naming because it is the one this repository exists to rule out: a fraction
  whose numerator was checked against the documents and whose denominator was typed from memory. The
  guard checks the denominator against the files, which is the only place either number should ever
  come from.

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
