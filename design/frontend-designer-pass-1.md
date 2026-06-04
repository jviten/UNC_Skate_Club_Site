# UNC Skate Club site — visual-language spec (anti-AI angle)

*Pass 1 from `frontend-designer` agent, 2026-05-19.*

## 1. Palette (CSS custom properties)

```
--carolina:   #4B9CD3;   /* logo skull body — restrained, NOT saturated */
--carolina-ink: #1d3a5f; /* the dark outline around the ram skull */
--paper:      #ebe4d2;   /* see note */
--ink:        #111111;   /* near-black, not pure #000 */
--magenta:    #ff2bd6;   /* Pluto title / Women in Skate stamp ONLY */
--purple:     #6b3fb5;   /* Skate X Croquis event-flyer contexts ONLY */
```

**Cream pushback.** `#f0ebe1` reads beach-wedding-stationery next to Carolina blue — too warm, too soft, fights the ink-heavy zine flyers. Proposing **bone `#ebe4d2`** as the working paper tone: still warm enough to honor the logo horns, but with enough chroma drop to hold its own as a page background. Flag for sign-off before committing. If bone still reads vintage in prototype, fall back to concrete gray `#d4d4d2`. Do not let it drift to pure white — pure white is the AI tell.

**Cohesion enforced in code:** `--accent` is set per-page (a body class like `.context-video` or `.context-event`) — never both. Resting state pages omit the accent variable entirely.

## 2. Typefaces (all Google Fonts / SIL-OFL)

- **VT323** (Google Fonts) — pixel/arcade voice for any video moment. Matches the Pluto premiere title exactly. Use sparingly; reserved.
- **Bowlby One SC** (Google Fonts) — condensed-ish bold display sans for headlines. Druk is paywalled; Bowlby is the closest open-source replacement with real weight. Reserve **Anton** as the lighter alt for body-headline sizes.
- **Cabin Sketch** (Google Fonts) — hand-drawn structural face for sub-headlines and section labels. Echoes the "UNC SKATE CLUB" hand-lettering around the logo without trying to forge it.
- **Special Elite** (Google Fonts) — typewriter body face for long copy. Reads zine/photocopied without the legibility cost of a true marker font. Pair with `font-feature-settings` off, no ligatures, slightly looser line-height.

Hard no on: Inter, Poppins, Roboto, Montserrat, Work Sans, anything `system-ui`. If a `font-family` stack ever falls back to a generic sans, the design has failed.

## 3. Layout idioms

- **Griptape texture** (`skate-spot-oec-griptape.png`-style): full-bleed background on **one** marquee section per page — the spot-map hero on `/spots/`, the meetings block on `/`, the event block on `/about`. Not site-wide; it loses its weight if it's everywhere. Use a tileable PNG, `background-attachment: scroll` (not fixed — fixed is an AI tell on mobile), no overlay.
- **Ram skull** as a structural element, not a logo lockup. Three uses, repeated: (a) header-left at ~48px, hard-cropped against the top edge; (b) watermark behind photos at ~30% opacity, bottom-right, deliberately overlapping the photo's corner; (c) full-size centerpiece on the landing's first block. Never enlarge it past 480px — it's an illustration, not a hero graphic.
- **Section dividers**: hard 2px `--ink` rules with text labels sitting on top of them (label in `--paper`, knocked out of the rule). No torn-paper SVGs — those are a Pinterest tell when done in CSS. Real torn edges only inside the `women-in-skate-flyer.png`-style poster blocks, and only as raster PNG masks of actual scanned torn paper.
- **Photos** are pasted, not framed. Slight rotation (`-2deg` / `+1.5deg`, never the same), hard 4px `--ink` border, no shadow, no radius. Overlap photos onto headlines and onto each other on purpose. The grid betrays the hand: photos break the column.

## 4. Above-the-fold wireframe — landing

Bone background.

- **Top edge, no header bar.** Ram skull pinned to top-left, touching both the top and left viewport edges (no margin). To its right, on the same baseline as the skull's lower jaw, a single hand-set nav row in Cabin Sketch: `meetings · spots · about · @uncskate.club`. No logotype next to the mark — the mark *is* the logotype.
- **Asymmetric headline block, anchored bottom-left of the fold.** Two lines, Bowlby One SC, all caps, ink, set ~140px on mobile-down/240px desktop, line-height 0.85, kerned tight: `UNC / SKATE CLUB`. Forty percent of the second line breaks the safe-area margin and bleeds off the right edge. No subhead under it.
- **One real photo**, top-right quadrant, rotated `-2deg`, hard ink border, overlapping the headline's "B" by ~30px. From the exec portraits set. No caption.
- **Single line of running copy**, Special Elite, ink on bone, ~18px, sitting in the gutter under the headline: `thursdays · 6:30 · the pit · any wheels, first board's on us`. That is the entire CTA. No button. The next section's griptape edge is already visible at the bottom of the fold, ~80px showing, signaling there's more.

No centered hero. No primary/secondary CTA pair. No illustration-right-headline-left. No "Welcome to" anything.

## 5. Open questions

- **Paper tone**: bone `#ebe4d2` vs. user-original cream `#f0ebe1` vs. concrete `#d4d4d2`. Need a side-by-side prototype to lock.
- **Carolina blue saturation**: official UNC `#4B9CD3` matches the logo, but on bone at large fills it can push toward "corporate athletics." Acceptable to desaturate ~8% (`#5e9ec7`) for large background fills while keeping `#4B9CD3` for the mark and small UI?
- **Photo border weight at small sizes** — 4px reads heavy on thumbnails; drop to 2px under 200px width, or keep flat 4px everywhere for consistency?
- **Skull-as-favicon**: crop to head only or full mark? Full mark goes muddy at 32px; head-only loses the horns.
- **Griptape source**: rip a high-res tile from `skate-spot-oec-griptape.png`, or shoot a real piece of grip and scan it? Real scan wins on authenticity but adds a production step.

Likely disagreement with skate-stylist: I expect them to push for warmer paper (closer to the original cream) because it reads more zine. I'm pushing cooler (bone/concrete) because cream + Carolina blue is the exact combo that lands as "preppy Carolina alumni newsletter" if it goes one degree wrong. Let the user pick.
