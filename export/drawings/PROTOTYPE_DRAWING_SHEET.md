# SHEX-BP-UHEX-54 — Detailed Prototype Drawing Sheet

**Drawing No:** DWG-006 (companion document)  
**Revision:** A  
**Scale:** Views as noted | Units: inches unless stated

---

## 1. Tool summary

| Parameter | Value |
|-----------|-------|
| Part name | SHEX-BP-UHEX-54 High-Expansion Retrievable Bridge Plug |
| Total length | **54.0 in** (1371.6 mm) |
| Run-in OD (max) | **1.688 in** (42.88 mm) |
| Set OD (max) | **8.650 in** (219.7 mm) |
| Target casing | **9-5/8 in 40#** (drift ID **8.679 in**) |
| Expansion ratio | **5.14x** diameter |
| Target dP | 3000–5000 psi |

---

## 2. Assembly elevation — SET condition (bottom to top)

```
  TOP
  +------------------------------------------------------------------+
  | 13 | FISHING NECK / TOP SUB          L=3.00   OD=1.375          |
  +------------------------------------------------------------------+
  | 12 | UPPER SLIP ASSEMBLY (8 seg)       L=4.50   OD=8.72  ID=1.55 |
  +------------------------------------------------------------------+
  | 11 | UPPER MTM RING STACK (3 rings)    L=2.50   OD=8.80          |
  +------------------------------------------------------------------+
  | 10 | SEAL LAND 4 + 16 PETALS           L=4.50   OD=8.72  HNBR    |
  |  9 | SEAL LAND 3 + 16 PETALS           L=4.50   OD=8.72          |
  |  8 | SEAL LAND 2 + 16 PETALS           L=4.50   OD=8.72          |
  |  7 | SEAL LAND 1 + 16 PETALS           L=4.50   OD=8.72          |
  +------------------------------------------------------------------+
  |  6 | STAGE 3 IRIS MODULE               L=7.50   OD=8.65  ID=5.75 |
  |      | 16 segments t=0.187, helix actuation 4.0 in stroke        |
  +------------------------------------------------------------------+
  |  5 | STAGE 2 MIDDLE STENT + WEDGE       L=5.00   OD=5.75  ID=3.38 |
  |      | Belleville internal actuator, 5.0 in travel               |
  +------------------------------------------------------------------+
  |  4 | STAGE 1 INNER STENT + BLADDER      L=4.00   OD=3.38  ID=1.45 |
  |      | Bladder internal actuator, 5.0 in travel                   |
  +------------------------------------------------------------------+
  |  3 | LOWER SLIP ASSEMBLY (8 seg)        L=4.50   OD=8.72          |
  +------------------------------------------------------------------+
  |  2 | BOTTOM EQUALIZING SUB              L=2.00   OD=1.688        |
  +------------------------------------------------------------------+
  |  1 | SETTING MANDREL TAIL               L=3.00   OD=1.350        |
  BOTTOM
  +------------------------------------------------------------------+
  TOTAL LENGTH = 54.00 in
```

---

## 3. Run-in elevation (collapsed)

All expansion modules collapsed on mandrel. Protective sheath optional (OD 1.82 in max).

| Zone | Length (in) | OD (in) |
|------|-------------|---------|
| Fishing neck | 3.00 | 1.375 |
| Collapsed body (stent cascade + seal pack) | 48.00 | **1.688** |
| Mandrel tail | 3.00 | 1.350 |
| **Total** | **54.00** | **1.688 max** |

---

## 4. Section views

### Section A-A — Seal module (through seal land 2)

- HNBR cup: OD 8.72 in, ID 1.55 in, axial 4.5 in per land
- 16 petal backups per land, 17-4 PH, 0.55 x 1.4 in
- MTM ring groove at OD 8.80 in

### Section B-B — Stage 3 iris (through iris module center)

- 16 segments @ 22.5 deg, t=0.187 in
- Collapsed ID 5.75 in → deployed OD 8.65 in
- Inconel 718 double-start helix guide, 4.0 in lead
- Root fillet R0.030 in min

### Section C-C — Expansion cascade (through Stage 1+2)

- Inner mandrel bore 1.35 in OD
- Stage 1 bladder in annulus 1.45–3.38 in
- Stage 2 Belleville stack in annulus 3.38–5.75 in

---

## 5. Setting tool interface (companion assembly)

| Parameter | SHEX-ST-54 |
|-----------|------------|
| Length | 20.5 ft (246 in) |
| OD | 3.625 in |
| Stroke | 12.0 in |
| Force | 55 klbf max |
| Bottom conn | 1.375 in AMMT → Item 13 fishing neck |

Combined run string: **26.5 ft** (see DWG-004)

---

## 6. Files for prototype build

| Type | Path |
|------|------|
| **Setting sequence guide** | `docs/SETTING_SEQUENCE.md` |
| **Setting tool detail guide** | `docs/SETTING_TOOL_DETAIL.md` |
| **Fusion shop drawing workflow** | `docs/FUSION_SHOP_DRAWINGS.md` |
| **Drawing register (status)** | `export/drawings/DRAWING_REGISTER.csv` |
| **Setting tool BOM (COTS)** | `export/drawings/ST-BOM-001.csv` |
| **Setting tool module drawings** | `export/drawings/dxf/setting_tool/ST-DWG-001 … ST-DWG-010` |
| **Setting tool module STEP** | `export/cad/parts/setting_tool/` |
| **Detailed 2D drawing** | `export/drawings/dxf/DWG-006_prototype_whole_tool_detailed.dxf` |
| **3D assembly STL** | `output/stl/shex_54/40_plug_uhex_54in_assembly.stl` |
| **Combined string STL** | `output/stl/shex_54/42_combined_string_lube_check.stl` |
| **Part STLs** | `output/stl/` and `output/stl/uhex_9625/` |
| **BOM** | `export/drawings/BOM-001.csv` |

---

## 7. Prototype build sequence

1. Machine mandrel, subs, helix guide (SHEX-002, 011–013)
2. Laser-cut stent sleeves Stages 1–3 (SHEX-008–010)
3. EDM iris segments x16 (SHEX-001, DWG-001)
4. Mold HNBR seal lands x4 (SHEX-004)
5. Assemble cascade on mandrel; function-test expansion Stages 1→2→3
6. Install seal module + slips; latch to SHEX-ST-54 setting tool
7. Set in 9-5/8 in test fixture; pressure test to 3000 psi

---

*For CAD: open DWG-006 in AutoCAD/Fusion. For 3D review: import `40_plug_uhex_54in_assembly_set.stl` (set) or `40_plug_uhex_54in_assembly_run_in.stl` (run-in). Open `export/viewer/index.html` in a browser for interactive review.*
