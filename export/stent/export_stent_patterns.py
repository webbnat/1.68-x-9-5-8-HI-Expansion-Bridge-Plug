#!/usr/bin/env python3
"""Export developed stent laser patterns + validation reports for SHEX-008 / SHEX-009."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import ezdxf

from cad.stent_pattern import (
    build_pattern,
    format_validation_report,
    load_spec_from_yaml,
    map_developed_to_cylinder,
    validate_pattern,
)

OUT = ROOT / "export" / "stent"
DXF_DIR = OUT / "developed_dxf"
REPORT_DIR = OUT / "reports"


def _draw_pattern_dxf(pattern, path: Path, title: str) -> None:
    spec = pattern.spec
    doc = ezdxf.new("R2010")
    msp = doc.modelspace()
    w = spec.w_run if pattern.state == "run_in" else spec.w_set

    msp.add_lwpolyline(
        [(0, 0), (w, 0), (w, spec.length_in), (0, spec.length_in), (0, 0)],
        dxfattribs={"layer": "OUTLINE"},
    )
    msp.add_text(
        title,
        dxfattribs={"layer": "TEXT", "height": 0.05},
    ).set_placement((0.05, spec.length_in + 0.08))

    for seg in pattern.strut_segments:
        (x0, y0), (x1, y1) = seg
        msp.add_line((x0, y0), (x1, y1), dxfattribs={"layer": "STRUT_CENTERLINE"})

    for ap in pattern.aperture_polygons:
        if len(ap) >= 3:
            pts = list(ap) + [ap[0]]
            msp.add_lwpolyline(pts, dxfattribs={"layer": "LASER_KERF"})

    # Seam marker
    msp.add_line((0, 0), (0, spec.length_in), dxfattribs={"layer": "SEAM"})

    path.parent.mkdir(parents=True, exist_ok=True)
    doc.saveas(path)


def _draw_wrap_preview_dxf(pattern, path: Path) -> None:
    """Polar unwrap preview — one row of diamonds mapped to angle vs Z."""
    spec = pattern.spec
    doc = ezdxf.new("R2010")
    msp = doc.modelspace()
    for ap in pattern.aperture_polygons:
        pts = []
        for x, y in ap:
            theta_deg = 360.0 * (x % spec.w_run) / spec.w_run
            pts.append((theta_deg, y))
        if len(pts) >= 3:
            pts.append(pts[0])
            msp.add_lwpolyline(pts, dxfattribs={"layer": "WRAP_PREVIEW"})
    path.parent.mkdir(parents=True, exist_ok=True)
    doc.saveas(path)


def export_part(part_key: str) -> dict:
    spec = load_spec_from_yaml(part_key)
    v = validate_pattern(spec)
    run_pat = build_pattern(spec, "run_in")
    set_pat = build_pattern(spec, "set")

    dxf_run = DXF_DIR / f"{spec.part_no}_developed_RUNIN.dxf"
    dxf_set = DXF_DIR / f"{spec.part_no}_developed_SET_check.dxf"
    dxf_wrap = DXF_DIR / f"{spec.part_no}_wrap_preview_RUNIN.dxf"
    report_txt = REPORT_DIR / f"{spec.part_no}_pattern_validation.txt"
    report_json = REPORT_DIR / f"{spec.part_no}_pattern_validation.json"

    _draw_pattern_dxf(
        run_pat,
        dxf_run,
        "%s RUN-IN developed (laser authority) W=%.3f L=%.3f"
        % (spec.part_no, spec.w_run, spec.length_in),
    )
    _draw_pattern_dxf(
        set_pat,
        dxf_set,
        "%s SET check (deployed pitch) W=%.3f" % (spec.part_no, spec.w_set),
    )
    _draw_wrap_preview_dxf(run_pat, dxf_wrap)

    report_text = format_validation_report(v)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_txt.write_text(report_text, encoding="utf-8")

    payload = {
        "part_no": spec.part_no,
        "drawing": spec.drawing,
        "run_in": {
            "od_in": spec.od_run_in,
            "id_in": spec.id_run_in,
            "length_in": spec.length_in,
            "developed_width_in": spec.w_run,
            "pitch_in": v.pitch_run_in,
            "cells": spec.cells_around,
            "rings": spec.rings,
        },
        "set_envelope": {
            "od_in": spec.od_set_in,
            "id_in": spec.id_set_in,
            "pitch_in": v.pitch_at_set_target,
            "length_deploy_in": v.length_after_deploy,
        },
        "kinematics": {
            "circumferential_stretch_ratio": v.circumferential_stretch_ratio,
            "od_expansion_ratio": spec.od_expansion_ratio,
            "foreshortening_in": v.foreshortening_in,
            "foreshortening_pct": v.foreshortening_pct,
            "strut_length_in": v.strut_length_in,
        },
        "files": {
            "developed_run_in_dxf": str(dxf_run.relative_to(ROOT)),
            "developed_set_check_dxf": str(dxf_set.relative_to(ROOT)),
            "wrap_preview_dxf": str(dxf_wrap.relative_to(ROOT)),
        },
        "notes": v.notes,
    }
    report_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    return payload


def main() -> None:
    results = {}
    for key in ("SHEX-008", "SHEX-009"):
        results[key] = export_part(key)
        print(format_validation_report(validate_pattern(load_spec_from_yaml(key))))
        print("-" * 60)

    summary = OUT / "pattern_index.json"
    summary.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print("Wrote:", summary)


if __name__ == "__main__":
    main()
