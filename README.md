# SHEX-BP-UHEX-54 — 1.68 × 9-5/8 High-Expansion Bridge Plug

Parametric engineering package for a retrievable, ultra-high-expansion downhole
bridge plug (1.68 in run-in OD, sets in 9-5/8 in casing) plus its setting
adapter kit and stage-1/2 internal actuators. Everything here is generated from
parametric CAD scripts: B-rep solids and STEP via `gmsh` (OpenCASCADE), 2D
manufacturing drawings via `ezdxf`, and figures/previews via `matplotlib`.

## Repository layout

```
cad/                     parametric solid models (release_solids, actuator_solids, ...)
generate_*.py            generators: full tool, actuators, setting kit
build_revisions.py       assembles the per-revision archive (Rev A / Rev B)
export/
  release/               released STEP parts + assemblies, drawings (dxf/pdf), manuals, figures
  full_tool/             complete tool: STEP + STL + previews (run-in & set)
  REVISIONS/             clean per-revision snapshots (see below)
  analysis/              engineering analysis scripts + memos (incl. DCN-12 trigger)
  drawings/              drawing generators + part specs
  _stl_archive/          large STL meshes as a multi-volume RAR (see its README)
```

## Revisions

| Revision | Folder | Complete tool (run-in / set) | Notes |
|---|---|---|---|
| **Rev B — current** | `export/REVISIONS/Rev-B_DCN-12_CURRENT/` | 47 / 48 bodies | adds the **SHEX-017** sequence/initiation sub (DCN-12 first-stroke trigger + EQ interlock) |
| Rev A — previous | `export/REVISIONS/Rev-A_DCN-01-11_PREVIOUS/` | 44 / 45 bodies | plug + setting kit + stage-1/2 bladder actuators |

Each revision folder is self-contained: engineering, design, part-specs,
drawings (dxf+pdf), STEP (parts/assemblies/full-tool), STL, and previews. See
`export/REVISIONS/README.md` for the full DCN-01…12 history.

## STL meshes

Loose `.stl` files are **git-ignored** because several exceed GitHub's 100 MB
limit. They are shipped as a multi-volume RAR under
[`export/_stl_archive/`](export/_stl_archive/README.md) and are also fully
reproducible from the scripts:

```
python generate_full_tool.py     # complete run-in / set tool STL + STEP
python build_revisions.py         # per-revision archive
```

## Environment

Python 3.11 with `gmsh`, `ezdxf`, `matplotlib`, `numpy`, `pillow`. The `.venv/`
folders are intentionally excluded; recreate with `python -m venv .venv` and
install the above.

## Documentation

- Plug design/manufacture/assembly manual — `export/release/manual/MANUAL.md`
- Setting-tool (SHEX-AK-20) manual — `export/release/manual/SETTING_TOOL_MANUAL.md`
- Stage-1/2 actuator manual (Rev B) — `export/release/manual/ACTUATOR_MANUAL.md`
- First-stroke trigger memo (DCN-12) — `export/analysis/FIRST_STROKE_TRIGGER.md`
- Release notes / DCN log — `export/release/RELEASE_NOTES.md`
- Working log / forward plan — `WORKING_LOG.md`, `FORWARD_PLAN.md`
