#!/usr/bin/env python3
import json, os, sys, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.abspath(__file__))
API = "https://api.polyhaven.com/files/"

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "dungeon-game/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

def fetch_json(slug):
    return json.loads(get(API + slug).decode())

def save(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        print(f"  · cached {os.path.relpath(path, ROOT)}")
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = get(url)
    with open(path, "wb") as f:
        f.write(data)
    print(f"  ↓ {os.path.relpath(path, ROOT)}  ({len(data)//1024} KB)")

# --- TEXTURES: download Diffuse, nor_gl, arm (AO/Rough/Metal), Displacement at 2k ---
TEXTURES = {
    "wall":  "medieval_blocks_02",
    "floor": "cobblestone_floor_08",
    "wood":  "worn_planks",
    "metal": "rusty_metal_02",
}
WANT_MAPS = {"Diffuse": "diff", "nor_gl": "nor", "arm": "arm", "Displacement": "disp"}

print("=== TEXTURES ===")
for key, slug in TEXTURES.items():
    print(slug)
    d = fetch_json(slug)
    for apimap, short in WANT_MAPS.items():
        node = d.get(apimap, {})
        if "2k" in node and "jpg" in node["2k"]:
            url = node["2k"]["jpg"]["url"]
            save(url, os.path.join(ROOT, "assets", "tex", f"{key}_{short}.jpg"))

# --- MODELS: glTF at 1k, mirroring relative include paths ---
MODELS = ["treasure_chest", "Barrel_01", "wooden_crate_02", "wooden_crate_01",
          "wooden_lantern_01", "rock_07", "ornate_medieval_mace", "wooden_bucket_01"]

print("=== MODELS ===")
for slug in MODELS:
    try:
        d = fetch_json(slug)
    except Exception as e:
        print(f"  ! skip {slug}: {e}")
        continue
    g = d.get("gltf", {})
    res = "1k" if "1k" in g else (list(g.keys())[0] if g else None)
    if not res:
        print(f"  ! no gltf for {slug}")
        continue
    node = g[res]["gltf"]
    base = os.path.join(ROOT, "assets", "models", slug)
    fname = os.path.basename(node["url"])
    print(slug)
    save(node["url"], os.path.join(base, fname))
    for relpath, info in node.get("include", {}).items():
        save(info["url"], os.path.join(base, relpath))

# --- HDRI for environment reflections (1k, dark/indoor) ---
print("=== HDRI ===")
hd = fetch_json("moonless_golf")
hnode = hd.get("hdri", {}).get("1k", {}).get("hdr")
if hnode:
    save(hnode["url"], os.path.join(ROOT, "assets", "hdri", "env_1k.hdr"))
else:
    print("  ! hdri shape unexpected:", list(hd.get("hdri", {}).keys()))

print("DONE")
