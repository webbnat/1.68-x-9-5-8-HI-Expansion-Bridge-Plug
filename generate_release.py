"""Generate the SHEX-BP-UHEX-54 release package:

  export/release/step/parts/        one STEP per manufactured part
  export/release/step/assemblies/   full tool STEP, run-in + set
  export/release/stl/               mesh previews of both assemblies
  export/release/manifest.json

Run:  .venv\\Scripts\\python generate_release.py [--only PART]
"""

from __future__ import annotations

import json
import sys
import time
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from cad import release_solids as rs

ROOT = Path(__file__).parent
OUT = ROOT / "export" / "release"
PARTS_DIR = OUT / "step" / "parts"
ASSY_DIR = OUT / "step" / "assemblies"
STL_DIR = OUT / "stl"


PARTS = [
    # (filename, body name, material, qty per plug, builder)
    ("SHEX-001_iris_segment", "SHEX-001 iris segment", "17-4 PH H900 (H1150M)", 16,
     lambda m: rs.build_shex_001_iris_segment(m)),
    ("SHEX-002_helix_guide", "SHEX-002 helix guide insert", "Inconel 718 (AMS 5662)", 1,
     lambda m: rs.build_shex_002_helix_guide(m)),
    ("SHEX-003_mtm_ring_segment", "SHEX-003 MTM ring segment", "17-4 PH H900", 12,
     lambda m: rs.build_shex_003_mtm_segment(m)),
    ("SHEX-004_hnbr_seal_preform", "SHEX-004 HNBR seal liner preform", "HNBR 90A", 4,
     lambda m: rs.build_shex_004_hnbr_preform(m)),
    ("SHEX-005_petal_backup", "SHEX-005 petal backup", "17-4 PH H900", 64,
     lambda m: rs.build_shex_005_petal_backup(m)),
    ("SHEX-006_upper_slip_segment", "SHEX-006 upper slip segment", "17-4 PH H900, teeth case hardened", 8,
     lambda m: rs.build_slip_segment(m)),
    ("SHEX-007_lower_slip_segment", "SHEX-007 lower slip segment", "17-4 PH H900, teeth case hardened", 8,
     lambda m: rs.build_slip_segment(m)),
    ("SHEX-008_stage1_stent_runin", "SHEX-008 stage 1 stent sleeve (run-in)", "17-4 PH H900", 1,
     lambda m: rs.build_shex_008_stage1_stent(m)),
    ("SHEX-009_stage2_stent_runin", "SHEX-009 stage 2 stent sleeve (run-in)", "17-4 PH H900", 1,
     lambda m: rs.build_shex_009_stage2_stent(m)),
    ("SHEX-010_support_sleeve", "SHEX-010 stage 3 support sleeve", "17-4 PH H900", 1,
     lambda m: rs.build_shex_010_support_sleeve(m)),
    ("SHEX-011_inner_mandrel", "SHEX-011 inner mandrel", "17-4 PH H900", 1,
     lambda m: rs.build_shex_011_mandrel(m)),
    ("SHEX-011A_mandrel_tail_sleeve", "SHEX-011A mandrel tail sleeve", "4140 HT 28-32 HRC", 1,
     lambda m: rs.build_shex_011a_tail_sleeve(m)),
    ("SHEX-012_fishing_neck", "SHEX-012 fishing neck / top sub", "4140 HT 28-32 HRC", 1,
     lambda m: rs.build_shex_012_fishing_neck(m)),
    ("SHEX-013_equalizing_sub_body", "SHEX-013 equalizing sub body", "4140 HT 28-32 HRC", 1,
     lambda m: rs.build_shex_013_body(m)),
    ("SHEX-013S_sliding_sleeve", "SHEX-013S equalizing sliding sleeve", "4140 HT 28-32 HRC", 1,
     lambda m: rs.build_shex_013s_sleeve(m)),
]


def export_part(fname: str, body_name: str, material: str, builder) -> dict:
    t0 = time.time()
    with rs.session(fname) as m:
        tags = builder(m)
        m.register(body_name, material, tags)
        path = PARTS_DIR / f"{fname}.stp"
        m.write_step(path)
    return {"file": str(path.relative_to(ROOT)), "elapsed_s": round(time.time() - t0, 1)}


def export_assembly(state: str) -> dict:
    t0 = time.time()
    name = f"SHEX-BP-UHEX-54_{'RUN-IN' if state == 'run_in' else 'SET'}"
    with rs.session(name) as m:
        rs.build_assembly(m, state)
        step_path = ASSY_DIR / f"{name}.stp"
        m.write_step(step_path)
        stl_path = STL_DIR / f"{name}.stl"
        m.write_stl(stl_path, size_mm=4.0)
        n_bodies = len(m.bodies)
    return {
        "file": str(step_path.relative_to(ROOT)),
        "stl": str(stl_path.relative_to(ROOT)),
        "bodies": n_bodies,
        "elapsed_s": round(time.time() - t0, 1),
    }


def main() -> None:
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1]

    for d in (PARTS_DIR, ASSY_DIR, STL_DIR):
        d.mkdir(parents=True, exist_ok=True)

    manifest: dict = {"tool": "SHEX-BP-UHEX-54", "parts": {}, "assemblies": {}}
    failures: list[str] = []

    for fname, body_name, material, qty, builder in PARTS:
        if only and only not in fname:
            continue
        try:
            info = export_part(fname, body_name, material, builder)
            info.update({"material": material, "qty_per_plug": qty})
            manifest["parts"][fname] = info
            print(f"  ok  {fname}  ({info['elapsed_s']}s)")
        except Exception:
            failures.append(fname)
            print(f"  FAIL {fname}")
            traceback.print_exc()

    if not only:
        for state in ("run_in", "set"):
            try:
                info = export_assembly(state)
                manifest["assemblies"][state] = info
                print(f"  ok  assembly {state}  ({info['elapsed_s']}s, {info['bodies']} bodies)")
            except Exception:
                failures.append(f"assembly_{state}")
                print(f"  FAIL assembly {state}")
                traceback.print_exc()

    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"\nManifest: {OUT / 'manifest.json'}")
    if failures:
        print("FAILURES:", ", ".join(failures))
        sys.exit(1)


if __name__ == "__main__":
    main()
