# SHEX-013 — Bottom Equalizing Sub — Shop Drawing Spec

**Drawing No:** DWG-013-SHP  
**Part No:** SHEX-013  
**Qty:** 1  
**Material:** 4140 HT (AMS 6415), 28–32 HRC  
**Tier:** **MANUFACTURING** (`-SHP`) — **OD ≤ 1.688 in**  
**STEP import:** `export/cad/parts/SHEX-013_bottom_equalizing_sub.stp` *(envelope only — wrong ID bore; rebuild per §2)*  
**Mechanism ref:** `docs/SETTING_SEQUENCE.md` §6 Phase 1  
**Mates:** **SHEX-011** mandrel **Ø1.550** @ plug **Z = 3 – 5**; **SHEX-011A** tail sleeve below

---

## 1. Function

Bottom sub on plug (**plug item 2**, **Z = 3.000 – 5.000 in**). During **run-in**, radial ports **open** to equalize pressure above/below plug. Before setting, **sliding sleeve** shifts to **close ports** (Stage 1 pilot — no tool stroke). On **retrieval**, ports reopen.

**Part coordinates:** **Z = 0** at **bottom face** of this part (downhole end = plug **Z = 3.0**).

---

## 2. Authoritative dimensions (manufacturing)

| Feature | Dimension (in) | Tolerance | Notes |
|---------|----------------|-----------|-------|
| **Overall length** | **2.000** | ±0.005 | |
| **OD** | **1.688** | +0.000 / −0.005 | Run-in plug OD |
| **ID (mandrel bore)** | **Ø1.562** | +0.003 / −0.000 | Clearance on **Ø1.550** mandrel |
| **Wall thickness** | **0.063** | — | (1.688 − 1.562) / 2 — thin annulus |
| **Bottom face** | Flat | **Ra 32 µin** | Seats at plug **Z = 3.0** |
| **Top face** | Flat | **Ra 32 µin** | Butts lower slip / mandrel stack |

**Do not use STEP ID Ø0.750** — that envelope is obsolete. Mandrel is **Ø1.550** through this zone.

### 2.1 Axial stack (this part)

```
  Z′ (in)   Section
  ───────   ─────────────────────────────
  2.000     ┌─ Top face (plug Z = 5.0)
  1.625     │  Sleeve travel zone (closed @ top)
  1.250     │  Port centre plane (Z′ = 1.000)
  0.375     │  Sleeve travel (open @ bottom)
  0.000     └─ Bottom face (plug Z = 3.0)
```

---

## 3. Features to model in Fusion

### 3.1 Equalizing ports (run-in OPEN)

Thin-wall annulus — ports sized for **0.063 in** radial wall.

| Item | Spec | Notes |
|------|------|-------|
| Port count | **4×** radial, **90°** apart | |
| Port form | **Ø0.062** **or** slot **0.050 × 0.125** | Through wall to **Ø1.562** bore |
| Port centre **Z′** | **1.000** | From bottom face |
| Angular position | **0 / 90 / 180 / 270°** | Datum = pin hole or scribe |

### 3.2 Sliding sleeve (thin annulus ring)

| Item | Dimension (in) | Tolerance | Notes |
|------|----------------|-----------|-------|
| **OD** | **1.680** | +0.000 / −0.002 | Slides in body bore **Ø1.688** ID region |
| **ID** | **1.554** | +0.003 / −0.000 | Clears **Ø1.550** mandrel |
| **Length** | **1.200** | ±0.005 | |
| **Sleeve ports** | **4×** match §3.1 | Align with body ports when **OPEN** |
| **Closed position** | Sleeve shifts **+0.375** toward top (**Z′**) | Ports **misaligned** |
| **Open position** | Sleeve bottom @ **Z′ = 0.100** | Ports aligned |
| Pilot bore *(optional)* | **Ø0.250** × **0.300** deep | Top of sleeve — Stage 1 pilot *(TBD)* |

### 3.3 Static seals (body ↔ mandrel)

| Groove | Location **Z′** | O-ring | Notes |
|--------|-----------------|--------|-------|
| Lower | **0.250** | **Parker 2-212** Viton | Housing groove in **Ø1.562** bore |
| Upper | **1.750** | **Parker 2-212** Viton | — |

**Parker 2-212 groove (housing in ~1.562 bore / 1.550 shaft):**

| Feature | Dimension (in) | Tolerance |
|---------|----------------|-----------|
| Groove diameter | **1.575** | ±0.003 |
| Groove width **G** | **0.103** | ±0.003 |
| Groove depth **H** | **0.070** | +0.002 / −0.000 |

### 3.4 Anti-rotation

| Item | Spec |
|------|------|
| Pin | **Ø0.093 × 0.250** deep, **1 place** |
| Pin location | Body OD, **Z′ = 0.500**, drive sleeve slot |

---

## 4. Required drawing views (DWG-013-SHP)

| View | Type | Scale | Content |
|------|------|-------|---------|
| A | Front half-section | **2:1** | Full length — ports, sleeve, grooves |
| B | Section **B-B** @ **Z′ = 1.000** | **2:1** | Port pattern — **OPEN** solid / **CLOSED** dashed |
| C | Right end | **1:1** | OD **1.688**, bore **1.562** |
| DETAIL D | O-ring groove | **4:1** | §3.3 |
| DETAIL E | Sleeve travel | **2:1** | **0.375** shift, open vs closed |
| DETAIL F | Port | **4:1** | Ø0.062 or slot dims |

---

## 5. Dimension checklist

- [ ] Overall length **2.000**
- [ ] OD **1.688**
- [ ] Bore **Ø1.562** (mandrel **Ø1.550** clearance)
- [ ] Ports **4×** @ **Z′ = 1.000**, **90°** spacing
- [ ] Sleeve **OD 1.680 × ID 1.554 × L 1.200**
- [ ] Sleeve travel **0.375** (open → closed)
- [ ] O-ring grooves **2×** @ **Z′ = 0.250 / 1.750**
- [ ] Anti-rotation pin **Ø0.093**
- [ ] Surface finish **Ra 32 µin** on bore and faces
- [ ] Part number **SHEX-013**

---

## 6. General notes (copy to drawing)

```
1. UNLESS OTHERWISE SPECIFIED, DIMENSIONS ARE IN INCHES.
2. MATERIAL: 4140 HT, AMS 6415, HEAT TREAT 28-32 HRC.
3. MANUFACTURING DRAWING — RUN-IN OD 1.688 MAX.
4. PRESSURE-CONTAINING — 100% PT ALL PORTS AFTER MACHINING.
5. SLEEVE MUST TRAVEL 0.375 IN MIN WITHOUT BINDING.
6. ASSEMBLE WITH VITON 2-212 IN GROOVES; SILICONE GREASE.
7. FUNCTIONAL TEST: FLOW OPEN (ALIGNED); BLOCKED CLOSED (MISALIGNED).
8. PLUG Z LOCATION: 3.000 – 5.000 IN (ITEM 2).
9. SEE SETTING_SEQUENCE §6 PHASE 1 FOR OPEN/CLOSE TIMING.
```

---

## 7. Assembly context

| Neighbour | Plug Z | Interface |
|-----------|--------|-----------|
| Below | **3.0** bottom face | Open annulus / wellbore |
| Above | **5.0** top face | Lower slip module / mandrel **Ø1.550** |
| Mandrel | Through bore | **Ø1.550** — sleeve slides on mandrel OD |
| **SHEX-011A** tail sleeve | **0 – 3.0** | Below this sub on mandrel tail |

---

## 8. Fusion workflow

1. New design **`02_SHEX-013_equalizing_sub`**.
2. **Do not** trust STEP bore — model from §2: **Ø1.688 × 2.0 L**, bore **Ø1.562**.
3. Model **4× ports** @ **Z′ = 1.0** (§3.1).
4. Model **sleeve** as separate body (§3.2) — use **Component** for drawing section views.
5. Cut **O-ring grooves** @ **Z′ = 0.25 / 1.75** (§3.3).
6. **Drawing → From Design** → **DWG-013-SHP**; dimension per §5.
7. Export PDF → `export/drawings/shop_pdf/DWG-013-SHP.pdf`.
8. Mate-check with **SHEX-011** mandrel @ plug **Z = 3 – 5**.

---

## 9. Inspection

| Check | Method |
|-------|--------|
| OD / length | Micrometer / caliper |
| Bore **Ø1.562** | Bore gauge |
| Port location | CMM or pin gauge @ **Z′ = 1.0** |
| Sleeve travel | Mandrel + sleeve functional test |
| Pressure test | 100% PT per note 4 |

---

*Rev B — manufacturing dims for Ø1.550 mandrel / 1.688 OD annulus; STEP Ø0.750 obsolete.*
