#!/usr/bin/env python3
"""
Generate ANSYS-ready export package:
  - STEP solids (Gmsh OpenCASCADE kernel)
  - Gmsh volume meshes (.msh)
  - Abaqus INP meshes (ANSYS Mechanical import)
  - APDL scripts (geometry import, materials, contacts, loads)
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import gmsh
import meshio

from cad.mesh_utils import MeshData, cylinder, export_mesh, merge, translate, tube
from cad.units import in_to_mm

OUT = ROOT / "export" / "ansys"
STEP_DIR = OUT / "step"
MESH_DIR = OUT / "mesh"
APDL_DIR = OUT / "apdl"

MM = in_to_mm(1.0)


def _init_gmsh(name: str) -> None:
    gmsh.initialize()
    gmsh.model.add(name)


def _finalize_write_step(path: Path) -> None:
    gmsh.model.occ.synchronize()
    path.parent.mkdir(parents=True, exist_ok=True)
    gmsh.write(str(path))
    gmsh.finalize()


def export_iris_segment_step(path: Path) -> None:
    """Production iris segment t=0.187\" as extruded trapezoid arc segment."""
    _init_gmsh("iris_segment")
    t = in_to_mm(0.187)
    axial = in_to_mm(2.75)
    r_in = in_to_mm(5.750 / 2 + 0.08)
    r_out = in_to_mm(8.650 / 2 - 0.015)
    arc = math.radians(22.5)

    # Trapezoidal cross-section in XY, extrude in Z (axial)
    x0 = r_in * math.cos(-arc / 2)
    y0 = r_in * math.sin(-arc / 2)
    x1 = r_out * math.cos(-arc / 2)
    y1 = r_out * math.sin(-arc / 2)
    x2 = r_out * math.cos(arc / 2)
    y2 = r_out * math.sin(arc / 2)
    x3 = r_in * math.cos(arc / 2)
    y3 = r_in * math.sin(arc / 2)

    pts = [
        gmsh.model.occ.addPoint(x0, y0, 0),
        gmsh.model.occ.addPoint(x1, y1, 0),
        gmsh.model.occ.addPoint(x2, y2, 0),
        gmsh.model.occ.addPoint(x3, y3, 0),
    ]
    lines = [
        gmsh.model.occ.addLine(pts[0], pts[1]),
        gmsh.model.occ.addLine(pts[1], pts[2]),
        gmsh.model.occ.addLine(pts[2], pts[3]),
        gmsh.model.occ.addLine(pts[3], pts[0]),
    ]
    loop = gmsh.model.occ.addCurveLoop(lines)
    surf = gmsh.model.occ.addPlaneSurface([loop])
    gmsh.model.occ.extrude([(2, surf)], 0, 0, axial)
    _finalize_write_step(path)


def export_mtm_ring_step(path: Path) -> None:
    _init_gmsh("mtm_ring")
    ro = in_to_mm(8.800 / 2)
    ri = ro - in_to_mm(0.30)
    h = in_to_mm(0.45)
    gmsh.model.occ.addCylinder(0, 0, 0, 0, 0, h, ro)
    gmsh.model.occ.addCylinder(0, 0, 0, 0, 0, h, ri)
    _finalize_write_step(path)


def export_mandrel_step(path: Path) -> None:
    _init_gmsh("mandrel")
    r = in_to_mm(1.35 / 2)
    h = in_to_mm(54.0)
    gmsh.model.occ.addCylinder(0, 0, 0, 0, 0, h, r)
    _finalize_write_step(path)


def export_casing_surface_step(path: Path) -> None:
    """9-5/8\" 40# drift ID cylinder for contact target."""
    _init_gmsh("casing")
    r = in_to_mm(8.679 / 2)
    h = in_to_mm(12.0)
    gmsh.model.occ.addCylinder(0, 0, 0, 0, 0, h, r)
    _finalize_write_step(path)


def mesh_step_solid(step_path: Path, base_name: str, mesh_size_mm: float = 2.0) -> dict:
    """Tetrahedral solid mesh from STEP (for ANSYS import)."""
    MESH_DIR.mkdir(parents=True, exist_ok=True)
    gmsh.initialize()
    gmsh.model.add(base_name)
    gmsh.merge(str(step_path))
    gmsh.model.occ.synchronize()
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", mesh_size_mm)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", mesh_size_mm * 0.4)
    gmsh.model.mesh.generate(3)
    msh_path = MESH_DIR / f"{base_name}.msh"
    gmsh.write(str(msh_path))
    m = meshio.read(str(msh_path))
    inp_path = MESH_DIR / f"{base_name}.inp"
    try:
        # meshio abaqus writer for ANSYS External Model import
        meshio.write(str(inp_path), m, file_format="abaqus", translate_cell_names=False)
    except Exception as ex:
        print(f"    INP write note: {ex}")
        inp_path = inp_path if inp_path.exists() else None
    gmsh.finalize()
    return {
        "msh": str(msh_path),
        "inp": str(inp_path) if inp_path else None,
        "nodes": len(m.points),
        "elements": sum(len(c.data) for c in m.cells),
        "type": "solid_tet",
    }


def mesh_stl_to_files(stl_path: Path, base_name: str, mesh_size_mm: float = 3.0) -> dict:
    """Create mesh from STL shell; export msh and inp."""
    MESH_DIR.mkdir(parents=True, exist_ok=True)
    gmsh.initialize()
    gmsh.model.add(base_name)
    gmsh.merge(str(stl_path))
    gmsh.model.occ.synchronize()

    # Create volume from surface if possible
    s = gmsh.model.getEntities(2)
    if s:
        try:
            gmsh.model.occ.addVolume([s[0][1]])
            gmsh.model.occ.synchronize()
        except Exception:
            pass

    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", mesh_size_mm)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", mesh_size_mm * 0.5)
    gmsh.option.setNumber("Mesh.Algorithm3D", 1)  # Delaunay

    try:
        gmsh.model.mesh.generate(3)
    except Exception:
        gmsh.model.mesh.generate(2)

    msh_path = MESH_DIR / f"{base_name}.msh"
    gmsh.write(str(msh_path))

    # Convert to INP via meshio
    m = meshio.read(str(msh_path))
    inp_path = MESH_DIR / f"{base_name}.inp"
    meshio.write(str(inp_path), m, file_format="abaqus")

    gmsh.finalize()
    return {
        "msh": str(msh_path),
        "inp": str(inp_path),
        "nodes": len(m.points),
        "elements": sum(len(c.data) for c in m.cells),
    }


def write_apdl_materials(path: Path) -> None:
    path.write_text(
        r"""! SHEX-BP-UHEX-54 — Material definitions for ANSYS MAPDL
! Import: /INPUT,mat_SHEX,apdl

/prep7
! 17-4 PH H900 (iris segments, MTM rings)
MP,EX,1,28.5E6       ! psi
MP,PRXY,1,0.27
MP,DENS,1,0.282      ! lb/in3
TB,BISO,1,1,2
TBDATA,1,160000,1900000  ! yield, tangent (approx)

! HNBR seal (Mooney-Rivlin approx as neo-Hookean hyperelastic)
! Use TB,HYPER,2,... in full model — placeholder linear:
MP,EX,2,500
MP,PRXY,2,0.49

! P110 casing (contact target)
MP,EX,3,30E6
MP,PRXY,3,0.3

! Inconel 718 helix guide
MP,EX,4,29E6
MP,PRXY,4,0.29
TB,BISO,4,1,2
TBDATA,1,150000,0

ET,1,187               ! SOLID187 tet
ET,2,174               ! CONTA174 contact
ET,3,170               ! TARGE170 target

FINISH
"""
    )


def write_apdl_stage3_fea(path: Path) -> None:
    path.write_text(
        r"""! SHEX-BP-UHEX-54 Stage 3 Iris FEA — ANSYS MAPDL template
! Workflow:
!   1. Import STEP: File > Import > STEP in Workbench OR
!      /AUX15, IGESIN, stage3_iris_segment_mm.stp
!   2. Assign Material 1 (17-4 PH) to iris segments
!   3. Import casing surface as target body (Material 3, rigid or soft)
!   4. Define frictional contact (mu=0.12) segment toe -> casing
!   5. Apply displacement on mandrel: 4.0 in (101.6 mm) axial
!   6. Lock casing OD; apply 5000 psi on bore face after lock-up step

/CLEAR,START
/FILNAME,shex_stage3_iris

! --- Step 1: Deploy iris (4" mandrel stroke) ---
/SOLU
ANTYPE,STATIC
NLGEOM,ON
NSUBST,20,100,10

! Mandrel top face: UX=0, UY=0, UZ=101.6 mm (4.0 in)
! (Replace node component name with your selection)
! D,mandrel_top,UX,0
! D,mandrel_top,UY,0
! D,mandrel_top,UZ,101.6

! Casing inner surface fixed
! D,casing_nodes,UX,0
! D,casing_nodes,UY,0
! D,casing_nodes,UZ,0

SOLVE

! --- Step 2: Pressure lock-up 5000 psi ---
! SF,bore_face,PRES,5000  ! psi on bore

FINISH

! Post: PLNSOL,S,EQV for segment root fillet
!       CNTRSTAT for contact status
"""
    )


def write_apdl_cdb_from_inp(inp_path: Path, cdb_path: Path) -> None:
    """Generate APDL script to import Abaqus INP mesh into ANSYS."""
    cdb_path.write_text(
        f"""! Import mesh from Abaqus INP format
! ANSYS Workbench: External Model > Abaqus > {inp_path.name}
! MAPDL alternative:
! /AUX15
! ABAQUS,{inp_path.as_posix()}

! Or use CDREAD after converting via /INPUT in WB External Model component
"""
    )


def write_workbench_readme(manifest: dict) -> None:
    readme = OUT / "README_ANSYS_IMPORT.md"
    content = f"""# ANSYS Import Package - SHEX-BP-UHEX-54

Generated export for Stage 3 iris FEA and full assembly reference.

## Contents

### STEP solids (`step/`) - import into DesignModeler / SpaceClaim
| File | Description | Units |
|------|-------------|-------|
| `iris_segment_production_mm.stp` | Single iris segment t=0.187 in | mm |
| `mtm_ring_segment_mm.stp` | MTM backup ring | mm |
| `mandrel_54in_mm.stp` | Inner mandrel reference | mm |
| `casing_9625_40_drift_mm.stp` | 9-5/8 in 40# drift ID contact target | mm |

### Volume meshes (`mesh/`)
| File | Format | Use |
|------|--------|-----|
| `*.msh` | Gmsh native | Gmsh post-processing / import |
| `*.inp` | Abaqus INP | ANSYS External Model import |

### APDL scripts (`apdl/`)
| File | Purpose |
|------|---------|
| `mat_SHEX.apdl` | Material properties (17-4 PH, HNBR, P110, Inconel 718) |
| `stage3_iris_fea.apdl` | Analysis template (deploy + pressure steps) |
| `import_*.apdl` | Mesh import helpers |

## ANSYS Workbench workflow

1. **File > Import > STEP** -> `step/iris_segment_production_mm.stp`
2. **Circular pattern** 16 instances @ 22.5 deg (full iris ring)
3. **Import** `casing_9625_40_drift_mm.stp` as target surface
4. **Mechanical Model:**
   - Assign `mat_SHEX` Material 1 to iris
   - Frictional contact: segment toe -> casing (mu=0.12)
   - Displacement: mandrel 4.0 in (101.6 mm) axial - Step 1
   - Pressure: 5000 psi on bore - Step 2
5. **Mesh:** 0.08 in (2 mm) at root fillet, 0.2 in body

## Alternative: pre-mesh import

1. **External Model** -> select `mesh/stage3_iris_module_mm.inp`
2. Assign materials in Mechanical
3. Apply BCs per `apdl/stage3_iris_fea.apdl`

## Manifest

```json
{json.dumps(manifest, indent=2)}
```

## Material reference (17-4 PH H900)

| Property | Value | ANSYS |
|----------|-------|-------|
| E | 28.5 Msi | MP,EX,1 |
| nu | 0.27 | MP,PRXY,1 |
| Fy | 160 ksi | TB,BISO |
| Density | 0.282 lb/in3 | MP,DENS,1 |
"""
    readme.write_text(content, encoding="utf-8")


def main() -> None:
    STEP_DIR.mkdir(parents=True, exist_ok=True)
    MESH_DIR.mkdir(parents=True, exist_ok=True)
    APDL_DIR.mkdir(parents=True, exist_ok=True)

    manifest: dict = {"step": [], "mesh": [], "apdl": []}

    print("Generating ANSYS export package...")

    steps = [
        (export_iris_segment_step, "iris_segment_production_mm.stp"),
        (export_mtm_ring_step, "mtm_ring_segment_mm.stp"),
        (export_mandrel_step, "mandrel_54in_mm.stp"),
        (export_casing_surface_step, "casing_9625_40_drift_mm.stp"),
    ]
    for fn, name in steps:
        p = STEP_DIR / name
        try:
            fn(p)
            manifest["step"].append(str(p))
            print(f"  STEP ok {name}")
        except Exception as e:
            print(f"  STEP FAIL {name}: {e}")

    # Solid mesh from STEP (iris segment - primary FEA mesh)
    iris_step = STEP_DIR / "iris_segment_production_mm.stp"
    if iris_step.exists():
        try:
            info = mesh_step_solid(iris_step, "iris_segment_solid_mm", mesh_size_mm=2.0)
            manifest["mesh"].append(info)
            print(f"  SOLID MESH ok iris_segment ({info['nodes']} nodes, {info['elements']} elems)")
        except Exception as e:
            print(f"  SOLID MESH FAIL iris_segment: {e}")

    # Surface/volume meshes from STLs (reference)
    stl_sources = [
        (ROOT / "output/stl/stage3_iris/stage3_iris_module_75in.stl", "stage3_iris_module_mm", 4.0),
        (ROOT / "output/stl/shex_54/40_plug_uhex_54in_assembly.stl", "plug_uhex_54_assembly_mm", 8.0),
        (ROOT / "output/stl/stage3_iris/stage3_iris_single_segment.stl", "iris_single_segment_mm", 2.0),
    ]
    for stl, name, size in stl_sources:
        if stl.exists():
            try:
                info = mesh_stl_to_files(stl, name, mesh_size_mm=size)
                manifest["mesh"].append(info)
                print(f"  MESH ok {name} ({info['nodes']} nodes, {info['elements']} elems)")
            except Exception as e:
                print(f"  MESH FAIL {name}: {e}")
        else:
            print(f"  MESH skip {name} — STL missing, run generate scripts first")

    write_apdl_materials(APDL_DIR / "mat_SHEX.apdl")
    write_apdl_stage3_fea(APDL_DIR / "stage3_iris_fea.apdl")
    manifest["apdl"] = [str(APDL_DIR / "mat_SHEX.apdl"), str(APDL_DIR / "stage3_iris_fea.apdl")]

    for info in manifest.get("mesh", []):
        if info.get("inp"):
            write_apdl_cdb_from_inp(Path(info["inp"]), APDL_DIR / f"import_{Path(info['inp']).stem}.apdl")

    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2))
    write_workbench_readme(manifest)
    print(f"\nDone — package in {OUT}")


if __name__ == "__main__":
    main()
