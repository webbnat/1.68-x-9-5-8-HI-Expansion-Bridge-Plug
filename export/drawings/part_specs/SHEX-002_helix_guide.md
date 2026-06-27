# SHEX-002 — Iris Helix Guide Insert — Shop Drawing Spec

**Drawing No:** DWG-002A-SHP  
**Part No:** SHEX-002  
**Qty:** 1 per plug  
**Material:** Inconel 718 (AMS 5662), solution + age per spec  
**Tier:** **MANUFACTURING** — fits inside **SHEX-010** bore (≤ **Ø1.560** OD)  
**STEP import:** None — model in Fusion  
**Module ref:** `SHEX-IRIS_STACK_INDEX.md`  
**Mates:** **SHEX-010** pocket **Z′ = 3.250 – 7.250**; **SHEX-001** followers; **SHEX-011** cams §12.5

---

## 1. Function

**Double-start helix** insert fixed in support sleeve. Converts mandrel **axial + rotation** (setting tool Phase 4) into **radial segment motion** via **SHEX-001** follower slots riding in helix grooves.

| Parameter | Value |
|-----------|-------|
| **Lead** | **4.0 in** per full rotation |
| **Starts** | **2** (180° apart) |
| **Active axial length** | **4.0 in** |
| **Mandrel stroke** | **4.0 in** + **~2 rev** |

---

## 2. Envelope (shop)

| Feature | Dimension (in) | Tolerance | Notes |
|---------|----------------|-----------|-------|
| **OD** | **1.555** | +0.000 / −0.002 | Press/slip in **SHEX-010** pocket **Ø1.558** |
| **ID** | **Ø1.552** | +0.003 / −0.000 | Clears **Ø1.550** mandrel |
| **Length** | **4.000** | ±0.005 | |
| **Wall (nominal)** | **0.0015** | — | Thin ring — helix cut in ID |

**Install position (part Z′):** bottom @ **Z′ = 3.250**, top @ **Z′ = 7.250** (module local).

---

## 3. Helix grooves (2-start)

Cut on **inner diameter** — segment followers travel here.

| Feature | Dimension (in) | Tolerance | Notes |
|---------|----------------|-----------|-------|
| **Form** | Double-start helix | — | |
| **Lead** | **4.000** | ±0.010 | Axial per **360°** |
| **Groove width** | **0.125** | ±0.005 | |
| **Groove depth** | **0.080** | ±0.003 | Into wall from ID |
| **Starts** | **2** @ **180°** | — | |
| **Pitch** *(double-start)* | **2.000** axial / rev | — | 4.0 lead ÷ 2 starts |
| **Total rotation span** | **720°** | — | Over **4.0 in** length |
| **Root fillet** | **R0.015** min | — | EDM |

### 3.1 Groove centreline (module Z′, start @ 3.250)

| Start **Z′** | End **Z′** | Rotation |
|--------------|------------|----------|
| **3.250** | **7.250** | **2 rev** total |

---

## 4. Segment follower interface

Each **SHEX-001** segment carries a tab into groove:

| Feature | Dimension (in) | Notes |
|---------|----------------|-------|
| Follower width | **0.125** | Matches groove |
| Follower length | **0.625** | Per **SHEX-001** §4 |
| Radial clearance | **0.005** per side | In groove |

---

## 5. Retention

| Feature | Spec |
|------|------|
| Method | Split ring / pin / epoxy pocket per **SHEX-010** §4 |
| Anti-rotation | Pin **Ø0.062** through sleeve + insert, **1 place** |

---

## 6. Required drawing views (DWG-002A-SHP)

| View | Scale | Content |
|------|-------|---------|
| A | **2:1** | Half-section — ring **4.0 L** |
| B | **2:1** | Developed helix unwrap (one start) — **lead 4.0** |
| C | **4:1** | Groove cross-section |
| D | **1:1** | End view — **2 starts @ 180°** |

---

## 7. Dimension checklist

- [ ] OD **1.555**, ID **Ø1.552**, length **4.000**
- [ ] Helix lead **4.000**, **2-start**
- [ ] Groove **0.125 × 0.080**
- [ ] Install **Z′ = 3.250 – 7.250** *(reference dim on assy)*
- [ ] Material **Inconel 718**
- [ ] Part number **SHEX-002**

---

## 8. General notes

```
1. UNLESS OTHERWISE SPECIFIED, DIMENSIONS ARE IN INCHES.
2. MATERIAL: INCONEL 718 — AMS 5662.
3. MANUFACTURE: EDM OR 5-AXIS PREFERRED FOR HELIX GROOVES.
4. LEAD 4.000 IN VERIFIED WITH MANDREL CAMS (SHEX-011 §12.5).
5. FUNCTIONAL TEST IN SHEX-010 POCKET WITH 1× SHEX-001 + MANDREL.
6. NOT FOR SET OD 5.750 / 8.650 — RUN-IN MODULE ONLY.
```

---

## 9. Fusion workflow

1. Design **`05_SHEX-002_helix_guide`**.
2. Create base ring: **OD 1.555 × ID 1.552 × L 4.0**.
3. **Helix groove** toolpath or Coil path: **2 starts**, pitch **2.0 in/rev**, length **4.0**.
4. Validate with **SHEX-011** mandrel cams @ plug **Z = 19 – 23**.
5. Drawing **DWG-002A-SHP** → `shop_pdf/`.

**Reference schematic:** `dxf/DWG-002_iris_module_assy.dxf` VIEW 3.

---

*Rev A — helix insert for run-in iris module.*
