# SHEX-BP-UHEX-54 — Forward Plan

Living to-do / decision queue. Companion: [`WORKING_LOG.md`](WORKING_LOG.md).
Status keys: [ ] open, [~] in progress, [x] done, [!] blocked/decision needed.

---

## Active: setting-tool package (session 2)

- [x] Review repo setting-tool state; verify existing SHEX-AK-20 outputs.
- [x] Web-verify market tool stroke/force/OD (E-4 #05/#10/#20, Model J, B-series, HST).
- [x] Reconcile two-actuator "two-stroke" architecture vs 10/11.5 in stroke story.
- [x] Setting-tool manual (`SETTING_TOOL_MANUAL.md`): design+assumptions,
      market comparison, manufacturing, rig-up/operations.
- [x] Manual figures (string GA, interface section rigged/released, two-stroke,
      market conflict, stroke budget).
- [x] Verify SHEX-AK-20 STEP + ST-DWG drawings; render previews.
- [x] Update RELEASE_NOTES to include the kit + setting-tool manual.
- [x] Final verification pass; update WORKING_LOG.

## Active: stage 1/2 internal actuators (session 3) — COMPLETE

- [x] Establish annulus budget (0.146 in radial) and expansion targets.
- [x] Engineering analysis (`actuator_design.py`): pressures, forces, sizing.
- [x] Decide mechanism: DCN-10 ductile stent; DCN-11 stage-2 = 2nd bladder,
      Belleville = hold-only; energy = well pressure (CT / hydrostatic).
- [x] CAD (`cad/actuator_solids.py`) + STEP/STL parts & run-in/deployed
      assemblies (`generate_actuators.py`); round-trip verified.
- [x] Drawings ACT-DWG-014A/014B/014C/015/016 (DXF+PDF).
- [x] Figures + `ACTUATOR_MANUAL.md` (SHEX-MAN-003); RELEASE_NOTES updated.

## Open engineering items (carried, not resolved here)

- [!] **Actuator FEA + full-scale test.** Mesh plastic expansion (pressure,
      strain, fatigue, post-expansion recoil stiffness) per stage; bladder +
      stent deploy test in a representative annulus. First-order hand calcs only.
- [ ] **Burst-disk / orifice selection.** Crack pressures p1<p2 vs the well
      hydrostatic window per conveyance/depth; metering-orifice delay across temp.
- [ ] **Ratchet retrieval kinematics.** How the deployed stents re-collapse and
      the body-lock rings release on pull-out (inherited open item).
- [ ] **Mandrel update.** Add the charge-port drillings + ratchet bands to the
      SHEX-011 mandrel drawing/model (currently referenced, not cut on the part).
- [ ] **DCN-10 propagation.** Update SHEX-008/009 shop sheets to the ductile
      expandable alloy.
- [!] **Thru-tubing force conflict.** 45 klbf needs a ~3.8 in (#20) tool that
      cannot pass small tubing. Decision needed: (a) accept casing/large-bore
      deployment for the #20 kit (current assumption), or (b) re-architect
      seals+slips as pressure-energized so a ≤1.9 in / ≤10 klbf thru-tubing
      tool can set it. Affects whether "thru-tubing" is literal.
- [!] **Setting-force FEA.** 45 klbf release stud is an estimate; the real
      iris+seal+slip resistance is unverified (plug open item, MANUAL §1.10).
- [ ] **ST-DCN-3 thread verification.** Crosslink-sleeve and setting-mandrel
      thread callouts (3.250-8 UN, 1.500-12 UNF) are assumed; confirm against
      the specific tool make/serial before cutting the kit.
- [x] **First-stroke trigger / EQ interlock (DCN-12)** — designed AND built into
      a new revision. Memo `export/analysis/FIRST_STROKE_TRIGGER.md` (SHEX-EM-001)
      + `trigger_design.py`; commanded initiation (CT applied dP + ball seat /
      e-line EFI gate) + completion-gated sequencing + EQ pilot closes first;
      fail-safe states defined.
      - [x] CAD **SHEX-017** sub + **017A** arming sleeve + **017B** reference
            piston; wired into `add_actuator_hardware` (full tool Rev B 47/48).
      - [x] Drawing **ACT-DWG-017** (DXF+PDF, 3 views).
      - [x] `ACTUATOR_MANUAL.md` **Rev B** (§1.4–1.6, §4, DCN-12) + RELEASE_NOTES.
      - [x] `fig_act_trigger` schematic + DCN-12 sequence figure.
      - [!] **Still test/FEA-dependent (cannot close on paper):** EFI/gas-gen
            qualification; arming-sleeve + shear-pin calibration vs temperature;
            full-scale completion-gating deploy test; ball-seat / Model-J
            pressure interface; **SHEX-013 arming-port + SHEX-011 manifold
            drillings** to be cut on the actual mandrel/sleeve drawings.
- [ ] **Owen / Schlumberger interface variants.** Repeat-precision / Owen #20
      clones share the Baker interface; a Schlumberger-specific adapter would
      need that tool's bottom-sub drawing.

## Superseded / parked

- [x] (parked) Bespoke electromechanical SHEX-ST-54 — reference only; not a
      practical deliverable. Files kept under `First Pass Files/` and
      `export/analysis/setting_tool_design.py`.
