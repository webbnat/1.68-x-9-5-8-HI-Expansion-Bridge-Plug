"""Gmsh OpenCASCADE B-rep solid modeling — manufacturing-grade STEP export.

All dimensions internal: inches. STEP output: millimetres.
Z axis: bottom of tool at z=0, increasing upward.
"""

from __future__ import annotations

import math
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

import gmsh
from cad.units import in_to_mm

from cad.plug_visual import MODULES


@dataclass
class SolidPart:
    name: str
    material: str
    dimtags: list[tuple[int, int]] = field(default_factory=list)
    notes: str = ""


class OccModel:
    """One Gmsh OCC model session."""

    def __init__(self, name: str) -> None:
        gmsh.initialize()
        gmsh.model.add(name)
        self.name = name
        self.parts: list[SolidPart] = []

    def close(self) -> None:
        gmsh.finalize()

    def _mm(self, inches: float) -> float:
        return in_to_mm(inches)

    def _zmm(self, z_in: float) -> float:
        return self._mm(z_in)

    def _hmm(self, h_in: float) -> float:
        return self._mm(h_in)

    def _rmm(self, r_in: float) -> float:
        return self._mm(r_in)

    def add_cylinder(self, z_in: float, h_in: float, r_in: float) -> tuple[int, int]:
        tag = gmsh.model.occ.addCylinder(0, 0, self._zmm(z_in), 0, 0, self._hmm(h_in), self._rmm(r_in))
        return (3, tag)

    def add_cone(self, z_in: float, h_in: float, r_bot_in: float, r_top_in: float) -> tuple[int, int]:
        tag = gmsh.model.occ.addCone(
            0, 0, self._zmm(z_in),
            0, 0, self._hmm(h_in),
            self._rmm(r_bot_in), self._rmm(r_top_in),
        )
        return (3, tag)

    def add_annulus(self, z_in: float, h_in: float, ri_in: float, ro_in: float) -> list[tuple[int, int]]:
        if ri_in <= 1e-9:
            return [self.add_cylinder(z_in, h_in, ro_in)]
        outer = self.add_cylinder(z_in, h_in, ro_in)
        inner = self.add_cylinder(z_in, h_in, ri_in)
        result, _ = gmsh.model.occ.cut([outer], [inner])
        return result

    def add_box_radial(
        self,
        z_in: float,
        h_in: float,
        r_mid_in: float,
        radial_thk_in: float,
        arc_width_in: float,
        angle_deg: float,
    ) -> tuple[int, int]:
        """Box wedge at radius, rotated about Z."""
        x = self._rmm(r_mid_in) * math.cos(math.radians(angle_deg))
        y = self._rmm(r_mid_in) * math.sin(math.radians(angle_deg))
        tag = gmsh.model.occ.addBox(
            x - self._mm(arc_width_in) / 2,
            y - self._mm(radial_thk_in) / 2,
            self._zmm(z_in),
            self._mm(arc_width_in),
            self._mm(radial_thk_in),
            self._hmm(h_in),
        )
        gmsh.model.occ.rotate([(3, tag)], 0, 0, 0, 0, 0, 1, math.radians(angle_deg))
        return (3, tag)

    def add_iris_segment(self, z_in: float, angle_deg: float, axial_in: float = 2.75, t_in: float = 0.187) -> list[tuple[int, int]]:
        """Single stage-3 iris segment; extruded radial trapezoid."""
        arc = math.radians(22.5)
        r_in = 5.750 / 2 + 0.080
        r_out = 8.650 / 2 - 0.015
        z0 = self._zmm(z_in)
        axial = self._hmm(axial_in)

        def pt(r: float, a: float) -> tuple[float, float]:
            return r * math.cos(a), r * math.sin(a)

        ri, ro = self._rmm(r_in), self._rmm(r_out)
        a0, a1 = -arc / 2, arc / 2
        x0, y0 = pt(ri, a0)
        x1, y1 = pt(ro, a0)
        x2, y2 = pt(ro, a1)
        x3, y3 = pt(ri, a1)

        p0 = gmsh.model.occ.addPoint(x0, y0, z0)
        p1 = gmsh.model.occ.addPoint(x1, y1, z0)
        p2 = gmsh.model.occ.addPoint(x2, y2, z0)
        p3 = gmsh.model.occ.addPoint(x3, y3, z0)
        l0 = gmsh.model.occ.addLine(p0, p1)
        l1 = gmsh.model.occ.addLine(p1, p2)
        l2 = gmsh.model.occ.addLine(p2, p3)
        l3 = gmsh.model.occ.addLine(p3, p0)
        loop = gmsh.model.occ.addCurveLoop([l0, l1, l2, l3])
        surf = gmsh.model.occ.addPlaneSurface([loop])
        ext = gmsh.model.occ.extrude([(2, surf)], 0, 0, axial)
        vols = [(d, t) for d, t in ext if d == 3]
        if angle_deg != 0:
            gmsh.model.occ.rotate(vols, 0, 0, 0, 0, 0, 1, math.radians(angle_deg))
        return vols

    def register_part(self, name: str, material: str, dimtags: list[tuple[int, int]], notes: str = "") -> None:
        self.parts.append(SolidPart(name, material, list(dimtags), notes))

    def synchronize(self) -> None:
        gmsh.model.occ.synchronize()

    def write_step(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.synchronize()
        gmsh.write(str(path))


def _module_z_starts() -> list[tuple[str, float, float, float, float, float]]:
    """(name, z_start, length, set_od, set_id, run_od)."""
    z = 0.0
    rows = []
    for name, length, set_od, set_id, run_od in MODULES:
        rows.append((name, z, length, set_od, set_id, run_od))
        z += length
    return rows


def build_plug_set_model(model: OccModel) -> None:
    """54\" plug — SET condition, separate solid per BOM item."""
    rows = _module_z_starts()

    # --- Inner mandrel (stepped) ---
    mandrel_tags: list[tuple[int, int]] = []
    mandrel_tags.append(model.add_cylinder(0, 3.0, 1.35 / 2))
    mandrel_tags.append(model.add_cylinder(3.0, 51.0, 1.55 / 2))
    model.register_part("SHEX-011_inner_mandrel", "17-4 PH H900", mandrel_tags, "Through bore; tail 1.35 in")

    seal_idx = 0
    for name, z0, length, set_od, set_id, _run_od in rows:
        ro, ri = set_od / 2, set_id / 2 if set_id > 0 else 0.0
        tags: list[tuple[int, int]] = []

        if name == "mandrel_tail":
            tags = [model.add_cylinder(z0, length, ro)]
            model.register_part("SHEX-011_mandrel_tail_sleeve", "4140 HT", tags)

        elif name == "bottom_sub":
            tags = model.add_annulus(z0, length, 0.75 / 2, ro)
            model.register_part("SHEX-013_bottom_equalizing_sub", "4140 HT", tags, "Ported equalizing sub")

        elif name in {"lower_slips", "upper_slips"}:
            tags = model.add_annulus(z0, length, ri, ro)
            slip = "SHEX-007_lower_slip_cartridge" if "lower" in name else "SHEX-006_upper_slip_cartridge"
            for i in range(8):
                ang = i * 45.0
                tags.append(model.add_box_radial(z0 + 0.1, length - 0.2, (ri + ro) / 2, ro - ri, 0.35, ang))
            model.register_part(slip, "17-4 PH H900", tags, "8 wedge segments; case hardened OD")

        elif name == "stage1":
            tags = model.add_annulus(z0, length, 1.45 / 2, ro)
            model.register_part("SHEX-008_stage1_stent_sleeve", "17-4 PH H900", tags, "Laser cut; bladder actuated")

        elif name == "stage2":
            tags = model.add_annulus(z0, length, 3.375 / 2, ro)
            model.register_part("SHEX-009_stage2_stent_sleeve", "17-4 PH H900", tags, "Laser cut; Belleville actuated")

        elif name == "stage3_iris":
            tags = model.add_annulus(z0, length, 3.375 / 2, 5.750 / 2)
            model.register_part("SHEX-010_stage3_iris_support_sleeve", "17-4 PH H900", tags, "Fixed sleeve; helix guide bore")
            seg_tags: list[tuple[int, int]] = []
            seg_z = z0 + (length - 2.75) / 2
            for i in range(16):
                seg_tags.extend(model.add_iris_segment(seg_z, i * 22.5))
            model.register_part("SHEX-001_iris_segment_x16", "17-4 PH H900", seg_tags, "Qty 16; t=0.187 in")

        elif name == "seal_land":
            seal_idx += 1
            tags = model.add_annulus(z0, length * 0.82, ri, ro)
            lip = model.add_cone(z0 + length * 0.82, length * 0.18, ro - 0.08, ro)
            tags.extend([lip])
            model.register_part(f"SHEX-004_seal_land_{seal_idx}", "HNBR + 17-4 PH", tags, "HNBR cup + petal backups")

        elif name == "upper_mtm":
            tags = model.add_annulus(z0, length, 8.40 / 2, ro)
            model.register_part("SHEX-003_upper_mtm_stack", "17-4 PH H900", tags, "3 ring stack")

        elif name == "fishing_neck":
            tags = [model.add_cone(z0, length * 0.65, 1.55 / 2, 1.375 / 2)]
            tags.extend(model.add_annulus(z0 + length * 0.65, length * 0.35, 0, 1.375 / 2))
            model.register_part("SHEX-012_fishing_neck", "4140 HT", tags, "1.375 in AMMT")


def build_plug_run_in_model(model: OccModel) -> None:
    """54\" plug — RUN-IN (collapsed on mandrel)."""
    total = sum(m[1] for m in MODULES)
    mandrel = [model.add_cylinder(0, 3.0, 1.35 / 2), model.add_cylinder(3.0, total - 3.0, 1.55 / 2)]
    model.register_part("SHEX-011_inner_mandrel", "17-4 PH H900", mandrel)

    z = 0.0
    for name, length, _so, _si, run_od in MODULES:
        ro = run_od / 2
        if name == "fishing_neck":
            tags = [model.add_cone(z, length * 0.65, 1.55 / 2, 1.375 / 2)]
            tags.extend(model.add_annulus(z + length * 0.65, length * 0.35, 0, 1.375 / 2))
        elif name == "mandrel_tail":
            tags = [model.add_cylinder(z, length, ro)]
        else:
            tags = model.add_annulus(z, length, 1.55 / 2 + 0.02, ro + 0.03)
        model.register_part(f"run_in_{name}_{z:.1f}", "17-4 PH / HNBR", tags)
        z += length


SETTING_TOOL_MODULES = [
    ("ST_crossover", 10.0, 3.375, "4140 HT"),
    ("ST_release", 8.0, 3.375, "17-4 PH"),
    ("ST_pressure", 14.0, 3.625, "17-4 PH"),
    ("ST_stroke", 54.0, 3.625, "17-4 PH"),
    ("ST_loadcell", 10.0, 3.625, "17-4 PH"),
    ("ST_motor", 30.0, 3.625, "17-4 PH"),
    ("ST_battery", 84.0, 3.625, "17-4 PH"),
    ("ST_telemetry", 22.0, 3.625, "17-4 PH"),
    ("ST_head", 14.0, 3.625, "4140 HT"),
]


def build_setting_tool_model(model: OccModel) -> None:
    """SHEX-ST-54 setting tool — bottom crossover at z=0."""
    z = 0.0
    stroke_z = 10.0 + 8.0 + 14.0
    inner_tags: list[tuple[int, int]] = []

    for part_name, length, od, material in SETTING_TOOL_MODULES:
        ro = od / 2
        tags = [model.add_cylinder(z, length, ro)]
        flange_ro = ro + 0.06 if od >= 3.625 else ro + 0.04
        tags.extend(model.add_annulus(z + length - 0.35, 0.35, ro - 0.04, flange_ro))
        model.register_part(part_name, material, tags)
        z += length

    inner_tags.append(model.add_cylinder(stroke_z + 8.0, 11.6, 1.55 / 2))
    inner_tags.extend(model.add_annulus(stroke_z + 20.0, 11.6, 3.625 / 2 - 0.32, 3.625 / 2 - 0.18))
    model.register_part("ST_inner_stroke_mandrel", "17-4 PH H900", inner_tags, "Telescoping stroke bore")


def export_assembly_step(build_fn, assembly_name: str, path: Path) -> list[SolidPart]:
    with occ_session(assembly_name) as model:
        build_fn(model)
        model.write_step(path)
        return list(model.parts)


@contextmanager
def occ_session(name: str) -> Iterator[OccModel]:
    model = OccModel(name)
    try:
        yield model
    finally:
        model.close()


def export_key_part_steps(out_dir: Path) -> list[str]:
    """Dedicated single-part STEP exports for RFQ / machining."""
    out_dir.mkdir(parents=True, exist_ok=True)
    files: list[str] = []

    with occ_session("mandrel") as m:
        tags = [m.add_cylinder(0, 3.0, 1.35 / 2), m.add_cylinder(3.0, 51.0, 1.55 / 2)]
        p = out_dir / "SHEX-011_inner_mandrel.stp"
        m.write_step(p)
        files.append(str(p))

    with occ_session("iris_one") as m:
        tags = m.add_iris_segment(0, 0)
        m.register_part("SHEX-001_iris_segment", "17-4 PH H900", tags)
        p = out_dir / "SHEX-001_iris_segment.stp"
        m.write_step(p)
        files.append(str(p))

    with occ_session("iris_ring") as m:
        tags: list[tuple[int, int]] = []
        for i in range(16):
            tags.extend(m.add_iris_segment(0, i * 22.5))
        p = out_dir / "SHEX-001_iris_ring_16seg.stp"
        m.write_step(p)
        files.append(str(p))

    sleeve_parts = [
        ("SHEX-008_stage1", 4.0, 1.45 / 2, 3.375 / 2),
        ("SHEX-009_stage2", 5.0, 3.375 / 2, 5.750 / 2),
        ("SHEX-010_stage3_support", 7.5, 3.375 / 2, 5.750 / 2),
    ]
    for pname, h, ri, ro in sleeve_parts:
        with occ_session(pname) as m:
            m.add_annulus(0, h, ri, ro)
            p = out_dir / f"{pname}.stp"
            m.write_step(p)
            files.append(str(p))

    # Machined subs — standalone at z=0 for Fusion part drawings
    standalone = [
        ("SHEX-012_fishing_neck", lambda m: (
            m.add_cone(0, 3.0 * 0.65, 1.55 / 2, 1.375 / 2),
            m.add_annulus(3.0 * 0.65, 3.0 * 0.35, 0, 1.375 / 2),
        )),
        ("SHEX-013_bottom_equalizing_sub", lambda m: (
            m.add_annulus(0, 2.0, 0.75 / 2, 1.688 / 2),
        )),
        ("SHEX-011_mandrel_tail_sleeve", lambda m: (
            m.add_cylinder(0, 3.0, 1.35 / 2),
        )),
    ]
    for fname, build_fn in standalone:
        with occ_session(fname) as m:
            build_fn(m)
            p = out_dir / f"{fname}.stp"
            m.write_step(p)
            files.append(str(p))

    return files
