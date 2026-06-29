# The Forgotten Cell — a 3D dungeon room

A single-room, first-person 3D dungeon built with **Three.js** (WebGL). Real
photogrammetry-grade PBR textures and sculpted glTF props, dynamic torch
lighting with shadows, GTAO ambient occlusion, an HDRI environment map for
reflections, bloom, and atmospheric fog.

## Play

```bash
./play.sh
```

That serves the folder at <http://localhost:8765/> and opens your browser. A
local server is required because the game loads ES modules and asset files
(opening `index.html` as a `file://` URL will not work).

Manual alternative:

```bash
python3 -m http.server 8765   # then open http://localhost:8765/index.html
```

## Controls

| Key | Action |
|-----|--------|
| `W A S D` | Move |
| Mouse | Look |
| `Shift` | Sprint |
| `E` | Interact (open the chest / try the gate) |
| `Esc` | Release the mouse cursor |

**Goal:** open the treasure chest to claim the hoard, then escape through the
barred gate.

## How it's built

- **Renderer:** ACES filmic tone mapping, PCF soft shadows, pixel-ratio capped at 2.
- **Materials:** PBR `MeshStandardMaterial` with `diff` + `nor_gl` (OpenGL
  normal) + packed `arm` (AO/Rough/Metal) maps. The floor also uses a
  displacement map on subdivided geometry for real geometric relief.
- **Props:** glTF models auto-scaled to fit and seated on the floor; the chest
  lid is re-parented to a hinge pivot so it swings open.
- **Lighting:** 4 flickering shadow-casting torch point-lights + a lantern
  light + cold fill light, plus an HDRI-derived environment map (PMREM) for
  metal/gold reflections.
- **Post:** GTAO (ground-truth ambient occlusion) → UnrealBloom → gamma.

## Assets & licensing

All textures, HDRI, and 3D models are from **[Poly Haven](https://polyhaven.com)**
and are **CC0 (public domain)** — free to use commercially with no attribution
required. They were downloaded locally via `download_assets.py` (re-runnable).

Models: `treasure_chest`, `wine_barrel_01`, `wooden_crate_01/02`,
`wooden_lantern_01`, `wooden_bucket_01`, `ornate_medieval_mace`, `rock_07`.
Textures: `medieval_blocks_02` (walls), `cobblestone_floor_08` (floor),
`worn_planks` (wood), `rusty_metal_02` (iron). HDRI: `moonless_golf`.

Three.js is loaded from the jsDelivr CDN, so the **first run needs an internet
connection** (the engine itself isn't vendored locally; the art assets are).
