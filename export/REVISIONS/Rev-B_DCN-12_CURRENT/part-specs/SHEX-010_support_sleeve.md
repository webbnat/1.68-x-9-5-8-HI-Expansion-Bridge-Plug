# SHEX-010 — Stage 3 Iris Support Sleeve — Shop Drawing Spec

**Drawing No:** DWG-012-SHP  
**Part No:** SHEX-010  
**Qty:** 1 per plug  
**Material:** 17-4 PH H900 (H1150M)  
**Tier:** **MANUFACTURING** — **OD 1.688 in max**  
**STEP import:** `export/cad/parts/SHEX-010_stage3_support.stp` *(ignore — OD 5.750 is set-reference only)*  
**Module ref:** `SHEX-IRIS_STACK_INDEX.md`  
**Set viz:** Deployed context in **DWG-002-SET** only

---

## 1. Function

Fixed **support sleeve** for Stage 3 iris module. Does **not** expand. Provides:

- **Run-in outer envelope** **Ø1.688** (plug body OD)
- **Bore** for **Ø1.550** mandrel clearance
- **16 guide slots** for **SHEX-001** segments
- **Helix insert pocket** for **SHEX-002**

**Plug location:** **Z = 18.500 – 26.000 in** (length **7.500 in**).  
**Part coordinates:** **Z′ = 0** at **bottom face** (= plug **Z = 18.500**).

---

## 2. Authoritative dimensions (shop)

| Feature | Dimension (in) | Tolerance | Notes |
|---------|----------------|-----------|-------|
| **OD** | **1.688** | +0.000 / −0.005 | Run-in plug OD |
| **Length** | **7.500** | ±0.010 | |
| **ID (mandrel bore)** | **Ø1.562** | +0.003 / −0.000 | **Ø1.550** mandrel + clearance |
| **Wall (nominal)** | **0.063** | — | (1.688 − 1.562) / 2 |
| **Bottom face** | Flat | **Ra 32 µin** | Mates Stage 2 module top |
| **Top face** | Flat | **Ra 32 µin** | Lock land / seal module below |

---

## 3. Segment guide slots (16×)

Radial **internal** slots on bore for **SHEX-001** segment toes. All within **Ø1.688** OD.

| Feature | Dimension (in) | Tolerance | Notes |
|---------|----------------|-----------|-------|
| Count | **16** | — | |
| Angular pitch | **22.5°** | ±0.5° | Datum: slot **#1** @ **0°** |
| Slot centre **Z′** | **2.375** | ±0.010 | Aligns segment centre (plug **Z = 20.875**) |
| Slot length (axial) | **2.750** | ±0.010 | Matches segment length |
| Slot width (circ.) | **0.120** | ±0.005 | At **Ø1.562** bore |
| Slot depth (radial) | **0.055** | +0.005 / −0.000 | From bore into wall |

---

## 4. Helix guide pocket (SHEX-002)

| Feature | Dimension (in) | Notes |
|---------|----------------|-------|
| Pocket **Z′** span | **3.250 – 7.250** | **4.000 in** axial |
| Pocket ID | **Ø1.558** | **SHEX-002** insert OD + clearance |
| Pocket depth | **0.040** min | Axial groove or counterbore for insert retention |
| Retaining ring groove | **0.030 × 0.040** | At **Z′ = 7.200** *(or pin)* |

*Detail mate: `SHEX-002_helix_guide.md`.*

---

## 5. Bottom coupling (Stage 2 mate)

| Feature | Dimension (in) | Notes |
|---------|----------------|-------|
| Pilot length **Z′** | **0.000 – 0.750** | Overlap with Stage 2 stent top |
| Pilot OD | **1.688** | Same as body |
| Pilot ID | **Ø1.562** | Continuous bore |

---

## 6. Top lock land

| Feature | Dimension (in) | Notes |
|---------|----------------|-------|
| **Z′** span | **7.250 – 7.500** | **0.250 in** |
| ID step *(optional)* | **Ø1.540** | Captures segment tops / retainer |

---

## 7. Required drawing views (DWG-012-SHP)

| View | Scale | Content |
|------|-------|---------|
| A | **1:2** | Half-section — full **7.5 L**, bore, slots |
| B | **1:1** | End view @ **Z′ = 2.375** — **16 slots @ 22.5°** |
| C | **2:1** | Slot detail |
| D | **2:1** | Helix pocket @ **Z′ = 5.25** |
| E | **2:1** | Top lock land |

---

## 8. Dimension checklist

- [ ] OD **1.688**, length **7.500**
- [ ] Bore **Ø1.562**
- [ ] **16×** guide slots @ **22.5°**, **Z′ = 2.375**
- [ ] Helix pocket **Z′ = 3.250 – 7.250**
- [ ] Bottom / top faces flat, **Ra 32 µin**
- [ ] Part number **SHEX-010**

---

## 9. General notes

```
1. UNLESS OTHERWISE SPECIFIED, DIMENSIONS ARE IN INCHES.
2. MATERIAL: 17-4 PH H900, HEAT TREAT H1150M.
3. MANUFACTURING — RUN-IN OD 1.688 MAX. NOT Ø5.750.
4. FIXED SLEEVE — DOES NOT EXPAND WITH IRIS.
5. DEBURR SLOTS; NO BURRS IN HELIX POCKET.
6. PLUG Z: 18.500 – 26.000 IN (ITEM 6).
7. MATE SHEX-002 INSERT + 16× SHEX-001 IN MODULE ASSY.
```

---

## 10. Fusion workflow

1. Design **`07_SHEX-010_support_sleeve`** — **do not import** 5.750 STEP as finished part.
2. Revolve **Ø1.688 × 7.5 L**, bore **Ø1.562**.
3. Cut **16 slots** per §3 (sketch on plane @ **Z′ = 2.375** or wrap).
4. Cut **helix pocket** per §4.
5. Drawing **DWG-012-SHP** → `shop_pdf/`.
6. Insert into **`08_iris_run_in_assy`** with mandrel + one segment for slot fit.

---

*Rev A — manufacturing sleeve @ OD 1.688 for iris stack.*
