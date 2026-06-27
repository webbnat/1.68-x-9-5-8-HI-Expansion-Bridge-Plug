# Stage 3 Iris Module — Assembly & Fusion Guide

**Manufacturing index:** `SHEX-IRIS_STACK_INDEX.md` ← **start here for shop drawings**  
**Part specs:** `SHEX-010_support_sleeve.md` | `SHEX-002_helix_guide.md` | `SHEX-001_iris_segment.md`  
**Set illustration:** **DWG-002-SET** *(expanded deployed view — not for machining)*  
**Plug item:** 6  
**Plug Z range:** **18.500 – 26.000 in** (bottom → top)  
**Module length:** **7.500 in**

| Part | P/N | Qty | Shop drawing | Set viz |
|------|-----|-----|--------------|---------|
| Support sleeve | **SHEX-010** | 1 | **DWG-012-SHP** @ **OD 1.688** | Shown expanded in **DWG-002-SET** |
| Helix guide | **SHEX-002** | 1 | **DWG-002A-SHP** | — |
| Iris segment | **SHEX-001** | 16 | **DWG-001-SHP** | Deployed in **DWG-002-SET** |
| Top retainer ring | **SHEX-002R** *(TBD)* | 1 | TBD | — |

**Drawing tiers:** See `docs/FUSION_SHOP_DRAWINGS.md` — **`-SHP`** = manufacturing (run-in); **`-SET`** = set illustration.

**Mates:** **SHEX-011** mandrel §12.5 (helix cams **Z = 19.0 – 23.0**); **SHEX-009** Stage 2 below; seal module above @ **Z = 26.0**.

---

## 1. Function

Third expansion stage: **5.750 in → 8.650 in OD** via **16 solid segments** on a **double-start helix** (lead **4.0 in**). First phase that uses setting-tool stroke (**4.0 in axial + ~2 rev rotation**).

| State | Module outer OD | Used on which drawing tier |
|-------|-----------------|----------------------------|
| **Run-in** | **1.688 in** max | **`-SHP`** manufacturing (what shop builds) |
| **Set** | **8.650 in** max | **`-SET`** illustration only (virtual deployed assy) |

---

## 2. Module envelope (plug coordinates)

**Z = 0** at plug bottom; **Z+ uphole**.

| Parameter | Value |
|-----------|-------|
| Module bottom | **Z = 18.500** |
| Module top | **Z = 26.000** |
| Length | **7.500 in** |
| Mandrel through-bore | **Ø1.550** clearance *(mandrel §12.5 cams in this span)* |
| Set OD (deployed) | **8.650 in** |
| Collapsed substrate OD | **5.750 in** *(fixed support sleeve)* |

### 2.1 Axial zones within module *(local Z′ = 0 at module bottom)*

| Local Z′ (in) | Plug Z (in) | Zone | Content |
|---------------|-------------|------|---------|
| 0.000 – 0.750 | 18.500 – 19.250 | **Bottom coupling** | Pilot / overlap with Stage 2 stent (**Ø5.750** land) |
| 0.750 – 3.250 | 19.250 – 21.750 | **Collapsed pocket** | Segments nested @ **R ≈ 2.955 – 3.100 in** |
| 3.250 – 7.250 | 21.750 – 25.750 | **Helix actuation** | **SHEX-002** guide + segment travel; **4.0 in** mandrel stroke |
| 7.250 – 7.500 | 25.750 – 26.000 | **Lock land** | Top retainer / anti-backout |

*Segment centre **Z = 20.875 in** (local **2.375 in**) — matches CAD generator.*

---

## 3. Part — SHEX-010 Support sleeve *(manufacturing: DWG-012-SHP)*

**Material:** 17-4 PH H900  
**Role:** Fixed steel shell — does **not** expand with iris.

### 3.1 Shop drawing (run-in — what machinist builds)

| Feature | Dimension (in) | Tolerance | Notes |
|---------|----------------|-----------|-------|
| **OD** | **1.688** | +0.000 / −0.005 | **Run-in max** — same as plug body |
| **Length** | **7.500** | ±0.010 | Full module |
| **ID** | Per mandrel + segment pocket | +0.003 / −0.000 | **Ø1.550** mandrel clearance min |
| **16 guide slots** | **22.5°** spacing | ±0.5° | All features within **1.688 OD** envelope |
| Mandrel clearance | **Ø1.560** min | — | Over **Ø1.550** mandrel |

**Do not use** `SHEX-010_stage3_support.stp` OD (**Ø5.750**) on the shop drawing — that STEP is **set-reference envelope** only.

### 3.2 Set illustration only (DWG-002-SET)

| Feature | Value | Notes |
|---------|-------|-------|
| Substrate OD | **Ø5.750** | After Stage 2 expansion — visualization context |
| Deployed module OD | **Ø8.650** | Segments extend outside sleeve |
| STEP / `plug_set_assembly.stp` | Reference | For **`-SET`** assembly, not **`-SHP`** |

---

## 4. Part — SHEX-002 Helix guide

**Material:** Inconel 718  
**Role:** Double-start helical path; converts mandrel **axial + rotation** to segment radial motion.

| Feature | Value | Notes |
|---------|-------|-------|
| **Form** | **Double-start helix** | 2 parallel grooves 180° apart |
| **Lead** | **4.0 in** | Axial advance per **one full rotation** |
| **Active length** | **~4.0 in** | Overlaps mandrel cam zone **Z = 19.0 – 23.0** |
| **Groove width** | **0.250** | ±0.005 — segment follower pin |
| **Groove depth** | **0.125** | ±0.003 |
| **Install position** | Local **Z′ = 3.25 – 7.25** | Fixed to **SHEX-010** or mandrel — *validate both options in skeleton* |

**Preferred architecture (Rev A):**

- **SHEX-002** = insert ring(s) fixed in **SHEX-010** bore.
- **SHEX-011** mandrel carries **helical cams** (§12.5) that drive segment followers in **SHEX-002** grooves.

**Fusion:** Model from helix path (Insert → Coil / sweep) using **lead 4.0 in**, **2 starts**, **2 rev** over **4.0 in** axial.

**Reference schematic:** `dxf/DWG-002_iris_module_assy.dxf` — VIEW 3 “LEAD 4.0 IN”.

---

## 5. Part — SHEX-001 Iris segment (×16)

**Material:** 17-4 PH H900  
**Qty:** 16 per module  
**Finish:** Electropolish; break sharp edges **0.025 in** max

| Feature | Dimension (in) | Tolerance | Notes |
|---------|----------------|-----------|-------|
| **Angular span** | **22.5°** | ±0.5° | 16 segments / 360° |
| **Axial length** | **2.750** | ±0.010 | — |
| **Thickness** | **0.187** | ±0.005 | Production; 0.125 marginal @ 5000 psi FEA |
| **Inner radius R1** | **2.955** | — | = 5.750/2 + **0.080** |
| **Outer radius R2** | **4.318** | — | = 8.650/2 − **0.015** |
| **Radial travel** | **1.363** | — | R2 − R1 |
| **Root fillet** | **R0.030** min | — | Toe / root |
| **Toe chamfer** | **0.25 × 45°** | — | — |
| **Helix follower slot** | **0.625 × 0.125** | — | Engages **SHEX-002** *(Detail D, DWG-001)* |

**Segment centre Z (plug):** **20.875 in**  
**Pattern:** **Circular pattern 16× @ 22.5°** about plug centreline.

**Fusion:** Import one `SHEX-001_iris_segment.stp` → refine profile → **Pattern → Circular** 16 instances.

**Reference schematic:** `dxf/DWG-001_iris_segment.dxf`

---

## 6. Deployment kinematics

| Parameter | Value |
|-----------|-------|
| Mandrel stroke (Phase 4) | **4.0 in** + **~2 rev** |
| Radial travel per segment | **1.363 in** |
| Expansion ratio (Stage 3) | **8.650 / 5.750 = 1.50×** |
| Setting force *(typ)* | **~12 klbf** at iris *(see `docs/SETTING_SEQUENCE.md`)* |

**Run-in:** Mandrel index **0**; segments inside **Ø5.750** pocket.  
**Set end:** Mandrel **+4.0 in**; segments at **Ø8.650** OD envelope.

---

## 7. Fusion project structure

```
Plug/
├── 05_SHEX-002_helix_guide          ← DWG-002A-SHP (manufacturing)
├── 06_SHEX-001_iris_segment         ← DWG-001-SHP
├── 07_SHEX-010_support_sleeve       ← DWG-012-SHP @ OD 1.688
├── 08_stage3_iris_module_SET        ← DWG-002-SET (set illustration only)
└── 99_plug_SET                      ← DWG-003-SET plug GA
```

### 7.1 Manufacturing models (`-SHP`) first

Build and release **DWG-012-SHP**, **DWG-001-SHP**, **DWG-002A-SHP** before the set illustration.

### 7.2 Set illustration assembly (`-SET`)

| Step | Action |
|------|--------|
| **1** | Create **`08_stage3_iris_module_SET`** — label drawing **NOT FOR MANUFACTURE** |
| **2** | Insert **`-SHP` part models** OR import `plug_set_assembly.stp` as reference |
| **3** | Position segments **deployed** to **Ø8.650**; use set envelopes if needed |
| **4** | Drawing **DWG-002-SET** — no run-in OD dims required; balloon to **-SHP** part numbers |
| **5** | Export PDF → `export/drawings/set_viz_pdf/` |

### 7.3 Manufacturing modeling order

| Step | Action |
|------|--------|
| **1** | Model **SHEX-010** @ **OD 1.688 × 7.5 L** + **16 guide slots** → release **DWG-012-SHP** |
| **2** | Model **SHEX-001** segment profile → release **DWG-001-SHP** |
| **3** | Model **SHEX-002** helix (fits inside 1.688 bore) → release **DWG-002A-SHP** |
| **4** | Optional: run-in assy check with mandrel @ **OD ≤ 1.688** — interference only |

### 7.4 Set illustration validation (DWG-002-SET)

| Config | Mandrel ΔZ | Segment state | Check |
|--------|------------|---------------|-------|
| **RUN-IN** *(reference)* | **0** | Nested in pocket | OD **≤ 1.688** |
| **DEPLOYED** | **+4.0 in** | Full radial travel | OD **8.650**; no clash with casing drift **8.679** |

Use **Fusion Configurations** in the **`-SET`** assembly only.

### 7.5 Skeleton cross-check

| Tier | Condition | Module OD | Z |
|------|-----------|-----------|---|
| **-SHP** | Run-in | **1.688** | 18.5 – 26.0 |
| **-SET** | Deployed | **8.650** | 18.5 – 26.0 |

---

## 8. Required drawing views

### DWG-012-SHP (SHEX-010 sleeve — manufacturing)

| View | Scale | Content |
|------|-------|---------|
| A | **1:2** | Half-section — **OD 1.688** × **7.5 L** |
| B | **1:1** | End view — slot pattern |
| C | **2:1** | Slot detail |

### DWG-002-SET (module — set illustration)

| View | Scale | Content |
|------|-------|---------|
| A | **1:4** broken | Module **7.5 in** — **deployed OD 8.650** |
| B | **1:4** section | Helix zone |
| C | **1:2** plan | **16 segments @ 22.5°** deployed |

---

## 9. Dimension checklist

### Manufacturing (`-SHP`)

- [ ] Module length **7.500** @ plug **Z = 18.500 – 26.000**
- [ ] Support sleeve **SHEX-010** OD **1.688** × **7.500** *(see support sleeve spec)*
- [ ] Helix guide **SHEX-002** lead **4.0 in**, double-start
- [ ] Segments **16× SHEX-001** @ **22.5°**, **t = 0.187**, **L = 2.750**
- [ ] Mandrel helix cams @ **Z = 19.0 – 23.0** *(SHEX-011 §12.5)*

### Set illustration (`-SET`) only

- [ ] Deployed OD **8.650** vs drift **8.679**
- [ ] Inner / outer segment radii **2.955 / 4.318** in deployed view

---

## 10. General notes (assembly drawing)

```
1. UNLESS OTHERWISE SPECIFIED, DIMENSIONS ARE IN INCHES.
2. STAGE 3 IRIS MODULE — ITEM 6 ON PLUG GA (DWG-003-SET).
3. THIS DRAWING TIER: see title block — SHP = MANUFACTURE / SET = ILLUSTRATION ONLY.
4. DEPLOY: SETTING TOOL AXIAL 4.0 IN + ROTATION (~2 REV) ON MANDREL.
5. MANUFACTURING PARTS: SHEX-010 @ OD 1.688 | SHEX-001 ×16 | SHEX-002.
6. SET ILLUSTRATION: DEPLOYED OD 8.650 IN — NOT A MACHINING DIMENSION.
```

---

## 11. Related files

| File | Purpose |
|------|---------|
| `SHEX-011_inner_mandrel.md` §12.5 | Mandrel helix cam zone |
| `docs/SETTING_SEQUENCE.md` § Phase 4 | Setting sequence |
| `config/design_uhex_54in.yaml` → `stage3_iris` | Segment count, stroke, material |
| `cad/plug_visual.py` → `MODULES` | Stack OD/ID |
| `output/stl/stage3_iris/` | Visual STLs *(run `generate_stage3_iris.py`)* |

---

*Rev A — Stage 3 iris module assembly spec for Fusion modeling.*
