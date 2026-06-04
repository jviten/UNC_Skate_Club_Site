# v2 changes — deltas from locked-spec for builder

*Synthesis of frontend-designer pass-3 + skate-stylist pass-3, 2026-05-19. Both agents reviewed v1 + new texture assets + user feedback. Apply these deltas on top of v1 (`index.html` + `styles/global.css`); do not restart from scratch.*

## What changes from v1

### 1. Wall = bulletin board, not ink black

- Replace `--wall: #111` body background with `background-image: url("../assets/textures/Bulletin board, option one. .jpg")`, `background-size: 600px`, `background-repeat: repeat`.
- Keep `--wall` CSS variable defined as `#111` for inner-tear fallback (where the wall shows through inside the paper), but use the bulletin board image on `<body>`.

### 2. Griptape = real photo, not synthesized SVG

- Replace the `griptape.svg` reference on the hero band with `assets/textures/Skateboard grip tape.jpg`.
- Use `background-size: cover` on the hero band. The photo has organic variation that benefits from being scaled to fit, not tiled.
- The synthesized `griptape.svg` can stay in the textures folder but is unused now.

### 3. Torn paper edges = real photographic tear, not hand-drafted SVG

- Replace the four edge SVGs (`edge-top.svg`, `edge-bottom.svg`, `edge-left.svg`, `edge-right.svg`) with a single asset re-used four times: `assets/textures/white-ripped-paper-png.webp`.
- Per side: rotate the source via CSS `transform: rotate()` — top native, bottom `rotate(180deg)`, left `rotate(-90deg)`, right `rotate(90deg)`.
- Per side: apply a different `background-position` (e.g. `0 0`, `-200px 0`, `-400px 0`, `-100px 0`) so the four edges aren't visibly identical — kills the symmetry tell.
- Bump edge dimensions: top/bottom height `60px`, left/right width `50px`. Bleed offsets: `top/bottom: -28px`, `left/right: -24px` so the fringe fully clears the paper rect.
- Reject `brown-ripped-paper-background-with-place-for-your-text-vector.jpg` — it's the stock vector trap.

### 4. Collapse the two rams into one

User feedback: "the big ram is not next to the logo, which is where I want it." Both agents agree the small banner mark + big hero skull read as disconnected. **Kill one of them.**

**Builder: choose skate-stylist's path** — collapse into ONE big mark.

- Remove `.banner__mark` (the small header logo) OR remove `.hero__skull` (the big hero ram), then resize the survivor to ~280–320px.
- The Anton wordmark "SKATE CLUB / AT UNC" sits immediately to the right of the survivor's horns (not in a separate banner above).
- The capsule with "spring 26 / chapel hill" stays on the right side of the griptape band.
- The horns should still hard-crop through the torn top edge (paper looks "torn through" with the horns).
- The nav row (`SPOTS · MEETINGS · ABOUT · IG`) moves to sit on the cream paper *below* the hero band — not above, not inside the griptape area.
- Meeting info (Permanent Marker — `thursdays · 6:30 · the pit` + inclusivity line) sits on the cream paper below the nav row.

Net layout from top:

```
[wall: bulletin board]
[paper: cream, four torn edges, four corner tapes]
  [hero band — full inner width of paper, ~45vh, griptape image background]
    [big ram, left third, cropped through torn top edge]
    [Anton "SKATE CLUB / AT UNC", right of horns]
    [Carolina-blue capsule + hand-drawn line, right side]
  [thin gap / ink hairline rule]
  [nav row — Cabin Sketch caps]
  [meeting info — Permanent Marker]
  [one inner tear, asymmetric placement]
[page ends]
```

This is a real restructure. Treat the existing v1 layout as a starting point but don't try to preserve `.banner` / `.hero` as separate sections — they merge.

### 5. Logo background

- Apply `mix-blend-mode: multiply` to the ram-skull `<img>` for v2.
- **Known limitation, document in report**: multiply against the bulletin board wall *or* the griptape band will fail — the white horns will go dark/muddy because the underlying texture is dark. This is unavoidable without a transparent PNG.
- **Flag explicitly to the user in your report**: "the logo's white background reads cleanly on cream-paper areas, but where the ram overlaps the griptape band, the multiply blend goes muddy. A transparent PNG of the logo is the proper fix. The user said earlier they could source one — this is the moment to ask."

## What does NOT change from v1

- Tape pieces and rotations (user said tape looks good)
- Cream paper color `#f0ebe1`
- Anton + Permanent Marker + Cabin Sketch + Special Elite font loads
- Inner tear concept and placement rule (~6px wide, asymmetric)
- All hard constraints (square corners, no gradients, no soft shadows, no `border-radius`, no generic sans)
- Mobile degradation rules (drop side edges + 2 tapes under 600px)

## Files to touch

- `C:\Users\julia\Tempo\uncskate-site\index.html` — restructure to merge banner into hero band
- `C:\Users\julia\Tempo\uncskate-site\styles\global.css` — wall background, edge swap + sizing, griptape swap, ram collapse, multiply blend

## Files NOT to touch

- All four tape SVGs (`tape-scotch.svg`, `tape-masking.svg`, `tape-painter.svg`, `tape-duct.svg`) — user approved
- `inner-tear.svg` — still fine
- `paper-texture.svg` — keep as the paper grain overlay
- `locked-spec.md` — will be updated by Claude after v2 is verified by the user
