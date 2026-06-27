# SHEX-012 — Fishing Neck / Top Sub — Shop Drawing Spec

**Drawing No:** DWG-010-SHP  
**Part No:** SHEX-012  
**Qty:** 1  
**Material:** 4140 HT (AMS 6415), 28–32 HRC  
**STEP import:** `export/cad/parts/SHEX-012_fishing_neck.stp` *(envelope only — remake in Fusion per this spec)*  
**Schematic ref:** `export/drawings/dxf/DWG-010_fishing_neck.dxf` *(layout reference — superseded by Rev D dims)*  
**Mate mandrel:** `SHEX-011_inner_mandrel.md` §3 **Rev D**

---

## 1. Function

Top connector on the plug. **1 in AMT** top connection (pin section + external thread) mates with setting-tool crossover. **Bottom** threads onto **SHEX-011** mandrel (**1½-12 UNF**) with **Parker 2-216** face seal. Locates on upper slip ring at **Z = 51.0 in** (no direct fastener to slips). See **§5**.

**Plug length note:** This neck is **6.000 in** (was 3.000 in) — **overall plug assembly = 57.0 in** unless another module is shortened.

---

## 2. Authoritative dimensions

Coordinate: **Z = 0 at bottom face** (mandrel end), **Z+ uphole**.

| Feature | Value | Tolerance | Notes |
|---------|-------|-----------|-------|
| **Overall length** | **6.000 in** | ±0.010 | — |
| **Main body OD** | **1.688 in** | ±0.005 | Middle section |
| **Main body length** | **3.000 in** | — | Z = 1.500 – 4.500 (derived: 6 − 1.5 − 1.5) |
| **Pin section (A) OD** | **1.375 in** | ±0.005 | Top section |
| **Pin section (A) length** | **1.500 in** | ±0.005 | Z = 4.500 – 6.000 |
| **Through bore (G)** | **Ø0.750 in** | +0.002 / −0.000 | Full length where bored |
| **Top chamfer** | **0.030 × 45°** | — | AMT / external thread lead |
| **External thread (top)** | **1 3/8-8 UN-2A × 1.125 in** | Class 2A | On pin section; major Ø1.375 |
| **Top connection** | **1 in AMT** | — | Per API 11BR / shop AMT gauge |
| **Bottom chamfer** | **0.040 × 45°** | — | Bore / counterbore entry |
| **Seal counterbore** | **Ø1.530 in × 0.500 in deep** | +0.005 / −0.000 | From bottom face |
| **Internal thread (bottom)** | **1½-12 UNF-2B × 1.000 in** | Class 2B | (= 1.500-12 UNF) |
| **Total bottom zone** | **1.500 in** | — | Z = 0 – 1.500 (counterbore + thread + seal face) |
| **Bottom seal face** | Flat | 0.001 FIM | Ra 32 µin max; compresses O-ring |
| **Anti-rotation pin** | **Ø0.125 in**, 1 place | — | Assembly drill @ **Z = 51.500** plug assy |

### 2.1 Axial stack (this part)

```
  Z (in)    Section
  ───────   ─────────────────────────────────────
  6.000     ┌─ Top — 1" AMT / 1 3/8-8 UN-2A (1.125 L)
  4.500     ├─ Pin section (A)  Ø1.375 × 1.500
            │     Through bore Ø0.750
  4.500     ├─ Main body  Ø1.688 × 3.000
  1.500     │
  1.500     ├─ Bottom zone  (total 1.500)
            │     Counterbore Ø1.530 × 0.500
            │     1½-12 UNF-2B × 1.000
  0.000     └─ Bottom seal face → mandrel Ø1.500 shoulder
```

---

## 3. Features to model in Fusion

| Item | Spec | Notes |
|------|------|-------|
| Top connection | **1 in AMT** | Mate to setting-tool crossover |
| External thread | **1 3/8-8 UN-2A × 1.125** | On **Ø1.375** pin section |
| Top chamfer | **0.030 × 45°** | Thread lead |
| Through bore **(G)** | **Ø0.750** | Through main body + pin section |
| Main body | **Ø1.688 × 3.000** | — |
| Pin section **(A)** | **Ø1.375 × 1.500** | — |
| Seal counterbore | **Ø1.530 × 0.500** | From bottom face |
| Internal thread | **1½-12 UNF-2B × 1.000** | Within bottom zone |
| Bottom seal face | **Ra 32 µin**, **0.001 flatness** | Parker **2-216** compression |
| Bottom chamfer | **0.040 × 45°** | Bore entry |
| Pin hole | **Ø0.125**, 1 place | After mandrel makeup |

---

## 4. Inspection

| Check | Method |
|-------|--------|
| Overall length | 6.000 ±0.010 |
| Main body OD | 1.688 ±0.005 |
| Pin section OD | 1.375 ±0.005 |
| Through bore **(G)** | Ø0.750 plug gauge |
| External thread | **1 3/8-8 UN-2A** ring gauge |
| 1 in AMT | Go/no-go AMT gauge |
| Internal thread | **1½-12 UNF-2B** plug gauge |
| Counterbore | Ø1.530 × 0.500 depth |
| Seal face | Flatness 0.001 FIM; Ra 32 µin |
| Hardness | 28–32 HRC spot check |

---

## 5. Mates and assembly

### 5.1 Part directly below — upper slip cartridge (SHEX-006)

| | Fishing neck | Upper slip module |
|--|--------------|-------------------|
| Position | Item **13** — top of plug | Item **12** — directly below |
| Axial (57 in plug) | **Z = 51.0 – 57.0 in** | **Z = 46.5 – 51.0 in** |
| Run-in OD | **1.688 in** (main body) / **1.375 in** (pin) | **1.688 in** |
| Set OD | **1.375 in** (pin only) | **8.720 in** |

**No direct fastener to slip cartridge.** Bottom seal face @ **Z = 51.0** locates on mandrel shoulder; slip ring top face is adjacent at same plane.

```
        Section at Z ≈ 51 in

              ┌─── SHEX-012  Ø1.688 body / Ø1.375 pin (above)
              │      Through bore Ø0.750
    ──────────┼──●──────────  SHEX-011 mandrel Ø1.550
              │  │
    ══════════╪══╪══════════  SHEX-006 upper slip (Ø1.688 run-in)
              └──┘
```

---

### 5.2 Primary connection — inner mandrel (SHEX-011)

**Threaded + O-ring face seal + pin.** Mandrel groove per **`SHEX-011_inner_mandrel.md` §3** — **update male thread length to 1.000 in**.

| Feature | Fishing neck (female) | Mandrel (male) |
|---------|----------------------|----------------|
| Thread | **1½-12 UNF-2B × 1.000** | **1½-12 UNF-2A × 1.000** |
| Seal counterbore | **Ø1.530 × 0.500** | — |
| Shoulder / seal | Bottom face on **Ø1.500** shoulder | **Ø1.500** shoulder @ **Z = 51.0** |
| O-ring | **Parker 2-216** Viton — compressed by bottom face | Groove in shoulder face |
| Pin | **Ø0.125**, 1 place | @ **Z = 51.500** |
| Makeup torque | **250 ft-lb** min | — |

#### Female internal dimensions (bottom zone — 1.500 in total)

Machine from **bottom face (Z = 0)** upward:

| Zone | ID (in) | Depth | Tolerance | Notes |
|------|---------|-------|-----------|-------|
| **Seal counterbore** | **Ø1.530** | **0.500** | +0.005 / −0.000 | Clears O-ring; non-threaded |
| **Tap / thread** | **1½-12 UNF-2B** | **1.000** | Class 2B | Overlaps counterbore zone |
| **Through bore (G)** | **Ø0.750** | Above bottom zone | +0.002 / −0.000 | Full length |

**1½-12 UNF-2B reference (ANSI B1.1):**

| Diameter | Size (in) |
|----------|-----------|
| Major (internal) | **1.5000** |
| Pitch diameter (2B) | **1.4508 – 1.4565** |
| Minor (internal, ref) | **1.4224** |

#### **1 3/8-8 UN-2A reference (external, pin section)**

| Diameter | Size (in) |
|----------|-----------|
| Major (external) | **1.3750** |
| Pitch diameter (2A, ref) | **1.3210 – 1.3270** |
| Thread length | **1.125** |
| Pitch | **8 UN** (0.125 in) |

#### Assembly sequence

1. Stack plug modules on mandrel.
2. Install **Parker 2-216** in mandrel shoulder groove.
3. Thread neck onto mandrel (**1.000 in** engagement min); bottom face seats on **Ø1.500** shoulder.
4. Torque **250 ft-lb**.
5. Drill **Ø0.125** pin @ **Z = 51.500**.
6. Make up setting tool **1 in AMT** at surface (§5.3).

---

### 5.3 Top connection — setting tool (SHEX-ST-54)

| Feature | Spec |
|---------|------|
| Connection | **1 in AMT** |
| Pin section | **Ø1.375 × 1.500** |
| External thread | **1 3/8-8 UN-2A × 1.125** — mates tool crossover **internal thread** |
| Through bore **(G)** | **Ø0.750** — wireline / mandrel clearance |
| Makeup | At **surface** before run-in |

---

## 6. Required drawing views

| View | Type | Scale | Content |
|------|------|-------|---------|
| A | Front half-section | 1:2 | Full 6.000 length, bore **(G)** |
| B | Right end (top) | 1:1 | Pin **Ø1.375**, AMT |
| DETAIL C | External thread | 2:1 | **1 3/8-8 UN-2A × 1.125** |
| DETAIL D | Bottom zone | 2:1 | Counterbore **Ø1.530 × 0.500**, **1½-12 UNF-2B × 1.000** |
| DETAIL E | Slip interface | 2:1 | Bottom face @ Z = 51.0 |
| DETAIL F | Pin hole | 4:1 | Ø0.125 @ Z = 51.500 |
| DETAIL G | Seal face + O-ring | 2:1 | Parker **2-216** |

---

## 7. Dimension checklist

- [ ] Overall length **6.000**
- [ ] Main body **Ø1.688 × 3.000**
- [ ] Pin section **(A) Ø1.375 × 1.500**
- [ ] Through bore **(G) Ø0.750**
- [ ] External thread **1 3/8-8 UN-2A × 1.125**
- [ ] Top connection **1 in AMT**
- [ ] Top chamfer **0.030 × 45°**
- [ ] Counterbore **Ø1.530 × 0.500**
- [ ] Internal thread **1½-12 UNF-2B × 1.000**
- [ ] Total bottom zone **1.500**
- [ ] Bottom chamfer **0.040 × 45°**
- [ ] Bottom seal face flatness **0.001 FIM**, Ra 32 µin
- [ ] O-ring **Parker 2-216** (on mandrel)
- [ ] Pin **Ø0.125** @ Z = 51.500
- [ ] Part number **SHEX-012**

---

## 8. General notes (copy to drawing)

```
1. UNLESS OTHERWISE SPECIFIED, DIMENSIONS ARE IN INCHES.
2. TOLERANCES: ±0.005 IN; BORES ±0.001 IN; ANGLES ±0.5°.
3. MATERIAL: 4140 HT PER AMS 6415, 28-32 HRC.
4. BREAK ALL SHARP EDGES 0.010 R UNLESS NOTED.
5. TOP CONNECTION: 1 IN AMT; EXTERNAL THREAD 1 3/8-8 UN-2A × 1.125.
6. THROUGH BORE (G): Ø0.750.
7. BOTTOM THREAD: 1½-12 UNF-2B × 1.000 — MATE SHEX-011 Ø1.500 SHOULDER.
8. COUNTERBORE Ø1.530 × 0.500 FROM BOTTOM FACE.
9. SEAL: PARKER 2-216 VITON IN MANDREL GROOVE; COMPRESS WITH BOTTOM FACE.
10. TORQUE 250 FT-LB MIN; DRILL Ø0.125 PIN @ Z=51.500 AFTER MAKEUP.
11. NO DIRECT FASTENER TO SHEX-006 SLIP CARTRIDGE.
12. PLUG ASSY LENGTH WITH THIS NECK: 57.0 IN (WAS 54.0 IN).
13. DEBURR AND INSPECT 100% BEFORE ASSEMBLY.
```

---

*Rev D — 6.000 in length; 1 in AMT top; 1 3/8-8 UN-2A; 1½-12 UNF bottom; Ø1.530 × 0.500 counterbore.*
