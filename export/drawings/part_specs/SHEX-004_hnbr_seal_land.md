# SHEX-004 — HNBR Seal Land Liner — Mold / Part Spec

**Drawing No:** DWG-007B-SHP  
**Part No:** SHEX-004  
**Qty:** **4** per plug (items **7–10**)  
**Material:** HNBR **90 durometer** (Shore A)  
**Tier:** **MANUFACTURING** — **molded elastomer preform** *(thin liner — not full seal OD)*  
**Module ref:** Seal lands | Schematic: `dxf/DWG-007_seal_land_module.dxf`

---

## 1. Function

Molded **thin HNBR liner** in each seal land module. **SHEX-005** petals provide anti-extrusion structure and carry the liner **outward** during setting; the liner **finishes** the seal face against casing.

| Parameter | Value |
|-----------|-------|
| Seal lands per plug | **4** |
| Petals per land | **16** (**SHEX-005**) |
| **Set contact OD** *(in-well)* | **Ø8.720 in** |
| **Run-in module OD** *(nested)* | **Ø1.688 in** |
| Mandrel | **Ø1.550 in** |

### 1.1 Cascade nesting (Option B — authoritative)

**No single element expands from 1.688″ to 8.720″.** Total expansion is the **product of nested stages** — each module runs at **run-in OD** until its stage opens the bore for the next:

| Stage | Item | Run-in OD | Set OD | Mechanism |
|-------|------|-----------|--------|-----------|
| 1 | Stent + bladder | **1.688** | **3.375** | Internal bladder |
| 2 | Stent + Belleville | *(nested)* | **5.750** | Internal wedge |
| 3 | Iris + sleeve | *(nested)* | **8.650** | Helix + 16 segments |
| **4** | **Seals + petals** | *(nested)* | **8.720** | Petals deploy + liner stretch + mandrel compress |

Seal modules **ride inside** the collapsed cascade at **Ø1.688** (same body envelope as **SHEX-010**). After Stage 3 opens the bore to **~Ø8.650**, petals and HNBR **only finish the last ~0.035″ radial** to seal OD and casing drift **8.679″** — they are **not** storing a solid **Ø8.720 × 4.5″** rubber donut at run-in.

**Shop mold (this drawing):** **run-in preform** only.  
**Set OD 8.720:** **in-well energized envelope** — see **DWG-007-SET** / `build_seal_stack_assy` *(illustration)*.

---

## 2. Molded preform geometry (authoritative — DWG-007B-SHP)

Thin **carrier-wall liner** at petal zone. Datum: **Z′ = 0** at land bottom; liner centre **Z′ = 2.250**.

| Feature | Dimension (in) | Tolerance | Notes |
|---------|----------------|-----------|-------|
| **Radial thickness t** | **0.050** | ±0.005 | In **0.063** carrier wall |
| **Inner radius Ri** | **0.781** | +0.005 / −0.000 | At **Ø1.562** carrier bore |
| **Outer radius Ro** | **0.831** | ±0.005 | Within **Ø1.688** OD |
| **Axial length L** | **0.550** | ±0.010 | Matches **SHEX-005** active zone |
| **Angular coverage** | **360°** | — | Continuous ring per land |

*Not molded:* full **4.500** land height; **Ø8.720** set OD — those are module / performance limits.

### 2.1 Set envelope *(illustration only — not mold)*

| Feature | Value | Notes |
|---------|-------|-------|
| Contact OD | **8.720** | After petals @ **R2 4.011** + liner stretch |
| Energize | Mandrel **+Z** | **SHEX-011** §12.6 ramps — axial compression |

### 2.2 Mold detail

| Feature | Notes |
|---------|-------|
| Parting line | **Mid-thickness** *(typ)* |
| Draft | **1°** min |
| Flash | **≤0.010** |
| Bond | Mechanical grip in carrier — **no bond to petal faces** |

---

## 3. Position in plug stack

| Land | Item | Plug **Z** | Module **Z′** |
|------|------|------------|---------------|
| **1** | 7 | **26.0 – 30.5** | 0 – 4.5 |
| **2** | 8 | **30.5 – 35.0** | 0 – 4.5 |
| **3** | 9 | **35.0 – 39.5** | 0 – 4.5 |
| **4** | 10 | **39.5 – 44.0** | 0 – 4.5 |

---

## 4. Fusion workflow

| Script | Purpose |
|--------|---------|
| `build_SHEX_004_hnbr_seal_land` | One **preform liner** (molded part) |
| `build_SHEX_004_hnbr_mold` | Mold cavity + preform check |
| `build_seal_run_in_assy` | **4× nested lands** — 64 petals + 4 liners @ **1.688** |
| `build_seal_stack_assy` | **SET illustration** — energized envelope @ **8.720** |

---

## 5. General notes

```
1. UNLESS OTHERWISE SPECIFIED, DIMENSIONS ARE IN INCHES.
2. MATERIAL: HNBR 90 DUROMETER (SHORE A).
3. QTY: 4 PER PLUG (ITEMS 7–10).
4. MOLD THE RUN-IN PREFORM ONLY — NOT THE SET OD 8.720 CUP.
5. PETALS (SHEX-005) DEPLOY FIRST; LINER STRETCHES WITH PETAL BACKS.
6. MODULE OD AT RUN-IN = 1.688 (NESTED IN CASCADE) — NOT RADIAL CRIMP OF 8.720 RUBBER.
7. POST-MOLD TRIM FLASH; NO MOLD RELEASE IN SEAL ZONE.
```

---

*Rev B — Option B: thin preform + nested cascade; SET OD is in-well envelope.*
