# Skate-stylist punch list — v1 → v2

*Pass 3, 2026-05-19. Reaction to v1 build + user feedback + new texture assets.*

Five calls, no maybes.

## 1. Wall: **Bulletin Board 1** (`assets/textures/Bulletin board, option one. .jpg`)

A bulletin board is *literally* where skate flyers live — telephone poles, coffee shops, the cork board outside the rec center. It extends the Women in Skate "flyer-on-a-pole" logic the locked-spec already cites. Chalkboards read classroom (option 1 is too smooth/Pinterest-y; option 2 is better but still says "café menu," not skate spot). Ink black is safe but flat — and the spec already said v1 was *temporarily* flat-black because no scan existed. We have a scan now.

Pick **option 1** specifically — the chunky cork grain reads at distance; option 2 is finer and reads almost like sandpaper, which will fight the griptape band. Tile it; don't stretch.

Note: the locked-spec wall is `#111`. Overriding it is a real change — flag in the build note, don't sneak it in.

## 2. Griptape: **use `Skateboard grip tape.jpg` directly**

Real grit beats vector grit, every time. The current SVG looks like a noise filter. Drop the JPG in as the hero band's `background-image`, `background-size: ~600px` (don't zoom in so much it loses the silica sparkle, don't zoom out so much it tiles obviously). Keep `repeat`. Confirmed, not pushback.

## 3. Torn paper edges: **replace with `white-ripped-paper-png.webp`** — but only after surgery

The PNG is real-scanned and good (fibrous, asymmetric, no sine-wave tell). The brown vector is exactly the stock-vector trap to avoid — it has the AI/Canva tell. Reject it.

Use the white webp, but: it's *one* strip. `builder` needs to flip/rotate/slice it into four genuinely-different edges (top, bottom, left, right). Same source asset four times in the same orientation = the wrong kind of polish. Cut a different segment per edge.

## 4. Ram-skull alignment: **collapse into one element**

The user is right that the big ram should be next to the wordmark. I'd go further: kill the small header mark entirely. Real skate flyers have **one mascot**, big, with the wordmark beside or under it — see `women-in-skate-flyer.png`, see Thrasher covers, see every Polar ad. Two rams (small header + big hero) is a corporate-style "brand consistency" move that flyers don't make.

New layout: hero band keeps the big ram on the left third. Wordmark "SKATE CLUB / AT UNC" in Anton sits *immediately right of the ram's horns*, not in a separate banner above. Capsule and meeting info slot below or to the right.

This also fixes the "banner mark torn-through the top edge" gimmick, which was clever but reads as design-trick, not flyer.

## 5. Logo background: **transparent PNG, required**

`mix-blend-mode: multiply` works on white-paper backgrounds but will eat the cream's warmth and tint the ram's white horns gray. On a *bulletin board* wall it'll fail entirely — the cork will show through the horns. Get a transparent PNG. Non-negotiable. Filename: `assets/logo/UNC SKATE LOGO transparent.png`, swap in `index.html`.

Interim if no transparent version exists in 5 minutes: `mix-blend-mode: multiply` is acceptable *only* on the cream-paper instance, never the hero on griptape.
