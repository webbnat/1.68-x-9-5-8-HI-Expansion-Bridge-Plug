# Rev B — DCN-12 (CURRENT)

Complete tool: **47 bodies (run-in) / 48 bodies (set)**.

Adds the **SHEX-017 sequence/initiation sub** (+ 017A arming sleeve, 017B
reference piston) implementing DCN-12: commanded initiation (CT applied
differential + ball seat, or e-line EFI gate), completion-gated sequencing, and
the EQ pilot interlocked to close first.

## Contents
- `engineering/` — analysis scripts + data, incl. `trigger_design.py` and
  `FIRST_STROKE_TRIGGER.md` (SHEX-EM-001).
- `design/` — `MANUAL.md`, `SETTING_TOOL_MANUAL.md`, `ACTUATOR_MANUAL.md`
  (Rev B), `figures/`.
- `part-specs/` — per-part shop specs.
- `drawings/dxf`, `drawings/pdf` — incl. **ACT-DWG-017**.
- `step/parts` — incl. **SHEX-017 / 017A / 017B**.
- `step/assemblies` — AK-20 interface + ACT-S12 subs (23 bodies, with 017).
- `step/full-tool`, `stl/full-tool` — **complete run-in & set tool** (47/48).
- `previews/` — full-tool isometric + section renders.
