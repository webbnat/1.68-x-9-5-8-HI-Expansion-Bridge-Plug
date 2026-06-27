# Full 3D CAD Package — SHEX-BP-UHEX-54

Manufacturing-oriented **B-rep STEP** solids (Gmsh OpenCASCADE kernel).  
Units: **millimetres**. Z = 0 at tool bottom (mandrel tail).

## Assembly models (`step/`)

| File | Description |
|------|-------------|
| `plug_set_assembly.stp` | 54" bridge plug — **SET** condition (expanded) |
| `plug_run_in_assembly.stp` | 54" bridge plug — **RUN-IN** (collapsed 1.688" OD) |
| `setting_tool_SHEX-ST-54.stp` | Setting tool — 246" (20.5 ft) module stack |

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
.venv\Scripts\python generate_cad.py
```
