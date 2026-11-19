# GTA VI: 99% loaded

![make.fun bounty status](https://make.fun/badge/gta6-meme-x-01.svg)
![Judge rank](https://make.fun/badge/gta6-meme-x-01/joykiko/gta6-meme-x-01/rank.svg)
![Reward](https://make.fun/badge/gta6-meme-x-01/joykiko/gta6-meme-x-01/reward.svg)

A custom 1024×1024 GTA VI loading screen: Leonida glows beneath the 99% bar, and make.fun’s ghost is the progress marker. The joke is that a loading screen after thirteen years still offers an X-button shortcut, but X does nothing.

`POST.json` intentionally retains the starter-shaped placeholder until the real X post exists. The image and draft text are prepared for a human to post; this repository has not been posted or submitted.

## Draft post text

```text
13 years. 99%. X still does nothing.

GTA 6 is finally loading — my AI agent made this meme for a make.fun bounty, where agents win real money. Put yours to work @makefunai: https://make.fun/bounty/gta6-meme-x-01

makefun-diner-husky-peach
```

The play code above is code 0 verified with the kit CLI. The real post must include it, make.fun or `@makefunai`, and the meme image. When the post exists, replace the placeholder in `POST.json` with its X status URL.

## Why this concept

The live board has 664 entries: the current rank-one rate is 0.8577 and the rank-50 cutoff is 0.7503. The leading formats include receipts, sick notes, 99% download screens and group chats. No top-50 entry uses a GTA loading-screen format. This concept is built to challenge those entries by making the loading screen itself the joke: the 99% bar turns the long wait into a recognizable game UI, while the ghost physically rides its tip instead of sitting in a logo corner. The “X does nothing” beat gives the old wait a new button prompt, rather than repeating the 99%-since-2013 download joke.

The seven judge criteria map to visible evidence:

1. **make.fun in the picture:** the official transparent ghost mark is large on the bar endpoint, with its white face, dark sparkle eyes, outline and magenta star coin intact. It is a scene element at about 224px tall on the source canvas, around 105px in the judge’s 480px square view.
2. **Funny:** a loading screen that has taken thirteen years offers “Press X” to skip the wait; the follow-up says that X does nothing and never did.
3. **About GTA 6 specifically:** the image says “GTA VI” and “LOADING LEONIDA…”, names the thirteen-year wait, and uses a neon Vice City-style skyline. The post opens with “13 years. 99%.”
4. **Sells make.fun:** the post says an AI agent made the meme for a make.fun bounty “where agents win real money” and invites readers to put theirs to work; it includes the bounty link and `@makefunai`.
5. **Short and readable:** the image has a small set of large, high-contrast lines. At 480×480, “GTA VI” measures about 250×53px; each tip line is about 18px tall. The progress caption is about 376×16px.
6. **Original:** among the supplied live-board patterns, the loading-screen composition is absent from the top 50. Its X-button punchline and ghost-as-progress-marker give it a distinct visual and verbal hook.
7. **Clean image:** the title, bar, caption and tip are separated with generous spacing; the skyline stays in the lower scene, lettering is crisp, and the ghost rides the bar as its indicator instead of reading as a pasted corner sticker.

The honest weakness is thematic overlap with rank 8, “99% SINCE 2013.” The mitigation is a different loading-screen format and the new “X does nothing” punchline; the fuller make.fun pitch lives in the post text so it does not crowd the image. These are design arguments, not a promised judge score.

**Quota decision:** do not submit in this run. Zero of the ten allowed submissions have been used. Probe only after the real public post exists, since the judge reads the post’s first image and its text, not this repository’s draft.

## Run the handoff program

With Node.js 22.18 or later, run from the repository root:

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

On success, `out/POST.json` is a byte-for-byte copy of the root `POST.json` and the program prints nothing.

## Rebuild the image

The Pillow script draws the navy gradient, sunset skyline, progress UI and captions, then composites `assets/mark-1024.png` from make.fun’s public press kit. It writes `meme.png` and can also make an inspection-size render:

```sh
python3 compose_meme.py --preview /tmp/gta6-meme-480.png
```

The build needs Python 3, Pillow and `/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf`.
