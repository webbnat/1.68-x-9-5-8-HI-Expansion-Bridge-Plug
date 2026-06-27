# -*- coding: utf-8 -*-
# =============================================================================
# SHEX Stage 3 Iris — DesignModeler journal (STEP multi-body import)
# =============================================================================
# Use with STEP workflow. Run from Geometry cell:
#   Right-click Geometry > Import Geometry > Run Script > this file
#
# Imports iris segment + casing; user completes 16x circular pattern in DM.
# =============================================================================

import os

EXPORT_ROOT = r"D:\letsseewhatthiscando\export\ansys"
STEP_IRIS = os.path.join(EXPORT_ROOT, "step", "iris_segment_production_mm.stp")
STEP_CASING = os.path.join(EXPORT_ROOT, "step", "casing_9625_40_drift_mm.stp")

# DesignModeler API
Agb = GetAgb()
File1 = Agb.AddImportFile(STEP_IRIS)
File1.Generate()

File2 = Agb.AddImportFile(STEP_CASING)
File2.Generate()

# Rename bodies for clarity
# Body objects accessible via Agb.GetRoot().Children

ExtAPI.Log.WriteMessage("Imported iris segment and casing STEP.")
ExtAPI.Log.WriteMessage("Manual: Create 16-instance circular pattern of iris about Z axis, 22.5 deg.")
ExtAPI.Log.WriteMessage("Create Named Selections: NS_MANDREL_TOP, NS_BORE_FACE, NS_CASING_INNER, NS_SEGMENT_TOE")
