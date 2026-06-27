#!/usr/bin/env python3
"""Generate 54\" production plug, setting tool, and combined string STLs."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from cad.mesh_utils import export_mesh
from cad.plug_visual import casing_reference
from cad.shex_54 import (
    combined_run_in_string,
    plug_54_assembly,
    plug_54_run_in,
    plug_54_set_in_casing,
    plug_total_length,
    setting_tool_assembly,
)

OUTPUT = ROOT / "output" / "stl" / "shex_54"


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    files = []

    builders = [
        (plug_54_assembly, "40_plug_uhex_54in_assembly_set"),
        (plug_54_assembly, "40_plug_uhex_54in_assembly"),  # legacy alias
        (plug_54_run_in, "40_plug_uhex_54in_assembly_run_in"),
        (plug_54_set_in_casing, "40_plug_uhex_54in_set_with_casing"),
        (setting_tool_assembly, "41_setting_tool_shex_st54"),
        (combined_run_in_string, "42_combined_string_lube_check"),
        (casing_reference, "43_casing_9625_40_reference"),
    ]

    for builder, name in builders:
        path = OUTPUT / f"{name}.stl"
        export_mesh(builder(), str(path))
        files.append(name)
        print(f"  ok {name}.stl")

    meta = {
        "plug_length_in": plug_total_length(),
        "setting_tool_length_in": 246,
        "combined_string_in": 300,
        "combined_string_ft": 25.0,
        "orientation": "z=0 at tool bottom (mandrel tail); z increases to fishing neck",
        "files": files,
    }
    (OUTPUT / "manifest.json").write_text(json.dumps(meta, indent=2))
    print(f"\nPlug length: {meta['plug_length_in']:.1f} in")
    print(f"Combined string: {meta['combined_string_ft']:.1f} ft (fits 35 ft lubricator)")


if __name__ == "__main__":
    main()
