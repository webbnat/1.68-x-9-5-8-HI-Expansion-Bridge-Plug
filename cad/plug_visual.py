"""Realistic SHEX-BP-UHEX-54 plug mesh geometry (run-in and set states).

Z axis: bottom of tool at z=0 (mandrel tail), increasing upward to fishing neck.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from cad.mesh_utils import (
    MeshData,
    box,
    cone,
    cylinder,
    merge,
    rotate_z,
    stent_lattice,
    translate,
    tube,
    wedge_profile,
)

# Module stack bottom -> top (length in, set OD in, set ID in, run OD in)
MODULES: list[tuple[str, float, float, float, float]] = [
    ("mandrel_tail", 3.0, 1.35, 0.0, 1.35),
    ("bottom_sub", 2.0, 1.688, 0.75, 1.688),
    ("lower_slips", 4.5, 8.72, 1.55, 1.688),
    ("stage1", 4.0, 3.375, 1.45, 1.688),
    ("stage2", 5.0, 5.750, 3.375, 1.688),
    ("stage3_iris", 7.5, 8.650, 5.750, 1.688),
    ("seal_land", 4.5, 8.720, 1.55, 1.688),
    ("seal_land", 4.5, 8.720, 1.55, 1.688),
    ("seal_land", 4.5, 8.720, 1.55, 1.688),
    ("seal_land", 4.5, 8.720, 1.55, 1.688),
    ("upper_mtm", 2.5, 8.800, 8.40, 1.688),
    ("upper_slips", 4.5, 8.72, 1.55, 1.688),
    ("fishing_neck", 3.0, 1.375, 0.0, 1.375),
]

RUN_OD = 1.688
MANDREL_R = 1.35 / 2
MANDREL_BODY_R = 1.55 / 2
CASING_ID_R = 8.679 / 2


@dataclass
class StackCursor:
    z: float = 0.0

    def advance(self, length: float) -> float:
        base = self.z
        self.z += length
        return base


def _mandrel_shaft(length: float, r: float = MANDREL_R) -> MeshData:
    return cylinder(r, length, segments=64)


def _taper_transition(r_bot: float, r_top: float, length: float) -> MeshData:
    if abs(r_bot - r_top) < 1e-6:
        return cylinder(r_bot, length, segments=64)
    return cone(r_bot, r_top, length, segments=64)


def _iris_ring(
    r_inner: float,
    r_outer: float,
    height: float,
    segments: int = 16,
    thickness: float = 0.187,
) -> MeshData:
    parts: list[MeshData] = []
    span = 2 * math.pi / segments
    gap = math.radians(1.2)
    for i in range(segments):
        a0 = i * span + gap / 2
        a1 = (i + 1) * span - gap / 2
        am = (a0 + a1) / 2
        seg_w = (r_outer - r_inner) * 0.92
        seg_l = (r_inner + r_outer) / 2 * (a1 - a0) * 0.88
        mx = (r_inner + r_outer) / 2 * math.cos(am)
        my = (r_inner + r_outer) / 2 * math.sin(am)
        b = box(seg_l, seg_w, thickness, center=(mx, my, height / 2))
        b = rotate_z(b, math.degrees(am))
        parts.append(b)
    inner = cylinder(r_inner, height, segments=64)
    return merge(*parts, inner)


def _slip_wedges(
    count: int,
    contact_r: float,
    mandrel_r: float,
    height: float,
) -> MeshData:
    parts: list[MeshData] = []
    circum = math.pi * contact_r / count * 0.48
    radial_len = max(0.15, contact_r - mandrel_r - 0.10)
    for i in range(count):
        ang = 2 * math.pi * i / count
        mid_r = mandrel_r + radial_len / 2 + 0.05
        mx, my = mid_r * math.cos(ang), mid_r * math.sin(ang)
        block = box(radial_len, circum, height * 0.72, center=(mx, my, height / 2))
        block = rotate_z(block, math.degrees(ang))
        parts.append(block)
    parts.append(cylinder(mandrel_r, height, segments=48))
    parts.append(tube(contact_r, mandrel_r + 0.06, height, segments=64))
    return merge(*parts)


def _seal_cup(od: float, mandrel_r: float, length: float) -> MeshData:
    outer_r = od / 2
    cup = tube(outer_r, mandrel_r + 0.04, length * 0.82, segments=64)
    lip_r = outer_r - 0.08
    lip = translate(cone(lip_r, outer_r, length * 0.18, segments=64), 0, 0, length * 0.82)
    petals: list[MeshData] = []
    for i in range(16):
        ang = 2 * math.pi * i / 16
        px = (mandrel_r + 0.12) * math.cos(ang)
        py = (mandrel_r + 0.12) * math.sin(ang)
        petal = wedge_profile(0.55, 1.4, 0.08, center=(px, py, length * 0.45))
        petal = rotate_z(petal, math.degrees(ang) + 90)
        petals.append(petal)
    return merge(cup, lip, *petals)


def _mtm_stack(od: float, id_: float, length: float, rings: int = 3) -> MeshData:
    outer_r = od / 2
    inner_r = id_ / 2
    parts = [tube(outer_r, inner_r, length, segments=64)]
    pitch = length / (rings + 1)
    groove_w = 0.12
    for i in range(1, rings + 1):
        z = i * pitch - groove_w / 2
        groove = translate(
            tube(outer_r + 0.02, outer_r - 0.06, groove_w, segments=64),
            0,
            0,
            z,
        )
        parts.append(groove)
    return merge(*parts)


def _stage_stent(od: float, wall: float, length: float, cells: int, rings: int) -> MeshData:
    return stent_lattice(od, wall, length, cells=cells, rings=rings, strut_w=0.045)


def _fishing_neck(length: float) -> MeshData:
    body = cone(MANDREL_R, 1.375 / 2, length * 0.65, segments=64)
    box_top = translate(cylinder(1.375 / 2, length * 0.35, segments=64), 0, 0, length * 0.65)
    thread = translate(
        tube(1.375 / 2, 1.375 / 2 - 0.06, length * 0.22, segments=48),
        0,
        0,
        length * 0.08,
    )
    return merge(body, box_top, thread)


def _run_in_sheath(length: float, r: float = RUN_OD / 2) -> MeshData:
    """Thin run-in body with subtle stent band hints."""
    parts = [tube(r + 0.03, r - 0.02, length, segments=64)]
    band_pitch = 1.25
    n_bands = max(1, int(length / band_pitch))
    for i in range(n_bands):
        z = (i + 0.5) * length / n_bands
        band = translate(
            tube(r + 0.04, r - 0.01, 0.08, segments=48),
            0,
            0,
            z,
        )
        parts.append(band)
    return merge(*parts)


def plug_run_in() -> MeshData:
    """Collapsed thru-tubing configuration, z=0 at mandrel tail."""
    cur = StackCursor()
    parts: list[MeshData] = []

    for name, length, _set_od, _set_id, run_od in MODULES:
        z0 = cur.advance(length)
        run_r = run_od / 2

        if name == "mandrel_tail":
            parts.append(translate(_mandrel_shaft(length), 0, 0, z0))
            parts.append(translate(cylinder(run_r, length, segments=64), 0, 0, z0))
        elif name == "bottom_sub":
            parts.append(translate(_mandrel_shaft(length, MANDREL_R), 0, 0, z0))
            parts.append(translate(tube(run_r, MANDREL_R + 0.02, length, segments=64), 0, 0, z0))
            parts.append(
                translate(
                    tube(run_r + 0.05, run_r, length * 0.35, segments=64),
                    0,
                    0,
                    z0 + length * 0.55,
                )
            )
        elif name == "fishing_neck":
            parts.append(translate(_fishing_neck(length), 0, 0, z0))
        else:
            parts.append(translate(_mandrel_shaft(length, MANDREL_BODY_R), 0, 0, z0))
            parts.append(translate(_run_in_sheath(length, run_r), 0, 0, z0))
            if name.startswith("stage"):
                hint = _stage_stent(run_od, 0.035, length, cells=10, rings=6)
                parts.append(translate(hint, 0, 0, z0))

    return merge(*parts)


def plug_set() -> MeshData:
    """Expanded set configuration against 9-5/8\" 40# casing."""
    cur = StackCursor()
    parts: list[MeshData] = []

    for name, length, set_od, set_id, _run_od in MODULES:
        z0 = cur.advance(length)
        od_r = set_od / 2
        id_r = (set_id / 2) if set_id > 0 else MANDREL_BODY_R

        if name == "mandrel_tail":
            parts.append(translate(_mandrel_shaft(length), 0, 0, z0))
            parts.append(translate(cylinder(od_r, length, segments=64), 0, 0, z0))
        elif name == "bottom_sub":
            parts.append(translate(_mandrel_shaft(length, MANDREL_R), 0, 0, z0))
            parts.append(translate(tube(od_r, MANDREL_R + 0.02, length, segments=64), 0, 0, z0))
        elif name == "fishing_neck":
            parts.append(translate(_fishing_neck(length), 0, 0, z0))
        elif name in {"lower_slips", "upper_slips"}:
            parts.append(translate(_slip_wedges(8, od_r, id_r, length), 0, 0, z0))
        elif name == "upper_mtm":
            parts.append(translate(_mtm_stack(set_od, set_id, length), 0, 0, z0))
        elif name == "seal_land":
            parts.append(translate(_seal_cup(set_od, id_r, length), 0, 0, z0))
            parts.append(translate(_mandrel_shaft(length, id_r), 0, 0, z0))
        elif name == "stage3_iris":
            parts.append(
                translate(
                    _iris_ring(5.750 / 2, 8.650 / 2, length, segments=16, thickness=0.187),
                    0,
                    0,
                    z0,
                )
            )
            parts.append(translate(tube(od_r, 5.750 / 2, length, segments=64), 0, 0, z0))
            parts.append(translate(_mandrel_shaft(length, 3.375 / 2), 0, 0, z0))
        elif name == "stage2":
            parts.append(translate(_stage_stent(set_od, 0.040, length, cells=14, rings=10), 0, 0, z0))
            parts.append(translate(tube(od_r, id_r, length, segments=64), 0, 0, z0))
            parts.append(translate(_mandrel_shaft(length, 1.45 / 2), 0, 0, z0))
        elif name == "stage1":
            parts.append(translate(_stage_stent(set_od, 0.035, length, cells=12, rings=8), 0, 0, z0))
            parts.append(translate(tube(od_r, id_r, length, segments=64), 0, 0, z0))
            parts.append(translate(_mandrel_shaft(length, MANDREL_BODY_R), 0, 0, z0))
        else:
            parts.append(translate(cylinder(od_r, length, segments=64), 0, 0, z0))

    return merge(*parts)


def casing_reference(length: float | None = None) -> MeshData:
    """9-5/8\" 40# drift ID reference tube for scale context."""
    total = length if length is not None else sum(m[1] for m in MODULES)
    return tube(CASING_ID_R, CASING_ID_R - 0.25, total, segments=72)


def plug_54_assembly() -> MeshData:
    """Default export: set condition (primary review geometry)."""
    return plug_set()
