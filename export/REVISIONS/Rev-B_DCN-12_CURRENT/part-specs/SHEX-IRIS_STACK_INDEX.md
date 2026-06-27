# Stage 3 Iris Stack — Manufacturing Focus

**Plug item 6** | **Z = 18.500 – 26.000 in** | **Module length 7.500 in**

**Deferred:** SHEX-013 equalizing sub — pick up after iris stack is released.

---

## Manufacturing drawings (`-SHP`) — build in this order

| Order | Part | Drawing | Spec sheet | Fusion design |
|-------|------|---------|------------|---------------|
| **1** | Support sleeve | **DWG-012-SHP** | `SHEX-010_support_sleeve.md` | `build_SHEX_010_support_sleeve` |
| **1a** | Stage 1 stent | **DWG-009-SHP** | *(generate_drawings)* | `build_SHEX_008_stage1_stent` |
| **1b** | Stage 2 stent | **DWG-011-SHP** | *(generate_drawings)* | `build_SHEX_009_stage2_stent` |
| **2** | Helix guide | **DWG-002A-SHP** | `SHEX-002_helix_guide.md` | `build_SHEX_002_helix_guide` |
| **3** | Iris segment ×16 | **DWG-001-SHP** | `SHEX-001_iris_segment.md` | `06_SHEX-001_iris_segment` |
| **4** | Run-in assy check | — | `SHEX-010_stage3_iris_module.md` §7 | `build_iris_run_in_assy_rev1` |
| **4b** | Cascade run-in (S1–S3) | — | cascade Rev1 | `build_expansion_cascade_run_in_assy_rev1` |
| **5** | Set illustration | **DWG-002-SET** | Module spec §7.2 | `build_iris_set_assy_rev1` |
| **5b** | Cascade SET (S1–S3) | — | cascade Rev1 | `build_expansion_cascade_set_assy_rev1` |

**Set viz only (after `-SHP` parts):** `DWG-002-SET`, `DWG-003-SET`.

---

## Run-in rule (manufacturing)

| Part | Max cylindrical OD on shop drawing |
|------|-------------------------------------|
| **SHEX-010** sleeve | **1.688 in** |
| **SHEX-002** helix insert | **≤ 1.560 in** OD (fits in sleeve bore) |
| **SHEX-001** segment | **Profile part** — not a turned OD; EDM/laser from plate |

**SHEX-001** is dimensioned in **deployed arc geometry** (radii to **Ø8.650**). Sixteen segments are **nested in the sleeve at assembly**, then the module is **crimped to 1.688 OD** for run-in — same concept as stent sleeves.

---

## Stack section (run-in — manufacturing)

```
        ┌──────────────────────────────  OD 1.688  ── SHEX-010
        │  ┌─ 16× SHEX-001 segments (nested in annulus)
        │  │  ┌─ SHEX-002 helix grooves (fixed in sleeve bore)
        │  │  │  ║  SHEX-011 mandrel Ø1.550 + helix cams §12.5
        │  │  │  ║
        └─────────┴──┴──────────────────
              ← 7.500 in →
```

---

## Mandrel interface (SHEX-011 — complete)

| Mandrel feature | Plug Z | Mates |
|-----------------|--------|-------|
| Helix cams (2-start, L=4.0) | **19.0 – 23.0** | **SHEX-002** + segment followers |
| Smooth bearing | 18.5 – 19.0, 23.0 – 26.0 | Sleeve bore |

---

## Key numbers (all tiers)

| Parameter | Run-in (`-SHP`) | Set (`-SET` viz only) |
|-----------|-----------------|------------------------|
| Module OD | **1.688** | **8.650** |
| Mandrel | **Ø1.550** | **Ø1.550** |
| Iris stroke | — | **4.0 in** + **~2 rev** |
| Segments | **16 @ 22.5°** | Deployed to casing |

---

## Related files

| File | Purpose |
|------|---------|
| `SHEX-010_support_sleeve.md` | Sleeve shop drawing spec |
| `SHEX-002_helix_guide.md` | Helix insert shop drawing spec |
| `SHEX-001_iris_segment.md` | Segment EDM shop drawing spec |
| `SHEX-010_stage3_iris_module.md` | Module + set viz guide |
| `SHEX-011_inner_mandrel.md` §12.5 | Mandrel helix cams |
| `config/design_uhex_54in.yaml` | `stage3_iris` block |

---

*Use this index as the manufacturing entry point for the iris stack.*
