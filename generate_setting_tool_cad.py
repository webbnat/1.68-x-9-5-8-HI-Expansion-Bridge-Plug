#!/usr/bin/env python3
"""Generate individual setting-tool module STEP files."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from cad.solid_cad import (
    OccModel,
    SETTING_TOOL_MODULES,
    build_setting_tool_model,
    export_assembly_step,
    occ_session,
)

OUT = ROOT / "export" / "cad" / "parts" / "setting_tool"


def export_module_step(part_name: str, length: float, od: float, path: Path) -> None:
    stroke_z = 10.0 + 8.0 + 14.0
    with occ_session(part_name) as m:
        ro = od / 2
        m.add_cylinder(0, length, ro)
        flange_ro = ro + 0.06 if od >= 3.625 else ro + 0.04
        m.add_annulus(length - 0.35, 0.35, ro - 0.04, flange_ro)
        if part_name == "ST_stroke":
            m.add_cylinder(8.0, 11.6, 1.55 / 2)
            m.add_annulus(20.0, 11.6, 3.625 / 2 - 0.32, 3.625 / 2 - 0.18)
        m.write_step(path)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    files: list[str] = []

    asm = ROOT / "export" / "cad" / "step" / "setting_tool_SHEX-ST-54.stp"
    export_assembly_step(build_setting_tool_model, "setting_tool", asm)

    for part_name, length, od, _mat in SETTING_TOOL_MODULES:
        path = OUT / f"{part_name}.stp"
        export_module_step(part_name, length, od, path)
        files.append(str(path))
        print(f"  ok {path.name}")

    with occ_session("ST_inner_stroke_mandrel") as m:
        m.add_cylinder(0, 11.6, 1.55 / 2)
        m.add_annulus(12.0, 11.6, 3.625 / 2 - 0.32, 3.625 / 2 - 0.18)
        p = OUT / "ST_inner_stroke_mandrel.stp"
        m.write_step(p)
        files.append(str(p))
        print(f"  ok {p.name}")

    (OUT / "manifest.json").write_text(json.dumps({"parts": files}, indent=2))
    print(f"\nDone — {len(files)} setting-tool part STEP files in {OUT}")


if __name__ == "__main__":
    main()
