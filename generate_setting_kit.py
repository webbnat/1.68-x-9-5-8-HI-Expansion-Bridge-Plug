"""Generate SHEX-AK-20 setting adapter kit STEP/STL exports.

Outputs to export/release/step/{parts,assemblies} alongside the plug
release. Run:  .venv\\Scripts\\python generate_setting_kit.py
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from cad import release_solids as rs
from cad import setting_kit_solids as ks

ROOT = Path(__file__).parent
OUT = ROOT / "export" / "release"
PARTS_DIR = OUT / "step" / "parts"
ASSY_DIR = OUT / "step" / "assemblies"
STL_DIR = OUT / "stl"

PARTS = [
    ("ST-101_setting_sleeve", "ST-101 setting sleeve/shoe", "4140 HT (AMS 6415)", 1,
     lambda m: ks.build_st101_setting_sleeve(m)),
    ("ST-102_tension_rod", "ST-102 tension rod", "4140 HT (AMS 6415)", 1,
     lambda m: ks.build_st102_tension_rod(m)),
    ("ST-103_shear_stud", "ST-103 shear stud 45 klbf", "4140 HT calibrated lot", 1,
     lambda m: ks.build_st103_shear_stud(m)),
    ("ST-104_stroke_spacer", "ST-104 stroke spacer", "4140 HT", 2,
     lambda m: ks.build_st104_spacer(m)),
]


def export_part(fname, body_name, material, builder) -> dict:
    t0 = time.time()
    with rs.session(fname) as m:
        tags = builder(m)
        m.register(body_name, material, tags)
        m.write_step(PARTS_DIR / f"{fname}.stp")
    dt = time.time() - t0
    print(f"  ok  {fname}  ({dt:.1f}s)")
    return {"file": str(PARTS_DIR / f"{fname}.stp"), "elapsed_s": round(dt, 1)}


def export_assembly(state: str) -> dict:
    name = f"SHEX-AK-20_INTERFACE_{state.upper()}"
    t0 = time.time()
    with rs.session(name) as m:
        ks.build_kit_assembly(m, state)
        m.write_step(ASSY_DIR / f"{name}.stp")
        m.write_stl(STL_DIR / f"{name}.stl", size_mm=3.0)
        n = len(m.bodies)
    dt = time.time() - t0
    print(f"  ok  assembly {state}  ({dt:.1f}s, {n} bodies)")
    return {"file": str(ASSY_DIR / f"{name}.stp"),
            "stl": str(STL_DIR / f"{name}.stl"), "bodies": n,
            "elapsed_s": round(dt, 1)}


def main() -> None:
    PARTS_DIR.mkdir(parents=True, exist_ok=True)
    ASSY_DIR.mkdir(parents=True, exist_ok=True)
    STL_DIR.mkdir(parents=True, exist_ok=True)
    manifest: dict = {"kit": "SHEX-AK-20", "parts": {}, "assemblies": {}}
    for fname, body, mat, qty, builder in PARTS:
        info = export_part(fname, body, mat, builder)
        info.update({"material": mat, "qty_per_kit": qty})
        manifest["parts"][fname] = info
    for state in ("rigged", "released"):
        manifest["assemblies"][state] = export_assembly(state)
    mpath = OUT / "manifest_setting_kit.json"
    mpath.write_text(json.dumps(manifest, indent=2))
    print(f"\nManifest: {mpath}")


if __name__ == "__main__":
    main()
