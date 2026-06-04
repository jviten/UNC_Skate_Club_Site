# UNC Skate Club site — visual-language spec, pass 2

*`frontend-designer`, 2026-05-19. Revisions to pass-1 only.*

## 1. Position: yes, with two caveats

The frame is right — earns the DIY-postering ethos and a model wouldn't propose it. Caveats:

1. **Real scanned torn paper only.** `clip-path` zigzags and SVG-generated edges are Pinterest tells. If we can't scan cardstock at 600dpi, kill it and revert to pass-1 dividers.
2. **Degrade, don't compress, on mobile.** Four edges in 360px = gimmick.

## 2. Frame architecture (back to front)

1. **Wall** = `<body>`, ink black `#111`. Content sits ON the paper; paper is pinned to the wall. The 12–24px of black past each edge is the point.
2. **Paper** = `<main>`, cream `#f0ebe1`, four edges masked by scanned-paper PNGs (one per edge, tileable along long axis). ~250kb total.
3. **Tape**: four corner PNGs, asymmetric. Scotch-yellow at top-left + bottom-right; white masking at top-right + bottom-left. Rotations `-7°`, `+4°`, `-3°`, `+9°`, baked in. Overhangs onto the wall. Matching tape all-around = AI tell.

**Griptape revised:** no longer a section background — fights the paper. Scoped to spots-page hero as a separate scrap of grip taped onto cream with black duct tape. Collaged element, not wallpaper.

**Mobile.** Under 600px: top + bottom edges only; paper edge-to-edge horizontally. Two tape pieces. Under 400px tape shrinks. Never auto-rotate.

## 3. Above-the-fold wireframe

Black wall, cream sheet inset 12–24px, two visible tape pieces (yellow top-left, white top-right).

- **Nav strip**, top of sheet: `meetings · spots · about · @uncskate.club`, Special Elite ~14px.
- **Banner**: `SKATE CLUB AT UNC` in Anton, all caps, ink, ~180px desktop / ~96px mobile, line-height 0.9. Final "C" kisses the right torn edge. **No EST line.**
- **Ram skull** (`assets/logo/UNC SKATE LOGO.png`) pinned top-left of paper, hard-cropped against the torn top edge so horns appear torn through. ~96px / ~64px.
- **Meeting info** under banner, left-aligned: `thursdays · 6:30 · the pit` in Special Elite ~20px; then `any wheels, first board's on us` in Cabin Sketch ~16px.
- **One real photo** from `ig-grid-exec-portraits.png`, rotated `-2°`, 4px ink border, overlapping banner's lower-right by ~40px.

No centered hero, no CTA pair.

## 4. Pass-1 specs that revise

- **Section dividers**: drop 2px ink rules — read as worksheet lines on paper. Replace with an *inner* horizontal tear: ~6px of black wall showing through. Max 2 per page.
- **Typefaces**: drop **Bowlby One SC**. Anton is the sole display face. Stack: Anton / Cabin Sketch / Special Elite / VT323 (video only).
- **Paper**: `--paper: #f0ebe1` locked. Bone fallback only.
- **Video**: YouTube `<iframe>` sits on a magenta torn-paper scrap (`#ff2bd6`) duct-taped onto cream. 4px ink border, no radius, lazy-load.

## 5. Open questions / risks

- **Scanned-paper production**: confirm we can scan real torn cardstock before locking. AI-generated edges fail.
- **Frame fatigue by visit 3**: vary per-page PNG variants so it isn't identical site-wide.
- **Hierarchy**: 180px Anton may swallow 20px Special Elite — bump meeting info to 24px if needed.
- **Inner padding**: 32px minimum between torn edge and text.
- **Skate-stylist**: will push for more tape/scraps. Hold the line — frame + one collaged scrap is the ceiling.
