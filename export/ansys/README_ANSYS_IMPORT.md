# ANSYS Import Package - SHEX-BP-UHEX-54

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

## ANSYS Workbench journal (automated)

See `workbench/README_WORKBENCH.md`.

```cmd
cd export\ansys\workbench
run_shex_fea.bat
```

Or in Workbench GUI: **File > Run Script** → `workbench/shex_stage3_iris.wbjn`

## ANSYS Workbench workflow (manual)

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
{
  "step": [
    "D:\\letsseewhatthiscando\\export\\ansys\\step\\iris_segment_production_mm.stp",
    "D:\\letsseewhatthiscando\\export\\ansys\\step\\mtm_ring_segment_mm.stp",
    "D:\\letsseewhatthiscando\\export\\ansys\\step\\mandrel_54in_mm.stp",
    "D:\\letsseewhatthiscando\\export\\ansys\\step\\casing_9625_40_drift_mm.stp"
  ],
  "mesh": [
    {
      "msh": "D:\\letsseewhatthiscando\\export\\ansys\\mesh\\iris_segment_solid_mm.msh",
      "inp": null,
      "nodes": 9972,
      "elements": 57975,
      "type": "solid_tet"
    },
    {
      "msh": "D:\\letsseewhatthiscando\\export\\ansys\\mesh\\stage3_iris_module_mm.msh",
      "inp": "D:\\letsseewhatthiscando\\export\\ansys\\mesh\\stage3_iris_module_mm.inp",
      "nodes": 677,
      "elements": 1280
    },
    {
      "msh": "D:\\letsseewhatthiscando\\export\\ansys\\mesh\\plug_uhex_54_assembly_mm.msh",
      "inp": "D:\\letsseewhatthiscando\\export\\ansys\\mesh\\plug_uhex_54_assembly_mm.inp",
      "nodes": 1838,
      "elements": 4416
    },
    {
      "msh": "D:\\letsseewhatthiscando\\export\\ansys\\mesh\\iris_single_segment_mm.msh",
      "inp": "D:\\letsseewhatthiscando\\export\\ansys\\mesh\\iris_single_segment_mm.inp",
      "nodes": 8,
      "elements": 12
    }
  ],
  "apdl": [
    "D:\\letsseewhatthiscando\\export\\ansys\\apdl\\mat_SHEX.apdl",
    "D:\\letsseewhatthiscando\\export\\ansys\\apdl\\stage3_iris_fea.apdl"
  ]
}
```

## Material reference (17-4 PH H900)

| Property | Value | ANSYS |
|----------|-------|-------|
| E | 28.5 Msi | MP,EX,1 |
| nu | 0.27 | MP,PRXY,1 |
| Fy | 160 ksi | TB,BISO |
| Density | 0.282 lb/in3 | MP,DENS,1 |
