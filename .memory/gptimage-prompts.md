---
name: gptimage-prompts
description: "Every new article gets a Zapret-tan/RKN-tan cover prompt; template, scenes, camera presets in vault gptimage/; white RKN-emblem mug (no text) in every prompt; medium shot sometimes"
metadata:
  node_type: memory
  type: project
  originSessionId: c655fef4-7ed0-4895-af65-85b257e77724
  modified: 2026-10-24T20:17:00.506Z
---

Rules from the user, 2026-10-24 (also written into the "Обложки статей" section of `/home/codex-pve/Privacy/AGENTS.md` and into the vault-image skill):

- For every new article, come up with a cover: what Zapret-tan and RKN-tan do (it should fit the article's topic), where, and the camera: far and full body, or a medium thigh-up shot.
- Use the medium shot (preset B in `gptimage/camera-presets.md`) **sometimes**, not always the full-body one.
- **Every prompt includes the characters block from `gptimage/characters.md`.** Clothes are NOT described in text: they come only from the attached references. The text names only invariant traits (hair, eyes, fangs) and says the references take priority. Each character has two looks: Halloween (black-orange character sheets saved in gptimage/) and everyday (navy suit / blue cropped jacket). Lesson of 2026-10-24: first the "realistic faces" line made the generator redraw faces; then a block that described the everyday outfit made it override the Halloween sheets, because the text won over the images.
- **The block always states age and build:** both are adult women of about 25, tall, long-legged, adult proportions, serious and confident, nothing childlike (Russian Important line + English block + Constraints item). On 2026-10-24 the user said they came out "too childish" once the outfit text was removed; "cute/tiny/playful" in the scene made it worse. Never use those words near the characters.
- **Every prompt includes a white ceramic mug with the Roskomnadzor emblem, no lettering.** In Constraints it is the only allowed logo.
- Save each prompt in `/home/codex-pve/Privacy/gptimage/`: one `.md` per scene (`publish: false`), with the result or reference image next to it under the same name. Saved locations: office (in the Halloween file), Halloween living room, regular living room, office hallway with a pillar, night lounge with laptop, Halloween DPI checkpoint cover. Also `zapret-kvn-app-logo.md`: app icon (shield + character opening a door), no mug since it is an icon. The user wants Windows 11 Fluent Design style: calm medium-saturated Fluent blues, no lineart, soft top light; the pastel v1 was "too bright". Split styles: only the badge is Fluent 3D; the character stays flat minimalist 2D anime (lineart, cel shading, minimal face). Applying Fluent to her made her "too realistic" (v2). Later lessons: the icon outline is the shield with a huge keyhole, and she is seen only through it (when she stood in front, her body hid the keyhole); for the logo she is ~20 with a soft face ("mid-twenties", "smirk", "sharp" made her too old); keep it minimal: no earpiece, badges or thin strands (user: "too detailed"); no visible eyes at all, the opaque sunglasses stay on (user: "I don't like the eyes at all"). Iterations live in gptimage/zapret-kvn-app-logo.md.

The template: Russian lines about Image 1 / Image 2 emotions, then English Scene / Composition / Style / Constraints blocks (anatomy, no extra characters, no readable text). RKN-tan has purple hair and a blue suit; Zapret-tan has blue hair, a cropped jacket and fishnets. "Change only the scene" means rewriting Scene plus only the lines in other blocks that name the old room's objects. References sometimes show text on the mug; the prompts must not reproduce that. There is no modesty / "nothing under the skirts" constraint: the owner removed it on 2026-11-03 as added by mistake, and accepted a cover that shows under a skirt.

**Why:** the user wants consistent cover art for articles and asked to write it down "so we don't forget".

**How to apply:** when writing a new article, propose the cover prompt too. Don't commit `gptimage/` without asking: any vault commit rebuilds the public wiki, and `publish: false` doesn't protect images (see [[vault-push-and-shared-dirs]]).
