# SHEX-001 — Stage 3 Iris Segment — Shop Drawing Spec

**Drawing No:** DWG-001-SHP  
**Part No:** SHEX-001  
**Qty:** **16** per plug  
**Material:** 17-4 PH H900 (H1150M)  
**Tier:** **MANUFACTURING** — **profile / EDM part** *(not a turned OD)*  
**STEP import:** `export/cad/parts/SHEX-001_iris_segment.stp` *(rough envelope — refine profile)*  
**Module ref:** `SHEX-IRIS_STACK_INDEX.md`

---

## 1. Function

One of **16** radial segments. At setting, slides on **SHEX-002** helix from collapsed nest to **deployed** arc contacting **9-5/8" 40#** casing (**8.679 in** drift).

| Parameter | Value |
|-----------|-------|
| Angular span | **22.5°** |
| Deployed outer arc | **R 4.318 in** *(Ø8.650)* |
| Collapsed inner arc | **R 2.955 in** *(nest in module)* |
| Radial travel | **1.363 in** |

**Assembly note:** Segments are **nested in SHEX-010** at module build; module **crimped to OD 1.688** for run-in — same as stent sleeves. Shop drawing dimensions **finished segment** (deployed geometry).

---

## 2. Profile geometry (authoritative)

Arc segment in **radial plane**, extruded **axially** (plug **Z**).

| Feature | Dimension (in) | Tolerance | Notes |
|---------|----------------|-----------|-------|
| **Angular span** | **22.5°** | ±0.5° | |
| **Inner radius R1** | **2.955** | ±0.005 | = **5.750/2 + 0.080** |
| **Outer radius R2** | **4.318** | ±0.005 | = **8.650/2 − 0.015** |
| **Radial width** | **1.363** | — | R2 − R1 |
| **Axial length L** | **2.750** | ±0.010 | |
| **Thickness t** | **0.187** | ±0.005 | Production; **0.125** marginal @ 5000 psi FEA |

### 2.1 Arc endpoints (datum = segment bisector @ 0°)

| Point | Radius (in) | Angle from bisector |
|-------|-------------|---------------------|
| Inner toe | **2.955** | **±11.25°** |
| Outer toe | **4.318** | **±11.25°** |

### 2.2 Edge treatments

| Feature | Dimension (in) | Notes |
|---------|----------------|-------|
| Root fillet (inner) | **R0.030** min | |
| Outer toe chamfer | **0.025 × 45°** | Both faces |
| Side edges | Break **0.010** max | |

---

## 3. Helix follower tab

Engages **SHEX-002** groove on **inner/center side** of segment.

| Feature | Dimension (in) | Tolerance | Notes |
|---------|----------------|-----------|-------|
| Tab length (axial) | **0.625** | ±0.005 | |
| Tab width | **0.125** | ±0.003 | Matches helix groove |
| Tab height (radial) | **0.080** | ±0.003 | |
| Tab location | **Mid-length** on segment | — | **Z** centre of **2.750 L** |
| Tab angular position | **Bisector plane** | — | Points toward mandrel |

---

## 4. Guide toe (SHEX-010 slot)

| Feature | Dimension (in) | Notes |
|---------|----------------|-------|
| Toe radius | **R2.955** | Rides in sleeve slot §3 |
| Toe width (circ.) | **0.110** | Clearance in **0.120** slot |

---

## 5. Required drawing views (DWG-001-SHP)

| View | Scale | Content |
|------|-------|---------|
| A | **1:2** | **Radial end** — arc **22.5°**, R1/R2 |
| B | **1:2** | **Axial section** — **L 2.750 × t 0.187** |
| C | **3:1** | Root fillet + toe chamfer |
| D | **2:1** | Helix follower tab |
| E | **1:1** | **Plate nest layout** — **16 segments** per sheet *(optional)* |

---

## 6. Dimension checklist

- [ ] Span **22.5°**
- [ ] **R1 = 2.955**, **R2 = 4.318**
- [ ] **L = 2.750**, **t = 0.187**
- [ ] Root **R0.030** min
- [ ] Follower tab **0.625 × 0.125 × 0.080**
- [ ] Qty **16** per module on drawing
- [ ] Part number **SHEX-001**

---

## 7. General notes

```
1. UNLESS OTHERWISE SPECIFIED, DIMENSIONS ARE IN INCHES.
2. MATERIAL: 17-4 PH H900, HEAT TREAT H1150M.
3. QTY: 16 PER IRIS MODULE (ITEM 6).
4. MANUFACTURE: WIRE EDM OR CNC FROM PLATE — NOT TURNED OD.
5. FINISH: ELECTROPOLISH ALL EXPOSED FACES.
6. BREAK SHARP EDGES 0.010 MAX EXCEPT NOTED CHAMFERS.
7. ANGULARITY ±0.5° TO TAB DATUM.
8. DEPLOYED ARC RADII SHOWN — MODULE CRIMPED TO 1.688 OD AT ASSY.
9. VERIFY RADIAL TRAVEL 1.363 IN IN DWG-002-SET ASSY CHECK.
```

---

## 8. Fusion workflow

1. Design **`06_SHEX-001_iris_segment`** — one segment only.
2. Sketch arc **22.5°** between **R1/R2** → extrude **2.750**.
3. Add **follower tab** §3; fillets §2.2.
4. Drawing **DWG-001-SHP** → `shop_pdf/`.
5. In **`08_iris_run_in_assy`**: pattern **×16** @ **22.5°**, centre **Z = 20.875**.

**Reference schematic:** `dxf/DWG-001_iris_segment.dxf`

---

## 9. Inspection

| Check | Method |
|-------|--------|
| R1, R2 | CMM or profile gauge |
| Thickness **0.187** | Micrometer |
| Span **22.5°** | CMM / fixture |
| Tab **0.125** width | Pin gauge |

---

*Rev A — iris segment EDM profile for manufacturing.*
