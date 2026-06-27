# SHEX-BP-UHEX-54 — Working Log

Reverse-chronological engineering log. Newest entry on top. Each entry:
date, who, what changed, why, and what to check next. Companion file:
[`FORWARD_PLAN.md`](FORWARD_PLAN.md).

---

## 2026-06-13 — Revision archive (clear Rev A vs Rev B separation)

**Author:** Fable (AI), session 3 (cont.).

**Why:** user could not tell old-revision vs new-revision parts apart and asked
for each revision's full deliverable set in one folder, with the complete
run-in & set tool STL in the latest folder.

**What changed:**

- Added `build_revisions.py` and an `INCLUDE_SEQ_SUB` toggle in
  `cad/actuator_solids.py` (skips the DCN-12 sub to reconstruct pre-DCN-12).
- Built `export/REVISIONS/` with two **self-contained** snapshots, each holding
  engineering / design / part-specs / drawings(dxf+pdf) / step(parts,
  assemblies, full-tool) / stl(full-tool + sub-assemblies) / previews:
  - **`Rev-B_DCN-12_CURRENT/`** — latest. Complete tool **47 / 48 bodies**;
    includes SHEX-017/017A/017B, ACT-DWG-017, trigger memo, ACTUATOR_MANUAL
    Rev B. Full-tool STL copied from current build (run-in 28.5 MB, set 140 MB).
  - **`Rev-A_DCN-01-11_PREVIOUS/`** — regenerated with the trigger sub OFF:
    complete tool **44 / 45 bodies** (run-in 27.6 MB, set 139 MB), no SHEX-017 /
    ACT-DWG-017 / trigger files; carries a Rev-A scope note in place of the
    Rev B actuator manual.
- `export/REVISIONS/README.md` indexes both revisions + the full DCN history.
- Canonical working copies under `export/release/`, `export/full_tool/`,
  `export/analysis/` are unchanged; the archive is the clean per-revision view.

**Check next:** revisions are file snapshots; regenerate via `build_revisions.py`
if parts change. Open engineering items unchanged (FORWARD_PLAN).

---

## 2026-06-13 — DCN-12 built into a new revision (SHEX-017 + full-tool Rev B)

**Author:** Fable (AI), session 3 (cont.).

**Why:** user approved building the DCN-12 trigger/interlock architecture and
asked for it in a new revision.

**What changed:**

- `cad/actuator_solids.py`: new builders **SHEX-017** sequence/initiation sub
  (gate + EFI/pilot port + manifold + metering orifice + ref-piston seal lands),
  **SHEX-017A** stage1->2 arming sleeve (shear-pinned shuttle), **SHEX-017B**
  reference/ball-seat piston. Wired into `add_actuator_hardware` (rides the
  mandrel group), so they appear in every assembly incl. the full tool.
- `generate_actuators.py`: 3 new parts exported (round-trip OK, 1 solid each);
  sub-assemblies now 23 bodies (was 20).
- `export/drawings/generate_actuator_drawings.py`: **ACT-DWG-017** (3 views:
  housing / arming sleeve / reference piston) DXF+PDF; QA-rendered, labels and
  title-block clearances fixed.
- `figures_actuators.py`: updated `fig_act_sequence` to the DCN-12 story; added
  **`fig_act_trigger`** (why passive fails | commanded+completion-gated chain).
- `ACTUATOR_MANUAL.md` -> **Rev B**: new §1.4-1.6 (energy / trigger DCN-12 /
  sequence), §4.2-4.4 (CT ball+dP / e-line EFI ops + fail-safe state table),
  Part-3 SHEX-017 rows, **DCN-12** in Part 5, refreshed open items + file index.
- `RELEASE_NOTES.md`: DCN-12 entry + SHEX-017 / memo / full-tool Rev B index.
- `generate_full_tool.py`: manifest tagged **revision B**; regenerated
  `export/full_tool/` -> RUN-IN **47 bodies**, SET **48 bodies** (+3), STL +
  previews refreshed.

**Verification:** all 10 actuator parts export as single solids; full tool both
states build clean (47/48); previews confirm slim run-in and staged set.

**Status:** DCN-12 design BUILT (CAD/drawings/manual/figures/full-tool Rev B).
Remaining items are test/FEA-dependent (EFI/gas-gen qual, shear-pin calibration,
completion-gating deploy test, ball-seat/Model-J interface) — carried in
FORWARD_PLAN.

---

## 2026-06-13 — First-stroke TRIGGER + EQ interlock worked properly (DCN-12 proposed)

**Author:** Fable (AI), session 3 (cont.).

**Why:** the top open item — the trigger / equalizing-sleeve interlock that
makes the "first stroke" *real* — was only ever a narrative (burst disk
p1<p2 + 30 s orifice + "pilot cracks first"). Pressure-tested it; it does not
hold up.

**Key finding (proven, not asserted):** a passive burst disk referenced to a
sealed/atmospheric chamber sees **absolute hydrostatic**, which rises while
running in, so it **fires on the way down, not at depth**. There is no single
absolute-pressure setting that survives run-in to a deep target *and* fires
only at target depth (`trigger_design.py` §1). Order also isn't enforced
(p1/p2 a few hundred ft apart) and stage-2's 1898 cc can't come from any
annulus-fit chamber — it must come from the well. So passive pressure
triggering is **fatally** position-blind.

**Proposed fix (DCN-12):** separate the three jobs the old concept conflated —
- **Energy/volume** = the well (CT pump fluid, or wellbore hydrostatic), *gated*.
- **Initiation** = a position-correct **command**: CT applied differential
  (+~1500 psi over annulus, depth-independent) + ball seat; or e-line **EFI
  gate** that opens and lets hydrostatic fill (mirrors the E-4).
- **Sequencing** = **completion-gated**: each stent's bottom-out pressure
  climb shifts a shear-pinned arming sleeve (~1720 psi) that uncovers the next
  stage's feed port. The EQ pilot (SHEX-016A) strokes first → closes SHEX-013 →
  uncovers stage-1 port, so EQ-close-before-S1 is mechanically guaranteed.
Defines fail-safe states (collapsed / EQ-only / S1-only / S1+2 / set) and a
shift-to-release retrieval path. Adds new sub **SHEX-017** (gate + ball seat +
reference piston + arming sleeve + manifold); re-tasks SHEX-013/014C/015E/016A.

**Work done:** `export/analysis/trigger_design.py` (+ `.json`) — proves §1,
sizes the CT margin, e-line hydrostatic window, completion-shift pressure,
pilot force, stage-2 fill time (~tens of s), fail-safe table, full sequence.
`export/analysis/FIRST_STROKE_TRIGGER.md` (SHEX-EM-001) — the engineering memo.

**Status:** architecture defined + grounded; **DCN-12 proposed, not yet built**
into CAD/drawings/manual (offered as next step, awaiting go-ahead). FORWARD_PLAN
item moved to in-progress with the build plan.

---

## 2026-06-13 — Complete full-tool rebuild (plug + actuators), new folder

**Author:** Fable (AI), session 3 (cont.).

**Why:** the existing full-tool assemblies (`export/release/.../SHEX-BP-UHEX-54_
RUN-IN/_SET`) predated the stage 1/2 actuators and did not contain them. User
asked for fresh run-in and set tools built from all current parts, in a new
folder.

**What changed:**

- `cad/actuator_solids.py`: factored the hardware registration into
  `add_actuator_hardware(m, bladder_state, dz)` so it can be injected into any
  assembly with the correct mandrel-group shift.
- `cad/release_solids.py` `build_assembly()`: now injects the SHEX-014/015/016
  actuator hardware (mandrel-mounted → rides the mandrel group; bladders shown
  folded/spent in both end states, the inflated transient stays in
  `SHEX-ACT-S12_DEPLOYED`). Stent material updated to ductile per DCN-10.
- `generate_full_tool.py`: new generator → **`export/full_tool/`**.

**New deliverable (`export/full_tool/`):**

- `step/SHEX-BP-UHEX-54_FULL_RUN-IN.stp` (44 bodies) and `..._FULL_SET.stp`
  (45 bodies incl. casing ref) — the single complete tool model.
- `stl/` meshes + `png/` iso & section previews (run-in uses radial-exaggerated
  view; set uses true proportions, casing hidden).
- `manifest_full_tool.json` (body lists per state).

**Verification:** both STEP build clean (44 / 45 bodies); previews confirm the
slim Ø1.688 run-in and the staged set geometry (slips, stage 1/2, iris, 4 seal
lands, MTM, mandrel pin extended +10).

**Note:** `build_assembly` is now canonical for the complete tool, so re-running
`generate_release.py` would also pick up the actuators. The pre-existing
`export/release/.../SHEX-BP-UHEX-54_{RUN-IN,SET}` files were left untouched.

---

## 2026-06-13 — Stage 1/2 internal actuators (session 3, IN PROGRESS)

**Author:** Fable (AI), session 3.

**Goal:** design the internal stage-1/2 actuators that the two-actuator
architecture depends on (the "first stroke"). Until now these were referenced
(`SHEX-014` bladder, `SHEX-015` Belleville) but never engineered or modelled.
Carried as the top open item in FORWARD_PLAN.

**Geometry budget established (from `cad/release_solids.py`):**

- Stage-1 zone Z 9.5–13.5 (4.0 in); Stage-2 zone Z 13.5–18.5 (5.0 in).
- Mandrel is necked to **Ø1.270** (the DCN-1 helix neck, Z 10.4–25.9) through
  both zones → annulus radius 0.635.
- Stent sleeves (SHEX-008/009): ID 1.562 (r 0.781), OD 1.688, wall 0.063.
- **Available annulus = 0.781 − 0.635 = 0.146 in radial** (0.292 diametral) —
  this is the entire space the actuators must live in. Tight.
- Expansion targets: stage 1 OD 1.688→3.375 (ΔR 0.844/side); stage 2
  3.375→5.750 (ΔR 1.188/side). Neither contacts the 8.679 casing drift.

**Key early finding (drives the mechanism choice):** a self-contained stored-
energy spring/Belleville big enough to expand a stent (~10 klbf-class radial)
cannot fit a 0.146-in annulus. Therefore the actuators are **pressure-driven**
(wellbore hydrostatic / applied CT pressure admitted through a burst disk),
with the Belleville stack repurposed as the **hold-open / preload** element
rather than the prime mover. Documented as DCN-11 (see analysis).

**Mechanism decisions (corrections to the inherited concept):**

- **DCN-10** — stents SHEX-008/009 re-specified 17-4 PH H900 → ductile
  expandable alloy (annealed 316L / Ni): a balloon-expandable mesh must
  plastically hinge ~2x; H900 cracks.
- **DCN-11** — stage 2 prime mover changed from Belleville/swage wedge → a
  **second inflatable bladder**. A rigid expander starting ≤ stent ID 1.562
  cannot grow to back the Ø5.624 deployed stent in a 0.146-in annulus
  (geometrically impossible; an annulus-fit Belleville is ~2 orders of
  magnitude short on force). Belleville retained as hold-open/anti-recoil only.
- Energy source = **the well**: applied CT pump pressure, or e-line hydrostatic
  gated by a burst disk vs a sealed reference chamber (SHEX-016). Deploy
  pressures (941/470 psi) sit below hydrostatic even at 3000 ft.

**Work done this session:**

- `export/analysis/actuator_design.py` (+ `.json`): annulus budget, expansion
  pressures/forces, bladder sizing, Belleville check, sequence/interlock,
  open items. Numbers: stage-1 deploy ~941 psi / 433 cc; stage-2 ~470 psi /
  1898 cc; radial forces ~20–25 klbf.
- `cad/actuator_solids.py` + `generate_actuators.py`: 7 machined parts
  (SHEX-014A/014B/014C/015B/015C/016/016A) + run-in & deployed sub-assemblies
  (`SHEX-ACT-S12_*`, 20 bodies each). Round-trip verified — every part 1 solid,
  0 orphan surfaces (`export/release/verify_actuators.py`); previews rendered.
- 5 manual figures (`figures_actuators.py`): run-in & deployed sections,
  first-stroke sequence, pressure budget, why-bladder.
- 5 drawings ACT-DWG-014A/014B/014C/015/016 (DXF+PDF).
- `export/release/manual/ACTUATOR_MANUAL.md` (SHEX-MAN-003): design, sizing,
  manufacturing, arming/operation, DCN-10/11, open items.
- RELEASE_NOTES updated (DCN-10/11 + actuator package index).

**Status: session 3 deliverables COMPLETE.** Remaining items are
data-dependent (FEA, full-scale deploy test, burst-disk/orifice selection,
ratchet retrieval kinematics, add charge-port/ratchet-band to SHEX-011
mandrel drawing) and carried in FORWARD_PLAN.

---

## 2026-06-13 — Setting-tool package (continuation)

**Author:** Fable (AI), session 2.

**Context resumed from:** plug release package complete (STEP + drawings +
`export/release/manual/MANUAL.md`). Setting-tool work had been *started* by a
prior session — SHEX-AK-20 adapter kit STEP/DXF existed — but with no working
log, no market comparison, no CT path write-up, and no setting-tool manual.

**Review findings (before starting):**

1. Two parallel setting-tool lines exist in the repo:
   - **Legacy bespoke electromechanical tool** `SHEX-ST-54` (docs
     `First Pass Files/docs/SETTING_TOOL_DETAIL.md`, config
     `export/config/setting_tool_shex_st54.yaml`, analysis
     `export/analysis/setting_tool_design.py`). 246 in, 3.625 OD, motor +
     ball screw, 12 in stroke, 55 klbf. **Status: superseded** — bespoke
     downhole electromechanical setting tools are a multi-year qualified-vendor
     program, not a deliverable here. Kept for reference only.
   - **Commercial-tool adapter kit** `SHEX-AK-20` (`cad/setting_kit_solids.py`,
     `generate_setting_kit.py`, `export/drawings/generate_kit_drawings.py`).
     **Status: active direction** — this is the right answer and what this
     session completes.
2. Adapter kit already generated (verified on disk):
   - Parts ST-101 (setting sleeve/shoe), ST-102 (tension rod), ST-103
     (calibrated shear stud), ST-104 (stroke spacer) — STEP in
     `export/release/step/parts/`.
   - Assemblies `SHEX-AK-20_INTERFACE_RIGGED.stp` (8 bodies) and
     `..._RELEASED.stp` (9 bodies) in `export/release/step/assemblies/`.
   - Drawings ST-DWG-101/102/103 (DXF + PDF).
   - `export/release/manifest_setting_kit.json`.
3. Plug DCN log already carries the settability decisions:
   - **DCN-7** top joint downsized (Ø1.375 pin, Rev E neck Ø1.450 body) so a
     setting sleeve can pass over the neck and land on the upper slip carrier.
   - **DCN-8** net set stroke re-budgeted 11.0 → **10.0 in** (+0.25 overtravel
     = 10.25 demand) to fit a Baker E-4 No. 20 (10.777 in stroke) and #20 CT
     tools; release stud calibrated **45 klbf**.
   - **DCN-9** iris drive interference fix + module re-index.

**Market data captured (this session, web-verified):**

| Tool | Type | Stroke (in) | Max force (lbf) | OD (in) | Notes |
|---|---|---|---|---|---|
| Baker E-4 #05 | e-line, gas | 5.879 | 10,000 | 1.718 | only size that passes 2-3/8 tubing |
| Baker E-4 #10 | e-line, gas | 5.707 | 35,000 | 2.750 (HD 3.800) | 5-in-class plugs |
| **Baker E-4 #20** | e-line, gas | **10.777** | **55,000** | **3.800** (HD 4.125) | **selected interface** |
| Baker Model J #10/#20 | CT hydraulic | matches E-4 | pressure×pistons | = E-4 size | **same adapter kits as E-4** |
| TechWest B20 / Renown B-20 | CT hydraulic | ~10–11 | 50,000 (stud) | 3.8–4.25 | #20 clone, same adapters |
| Pinnacle HST 425 | CT hydraulic | 11 | pressure×pistons | Baker 20 conn | same adapters as E-4 |
| TechWest B105 / Renown B-10 | CT hydraulic | ~6 | low (thru-tubing) | 1.81 | thru-tubing, low force |

Sources: Baker Hughes E-4 technical unit PDF; Owen MAN-SET-E410; RepeatPrecision
Baker-20; Pinnacle, TechWest, MAP, Renown, Alpha product pages.

**Key reconciliation (the stroke story):**

- The plug is a **two-actuator** machine (confirmed in
  `First Pass Files/docs/SETTING_SEQUENCE.md`):
  - **First / internal actuation** — stage-1 bladder (SHEX-014, burst-disk
    fired) and stage-2 Belleville (SHEX-015) expand the two stent stages
    radially. **This does not draw on the setting tool.** This is the
    "first stroke initiated somehow" — it is initiated by the burst disk /
    arming event, *not* by the setting tool.
  - **Secondary / tool stroke (10.0 in)** — the market setting tool's single
    axial stroke completes stage-3 iris + 4 seal lands + dual slips, then
    shears free. A single-stroke pyrotechnic E-4 or a single-stroke CT
    hydraulic tool both satisfy this because the internal stages have already
    fired before the tool strokes.
- **The real market conflict (this session's headline finding):** a tool that
  delivers 45–55 klbf at the #20 interface is ~3.8 in OD and **cannot pass
  through 2-3/8 / 2-7/8 tubing**. Only the E-4 #05 (1.718 in OD) passes
  small tubing, and it makes just 10 klbf / 5.879 in. Therefore:
  - **SHEX-AK-20 (#20) is for deployment in casing or ≥4-1/2 in tubing/liner**
    where a 3.8 in tool can reach setting depth. This is the realistic
    45-klbf solution and the primary deliverable.
  - **Genuine small-tubing thru-tubing setting** (tool OD ≤1.9 in) caps out
    near 10 klbf, which requires the seal/slip system to be *pressure-energized*
    rather than *stroke-energized*. Logged as an open redesign item, not
    resolved here.

**Work done this session:**

- Created this log + `FORWARD_PLAN.md`.
- Market comparison + stroke/force reconciliation captured (tables above).
- Verified SHEX-AK-20 STEP round-trip (ST-101 L15.000, ST-102 L15.100,
  ST-103 L3.200, ST-104 L0.250; each 1 solid, 0 orphan surfaces) and
  re-rendered interface previews.
- Generated 8 manual figures (`figures_setting.py`): run-string GA, rigged &
  released interface sections, two-actuator architecture, market OD-vs-force
  conflict, stroke budget. Fixed label crowding on GA/two-stroke/market plots.
- Wrote setting-tool manual
  `export/release/manual/SETTING_TOOL_MANUAL.md` (SHEX-MAN-002 Rev A):
  Part 0 why-adapter-not-bespoke, Part 1 engineering design (two-actuator),
  Part 2 market selection + OD-vs-force conflict, Part 3 manufacturing,
  Part 4 rig-up/operations (e-line + CT), Part 5 assumptions/open items.

**Status: session 2 deliverables COMPLETE.** Remaining items are
engineering-data dependent (FEA, internal-actuator design, tool-thread
verification) and carried in FORWARD_PLAN.

**Check next:** see FORWARD_PLAN.

---

## (earlier) — Plug release package

Plug STEP (15 parts + 2 assemblies), 14 manufacturing drawings, and
`export/release/manual/MANUAL.md` completed in session 1. DCN-1..6 resolved
spec contradictions; geometry round-trip verified (1 solid/part, 0 orphan
surfaces). See `export/release/RELEASE_NOTES.md`.
