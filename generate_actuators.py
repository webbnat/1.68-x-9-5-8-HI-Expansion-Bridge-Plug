"""Generate SHEX stage 1/2 internal actuator STEP/STL exports.

Outputs to export/release/step/{parts,assemblies} alongside the plug and the
setting kit. Run:  .venv\\Scripts\\python generate_actuators.py
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from cad import release_solids as rs
from cad import actuator_solids as acs

ROOT = Path(__file__).parent
OUT = ROOT / "export" / "release"
PARTS_DIR = OUT / "step" / "parts"
ASSY_DIR = OUT / "step" / "assemblies"
STL_DIR = OUT / "stl"

PARTS = [
    ("SHEX-014A_gland_ring", "Bladder end gland / swage ring", "17-4 PH H1075", 4,
     lambda m: acs.build_shex_014a_gland_ring(m)),
    ("SHEX-014B_lock_ring", "Body-lock ratchet ring (stage 1/2)", "17-4 PH H1075", 2,
     lambda m: acs.build_shex_014b_lock_ring(m)),
    ("SHEX-014C_charge_sub", "Burst-disk charge sub", "4140 HT + burst disk", 2,
     lambda m: acs.build_shex_014c_charge_sub(m)),
    ("SHEX-015B_belleville", "Belleville hold washer", "Inconel 718", 4,
     lambda m: acs.build_shex_015b_belleville(m)),
    ("SHEX-015C_belleville_housing", "Belleville preload housing", "4140 HT", 1,
     lambda m: acs.build_shex_015c_belleville_housing(m)),
    ("SHEX-016_charge_chamber", "Charge / reference chamber sleeve", "4140 HT", 1,
     lambda m: acs.build_shex_016_charge_chamber(m)),
    ("SHEX-016A_pilot_piston", "Equalizing pilot piston", "17-4 PH H1075", 1,
     lambda m: acs.build_shex_016a_pilot_piston(m)),
    ("SHEX-017_sequence_sub", "Sequence / initiation sub (DCN-12)", "4140 HT", 1,
     lambda m: acs.build_shex_017_sequence_sub(m)),
    ("SHEX-017A_arming_sleeve", "Stage1->2 arming sleeve (DCN-12)", "17-4 PH H1075", 1,
     lambda m: acs.build_shex_017a_arming_sleeve(m)),
    ("SHEX-017B_reference_piston", "Reference / ball-seat piston (DCN-12)", "17-4 PH H1075", 1,
     lambda m: acs.build_shex_017b_reference_piston(m)),
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
    name = f"SHEX-ACT-S12_{state.upper()}"
    t0 = time.time()
    with rs.session(name) as m:
        acs.build_actuator_assembly(m, state)
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
    manifest: dict = {"package": "SHEX stage 1/2 actuators (SHEX-014/015/016)",
                      "parts": {}, "assemblies": {}}
    for fname, body, mat, qty, builder in PARTS:
        info = export_part(fname, body, mat, builder)
        info.update({"material": mat, "qty_per_plug": qty})
        manifest["parts"][fname] = info
    for state in ("run_in", "deployed"):
        manifest["assemblies"][state] = export_assembly(state)
    mpath = OUT / "manifest_actuators.json"
    mpath.write_text(json.dumps(manifest, indent=2))
    print(f"\nManifest: {mpath}")


if __name__ == "__main__":
    main()
