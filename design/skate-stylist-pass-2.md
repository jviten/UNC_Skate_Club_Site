# UNC Skate Club — Visual Language Spec, Pass 2 (skate-stylist)

*Revises pass-1 (`design/skate-stylist-pass-1.md`) against the locked decisions and the "site-as-taped-flyer" frame. 2026-05-19.*

## 1. Position on the torn-paper-frame concept

**It lands — but only if we commit to one specific real-world reference and execute it tight. Otherwise it cosplays Pinterest.**

The honest version: a skater puts a flyer up on a telephone pole, a stairwell wall, the back of a stop sign, a coffee-shop corkboard. The Women in Skate IG post (`assets/flyers/women-in-skate-flyer.png` pasted next to a "No Kings" flyer on a campus pole) is exactly that. The "site as a taped flyer on a computer screen" move is a literal digital extension of that — which means it's *earned*, not decorative. It's the strongest move on the table.

Where it goes wrong: if the torn edges look CSS-generated (uniform sine-wave teeth), if the tape is four identical 45-degree corner pieces, if the texture is a stock "ripped paper" asset from Envato. Then it's a wedding-invite scrapbook page, not a flyer. The defense is **asymmetry and real scans.**

Verdict on `frontend-designer`'s likely pushback (gimmick / Pinterest-at-scale): they're right *as a default failure mode*. They're wrong if we execute it as one specific flyer-on-pole, not "scrapbook chrome." The disagreement is about ambition, not direction — I'd hold the line and ask them to police the execution details rather than kill the concept.

## 2. Concrete proposal

**The page IS the flyer. Not the wall.** The cream paper is the page surface — content sits ON it. There's no second layer behind the torn edge. A flyer on a pole isn't see-through; it's an opaque piece of paper with the world ending at its torn edge. The browser viewport background outside the frame is **ink black** — the dark of an unlit dorm room, the back of the pole, the screen bezel. Not a textured wall image. That would re-introduce the gimmick.

**Paper texture:** one real-scanned cream sheet, photocopier-aged, used as a tiling background on the page. Not synthesized noise. Subtle — the fiber and toner-fleck should be visible at 100% zoom but not dominate. Same source asset re-used everywhere to keep cohesion.

**Torn edges:** four scanned torn-paper PNG strips, each one *different*, with transparent backgrounds. Top edge slightly diagonal. Bottom edge has one big tear and one clean section. Left and right are subtler — more like rough-cut than torn. Asymmetry is the whole point. The torn strip should bleed off ~12–20px into the black so it reads as paper-over-void.

**Tape — white masking tape.** Two pieces. One in the top-left corner at maybe 12° rotation, one in the bottom-right at ~−8°. Not four corners — that's scrapbook. Skaters putting up a flyer use two pieces of tape unless it's windy. The tape is off-white masking (`#ece6d2` ish), slightly translucent so you can see paper through it, with frayed fiber ends — not crisp rectangles. Avoid: scotch yellow (looks craft-store), blue painter's (too "fresh from Home Depot"), black duct (too aggressive). Masking is what's on a skater's workbench for griptape jobs anyway — there's a real-world tie.

**Griptape gets demoted, not removed.** Pass-1 had it as the full-bleed hero band. With the whole page now being a paper flyer, a griptape hero band would mean *a flyer with a griptape photo printed on it* — which is fine and more correct than griptape being the page's substrate. So: griptape stays as a printed-on-paper band behind the headline, contained inside the flyer's edges. The Carolina-blue OEC capsule still floats on it.

## 3. Above-the-fold wireframe

```
[viewport background: ink black #14171a, no texture]

[the flyer — cream paper, fills ~95% of viewport, torn edges on all 4 sides,
 bleeds off the edges so the page feels like it continues past the screen]

  [white masking tape, top-left corner, ~12° rotation, ~120px wide]

  [top banner — ink on cream, full width of the flyer interior]
    UNC SKATE LOGO.png on the left, ~60px tall
    Right side, Anton, ink, all-caps, stacked tight:
      "SKATE CLUB"
      "AT UNC"
    line-height crushed to ~0.9
    nav sits as a Space Mono caps row directly under the banner:
      SPOTS · MEETINGS · ABOUT · IG
    ink hairline under

  [meeting info block — directly below banner, cream paper]
    Permanent Marker, ink, ~28px:
      "thursdays · 6:30 · the pit"
    Permanent Marker, ink, ~16px:
      "any board. any wheels. first time on one is fine."
    (Resting state = ink only. Magenta/purple only if hero photo
     is anchored to Women-in-Skate or event-flyer context.)

  [hero band — griptape image, contained within the flyer,
   ~50vh, bleeds left/right to the torn edges but not top/bottom]
    Ram skull from UNC SKATE LOGO.png, large, left third, cropped slightly
    Right side: a single Carolina-blue capsule floating on the griptape,
    holding a brief hand-drawn line like "spring 26 / chapel hill"
    in cream Permanent Marker (the OEC capsule move applied as hero)

  [thin cream gap, ~24px, just paper]

  [second block — flyers wall / latest photo]
    (carries over from pass-1 §3)

  [white masking tape, bottom-right, ~-8° rotation]
```

No "EST." line. Banner answers "who"; meeting info answers "when / where / does this include me." That's the only job above the fold.

## 4. Pass-1 specs that revise

**Survives unchanged:**
- Palette (cream confirmed, accents-by-context rule, no neon-on-black)
- Type stack except headline: Anton replaces Bagnard/Druk; Permanent Marker, VT323, Space Mono, Newsreader all stand
- "Flyers wall" module — the whole site being a flyer makes this module a *flyer-on-a-flyer*, which is consistent (a wall of show posters tacked to a bigger flyer), not redundant
- Photo treatments (polaroid-tape, full-bleed B&W with magenta caption, untouched-on-cream)
- Buttons: square corners, 2px ink outline, hover inverts, ≤100ms transitions
- Ram skull placement at three sizes

**Revises:**
- **Hero griptape band** was full-bleed of the viewport, now contained inside the flyer's torn edges. Printed band on paper, not the page's floor.
- **Torn-paper section dividers** — biggest change. With the whole viewport already bounded by torn paper, adding more torn strips inside dilutes the move. **Drop the inter-section torn dividers. Use a single thin ink rule (1px) or a tall cream gap (~64px).** Strong edge outside, calm rhythm inside.
- **EST. [year] line** deleted, per locked decision.
- **Headline**: now banner stacks "SKATE CLUB / AT UNC" in Anton; meeting info moves to a Permanent Marker line directly below. Slab is for the poster's title; hand type is for the details written on the flyer — matches how real skate flyers are laid out (see Movie Nite zine flyer in `ig-grid-ram-skull-tees.png`).
- **Pluto video section**: YouTube `<iframe>` swapped in. VT323 + magenta + film grain treatment still applies, but the video is a black rectangle on cream paper with a hand-drawn-marker frame around it. Don't let the iframe sit naked — looks like a CMS dropped it in.

## 5. Open questions / risks

- **Real paper scan asset.** Biggest execution risk. If the texture is synthesized or stock, the concept collapses. Action: shoot one. Real cream sheet, photocopied a few times, torn by hand on four edges, scanned flat at 600dpi. An exec with a flatbed scanner, half hour.
- **Tape asset same constraint.** Real masking tape stuck to white surface, scanned with fiber ends, two pieces. Not a Pixabay PNG.
- **Mobile.** Torn-paper viewport frame on a 390px phone with a 95vw paper inside risks reading as a doily. Drop side torns on mobile, keep top + bottom only, drop one of the two tape pieces. Concept reads with less.
- **Performance.** Four torn-edge PNGs + paper-tile + two tape PNGs + griptape image + ram skull = real decorative weight. Lazy-load below-the-fold imagery, serve edges as optimized PNGs.
- **"Computer screen" part of the metaphor.** I'm reading the ink-black viewport background as the screen bezel / off-screen darkness. If the user wants a literal monitor-frame visible (window controls, bezel image), that's a different direction I'd push back on — it gimmicks fast.
- **Authenticity check.** Symmetry betrays this. Two pieces of tape at +15° both top corners both same size = scrapbook. Asymmetric tear, varied rotation, off-center tape placement — that's where the move lives or dies.
