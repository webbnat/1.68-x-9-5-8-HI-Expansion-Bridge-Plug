# SHEX-005 — Seal Land Petal Backup — Shop Drawing Spec

**Drawing No:** DWG-007A-SHP  
**Part No:** SHEX-005  
**Qty:** **64** per plug (**16** per seal land × **4** lands)  
**Material:** 17-4 PH H900 (H1150M)  
**Tier:** **MANUFACTURING** — **profile / EDM part** *(not a turned OD)*  
**Module ref:** Items **7–10** (seal lands) | Schematic: `dxf/DWG-007_seal_land_module.dxf`

---

## 1. Function

Radial **anti-extrusion rib** behind **SHEX-004** HNBR cup in each seal land module. Prevents elastomer extrusion under differential pressure; reacts on **SHEX-011** seal-set ramp (§12.6).

| Parameter | Value |
|-----------|-------|
| Per land | **16** @ **22.5°** |
| Seal lands per plug | **4** |
| Set seal land OD | **Ø8.720 in** |
| Mandrel clearance | **Ø1.550 in** |

**Assembly note:** Petals nested in seal carrier at module build. Module **OD 1.688** at run-in (**nested in cascade** — not a radial crush of deployed backup). Shop EDM profile shows **deployed backup** (same tier rule as **SHEX-001**). See **SHEX-004 Rev B** — thin HNBR liner, not full **Ø8.720** mold at run-in.

---

## 2. Profile geometry (authoritative)

Arc-sector rib in **radial plane**, extruded **axially** (plug **Z**).

| Feature | Dimension (in) | Tolerance | Notes |
|---------|----------------|-----------|-------|
| **Angular span** | **22.5°** | ±0.5° | **16** per land |
| **Inner radius R1** | **0.895** | ±0.005 | = **Ø1.550/2 + 0.120** |
| **Outer radius R2** | **4.011** | ±0.005 | = **Ø8.720/2 × 0.92** |
| **Radial width** | **3.116** | — | R2 − R1 |
| **Axial length L** | **0.550** | ±0.010 | Active backup length in land |
| **Plate note** | **0.55 × 1.4** | — | Legacy schematic label — radial extent governs via R1/R2 |

### 2.1 Arc endpoints (datum = petal bisector @ 0°)

| Point | Radius (in) | Angle from bisector |
|-------|-------------|---------------------|
| Inner toe | **0.895** | **±11.25°** |
| Outer toe | **4.011** | **±11.25°** |

### 2.2 Edge treatments

| Feature | Dimension (in) | Notes |
|---------|----------------|-------|
| Root fillet (inner) | **R0.015** min | |
| Outer toe chamfer | **0.015 × 45°** | Both faces |
| Side edges | Break **0.010** max | |

---

## 3. Position in seal land (module context)

| Feature | Value | Notes |
|---------|-------|-------|
| Seal land axial length | **4.500** | Per land (items 7–10) |
| Petal centre **Z** *(typ)* | Mid-land | **~2.25 in** from land bottom |
| Plug **Z** land 1 bottom | **26.000** | After iris module |

*Detail mate: **SHEX-004** HNBR cup OD **8.720**; **SHEX-011** §12.6 seal ramps.*

---

## 4. Required drawing views (DWG-007A-SHP)

| View | Scale | Content |
|------|-------|---------|
| A | **1:2** | **Radial end** — arc **22.5°**, R1/R2 |
| B | **1:2** | **Axial section** — **L 0.550** |
| C | **3:1** | Root fillet + toe chamfer |
| D | **1:1** | **Plate nest** — 16 petals per sheet *(optional)* |

---

## 5. Dimension checklist

- [ ] Span **22.5°**
- [ ] **R1 = 0.895**, **R2 = 4.011**
- [ ] **L = 0.550**
- [ ] Root **R0.015** min
- [ ] Qty **16** per seal land on drawing
- [ ] Part number **SHEX-005**

---

## 6. General notes

```
1. UNLESS OTHERWISE SPECIFIED, DIMENSIONS ARE IN INCHES.
2. MATERIAL: 17-4 PH H900, HEAT TREAT H1150M.
3. QTY: 16 PER SEAL LAND × 4 LANDS = 64 PER PLUG.
4. MANUFACTURE: WIRE EDM OR CNC FROM PLATE — NOT TURNED OD.
5. FINISH: PASSIVATE PER SPEC; BREAK SHARP EDGES 0.010 MAX.
6. DEPLOYED BACKUP RADII SHOWN — SEAL PACK CRIMPED TO 1.688 OD AT ASSY.
7. MATES SHEX-004 HNBR (DWG-007B-SHP) — PETAL BEHIND ELASTOMER.
```

---

## 7. Fusion workflow

1. Design **`09_SHEX-005_petal_backup`** — **one petal** only.
2. Sketch **22.5°** arc sector **R1/R2** → extrude **0.550**.
3. Root fillet §2.2.
4. Drawing **DWG-007A-SHP** → `shop_pdf/`.
5. Pattern **×16 @ 22.5°** per seal land in module assy (later).

**Script:** `fusion/scripts/build_SHEX_005_petal_backup/`

---

## 8. Seal land module assy

1. **File → New Design**
2. Run **`build_seal_land_assy`** — builds **16× petals** + HNBR cup envelope for **one** land (**L 4.5**).
3. Save as **`10_seal_land_module_assy`**.
4. Repeat or pattern ×4 for full seal stack in plug GA.

**Script:** `fusion/scripts/build_seal_land_assy/`

---

## 9. Run-in / unset nest (assy viz)

Shop drawing §2 shows **deployed backup** radii. At run-in the **module OD is 1.688″** (nested in the expansion cascade). Petals **nest in the carrier bore**; outer toe may sit in **carrier wall** (same tier as iris segments in **SHEX-010** slots):

| Feature | Run-in nest (in) | Deployed backup (in) |
|---------|------------------|----------------------|
| Inner radius R1 | **0.778** | **0.895** |
| Outer radius R2 | **0.816** | **4.011** |
| Angular span | **22.5°** | **22.5°** |
| Axial L | **0.550** | **0.550** |

*R2 **0.816** = **Ø1.562/2 + 0.035** into carrier wall (0.063″ wall to **Ø1.688** OD).*

**HNBR (**SHEX-004**):** thin **0.050″** liner in wall — not full seal cup at run-in.

**Fusion:** `build_seal_run_in_assy` — nested **4× lands**. SET illustration: `build_seal_stack_assy`.

---

*Rev A — petal backup EDM profile for manufacturing.*
