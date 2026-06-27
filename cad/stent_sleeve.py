"""
Parametric stent-inspired expansion sleeve — uses developed diamond pattern.

See cad/stent_pattern.py and config/stent_patterns.yaml for authority.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import cadquery as cq

from cad.stent_pattern import (
    StentStageSpec,
    build_pattern,
    load_spec_from_yaml,
    map_developed_to_cylinder,
)


@dataclass
class StentParams:
    """Legacy wrapper — prefer StentStageSpec from stent_pattern."""

    collapsed_od_in: float = 1.688
    expanded_od_in: float = 4.050
    wall_thickness_in: float = 0.035
    axial_length_in: float = 3.25
    cells_around: int = 12
    ring_count: int = 8
    strut_width_in: float = 0.045
    kerf_in: float = 0.008
    id_run_in: float | None = None
    id_set_in: float | None = None
    part_no: str = "SHEX-008"

    def to_spec(self) -> StentStageSpec:
        id_run = self.id_run_in if self.id_run_in is not None else self.collapsed_od_in - 2 * self.wall_thickness_in
        id_set = self.id_set_in if self.id_set_in is not None else self.expanded_od_in - 2 * self.wall_thickness_in
        return StentStageSpec(
            part_no=self.part_no,
            od_run_in=self.collapsed_od_in,
            id_run_in=id_run,
            od_set_in=self.expanded_od_in,
            id_set_in=id_set,
            length_in=self.axial_length_in,
            cells_around=self.cells_around,
            rings=self.ring_count,
            strut_width_in=self.strut_width_in,
            kerf_in=self.kerf_in,
        )


def _spec_from_part(part_no: str) -> StentStageSpec:
    try:
        return load_spec_from_yaml(part_no)
    except Exception:
        if part_no == "SHEX-009":
            return StentParams(
                part_no="SHEX-009",
                collapsed_od_in=1.688,
                expanded_od_in=5.750,
                wall_thickness_in=0.040,
                axial_length_in=5.0,
                cells_around=14,
                ring_count=10,
                id_run_in=1.562,
                id_set_in=3.375,
            ).to_spec()
        return StentParams(part_no="SHEX-008").to_spec()


def build_stent_sleeve_from_spec(spec: StentStageSpec, state: str = "collapsed") -> cq.Workplane:
    pat_state = "run_in" if state == "collapsed" else "set"
    pattern = build_pattern(spec, pat_state)

    od = spec.od_run_in if state == "collapsed" else spec.od_set_in
    id_ = spec.id_run_in if state == "collapsed" else spec.id_set_in
    outer_r = od / 2.0
    inner_r = id_ / 2.0

    sleeve = cq.Workplane("XY").circle(outer_r).circle(inner_r).extrude(spec.length_in)

    wall = max(outer_r - inner_r, spec.strut_width_in)
    slot_depth = wall + 0.015

    for ap in pattern.aperture_polygons:
        if len(ap) < 3:
            continue
        xs = [p[0] for p in ap]
        ys = [p[1] for p in ap]
        x_c = sum(xs) / len(xs)
        y_c = sum(ys) / len(ys)
        x0, y0, z0 = map_developed_to_cylinder(x_c, y_c, spec, 0.0)
        r_c = math.hypot(x0, y0)
        if r_c < 1e-6:
            continue
        ang = math.degrees(math.atan2(y0, x0))
        span = max(max(xs) - min(xs), spec.strut_width_in * 0.5)
        height = max(max(ys) - min(ys), spec.strut_width_in * 0.5)

        cutter = (
            cq.Workplane("XY")
            .center(r_c, 0)
            .rect(span, spec.strut_width_in * 1.1)
            .extrude(slot_depth)
            .translate((0, 0, y_c - slot_depth / 2.0))
            .rotate((0, 0, 0), (0, 0, 1), ang)
        )
        try:
            sleeve = sleeve.cut(cutter)
        except Exception:
            pass

    return sleeve


def build_stent_sleeve(params: StentParams, state: str = "collapsed") -> cq.Workplane:
    return build_stent_sleeve_from_spec(params.to_spec(), state=state)


def build_stent_sleeve_part(part_no: str, state: str = "collapsed") -> cq.Workplane:
    return build_stent_sleeve_from_spec(_spec_from_part(part_no), state=state)


def export_stent_stl(part_no: str, output_dir: str) -> dict[str, str]:
    from pathlib import Path

    from cad.units import in_to_mm

    spec = _spec_from_part(part_no)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    paths: dict[str, str] = {}

    for state in ("collapsed", "expanded"):
        model = build_stent_sleeve_from_spec(spec, state=state)
        fname = f"{part_no}_stent_{state}.stl"
        fpath = out / fname
        cq.exporters.export(model, str(fpath), exportType="STL", tolerance=0.001)
        _scale_stl_to_mm(fpath)
        paths[state] = str(fpath)

    return paths


def _scale_stl_to_mm(path) -> None:
    from pathlib import Path

    import numpy as np

    from cad.units import in_to_mm

    p = Path(path)
    data = p.read_bytes()
    if len(data) < 84:
        return

    tri_count = int.from_bytes(data[80:84], "little")
    out = bytearray(data[:84])
    scale = in_to_mm(1.0)

    for i in range(tri_count):
        off = 84 + i * 50
        chunk = bytearray(data[off : off + 50])
        for vi in (0, 1, 2):
            base = 12 + vi * 12
            for axis in range(3):
                idx = base + axis * 4
                val = np.frombuffer(chunk[idx : idx + 4], dtype="<f4")[0]
                chunk[idx : idx + 4] = np.array([val * scale], dtype="<f4").tobytes()
        out.extend(chunk)

    p.write_bytes(out)
