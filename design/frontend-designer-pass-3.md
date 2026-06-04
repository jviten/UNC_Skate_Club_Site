# Frontend-designer punch list — v1 → v2

*Pass 3, 2026-05-19. Reaction to v1 build + user feedback + new texture assets.*

## 1. Wall: **Bulletin Board 1** (`assets/textures/Bulletin board, option one. .jpg`)

The locked spec calls for ink-black wall, and `--wall: #111` is fine in the abstract — but the user clearly wants the wall to *do something*. Of the four options:

- **Chalkboard 1** (`blackchalkboardoption1.jpg`): too noisy/grungy, fights the cream paper.
- **Chalkboard 2** (`blackchalkboardoption2.png`): cleaner but reads "coffee shop menu," not skate.
- **Bulletin Board 2** (`Bulletin Board 2.jpg`): too uniform, looks like a stock cork swatch.
- **Bulletin Board 1**: high-contrast cork chunks, strongly textural, sells the "flyer pinned to the wall" metaphor the locked-spec is built around. Cork + tape + torn paper is the DIY postering culture the charter explicitly names (`women-in-skate-flyer.png` on a campus pole).

Switch `--wall` from `#111` to `url("../assets/textures/Bulletin board, option one. .jpg")` on `<body>`, `background-size: 600px`, `background-repeat: repeat`. Drop the spec's "no wall texture for v1" line — that decision predates the user having an asset they like.

## 2. Griptape: **use `Skateboard grip tape.jpg` directly**

Replace `griptape.svg`. The user said the synthesized version is "too non-realistic" — that's an asset problem, not a sizing problem, and we have a real photo of actual grit. Set `.hero` `background-image: url("../assets/textures/Skateboard grip tape.jpg")`, `background-size: cover` (not 200px repeat — the photo has organic variation; tiling it kills the realism that's the whole point).

## 3. Torn paper edges: **replace SVG with `white-ripped-paper-png.webp`, AND fix alignment in CSS**

Two separate problems, both real:

- **Texture (asset)**: the SVG edges read as a stylized line, not torn fiber. `white-ripped-paper-png.webp` is a real photographic tear with fringe and grain. Use it for all four edges by rotating one source: top = native, bottom = `rotate(180deg)`, left = `rotate(-90deg)`, right = `rotate(90deg)`. Each side gets a `background-position` offset so the four edges aren't visibly identical — combats AI-tell symmetry per charter.
- **Alignment (CSS)**: current `.edge--top` is `top: -16px` but `.paper` has `box-shadow: 2px 2px 0 var(--ink)` which extends the visual frame asymmetrically — the edges don't account for it. Also `height: 40px` is too thin to show real fringe. Bump edge heights to 60px, widths to 50px, increase bleed to `top/bottom: -28px`, `left/right: -24px` so the torn fringe fully clears the paper rect.

## 4. Ram-skull alignment: **replace the big hero ram with a larger banner mark, and move the banner mark to sit on the hero band**

Current structure: small 96px logo top-left in `.banner`, then meeting info, then a separate `.hero` band with a 42% skull on the left. The user says they read disconnected — they do. They're vertically separated by ~250px of empty paper.

Restructure: kill `.hero__skull`. Move `.banner__mark` into a position where it sits *across* the boundary between the cream paper banner area and the griptape hero band — top half on cream, bottom half overlapping the griptape. Size it 240–300px. The big Anton "SKATE CLUB / AT UNC" sits right of it. The capsule + scribble stay on the right side of the griptape band.

Concretely in CSS terms: `.banner` becomes `position: relative; z-index: 4`, `.banner__mark` gets `width: 280px; margin-bottom: -120px` (negative pull-down into the hero), and `.hero` keeps a `padding-left` large enough that the capsule doesn't collide. Net effect: logo and wordmark read as one unit, sitting *on* the griptape band, with horns punching through the torn top edge as the spec wants.

## 5. Logo background drop: **yes to `mix-blend-mode: multiply`** — but with a guard

On cream paper, `mix-blend-mode: multiply` on the logo PNG will drop the white background cleanly (white × cream = cream). On the griptape band (now a dark photo per #4), multiply will make the logo nearly invisible — the white horns will turn black.

Two options:

- **A (cheap)**: use `mix-blend-mode: multiply` and let the user see what happens.
- **B (correct)**: source a transparent PNG.

Recommend **A for this rev, B as a follow-up note**. Don't block the rebuild on sourcing a new asset.
