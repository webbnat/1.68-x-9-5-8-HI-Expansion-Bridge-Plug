#!/usr/bin/env python3
"""Generate Stage 3 iris segment and module STLs."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from cad.mesh_utils import box, cylinder, export_mesh, merge, rotate_z, translate, tube

OUTPUT = ROOT / "output" / "stl" / "stage3_iris"


def iris_segment(inner_r: float, outer_r: float, thickness: float, arc_deg: float) -> "MeshData":
    """Single petal/segment approximated as tapered box."""
    mid_r = (inner_r + outer_r) / 2
    arc_len = math.radians(arc_deg) * mid_r
    seg = box(arc_len, outer_r - inner_r, thickness)
    return translate(seg, mid_r, 0, thickness / 2)


def iris_ring_segmented(
    inner_od: float,
    outer_od: float,
    count: int = 16,
    thickness: float = 0.125,
    axial: float = 2.75,
) -> "MeshData":
    inner_r = inner_od / 2
    outer_r = outer_od / 2
    arc = 360 / count * 0.85
    parts = []
    for i in range(count):
        seg = iris_segment(inner_r, outer_r, axial, arc)
        parts.append(rotate_z(seg, i * (360 / count)))
    hub = cylinder(inner_r * 0.95, axial, segments=32)
    return merge(hub, *parts)


def helix_guide_ring(od: float, length: float) -> "MeshData":
    return tube(od / 2, od / 2 - 0.15, length)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    files = []

    # Collapsed: segments nested at 5.75" envelope
    collapsed = iris_ring_segmented(5.750, 6.200, count=16, thickness=0.125, axial=2.75)
    export_mesh(collapsed, str(OUTPUT / "stage3_iris_collapsed_575od.stl"))
    files.append("stage3_iris_collapsed_575od.stl")

    # Deployed: segments at 8.65" envelope
    deployed = iris_ring_segmented(5.750, 8.650, count=16, thickness=0.125, axial=2.75)
    export_mesh(deployed, str(OUTPUT / "stage3_iris_deployed_865od.stl"))
    files.append("stage3_iris_deployed_865od.stl")

    # Full module: iris + guide rings + actuator sleeve
    module = merge(
        helix_guide_ring(5.50, 1.25),
        translate(iris_ring_segmented(5.750, 6.200, 16, 0.125, 2.75), 0, 0, 1.25),
        translate(helix_guide_ring(5.75, 1.5), 0, 0, 4.0),
        translate(cylinder(2.5 / 2, 2.0), 0, 0, 5.5),
    )
    export_mesh(module, str(OUTPUT / "stage3_iris_module_75in.stl"))
    files.append("stage3_iris_module_75in.stl")

    # Single segment for machining detail
    export_mesh(iris_segment(5.750 / 2, 8.650 / 2, 2.75, 20), str(OUTPUT / "stage3_iris_single_segment.stl"))
    files.append("stage3_iris_single_segment.stl")

    (OUTPUT / "manifest.json").write_text(json.dumps({"files": files}, indent=2))
    print(f"Generated {len(files)} Stage 3 iris STLs in {OUTPUT}")


if __name__ == "__main__":
    main()
