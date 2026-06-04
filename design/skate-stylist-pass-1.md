# UNC Skate Club — Visual Language Spec (skate-stylist pass)

*Pass 1 from `skate-stylist` agent, 2026-05-19.*

## 1. Palette

```css
:root {
  /* resting state */
  --carolina:   #7BAFD4;  /* the logo blue, not the saturated athletic one */
  --carolina-deep: #4B9CD3; /* for outline/strokes against cream */
  --paper:      #f0ebe1;  /* PROVISIONAL — see note */
  --ink:        #14171a;  /* near-black, slight warmth, never pure #000 */

  /* contextual accents — never on the same page */
  --magenta:    #E5197F;  /* video / Women in Skate (pluto-premiere-flyer.png hue) */
  --purple:     #6E3AA8;  /* event flyers (skate x croquis hue from ig-grid-recent.png) */
}
```

**Skater's-eye gut check.** Carolina blue: `#7BAFD4` is right — it matches the logo and the OEC capsule in `skate-spot-oec-griptape.png`. Resist any nudge toward the brighter athletic `#4B9CD3` as a fill color — keep that for strokes. **Cream: provisionally fine, but I'm watching it.** Against full-bleed griptape it'll read warm-vintage / Polar-zine in a good way; but on long body-copy pages with photos it can drift toward "wedding invite." If that happens, swap to bone `#e6e1d3` or concrete `#d6d4cf`. Flagging now.

## 2. Type — four faces, by job

- **Headlines (graphic):** **Bagnard** or **Druk Wide** (Druk if you'll pay). Free fallback: **Anton** — narrow, brutal, all-caps. This is the SKATE X CROQUIS / OEC slab voice. Not "modern," not friendly.
- **Pixel / video moments:** **VT323** (Google Fonts). Cheap, real, looks like a 411VM lower-third. Used only inside Pluto / video sections. Don't sprinkle it elsewhere.
- **Hand-drawn / scratchy:** **Permanent Marker** (Google) as a safe baseline, **Caveat Brush** as alternate. The logo wordmark in `UNC SKATE LOGO.png` already sets this tone — the body face should feel like the same hand wrote a flyer. Used for pull-quotes, captions, "all skill levels welcome"-type notes.
- **Body:** **Space Mono** for short blocks and meta (dates, addresses, captions), **Newsreader** for any longer reading (about page). Newsreader has just enough warmth to live on cream without going corporate. **No Inter. No Poppins.** If body text feels too "site-y," fall back further to **VCR OSD Mono** for short-form pages.

Graffiti bubble (OEC flyer style): **not a system font.** Treat it as art — bake it into image assets only, like the club already does. Don't try to set HTML headlines in bubble script.

## 3. Layout idioms

- **Griptape texture is the floor, not the wallpaper.** Use it as a full-bleed band behind hero blocks and section breaks — see `skate-spot-oec-griptape.png`. Carolina-blue capsule shapes float on it the way the OEC bubble does. Don't tile it behind every page.
- **Ram skull placement.** Direct application, three sizes: large (hero watermark, low opacity over photos like the exec-portraits grid in `ig-grid-exec-portraits.png`), medium (section bookends, full color), tiny (favicon, list bullets, end-of-article mark — same role as a magazine's section-end dingbat).
- **Section dividers = torn paper.** Pull from `women-in-skate-flyer.png` — the white torn-paper stamp on magenta. On the site: cream torn strip over the griptape band when sections change. Hard cut, no fade.
- **Photo framing.** Three treatments only:
  1. Polaroid-tape look for portraits (`ig-grid-exec-portraits.png` does this).
  2. Full-bleed B&W with magenta hand-drawn caption for any Women-in-Skate / video lead-in.
  3. Untouched color on cream paper, slight inset shadow only — never a soft drop shadow. Photos should look pasted, not floated.
- **Posters as content.** A "flyers wall" module on the home page — actual past flyers, pinned at slight rotations on cream. Postering culture, like the `women-in-skate-flyer.png` IG post next to "No Kings."
- **Buttons / links.** Square corners. 2px ink outline on cream. Hover = inverts to ink fill, cream text. Click = instant. No transitions over 100ms anywhere.

## 4. Landing page above-the-fold (textual wireframe)

```
[top bar — ink on cream]
  UNC SKATE CLUB wordmark (image, the hand-drawn logo lockup, left)
  Nav right, Space Mono caps: SPOTS · MEETINGS · ABOUT · IG
  thin ink hairline under

[hero band — full-bleed griptape, ~70vh]
  Ram skull, large, left third, slightly cropped off the left edge
  Stacked Anton headline, cream, right side:
    "THURSDAYS"
    "6:30 PM"
    "@ THE PIT"
  Under headline, Permanent Marker, magenta-OR-purple-pick-one, smaller:
    "any board. any wheels. first time on one is fine."
  Bottom-right corner, Space Mono mono caps, cream:
    "CHAPEL HILL / CARRBORO — EST. [year]"

[torn-paper cream strip, ~40px, hard edge]

[second block — cream paper]
  Left half: latest photo from photographer, polaroid-tape treatment
  Right half: three flyer thumbnails from past events, rotated slightly,
    pinned look. Caption under each in Space Mono.
  Single ink-outline button bottom: "MORE ON IG →"
```

Resting state = blue + cream + ink. The one accent line ("any board. any wheels…") is the only color event above the fold, and it's anchored — magenta if the hero photo is a Women-in-Skate-tied moment, purple if it's an event-flyer week, otherwise *drop the accent entirely* and let that line sit in ink.

## 5. Open questions

- **Cream vs. bone vs. concrete** — locking after the first real prototype, per the cohesion memo. My bet: cream survives if photos do most of the talking; switch to bone if body copy starts to dominate.
- **Founding year** for the "EST." line — need a number.
- **Anton vs. paid Druk** — Anton is good enough; only worth Druk's price if a print run is coming.
- **Rollerblader photo** — for the inclusivity-by-photography move to land, we need at least one strong rollerblade shot in the photographer's library. If it doesn't exist, the about-page line carries it alone.
- **Pluto video embed** — is the full video hosted anywhere we can link, or is it IG-only? Affects whether the video section earns the magenta + VT323 treatment or stays a teaser.
