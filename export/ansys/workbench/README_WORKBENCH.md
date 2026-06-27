# ANSYS Workbench Journal — SHEX Stage 3 Iris FEA

## Files

| File | Purpose |
|------|---------|
| `shex_stage3_iris.wbjn` | **Main Workbench journal** — creates project, imports mesh/STEP |
| `shex_stage3_iris_mechanical.jscr` | **Mechanical journal** — materials, mesh, 2-step BCs |
| `shex_stage3_iris_designmodeler.js` | DesignModeler script for STEP multi-body import |
| `shex_materials.xml` | Engineering Data material library |
| `run_shex_fea.bat` | Windows batch launcher for `runwb2` |

## Quick start

### Interactive (recommended first run)

1. Open ANSYS Workbench
2. **File > Run Script...** → select `shex_stage3_iris.wbjn`
3. Double-click **Setup** to open Mechanical (runs `.jscr` if attached)
4. Review Command Objects; create Named Selections if prompted
5. **Solve**

### Batch (unattended)

```cmd
cd d:\letsseewhatthiscando\export\ansys\workbench
run_shex_fea.bat
```

Or manually:

```cmd
"C:\Program Files\ANSYS Inc\v242\Framework\bin\Win64\runwb2.exe" -B -R shex_stage3_iris.wbjn
```

Edit `ANSYS_VERSION` in `run_shex_fea.bat` to match your install (v231, v242, etc.).

## Workflows

### A — External Model (default, `USE_EXTERNAL_MODEL = True`)

- Imports `mesh/iris_segment_solid_mm.inp` (9,972 nodes, ~51k tets)
- Links to Static Structural
- Fastest path to stress results on single segment

### B — STEP geometry (`USE_EXTERNAL_MODEL = False`)

- Imports `step/iris_segment_production_mm.stp`
- Run `shex_stage3_iris_designmodeler.js` from Geometry cell
- Pattern 16 segments @ 22.5 deg; import casing STEP
- Full iris ring + contact simulation

## Named selections (STEP workflow)

Create in DesignModeler or Mechanical before Solve:

| Name | Purpose |
|------|---------|
| `NS_MANDREL_TOP` | 4" deploy displacement (101.6 mm UZ) |
| `NS_BORE_FACE` | 5000 psi pressure in Step 2 |
| `NS_CASING_INNER` | Fixed casing / contact target |
| `NS_SEGMENT_TOE` | Frictional contact source |
| `NS_ROOT_FILLET` | 0.8 mm mesh refinement |

## Analysis steps (configured in Mechanical journal)

| Step | Time | Load |
|------|------|------|
| 1 | 1.0 s | Mandrel UZ = 101.6 mm (iris deploy) |
| 2 | 2.0 s | Bore pressure = 34.47 MPa (5000 psi) |

Large deflection ON. Frictional contact mu = 0.12 (auto-detect if multi-body).

## Output

Project saved to: `workbench/SHEX_Stage3_Iris.wbpj`

Post-process: **Total Deformation**, **Equivalent Stress** at segment root fillet.

## Path configuration

If your project is not at `D:\letsseewhatthiscando`, edit `EXPORT_ROOT` at the top of:

- `shex_stage3_iris.wbjn`
- `shex_stage3_iris_mechanical.jscr`
- `shex_stage3_iris_designmodeler.js`
