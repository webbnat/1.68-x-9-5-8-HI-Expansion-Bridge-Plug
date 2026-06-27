# SHEX-011 — Inner Mandrel — Shop Drawing Spec

**Drawing No:** DWG-011B-SHP  
**Part No:** SHEX-011  
**Qty:** 1  
**Material:** 17-4 PH H900 (H1150M)  
**STEP import:** `export/cad/parts/SHEX-011_inner_mandrel.stp` *(envelope — add top end + steps in Fusion)*  
**Mate fishing neck:** `SHEX-012_fishing_neck.md` **Rev D**  
**Related:** `SHEX-011_mandrel_tail_sleeve.md` *(tail sleeve — separate part, DWG-011A)*

---

## 1. Function

Central **setting mandrel** — drives the full plug set sequence. All modules (slips, stents, iris, seals) slide or expand on this OD.

| End | Mate |
|-----|------|
| **Top (Z = 51.0)** | **SHEX-012** fishing neck — **1½-12 UNF-2A**, **Ø1.500** shoulder + **Parker 2-216** |
| **Bottom (Z = 0)** | **SHEX-013** equalizing sub + **SHEX-011A** tail sleeve |

**Overall mandrel length: 54.0 in** (matches STEP: 3 in tail + 51 in @ **Ø1.550**). **Neck joint** at **Z = 51.0** — see **§2.2**.

**Plug assembly:** Body modules **0 – 51.0 in**; fishing neck **51.0 – 57.0 in** (6 in). **Overall plug = 57.0 in**.

---

## 2. Authoritative dimensions

Coordinate: **Z = 0 at bottom face**, **Z+ uphole**.

| Section | Z range (in) | Length (in) | OD (in) | Tolerance |
|---------|--------------|-------------|---------|-----------|
| **Tail** | 0 – 3.0 | 3.0 | **1.350** | +0.000 / −0.002 |
| **Main body** | 3.0 – 54.0 | 51.0 | **1.550** | +0.000 / −0.002 |
| **Top joint** *(machined)* | 50.0 – 51.0 | 1.0 | **1.500** | Step, thread, shoulder |
| **Overall** | 0 – 54.0 | **54.0** | — | ±0.010 |

| Feature | Value | Notes |
|---------|-------|-------|
| Through bore | **Solid** | No through bore |
| Tail step | **Ø1.350 → Ø1.550** @ **Z = 3.0** | 30° chamfer or **R0.062** blend |
| Top step (joint) | **Ø1.550 → Ø1.500** @ **Z = 50.0** | Thread + shoulder zone |
| Shoulder face | **Z = 51.0** | **Ø1.500** + O-ring groove — mates SHEX-012 bottom |
| Module stack engagement | **Z = 0 – 51.0** | Slips, seals, iris, etc. on **Ø1.550** body |
| Straightness | **0.005 in** | Over any 12 in |
| Surface finish (slip/seal zones) | **Ra 32 µin** | Z = 3.0 – 51.0 |

### 2.1 Axial stack (this part)

```
  Z (in)    OD (in)    Section
  ───────   ────────   ─────────────────────────────
  54.0      1.550      ┌─ Top of STEP / turned bar
  51.0      1.550      │  Main body continues (no neck drift — §2.2)
  51.0      1.500      ├─ Shoulder face + O-ring groove (joint)
                        │  1½-12 UNF-2A × 1.000 (Z = 50.0 – 51.0)
  50.0      1.550 ──►  ├─ Step Ø1.550 → Ø1.500
  3.0       1.550      │  Main body — modules Z = 3 – 51
  3.0       1.350 ──►  ├─ Step Ø1.350 → Ø1.550
  0.0       1.350      └─ Tail
```

### 2.2 Fishing neck — no through-mandrel drift

**There is no requirement for the plug mandrel to pass through the fishing neck.**

| Topic | Clarification |
|-------|----------------|
| **SHEX-012 bore (G) Ø0.750** | Wireline / internal clearance in the **neck only** — **not** a mandrel through-bore |
| **How neck attaches** | **Separate part** — **1½-12 UNF-2B** picks up male thread at **Z = 50 – 51**; bottom face seals on **Ø1.500** shoulder @ **Z = 51** |
| **Engagement depth** | **~1.0 in** thread + shoulder — within neck **bottom 1.5 in zone** only |
| **Z = 51 – 54 on mandrel** | **Ø1.550** bar stock to **Z = 54** per STEP; **does not enter** neck bore (G). In assembly, **SHEX-012 occupies Z = 51 – 57 externally** — it is **not** a tube the mandrel slides through |
| **Z = 51 – 54 on mandrel (lathe)** | Top **3 in** of the **54 in** bar above the joint plane — **plain Ø1.550** unless parted off. **Not functionally required** inside the neck; may be **trimmed at Z = 51** after threading or left as non-interfering stub per neck OD envelope |

**Assembly model (side view):**

```
  Z=57  ──  SHEX-012 pin / AMT (neck only)
  Z=51  ──  ├─ Neck bottom face ═══ Shoulder @ mandrel Z=51
            │   (thread engagement 50–51 only)
            │   NO mandrel drift through neck bore (G)
  Z=51  ──  Upper slip top / module stack end
  Z=0   ──  Mandrel tail
```

---

## 3. Mandrel top end — mates SHEX-012 Rev D

```
  Plug Z     SHEX-012 (female)                 SHEX-011 (male)
  ───────    ─────────────────────             ─────────────────
  57.0       1" AMT / pin Ø1.375
  51.0       bottom seal face ─────────────►  shoulder @ Z=51.0
             counterbore Ø1.530 × 0.500          O-ring groove
             1½-12 UNF-2B × 1.000                  1½-12 UNF-2A × 1.000
  51.5       pin Ø0.125 (assembly) ◄──────────► pin @ Z=51.500
  46.5       (upper slip bore Ø1.550 clr)
```

### 3.1 Shoulder and O-ring groove (male)

| Feature | Dimension (in) | Tolerance | Notes |
|---------|----------------|-----------|-------|
| Shoulder face | **Z = 51.0** | — | Joint face — mates SHEX-012 bottom |
| Shoulder OD | **Ø1.500** | +0.000 / −0.002 | — |
| Shoulder flatness | — | **0.001 FIM** | Groove + seal land |
| Shoulder finish | **Ra 32 µin** | max | — |
| **O-ring** | **Parker 2-216** | — | Viton 90; AS568-216 |
| Groove OD | **Ø1.181** | ±0.003 | In shoulder face |
| Groove ID | **Ø1.087** | ±0.003 | — |
| Groove width **G** | **0.094** | ±0.003 | — |
| Groove depth **H** | **0.086** | +0.002 / −0.000 | — |
| Groove corner | **R0.015** | min | — |

### 3.2 Male thread and pin

| Feature | Spec | Notes |
|---------|------|-------|
| Thread | **1½-12 UNF-2A** | (= 1.500-12 UNF) |
| Thread length | **1.000 in** | **Z = 50.000 – 51.000** |
| Thread major OD | **Ø1.500** | — |
| Thread run-out | **0.030 × 45°** | At **Z = 50.000** |
| Cross pin | **Ø0.125 in**, **1 place** | Drill after neck makeup |
| Pin centre **Z** | **51.500** | Plug assembly coordinates |
| Makeup torque | **250 ft-lb** min | O-ring is primary seal |

**1½-12 UNF-2A reference (ANSI B1.1):**

| Diameter | Size (in) |
|----------|-----------|
| Major (external) | **1.5000** |
| Pitch diameter (2A) | **1.4565 – 1.4622** |
| Minor (external, ref) | **1.4224** |

### 3.3 Mates SHEX-012 female (cross-check)

| Female (SHEX-012) | Male (this part) |
|-------------------|------------------|
| Counterbore **Ø1.530 × 0.500** | Shoulder **Ø1.500** + groove clears in counterbore |
| **1½-12 UNF-2B × 1.000** | **1½-12 UNF-2A × 1.000** |
| Bottom seal face | Shoulder face @ **Z = 51.0** |
| Pin @ **Z = 51.500** | Pin @ **Z = 51.500** |

---

## 4. Mandrel bottom end — mates SHEX-013 / tail sleeve

| Feature | Spec | Notes |
|---------|------|-------|
| Bottom face | Flat, **Ra 63 µin** | **Z = 0** |
| Bottom OD | **Ø1.350 × 3.000** | Inside tail sleeve |
| Step to main | **Z = 3.0** | **Ø1.350 → Ø1.550** |
| Equalizing sleeve | Slides on **Ø1.550** | Above **Z = 3.0** |

*(Tail sleeve **SHEX-011A** — separate drawing DWG-011A-SHP.)*

---

## 5. Module boundary map (for drawing sections)

Use for **broken views**, **section cuts**, and Fusion **assembly** ballooning.

| Item | Module | Z start | Z end | Mandrel OD @ zone |
|------|--------|---------|-------|-------------------|
| 1 | Mandrel tail / sleeve | 0 | 3.0 | 1.350 |
| 2 | Bottom equalizing sub | 3.0 | 5.0 | 1.550 (through bore clearance) |
| 3 | Lower slips | 5.0 | 9.5 | 1.550 + taper (§12.3) |
| 4 | Stage 1 stent + bladder | 9.5 | 13.5 | 1.550 |
| 5 | Stage 2 stent + Belleville | 13.5 | 18.5 | 1.550 |
| 6 | Stage 3 iris | 18.5 | 26.0 | 1.550 + helix cams (§12.5) |
| 7–10 | Seal lands 1–4 | 26.0 | 44.0 | 1.550 + ramps (§12.6) |
| 11 | Upper MTM | 44.0 | 46.5 | 1.558 load land (§12.7) |
| 12 | Upper slips | 46.5 | 51.0 | 1.550 + taper (§12.8) |
| 13 | Fishing neck *(SHEX-012)* | 51.0 | 57.0 | — *(threads onto mandrel @ Z=51; no mandrel drift)* |

*Detailed OD features per zone — **§12**.*

---

## 6. Features to model in Fusion (not in STEP)

| Priority | Feature | Location | Status |
|----------|---------|----------|--------|
| **1** | Top step **Ø1.550 → Ø1.500** | Z = 50.0 | Required — §3 |
| **1** | **1½-12 UNF-2A × 1.000** | Z = 50.0 – 51.0 | Required — §3 |
| **1** | Shoulder + **O-ring groove** | Z = 51.0 | Required — §3 |
| **1** | Pin drill **Ø0.125** | Z = 51.500 | Assembly |
| **2** | Tail step **Ø1.350 → Ø1.550** | Z = 3.0 | Required — §4 |
| **2** | Lower slip **expander cone** | Z = 6.25 – 7.75 | §12.3 |
| **2** | Iris **drive helix / cams** | Z = 19.0 – 23.0 | §12.5 |
| **2** | Seal-set **ramps ×4** | Z = 26.0 – 44.0 | §12.6 |
| **2** | Upper slip **expander cone** | Z = 48.25 – 49.75 | §12.8 |
| **3** | MTM **load land** | Z = 44.75 – 45.25 | §12.7 |

---

## 12. Mandrel functional zones — OD steps and setting features

Provisional **Rev D.3** geometry derived from module stack (§5), setting sequence (`docs/SETTING_SEQUENCE.md`), and stroke budget (iris **4.0 in**, seals **~5.5 in**, slips **~1.5 in**). **Validate in Fusion skeleton assembly** before locking shop dims on SHEX-002 / SHEX-004 / SHEX-006 drawings.

### 12.1 Design basis

| Item | Value |
|------|-------|
| Mandrel OD (main) | **Ø1.550** +0.000 / −0.002 |
| Module bore on mandrel | **Ø1.550 +0.003 / −0.000** (slip / seal carriers) |
| Setting motion | Mandrel translates **+Z (uphole)** **~11.0 in** total vs fixed outer stack during Phases 4–6 |
| Run-in index | Mandrel **bottom face @ Z = 0**; top joint plane @ **Z = 51.0** |
| Finish | **Ra 32 µin** on all zones in §12.3 – §12.8 |

**Motion convention (Phases 4–6):** Tool push at fishing neck advances mandrel **uphole (+Z)** through fixed module carriers. Iris helix zone is engaged first, then seal ramps, then slip expander cones.

**Elevation (functional OD — not to scale):**

```
  Z=51  ──  Ø1.500 thread / shoulder (§3)
  Z=50  ──  ├─ step Ø1.550 → Ø1.500
  Z=49.8──  │  upper slip taper Ø1.550 → Ø1.620
  Z=45.3──  │  MTM load Ø1.558
  Z=42  ──  │  seal ramp 4 ↑
  Z=37.5──  │  seal ramp 3 ↑
  Z=33  ──  │  seal ramp 2 ↑
  Z=28.5──  │  seal ramp 1 ↑
  Z=23  ──  │  iris helix cams (2-start, L=4.0)
  Z=19  ──  │
  Z=18.5──  │  smooth Ø1.550 (stages 1–2)
  Z=9.5 ──  │
  Z=7.8 ──  │  lower slip taper Ø1.550 → Ø1.620
  Z=6.3 ──  │
  Z=3   ──  ├─ step Ø1.350 → Ø1.550
  Z=0   ──  └─ tail Ø1.350
```

### 12.2 Zone summary

| Zone | Item | Z range (in) | Mandrel OD / feature | Setting stroke |
|------|------|--------------|----------------------|----------------|
| A | Tail | 0 – 3.0 | **Ø1.350** step @ 3.0 | — |
| B | Equalizing / tail sleeve | 3.0 – 5.0 | **Ø1.550** smooth | — |
| C | Lower slips | 5.0 – 9.5 | **Expander cone** §12.3 | ~0.75 in (of 1.5 in slip budget) |
| D | Stage 1 stent | 9.5 – 13.5 | **Ø1.550** smooth | Internal (no tool stroke) |
| E | Stage 2 stent | 13.5 – 18.5 | **Ø1.550** smooth | Internal (no tool stroke) |
| F | Stage 3 iris | 18.5 – 26.0 | **Helix cams** §12.5 | **4.0 in** + rotation |
| G | Seal lands 1–4 | 26.0 – 44.0 | **Compression ramps ×4** §12.6 | **~5.5 in** total |
| H | Upper MTM | 44.0 – 46.5 | **Load land** §12.7 | Included in seal push |
| I | Upper slips | 46.5 – 51.0 | **Expander cone** §12.8 | ~0.75 in (of 1.5 in slip budget) |
| J | Top joint | 50.0 – 51.0 | **Ø1.500** thread + shoulder | — |

### 12.3 Lower slip expander cone (Item 3 — SHEX-007)

Wedges (8×) ride on mandrel OD; axial advance forces teeth outward against casing.

| Feature | Dimension (in) | Tolerance | Notes |
|---------|----------------|-----------|-------|
| Smooth lead-in | **Z = 5.000 – 6.250** | — | **Ø1.550** — slip carrier bore clearance |
| Taper start | **Z = 6.250** | — | **Ø1.550** |
| Taper end | **Z = 7.750** | — | **Ø1.620** |
| Taper length | **1.500** | — | **12° included** (6° half-angle) |
| Smooth trail | **Z = 7.750 – 9.500** | — | **Ø1.620** × 1.750 then blend to **Ø1.550** @ **Z = 9.500** *(0.125 × 45° chamfer)* |
| Radial rise | **0.070** | — | Drives wedge ~0.35 in radial at OD 8.72 |

**Run-in:** Taper centred in slip module; wedges retracted on **Ø1.550** land.  
**Set:** Mandrel **+Z ~0.75 in** positions full taper under wedges (Phase 6, shared with upper slip).

### 12.4 Stage 1 & 2 — smooth bearing lands (Items 4–5)

| Feature | Dimension (in) | Notes |
|---------|----------------|-------|
| OD | **Ø1.550** | No mandrel OD steps — stents expand in annulus |
| Z span | **9.500 – 18.500** | Stage 1 + Stage 2 modules |
| Scribe lines *(optional)* | **Z = 13.500** | Assembly reference only — 0.010 deep max |

### 12.5 Stage 3 iris drive zone (Item 6 — mates SHEX-002 / SHEX-001)

**SHEX-002** (Inconel 718) carries the **double-start helix path** (lead **4.0 in**). Mandrel carries **drive cams** that transfer tool rotation + axial push to iris segments via the fixed helix guide.

| Feature | Dimension (in) | Tolerance | Notes |
|---------|----------------|-----------|-------|
| Smooth bearing | **Z = 18.500 – 19.000** | — | **Ø1.550** — iris module entry |
| **Helix cam zone** | **Z = 19.000 – 23.000** | — | **4.0 in** active stroke span |
| Cam form | **2-start**, lead **L = 4.0** | — | Double-start — **2.0 in axial per 360°** |
| Cam rise | **0.062** above **Ø1.550** | ±0.003 | Radial drive for segment followers |
| Cam width *(axial)* | **0.250** | ±0.005 | At peak OD |
| Cam peak OD | **Ø1.674** | — | = 1.550 + 2×0.062 |
| Root between cams | **Ø1.550** | — | Bearing surface for guide sleeve |
| Smooth exit | **Z = 23.000 – 26.000** | — | **Ø1.550** — lock / support land |
| Rotation | **2 rev** max | — | Over 4.0 in stroke (matches SHEX-002) |

**Run-in:** Cams at **Z = 19.0 – 23.0** aligned with collapsed iris pocket (segments @ ID 5.750).  
**Set end:** Mandrel advanced **+4.0 in**; segments deployed to OD **8.650**.

*Cross-check:* `export/drawings/dxf/DWG-002_iris_module_assy.dxf` — **LEAD 4.0 IN**, **16 seg @ 22.5°**.

### 12.6 Seal-set compression ramps (Items 7–10 — SHEX-004 / SHEX-005)

Each **4.5 in** seal module has a **1.375 in** effective compression ramp on mandrel OD. Continued **+Z** advance after iris forces HNBR cups radially against casing; metal petals react on ramp shoulder.

| Land | Module Z | Ramp Z (start → end) | Start OD | End OD | Ramp angle |
|------|----------|----------------------|----------|--------|------------|
| **1** | 26.0 – 30.5 | **27.125 → 28.500** | **Ø1.550** | **Ø1.582** | **3° included** |
| **2** | 30.5 – 35.0 | **31.625 → 33.000** | **Ø1.550** | **Ø1.582** | **3° included** |
| **3** | 35.0 – 39.5 | **36.125 → 37.500** | **Ø1.550** | **Ø1.582** | **3° included** |
| **4** | 39.5 – 44.0 | **40.625 → 42.000** | **Ø1.550** | **Ø1.582** | **3° included** |

Between ramps: **Ø1.550** clearance bands (**~2.625 in** between ramp ends).

| Feature | Dimension (in) | Notes |
|---------|----------------|-------|
| Radial rise per ramp | **0.032** | (1.582 − 1.550) / 2 |
| Ramp length | **1.375** | ×4 ≈ **5.5 in** tool stroke |
| Downhole ramp face | **30° chamfer** | Transition to **Ø1.550** land |
| Uphole ramp face | **Flat** | Compresses petal carrier / HNBR back face |

**Run-in:** All ramps upstream (downhole side) of seal carriers — cups relaxed on **Ø1.550**.  
**Set:** Sequential ramp engagement lands 1 → 4 as mandrel advances **+Z** after iris.

### 12.7 Upper MTM load land (Item 11 — SHEX-003)

| Feature | Dimension (in) | Notes |
|---------|----------------|-------|
| Smooth approach | **Z = 44.000 – 44.750** | **Ø1.550** |
| **Load land** | **Z = 44.750 – 45.250** | **Ø1.558** × **0.500** — axially compresses 3-ring MTM stack |
| Smooth exit | **Z = 45.250 – 46.500** | **Ø1.550** |
| Radial rise | **0.008** | Metal-to-metal preload only — no elastomer |

### 12.8 Upper slip expander cone (Item 12 — SHEX-006)

Mirror of §12.3 — same geometry, upper module.

| Feature | Dimension (in) | Notes |
|---------|----------------|-------|
| Smooth lead-in | **Z = 46.500 – 48.250** | **Ø1.550** |
| Taper start | **Z = 48.250** | **Ø1.550** |
| Taper end | **Z = 49.750** | **Ø1.620** |
| Taper length | **1.500** | **12° included** |
| Blend to joint zone | **Z = 49.750 – 50.000** | **Ø1.620 → Ø1.550** before top step @ **Z = 50.0** |

**Set:** Final **~0.75 in** mandrel travel (Phase 6) positions taper under upper wedges.

### 12.9 Setting stroke index — mandrel vs stack

Mandrel **bottom face fixed @ Z = 0**; values are **cumulative +Z travel** from run-in index at start of Phase 4.

| Phase | Function | Cumulative +Z (in) | Mandrel feature engaged |
|-------|----------|-------------------|-------------------------|
| — | Run-in / Phases 1–3 | **0.0** | Internal stents only |
| 4 | Stage 3 iris | **0.0 → 4.0** | §12.5 helix cams + **2 rev** |
| 5 | Seal compression | **4.0 → 9.5** | §12.6 ramps 1 → 4 |
| 6 | Slip set | **9.5 → 11.0** | §12.3 lower + §12.8 upper cones |
| 7 | MTM load-up | *(within Phase 5 push)* | §12.7 load land |
| 8 | Tool release | **11.0 + 0.5** overtravel | Release collet — not on mandrel |

**Tool stroke budget:** 4.0 + 5.5 + 1.5 + 0.5 = **11.5 in required** / **12.0 in available** (0.5 in margin).

### 12.10 OD step ledger — machining order (tail → head)

Use for lathe programming and Fusion timeline. All dims from **Z = 0** bottom face.

| Step | Z from | Z to | OD (in) | Feature |
|------|--------|------|---------|---------|
| 1 | 0.000 | 3.000 | **1.350** | Tail |
| 2 | 3.000 | 5.000 | **1.550** | Step + equalizing zone |
| 3 | 5.000 | 6.250 | **1.550** | Lower slip lead-in |
| 4 | 6.250 | 7.750 | **1.550 → 1.620** | Lower slip taper |
| 5 | 7.750 | 9.500 | **1.620 → 1.550** | Lower slip trail blend |
| 6 | 9.500 | 18.500 | **1.550** | Stage 1 & 2 smooth |
| 7 | 18.500 | 19.000 | **1.550** | Iris entry |
| 8 | 19.000 | 23.000 | **1.550 + helix cams** | Iris drive (§12.5) |
| 9 | 23.000 | 26.000 | **1.550** | Iris exit |
| 10 | 26.000 | 27.125 | **1.550** | Seal 1 lead-in |
| 11 | 27.125 | 28.500 | **1.550 → 1.582** | Seal 1 ramp |
| 12 | 28.500 | 31.625 | **1.550** | Seal 1–2 gap |
| 13 | 31.625 | 33.000 | **1.550 → 1.582** | Seal 2 ramp |
| 14 | 33.000 | 36.125 | **1.550** | Seal 2–3 gap |
| 15 | 36.125 | 37.500 | **1.550 → 1.582** | Seal 3 ramp |
| 16 | 37.500 | 40.625 | **1.550** | Seal 3–4 gap |
| 17 | 40.625 | 42.000 | **1.550 → 1.582** | Seal 4 ramp |
| 18 | 42.000 | 44.750 | **1.550** | Seal 4 exit / MTM approach |
| 19 | 44.750 | 45.250 | **1.558** | MTM load land |
| 20 | 45.250 | 48.250 | **1.550** | MTM exit / upper slip lead-in |
| 21 | 48.250 | 49.750 | **1.550 → 1.620** | Upper slip taper |
| 22 | 49.750 | 50.000 | **1.620 → 1.550** | Blend to top step |
| 23 | 50.000 | 51.000 | **1.500** | Thread + shoulder (§3) |
| 24 | 51.000 | 54.000 | **1.550** | Top stub (§2.2 — optional trim) |

### 12.11 Fusion validation checklist

Before releasing DWG-011B-SHP:

- [ ] Skeleton assembly — module envelope cylinders @ §5 Z ranges; no interference at run-in and full-set positions
- [ ] Iris — **4.0 in** stroke + **2 rev** clears SHEX-010 bore and deploys segments to **Ø8.650**
- [ ] Seals — each ramp **1.375 in** travel compresses HNBR to casing ID **8.679** drift with petals engaged
- [ ] Slips — both tapers develop wedge load within **1.5 in** combined stroke
- [ ] MTM — **0.500 in** land preloads rings without elastomer contact
- [ ] Top joint — thread + shoulder still @ **Z = 51.0** after all steps modeled

---

## 7. Required drawing views

| View | Type | Scale | Content |
|------|------|-------|---------|
| A | Front elevation | **1:12 broken** | Full **54.0** length — OD step ledger §12.10 |
| B | Section B-B @ top | **2:1** | Thread, shoulder, groove |
| C | Section C-C @ Z=3 | **2:1** | Tail step |
| D | Section D-D @ Z=26 | **2:1** | Seal ramp 1 (§12.6) |
| E | Section E-E @ Z=21 | **2:1** | Iris helix cams (§12.5) |
| F | Section F-F @ Z=7 | **2:1** | Lower slip taper (§12.3) |
| G | Section G-G @ Z=49 | **2:1** | Upper slip taper (§12.8) |
| DETAIL H | O-ring groove | **4:1** | Parker 2-216 dims |
| DETAIL I | Thread | **4:1** | 1½-12 UNF-2A × 1.000 |
| DETAIL J | Pin | **4:1** | Ø0.125 @ Z=51.500 |
| DETAIL K | Top step @ joint | **2:1** | Ø1.550 → Ø1.500 @ Z=50 |

---

## 8. Dimension checklist

- [ ] Overall length **54.000**
- [ ] Tail **Ø1.350 × 3.000**
- [ ] Main body **Ø1.550** (Z = 3 – 54, with steps per §12.10)
- [ ] Top joint **Ø1.500** thread + shoulder (Z = 50 – 51)
- [ ] Tail step @ **Z = 3.000**
- [ ] Top step @ **Z = 50.000**
- [ ] Lower slip taper **Ø1.550 → Ø1.620** @ **Z = 6.250 – 7.750** (§12.3)
- [ ] Iris helix cams **2-start, L = 4.0** @ **Z = 19.000 – 23.000** (§12.5)
- [ ] Seal ramps **×4**, **Ø1.550 → Ø1.582 × 1.375** (§12.6)
- [ ] MTM load land **Ø1.558 × 0.500** @ **Z = 44.750 – 45.250** (§12.7)
- [ ] Upper slip taper **Ø1.550 → Ø1.620** @ **Z = 48.250 – 49.750** (§12.8)
- [ ] Shoulder face @ **Z = 51.000**, flatness **0.001 FIM**
- [ ] O-ring groove OD **1.181**, ID **1.087**, G **0.094**, H **0.086**
- [ ] Thread **1½-12 UNF-2A × 1.000**
- [ ] Pin **Ø0.125** @ **Z = 51.500** (assembly note)
- [ ] Straightness **0.005 / 12 in**
- [ ] Ra **32 µin** on Z = 3 – 51
- [ ] Material **17-4 PH H1150M**
- [ ] Part number **SHEX-011**

---

## 9. General notes (copy to drawing)

```
1. UNLESS OTHERWISE SPECIFIED, DIMENSIONS ARE IN INCHES.
2. MATERIAL: 17-4 PH H900, HEAT TREAT H1150M.
3. Ø1.550 BODY: 32 µin Ra ON SLIP/SEAL TRAVEL ZONES (Z=3 TO 51).
4. TOP END: 1½-12 UNF-2A × 1.000 — MATE SHEX-012 Rev D @ Z=51.0.
5. SHOULDER Ø1.500 @ Z=51.0; PARKER 2-216 VITON IN GROOVE BEFORE NECK MAKEUP.
6. TORQUE 250 FT-LB MIN AT NECK MAKEUP; DRILL Ø0.125 PIN @ Z=51.500 AFTER.
7. MANDREL 54.0 IN PER STEP; JOINT @ Z=51.0; NO DRIFT THROUGH SHEX-012 BORE (G) — §2.2.
8. FUNCTIONAL OD STEPS: §12 — SLIP TAPER, IRIS CAMS, SEAL RAMPS, MTM LAND.
9. NO DIRECT FASTENER TO SLIP CARTRIDGES — MANDREL-CENTRIC STACK.
10. CHROME PLATE NOT REQUIRED (CONTRAST ST-010 STROKE MANDREL).
11. DEBURR; INSPECT STRAIGHTNESS BEFORE ASSEMBLY.
```

---

## 10. Inspection

| Check | Method |
|-------|--------|
| OD 1.550 / 1.350 | Micrometer, 3 places per 12 in |
| OD 1.500 top stub | Micrometer |
| Thread | 1½-12 UNF ring gauge |
| O-ring groove | Groove dims §3.1 |
| Shoulder flatness | Surface plate + indicator |
| Straightness | V-block + dial indicator |
| Length 54.000 | Large caliper / CMM |
| Slip tapers (§12.3, §12.8) | Profile gauge / CMM @ Z = 7 & 49 |
| Seal ramps (§12.6) | Micrometer @ peak OD **1.582** |
| Iris cams (§12.5) | CMM or helix template |

---

## 11. Fusion workflow (quick start)

1. New design **`04_SHEX-011_inner_mandrel`**.
2. Import `SHEX-011_inner_mandrel.stp` — **54.0 in / Ø1.550** envelope matches §2.
3. Model **top joint** @ Z = 51 (step, thread, groove) — §3.
4. Model **tail step** @ Z = 3 (§4).
5. Add **functional OD steps** per **§12.10** ledger (slip tapers → iris cams → seal ramps → MTM land).
6. Resolve **Z = 51 – 54** per §2.2 (optional trim at shoulder — not a neck drift requirement).
7. Create drawing with **broken view** (§7) — section at each feature zone.
8. Assembly-check in skeleton with module envelopes (§12.11) and **SHEX-012** at joint @ Z = 51.

---

*Rev D.3 — §12 mandrel functional zones: slip tapers, iris helix cams, seal ramps, MTM land, OD step ledger.*
