# Machine Drawing Package - SHEX-BP-UHEX-54

## Two tiers (read first)

| Tier | Suffix | Folder | Who uses it |
|------|--------|--------|-------------|
| **Manufacturing** | **`-SHP`** | `shop_pdf/` | Machine shop — run-in parts, **OD ≤ 1.688 in** |
| **Set illustration** | **`-SET`** | `set_viz_pdf/` | Assembly / QA / field — expanded plug visualization |

Full rules: **`docs/FUSION_SHOP_DRAWINGS.md`** § Two-tier drawing system.

## Shop drawing workflow (Fusion 360)

**Start here:** `docs/FUSION_SHOP_DRAWINGS.md`  
**Progress tracker:** `export/drawings/DRAWING_REGISTER.csv`  
**Per-part specs:** `export/drawings/part_specs/`  
**Iris stack (current focus):** `export/drawings/part_specs/SHEX-IRIS_STACK_INDEX.md`

Schematic DXFs in `dxf/` are **legacy layout references** — not manufacturing or set releases.

## Drawing list (schematic — pre-Fusion, reference only)

| DWG NO | File | Description | Becomes |
|--------|------|-------------|---------|
| DWG-001 | `dxf/DWG-001_iris_segment.dxf` | Iris segment layout | **DWG-001-SHP** (mfg) |
| DWG-002 | `dxf/DWG-002_iris_module_assy.dxf` | Iris module layout | **DWG-002-SET** (set viz) |
| DWG-003 | `dxf/DWG-003_plug_54in_GA.dxf` | Plug GA | **DWG-003-SET** |
| DWG-004 | `dxf/DWG-004_setting_tool_SHEX-ST-54.dxf` | Setting tool GA | **DWG-004-SET** |
| DWG-005 | `dxf/DWG-005_mtm_ring_segment.dxf` | MTM segment layout | **DWG-005-SHP** |
| DWG-007 | `dxf/DWG-007_seal_land_module.dxf` | Seal land layout | **DWG-007A/B-SHP** |
| DWG-008 | `dxf/DWG-008_slip_segment.dxf` | Slip segment layout | **DWG-008A/B-SHP** |
| DWG-009 | `dxf/DWG-009_stage1_stent_sleeve.dxf` | Stage 1 stent | **DWG-009-SHP** |
| DWG-010 | `dxf/DWG-010_fishing_neck.dxf` | Fishing neck | **DWG-010-SHP** |
| DWG-011 | `dxf/DWG-011_stage2_stent_sleeve.dxf` | Stage 2 stent | **DWG-011-SHP** |
| DWG-012 | `dxf/DWG-012_stage3_iris_support_sleeve.dxf` | Iris sleeve layout | **DWG-012-SHP** *(run-in OD)* |
| **DWG-006** | **`dxf/DWG-006_prototype_whole_tool_detailed.dxf`** | Run-in + set sections | **DWG-006-SET** || **PROTOTYPE** | **`PROTOTYPE_DRAWING_SHEET.md`** | **Readable prototype spec with all dimensions** |
| BOM-001 | `BOM-001.csv` | Bill of materials |

## How to open

- **AutoCAD / BricsCAD / DraftSight:** Open `.dxf` files directly
- **Fusion 360:** Upload DXF to sketch plane
- **SolidWorks:** File > Open > DXF/DWG

## Tolerances (unless noted)

| Feature | Tolerance |
|---------|-----------|
| Machined bore | +/- 0.001 in |
| Segment thickness | +/- 0.001 in |
| Root fillet | R0.030 in min |
| Angular (segment pitch) | +/- 0.5 deg |
| Seal land OD | +0.010 / -0.000 in |

## Related FEA package

See `export/ansys/README_ANSYS_IMPORT.md` for STEP solids and mesh import.
