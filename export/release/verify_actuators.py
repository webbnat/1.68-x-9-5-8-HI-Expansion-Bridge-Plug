"""Verify actuator STEP round-trip + render run-in/deployed section previews."""

from __future__ import annotations

from pathlib import Path

import gmsh

from render_previews import mesh_step_to_stl, render_stl  # type: ignore

REL = Path(__file__).resolve().parent
PARTS = REL / "step" / "parts"
ASSY = REL / "step" / "assemblies"
STL = REL / "stl"
PNG = REL / "png"
PNG.mkdir(exist_ok=True)

PART_FILES = [
    "SHEX-014A_gland_ring", "SHEX-014B_lock_ring", "SHEX-014C_charge_sub",
    "SHEX-015B_belleville", "SHEX-015C_belleville_housing",
    "SHEX-016_charge_chamber", "SHEX-016A_pilot_piston",
]


def check_solids(step: Path) -> tuple[int, int, float]:
    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 0)
    gmsh.merge(str(step))
    vols = gmsh.model.getEntities(3)
    surfs = gmsh.model.getEntities(2)
    vol = sum(gmsh.model.occ.getMass(3, t) for _, t in vols) if vols else 0.0
    # orphan surfaces = surfaces not bounding any volume
    needed = set()
    for v in vols:
        for d, t in gmsh.model.getBoundary([v], combined=False, oriented=False):
            needed.add((d, abs(t)))
    orphans = [s for s in surfs if s not in needed]
    gmsh.finalize()
    return len(vols), len(orphans), vol / 25.4**3


def main() -> None:
    print("== part round-trip ==")
    for p in PART_FILES:
        step = PARTS / f"{p}.stp"
        if not step.exists():
            print(f"  MISSING {p}")
            continue
        nv, no, vin3 = check_solids(step)
        flag = "ok " if (nv == 1 and no == 0) else "!! "
        print(f"  {flag}{p:32s} solids={nv} orphans={no} vol={vin3:.3f} in^3")

    print("== assemblies ==")
    for state in ("RUN_IN", "DEPLOYED"):
        step = ASSY / f"SHEX-ACT-S12_{state}.stp"
        if not step.exists():
            print(f"  MISSING {state}")
            continue
        nv, no, vin3 = check_solids(step)
        print(f"  {state}: solids={nv} orphans={no}")
        stl = STL / f"SHEX-ACT-S12_{state}.stl"
        if stl.exists():
            render_stl(stl, PNG / f"SHEX-ACT-S12_{state}.png", elev=16, azim=-58)
            render_stl(stl, PNG / f"SHEX-ACT-S12_{state}_section.png",
                       elev=8, azim=-90, cut_half=True)


if __name__ == "__main__":
    main()
