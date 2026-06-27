"""Generate the COMPLETE full-tool SHEX-BP-UHEX-54 assemblies (plug + stage 1/2
internal actuators) in RUN-IN and SET positions, into a NEW folder.

This supersedes the earlier plug-only full-tool exports: build_assembly now
injects the SHEX-014/015/016 actuator hardware (mandrel-mounted), so these
files are the single complete tool model.

Output: export/full_tool/{step,stl,png}
Run:  .venv\\Scripts\\python generate_full_tool.py
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from cad import release_solids as rs

ROOT = Path(__file__).parent
OUT = ROOT / "export" / "full_tool"
STEP_DIR = OUT / "step"
STL_DIR = OUT / "stl"
PNG_DIR = OUT / "png"


def export_state(state: str) -> dict:
    label = "RUN-IN" if state == "run_in" else "SET"
    name = f"SHEX-BP-UHEX-54_FULL_{label}"
    t0 = time.time()
    with rs.session(name) as m:
        rs.build_assembly(m, state)
        bodies = [b.name for b in m.bodies]
        m.write_step(STEP_DIR / f"{name}.stp")
        m.write_stl(STL_DIR / f"{name}.stl", size_mm=5.0)
        n = len(m.bodies)
    dt = time.time() - t0
    print(f"  ok  {name}  ({dt:.1f}s, {n} bodies)")
    return {"step": str(STEP_DIR / f"{name}.stp"),
            "stl": str(STL_DIR / f"{name}.stl"),
            "bodies": n, "body_names": bodies, "elapsed_s": round(dt, 1)}


def render() -> None:
    sys.path.insert(0, str(ROOT / "export" / "release"))
    from render_previews import render_stl  # type: ignore

    for state, label in (("run_in", "RUN-IN"), ("set", "SET")):
        stl = STL_DIR / f"SHEX-BP-UHEX-54_FULL_{label}.stl"
        if not stl.exists():
            continue
        max_r = 112.0 if label == "SET" else None   # hide casing ref in SET
        stretch = label == "RUN-IN"   # exaggerate radius only for the slim run-in
        render_stl(stl, PNG_DIR / f"SHEX-BP-UHEX-54_FULL_{label}.png",
                   elev=14, azim=-55, stretch_z=stretch, max_r_mm=max_r)
        render_stl(stl, PNG_DIR / f"SHEX-BP-UHEX-54_FULL_{label}_section.png",
                   elev=8, azim=-90, stretch_z=stretch, max_r_mm=max_r, cut_half=True)


def main() -> None:
    for d in (STEP_DIR, STL_DIR, PNG_DIR):
        d.mkdir(parents=True, exist_ok=True)
    manifest = {"tool": "SHEX-BP-UHEX-54 (complete: plug + stage 1/2 actuators)",
                "revision": "B",
                "note": "Rev B adds the DCN-12 sequence/initiation sub "
                        "(SHEX-017 + 017A arming sleeve + 017B reference piston) "
                        "to the SHEX-014/015/016 actuator hardware; supersedes "
                        "the plug-only and Rev-A full-tool exports",
                "states": {}}
    for state in ("run_in", "set"):
        manifest["states"][state] = export_state(state)
    render()
    (OUT / "manifest_full_tool.json").write_text(json.dumps(manifest, indent=2))
    print(f"\nManifest: {OUT / 'manifest_full_tool.json'}")


if __name__ == "__main__":
    main()
