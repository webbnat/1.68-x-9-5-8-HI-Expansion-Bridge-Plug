#!/usr/bin/env python3
"""
Generate all STL files for the Stent-Inspired High-Expansion Retrievable Bridge Plug.

Uses CadQuery when available (Python <= 3.12); otherwise pure-Python mesh generator.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

OUTPUT = ROOT / "output" / "stl"
MANIFEST = ROOT / "output" / "manifest.json"


def _generate_with_mesh_utils() -> list[dict]:
    from cad.mesh_utils import (
        box,
        cone,
        cylinder,
        export_mesh,
        merge,
        rotate_z,
        stent_lattice,
        translate,
        tube,
        wedge_profile,
    )

    manifest: list[dict] = []
    OUTPUT.mkdir(parents=True, exist_ok=True)

    def save(data, name: str) -> None:
        path = OUTPUT / f"{name}.stl"
        export_mesh(data, str(path))
        manifest.append({"file": path.name, "path": str(path), "units": "mm", "engine": "mesh_utils"})
        print(f"  ok {path.name}")

    print("Generating STLs (pure-Python mesh engine)...")

    # Stent sleeves
    save(stent_lattice(1.688, 0.035, 3.25), "01_stent_sleeve_collapsed")
    save(stent_lattice(4.050, 0.035, 3.25), "01_stent_sleeve_expanded")
    save(stent_lattice(2.125, 0.040, 3.25), "01b_stent_sleeve_2125_collapsed")

    save(cylinder(1.35 / 2, 14.0), "02_inner_mandrel")
    save(tube(1.82 / 2, 1.72 / 2, 5.0), "03_outer_sheath")
    save(tube(3.85 / 2, 3.85 / 2 - 0.06, 3.0), "04_expansion_bladder_expanded")
    save(merge(cylinder(3.95 / 2, 1.75), cone(3.90 / 2, 3.85 / 2, 0.35)), "05_seal_element_hnbr")
    save(wedge_profile(0.55, 1.4, 0.08), "06_backup_petal")
    save(wedge_profile(0.65, 0.85, 0.45), "07_slip_segment")
    save(
        merge(cylinder(1.30 / 2, 2.5), translate(cone(1.22 / 2, 1.14 / 2, 0.4), 0, 0, 2.5)),
        "08_setting_piston",
    )
    save(merge(cylinder(1.65 / 2, 2.0), translate(cylinder(1.375 / 2, 1.2), 0, 0, 2.0)), "09_top_sub_fishing_neck")
    save(
        merge(cylinder(1.65 / 2, 1.5), translate(cylinder(0.18, 0.35), 1.65 / 2 - 0.15, 0, 0.675)),
        "10_bottom_equalizing_sub",
    )
    save(cone(1.55 / 2, 1.05 / 2, 1.8), "11_retrieval_cone")
    save(tube(3.90 / 2, 3.90 / 2 - 0.25, 0.35), "12_centralizer_ring")

    # Assemblies
    run_in = merge(
        cylinder(1.35 / 2, 14.0),
        translate(stent_lattice(1.688, 0.035, 3.25), 0, 0, 4.5),
        translate(tube(1.82 / 2, 1.72 / 2, 5.0), 0, 0, 4.2),
        translate(merge(cylinder(1.65 / 2, 2.0), translate(cylinder(1.375 / 2, 1.2), 0, 0, 2.0)), 0, 0, 12.5),
        cylinder(1.65 / 2, 1.5),
    )
    save(run_in, "20_assembly_run_in")

    base = 2.0
    petals = merge(
        *[
            translate(rotate_z(wedge_profile(0.55, 1.4, 0.08), i * 45), 1.55, 0, base + 3.0)
            for i in range(8)
        ]
    )
    slips = merge(
        *[
            translate(rotate_z(wedge_profile(0.65, 0.85, 0.45), i * 60 + 30), 1.85, 0, base + 4.9)
            for i in range(6)
        ]
    )
    set_asm = merge(
        cylinder(1.65 / 2, 1.5),
        translate(cylinder(1.30 / 2, 2.5), 0, 0, 1.5),
        translate(stent_lattice(4.050, 0.035, 3.25), 0, 0, base),
        translate(tube(3.85 / 2, 3.85 / 2 - 0.06, 3.0), 0, 0, base + 0.15),
        translate(merge(cylinder(3.95 / 2, 1.75), cone(3.90 / 2, 3.85 / 2, 0.35)), 0, 0, base + 3.1),
        petals,
        slips,
        translate(tube(3.90 / 2, 3.90 / 2 - 0.25, 0.35), 0, 0, base + 4.6),
        translate(cone(1.55 / 2, 1.05 / 2, 1.8), 0, 0, base + 5.2),
        translate(merge(cylinder(1.65 / 2, 2.0), translate(cylinder(1.375 / 2, 1.2), 0, 0, 2.0)), 0, 0, base + 6.8),
    )
    save(set_asm, "21_assembly_set")

    alt = merge(
        cylinder(2.05 / 2, 1.5),
        translate(stent_lattice(2.125, 0.040, 3.25), 0, 0, 3.0),
        translate(merge(cylinder(2.05 / 2, 2.0), translate(cylinder(1.5 / 2, 1.2), 0, 0, 2.0)), 0, 0, 8.0),
    )
    save(alt, "22_assembly_variant_2125")

    return manifest


def _generate_with_cadquery() -> list[dict]:
    import cadquery as cq

    from cad.assembly import build_assembly_alt_2125, build_assembly_run_in, build_assembly_set
    from cad.parts import (
        backup_petal,
        bottom_equalizing_sub,
        centralizer_ring,
        expansion_bladder,
        inner_mandrel,
        outer_sheath,
        retrieval_cone,
        seal_element,
        setting_piston,
        slip_segment,
        top_sub,
    )
    from cad.stent_sleeve import StentParams, build_stent_sleeve
    from cad.units import in_to_mm

    manifest: list[dict] = []
    OUTPUT.mkdir(parents=True, exist_ok=True)

    def export_part(workplane: cq.Workplane, name: str) -> None:
        scaled = workplane.scale(in_to_mm(1.0))
        path = OUTPUT / f"{name}.stl"
        cq.exporters.export(scaled, str(path), exportType="STL", tolerance=0.05, angularTolerance=0.05)
        manifest.append({"file": path.name, "path": str(path), "units": "mm", "engine": "cadquery"})
        print(f"  ok {path.name}")

    print("Generating STLs (CadQuery engine)...")
    parts = [
        (inner_mandrel(), "02_inner_mandrel"),
        (outer_sheath(), "03_outer_sheath"),
        (expansion_bladder(), "04_expansion_bladder_expanded"),
        (seal_element(), "05_seal_element_hnbr"),
        (backup_petal(), "06_backup_petal"),
        (slip_segment(), "07_slip_segment"),
        (setting_piston(), "08_setting_piston"),
        (top_sub(), "09_top_sub_fishing_neck"),
        (bottom_equalizing_sub(), "10_bottom_equalizing_sub"),
        (retrieval_cone(), "11_retrieval_cone"),
        (centralizer_ring(), "12_centralizer_ring"),
        (build_stent_sleeve(StentParams(), "collapsed"), "01_stent_sleeve_collapsed"),
        (build_stent_sleeve(StentParams(), "expanded"), "01_stent_sleeve_expanded"),
        (build_stent_sleeve(StentParams(collapsed_od_in=2.125), "collapsed"), "01b_stent_sleeve_2125_collapsed"),
    ]
    for wp, name in parts:
        export_part(wp, name)
    for builder, name in [
        (build_assembly_run_in, "20_assembly_run_in"),
        (build_assembly_set, "21_assembly_set"),
        (build_assembly_alt_2125, "22_assembly_variant_2125"),
    ]:
        export_part(builder(), name)
    return manifest


def main() -> None:
    try:
        import cadquery  # noqa: F401
        manifest = _generate_with_cadquery()
    except ImportError:
        manifest = _generate_with_mesh_utils()

    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps({"parts": manifest, "count": len(manifest)}, indent=2))
    print(f"\nDone — {len(manifest)} STL files in {OUTPUT}")


if __name__ == "__main__":
    main()
