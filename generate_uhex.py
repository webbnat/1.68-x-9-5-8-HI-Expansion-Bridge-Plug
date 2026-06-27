#!/usr/bin/env python3
"""Generate conceptual STLs for 9-5/8\" 40# ultra-high expansion variant."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from cad.mesh_utils import cylinder, export_mesh, merge, stent_lattice, translate, tube

OUTPUT = ROOT / "output" / "stl" / "uhex_9625"


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    manifest = []

    def save(data, name: str) -> None:
        path = OUTPUT / f"{name}.stl"
        export_mesh(data, str(path))
        manifest.append(name)
        print(f"  ok {name}.stl")

    print("Generating UHEX 9-5/8\" conceptual STLs...")

    # 3-stage expansion cascade (collapsed run-in)
    save(stent_lattice(1.688, 0.040, 4.0, cells=10, rings=6), "uhex_stage1_inner_stent_collapsed")
    save(stent_lattice(3.375, 0.045, 5.0, cells=14, rings=7), "uhex_stage2_middle_stent_collapsed")
    save(stent_lattice(5.750, 0.050, 6.0, cells=18, rings=8), "uhex_stage3_outer_stent_collapsed")

    # Expanded stage representations
    save(stent_lattice(3.375, 0.040, 4.0, cells=14, rings=6), "uhex_stage1_inner_stent_expanded")
    save(stent_lattice(5.750, 0.045, 5.0, cells=18, rings=7), "uhex_stage2_middle_stent_expanded")
    save(stent_lattice(8.650, 0.055, 6.0, cells=24, rings=10), "uhex_stage3_outer_stent_expanded")

    # Seal land module (one 4" x 8.72" OD unit)
    save(tube(8.720 / 2, 8.720 / 2 - 0.35, 4.0), "uhex_seal_land_module_4in")

    # MTM ring segment
    save(tube(8.800 / 2, 8.800 / 2 - 0.30, 0.45), "uhex_mtm_ring_segment")

    # Full conceptual assembly (module stack, not watertight union)
    z = 0.0
    parts = [
        cylinder(1.375 / 2, 3.0),  # fishing neck
    ]
    z = 3.0
    parts.append(translate(tube(8.720 / 2, 8.720 / 2 - 0.25, 4.5), 0, 0, z))  # upper slips zone
    z += 4.5
    parts.append(translate(tube(8.720 / 2, 8.720 / 2 - 0.30, 3.0), 0, 0, z))  # upper MTM
    z += 3.0
    # 36" seal represented as 9 modules
    for i in range(9):
        parts.append(translate(tube(8.720 / 2, 8.720 / 2 - 0.35, 4.0), 0, 0, z + i * 4.0))
    z += 36.0
    parts.append(translate(tube(8.720 / 2, 8.720 / 2 - 0.30, 3.0), 0, 0, z))  # lower MTM
    z += 3.0
    parts.append(translate(stent_lattice(5.750, 0.050, 6.0, cells=18, rings=8), 0, 0, z))  # cascade
    z += 6.0
    parts.append(translate(stent_lattice(3.375, 0.045, 5.0, cells=14, rings=7), 0, 0, z))
    z += 5.0
    parts.append(translate(stent_lattice(1.688, 0.040, 4.0, cells=10, rings=6), 0, 0, z))
    z += 4.0
    parts.append(translate(tube(8.720 / 2, 8.720 / 2 - 0.25, 4.5), 0, 0, z))  # lower slips
    z += 4.5
    parts.append(translate(cylinder(1.688 / 2, 2.0), 0, 0, z))  # bottom sub

    save(merge(*parts), "uhex_30_assembly_concept_72in")

    meta = OUTPUT / "manifest.json"
    meta.write_text(json.dumps({"files": manifest, "count": len(manifest)}, indent=2))
    print(f"\nDone — {len(manifest)} files in {OUTPUT}")


if __name__ == "__main__":
    main()
