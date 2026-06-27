"""Generate full 3D CAD (STEP) for plug and setting tool."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from cad.solid_cad import (
    build_plug_run_in_model,
    build_plug_set_model,
    build_setting_tool_model,
    export_assembly_step,
    export_key_part_steps,
)

OUT = ROOT / "export" / "cad"
STEP = OUT / "step"
PARTS = OUT / "parts"


def _write_readme(manifest: dict) -> None:
    text = f"""# Full 3D CAD Package — SHEX-BP-UHEX-54

Manufacturing-oriented **B-rep STEP** solids (Gmsh OpenCASCADE kernel).  
Units: **millimetres**. Z = 0 at tool bottom (mandrel tail).

## Assembly models (`step/`)

| File | Description |
|------|-------------|
| `plug_set_assembly.stp` | 54\" bridge plug — **SET** condition (expanded) |
| `plug_run_in_assembly.stp` | 54\" bridge plug — **RUN-IN** (collapsed 1.688\" OD) |
| `setting_tool_SHEX-ST-54.stp` | Setting tool — 246\" (20.5 ft) module stack |

Open in **Fusion 360**, **SolidWorks**, **FreeCAD**, or **Onshape** via File → Import → STEP.

Each assembly is a **multi-body** STEP — one solid per BOM item.

## Key individual parts (`parts/`)

| File | Description |
|------|-------------|
| `SHEX-011_inner_mandrel.stp` | Full-length inner mandrel |
| `SHEX-001_iris_segment.stp` | Single iris segment (t=0.187 in) |
| `SHEX-001_iris_ring_16seg.stp` | Full 16-segment iris ring |
| `SHEX-008_stage1.stp` / `SHEX-009_stage2.stp` / `SHEX-010_stage3_support.stp` | Expansion stage sleeves |

## Coordinate system

- **+Z** = uphole (toward fishing neck)
- **Origin** = bottom centreline of mandrel tail

## Regenerate

```powershell
.venv\\Scripts\\python generate_cad.py
```
"""
    (OUT / "README.md").write_text(text, encoding="utf-8")
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    STEP.mkdir(parents=True, exist_ok=True)
    manifest: dict = {"assemblies": [], "parts": []}

    assemblies = [
        (build_plug_set_model, STEP / "plug_set_assembly.stp"),
        (build_plug_run_in_model, STEP / "plug_run_in_assembly.stp"),
        (build_setting_tool_model, STEP / "setting_tool_SHEX-ST-54.stp"),
    ]

    for build_fn, path in assemblies:
        print(f"Building {path.name}...")
        parts = export_assembly_step(build_fn, path.stem, path)
        manifest["assemblies"].append({
            "file": str(path),
            "bodies": len(parts),
            "names": [p.name for p in parts],
        })
        print(f"  ok {path.name} ({len(parts)} bodies)")

    print("Exporting key individual parts...")
    part_files = export_key_part_steps(PARTS)
    manifest["parts"] = part_files
    print(f"  ok {len(part_files)} part files")

    manifest["plug_length_in"] = 54.0
    manifest["setting_tool_length_in"] = 246.0
    _write_readme(manifest)
    print(f"\nDone — CAD package in {OUT}")


if __name__ == "__main__":
    main()
