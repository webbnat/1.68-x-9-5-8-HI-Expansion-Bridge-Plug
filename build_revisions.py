"""Assemble a clear, self-contained revision archive under export/REVISIONS/.

The complete tool has two physical revisions the user cares about:

  Rev A (DCN-01..11, PREVIOUS) - plug + setting kit + stage 1/2 actuators;
        complete tool = 44 (run-in) / 45 (set) bodies; no trigger sub.
  Rev B (DCN-12, CURRENT)      - adds the SHEX-017 sequence/initiation sub;
        complete tool = 47 / 48 bodies.

Each revision folder is self-contained: engineering, design, part-specs,
drawings (dxf+pdf), step (parts/assemblies/full-tool), stl (full-tool +
sub-assemblies), and full-tool previews. Rev B's full tool is copied from the
current build; Rev A's complete tool + actuator sub-assemblies are regenerated
here with the DCN-12 sub switched off (cad.actuator_solids.INCLUDE_SEQ_SUB).

Run:  .venv\\Scripts\\python build_revisions.py
"""

from __future__ import annotations

import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from cad import release_solids as rs
from cad import actuator_solids as acs

REL = ROOT / "export" / "release"
PARTS = REL / "step" / "parts"
ASSY = REL / "step" / "assemblies"
DXF = REL / "drawings" / "dxf"
PDF = REL / "drawings" / "pdf"
MANUAL = REL / "manual"
FIG = MANUAL / "figures"
RELSTL = REL / "stl"
ANALYSIS = ROOT / "export" / "analysis"
SPECS = ROOT / "export" / "drawings" / "part_specs"
FULLTOOL = ROOT / "export" / "full_tool"

OUT = ROOT / "export" / "REVISIONS"
REVA = OUT / "Rev-A_DCN-01-11_PREVIOUS"
REVB = OUT / "Rev-B_DCN-12_CURRENT"

# files that exist only because of DCN-12 (Rev B only)
REVB_ONLY = {
    "SHEX-017_sequence_sub.stp", "SHEX-017A_arming_sleeve.stp",
    "SHEX-017B_reference_piston.stp",
    "ACT-DWG-017_sequence_sub.dxf", "ACT-DWG-017_sequence_sub.pdf",
    "trigger_design.py", "trigger_design.json", "FIRST_STROKE_TRIGGER.md",
    "fig_act_trigger.png",
}


def _mkdirs(base: Path) -> dict[str, Path]:
    d = {
        "engineering": base / "engineering",
        "design": base / "design",
        "figures": base / "design" / "figures",
        "specs": base / "part-specs",
        "dxf": base / "drawings" / "dxf",
        "pdf": base / "drawings" / "pdf",
        "parts": base / "step" / "parts",
        "assemblies": base / "step" / "assemblies",
        "ft_step": base / "step" / "full-tool",
        "ft_stl": base / "stl" / "full-tool",
        "sub_stl": base / "stl" / "sub-assemblies",
        "previews": base / "previews",
    }
    for p in d.values():
        p.mkdir(parents=True, exist_ok=True)
    return d


def copy_glob(src: Path, pattern: str, dst: Path, *, rev_b: bool) -> int:
    n = 0
    for f in sorted(src.glob(pattern)):
        if not f.is_file():
            continue
        if not rev_b and f.name in REVB_ONLY:
            continue
        shutil.copy2(f, dst / f.name)
        n += 1
    return n


def copy_shared(dirs: dict[str, Path], *, rev_b: bool) -> None:
    # engineering (analysis scripts + data); trigger_* only in Rev B
    for pat in ("*.py", "*.json", "*.md"):
        copy_glob(ANALYSIS, pat, dirs["engineering"], rev_b=rev_b)
    # design: plug + setting-tool manuals always; actuator manual is Rev B text
    for name in ("MANUAL.md", "SETTING_TOOL_MANUAL.md"):
        shutil.copy2(MANUAL / name, dirs["design"] / name)
    if rev_b:
        shutil.copy2(MANUAL / "ACTUATOR_MANUAL.md", dirs["design"] / "ACTUATOR_MANUAL.md")
    # manual figures (exclude the DCN-12 trigger figure from Rev A)
    copy_glob(FIG, "*.png", dirs["figures"], rev_b=rev_b)
    # part specs (shared)
    copy_glob(SPECS, "*.md", dirs["specs"], rev_b=rev_b)
    # drawings
    copy_glob(DXF, "*.dxf", dirs["dxf"], rev_b=rev_b)
    copy_glob(PDF, "*.pdf", dirs["pdf"], rev_b=rev_b)
    # step parts (SHEX-017* excluded from Rev A via REVB_ONLY)
    copy_glob(PARTS, "*.stp", dirs["parts"], rev_b=rev_b)
    # sub-assemblies: AK-20 interface always
    copy_glob(ASSY, "SHEX-AK-20_INTERFACE_*.stp", dirs["assemblies"], rev_b=rev_b)
    copy_glob(RELSTL, "SHEX-AK-20_INTERFACE_*.stl", dirs["sub_stl"], rev_b=rev_b)


def render_full_tool(stl_dir: Path, png_dir: Path) -> None:
    sys.path.insert(0, str(REL))
    try:
        from render_previews import render_stl  # type: ignore
    except Exception as e:  # pragma: no cover
        print(f"  (render skipped: {e})")
        return
    for label in ("RUN-IN", "SET"):
        stl = stl_dir / f"SHEX-BP-UHEX-54_FULL_{label}.stl"
        if not stl.exists():
            continue
        max_r = 112.0 if label == "SET" else None
        stretch = label == "RUN-IN"
        try:
            render_stl(stl, png_dir / f"SHEX-BP-UHEX-54_FULL_{label}.png",
                       elev=14, azim=-55, stretch_z=stretch, max_r_mm=max_r)
            render_stl(stl, png_dir / f"SHEX-BP-UHEX-54_FULL_{label}_section.png",
                       elev=8, azim=-90, stretch_z=stretch, max_r_mm=max_r,
                       cut_half=True)
        except Exception as e:  # pragma: no cover
            print(f"  (render {label} skipped: {e})")


def regen_revA(dirs: dict[str, Path]) -> dict:
    """Rebuild Rev A complete tool + actuator subs with the DCN-12 sub OFF."""
    acs.INCLUDE_SEQ_SUB = False
    counts = {}
    try:
        for state, label in (("run_in", "RUN-IN"), ("set", "SET")):
            name = f"SHEX-BP-UHEX-54_FULL_{label}"
            t0 = time.time()
            with rs.session(name) as m:
                rs.build_assembly(m, state)
                n = len(m.bodies)
                m.write_step(dirs["ft_step"] / f"{name}.stp")
                m.write_stl(dirs["ft_stl"] / f"{name}.stl", size_mm=5.0)
            counts[label] = n
            print(f"  Rev A {label}: {n} bodies ({time.time()-t0:.1f}s)")
        for state in ("run_in", "deployed"):
            name = f"SHEX-ACT-S12_{state.upper()}"
            with rs.session(name) as m:
                acs.build_actuator_assembly(m, state)
                m.write_step(dirs["assemblies"] / f"{name}.stp")
                m.write_stl(dirs["sub_stl"] / f"{name}.stl", size_mm=3.0)
    finally:
        acs.INCLUDE_SEQ_SUB = True
    render_full_tool(dirs["ft_stl"], dirs["previews"])
    return counts


def copy_revB(dirs: dict[str, Path]) -> None:
    """Rev B full tool + actuator subs = the current build (copied)."""
    for f in sorted((FULLTOOL / "step").glob("*.stp")):
        shutil.copy2(f, dirs["ft_step"] / f.name)
    for f in sorted((FULLTOOL / "stl").glob("*.stl")):
        shutil.copy2(f, dirs["ft_stl"] / f.name)
    for f in sorted((FULLTOOL / "png").glob("*.png")):
        shutil.copy2(f, dirs["previews"] / f.name)
    copy_glob(ASSY, "SHEX-ACT-S12_*.stp", dirs["assemblies"], rev_b=True)
    copy_glob(RELSTL, "SHEX-ACT-S12_*.stl", dirs["sub_stl"], rev_b=True)
    if FULLTOOL.joinpath("manifest_full_tool.json").exists():
        shutil.copy2(FULLTOOL / "manifest_full_tool.json",
                     dirs["ft_step"].parent / "manifest_full_tool.json")


REVA_NOTE = """# Actuator scope at Rev A (DCN-10/11)

At Rev A the stage-1/2 internal actuators are the **two inflatable bladders +
Belleville hold** (DCN-10 ductile stent, DCN-11 second bladder). The first-stroke
**trigger / equalizing interlock was still an open item** at this revision.

It is engineered at **Rev B (DCN-12)** — see
`../../Rev-B_DCN-12_CURRENT/design/ACTUATOR_MANUAL.md` (Rev B) and
`../../Rev-B_DCN-12_CURRENT/engineering/FIRST_STROKE_TRIGGER.md` (SHEX-EM-001),
which add the SHEX-017 sequence/initiation sub.
"""


def write_readmes(a_counts: dict) -> None:
    (OUT / "README.md").write_text(f"""# SHEX-BP-UHEX-54 — Revision Archive

Each folder below is a **self-contained snapshot** of one revision of the
complete tool: engineering, design, part-specs, drawings (dxf+pdf), step,
stl, and full-tool previews.

| Revision | Folder | DCNs | Complete tool (run-in / set) | What changed |
|---|---|---|---|---|
| **Rev B — CURRENT** | `Rev-B_DCN-12_CURRENT/` | DCN-01 … **DCN-12** | **47 / 48 bodies** | adds the **SHEX-017** sequence/initiation sub: commanded initiation + completion-gated sequencing + EQ pilot interlock (first-stroke trigger). |
| Rev A — previous | `Rev-A_DCN-01-11_PREVIOUS/` | DCN-01 … DCN-11 | 44 / 45 bodies | plug + setting kit + stage 1/2 bladder actuators; trigger still an open item. |

## Where the complete run-in & set tool live

- **Latest (Rev B):** `Rev-B_DCN-12_CURRENT/stl/full-tool/SHEX-BP-UHEX-54_FULL_RUN-IN.stl`
  and `..._FULL_SET.stl` (+ matching `.stp` in `step/full-tool/`).
- Previous (Rev A): same paths under `Rev-A_DCN-01-11_PREVIOUS/`.

## DCN history (full)

- DCN-01..06 — plug geometry resolutions (see `design/MANUAL.md`).
- DCN-07..09 — settability / 10-in stroke / iris re-index (`design/SETTING_TOOL_MANUAL.md`).
- DCN-10 — stent material → ductile expandable alloy.
- DCN-11 — stage-2 prime mover → second inflatable bladder (Belleville = hold only).
- DCN-12 — first-stroke initiation & sequencing → SHEX-017 (Rev B only).

*Generated by `build_revisions.py`. The canonical working copies remain under
`export/release/`, `export/full_tool/`, `export/analysis/`; this archive is the
clean per-revision view.*
""", encoding="utf-8")

    rb = a_counts  # for symmetry; counts below are fixed/known
    (REVB / "README.md").write_text("""# Rev B — DCN-12 (CURRENT)

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
""", encoding="utf-8")

    (REVA / "README.md").write_text(f"""# Rev A — DCN-01..11 (PREVIOUS)

Complete tool: **{a_counts.get('RUN-IN', 44)} bodies (run-in) / """
        f"""{a_counts.get('SET', 45)} bodies (set)** — regenerated here with the
DCN-12 sequence sub switched OFF.

Plug + setting kit + stage 1/2 bladder actuators (DCN-10 ductile stent, DCN-11
second bladder). The first-stroke **trigger/interlock is not present** at this
revision (it is added at Rev B / DCN-12).

## Contents
- `engineering/` — analysis scripts + data (no trigger memo).
- `design/` — `MANUAL.md`, `SETTING_TOOL_MANUAL.md`, `ACTUATOR_MANUAL_RevA_note.md`,
  `figures/`.
- `part-specs/`, `drawings/`, `step/parts` (no SHEX-017), `step/assemblies`
  (ACT-S12 subs, 20 bodies), `step/full-tool`, `stl/full-tool`, `previews/`.
""", encoding="utf-8")
    (REVA / "design" / "ACTUATOR_MANUAL_RevA_note.md").write_text(
        REVA_NOTE, encoding="utf-8")


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    da = _mkdirs(REVA)
    db = _mkdirs(REVB)
    print("Rev B (current) — copying current build ...")
    copy_shared(db, rev_b=True)
    copy_revB(db)
    print("Rev A (previous) — regenerating complete tool without SHEX-017 ...")
    copy_shared(da, rev_b=False)
    a_counts = regen_revA(da)
    write_readmes(a_counts)
    print(f"\nRevision archive: {OUT}")


if __name__ == "__main__":
    main()
