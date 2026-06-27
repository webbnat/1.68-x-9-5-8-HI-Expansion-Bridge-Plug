#!/usr/bin/env python3
"""
Machine drawing package — DXF drawings + BOM + drawing index.

Drawings (mm, ASME Y14.5 style notes):
  DWG-001  Stage 3 iris segment (production t=0.187")
  DWG-002  Stage 3 iris module assembly
  DWG-003  Plug 54" general arrangement
  DWG-004  Setting tool SHEX-ST-54 general arrangement
  DWG-005  MTM ring segment
  DWG-006  Detailed prototype whole-tool drawing (run-in + set + sections)
  DWG-007  Seal land module
  DWG-008  Slip segment
  DWG-009  Stage 1 stent sleeve
  DWG-010  Fishing neck / top sub
  DWG-011  Stage 2 stent sleeve
  DWG-012  Stage 3 iris support sleeve
  BOM-001  Bill of materials
"""

from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import ezdxf
from ezdxf import units as dxf_units
from ezdxf.enums import TextEntityAlignment

from cad.units import in_to_mm

OUT = ROOT / "export" / "drawings"
MM = in_to_mm(1.0)


def new_drawing(name: str) -> ezdxf.document.Drawing:
    doc = ezdxf.new("R2010")
    doc.units = dxf_units.MM
    doc.header["$INSUNITS"] = 4
    msp = doc.modelspace()
    doc.layers.add("OUTLINE", color=7)
    doc.layers.add("DIM", color=3)
    doc.layers.add("CENTER", color=1)
    doc.layers.add("TEXT", color=2)
    doc.layers.add("HIDDEN", color=8, linetype="DASHED")
    return doc


def title_block(doc: ezdxf.document.Drawing, dwg_no: str, title: str, rev: str = "A") -> None:
    msp = doc.modelspace()
    x0, y0 = 10, 10
    w, h = 180, 40
    msp.add_lwpolyline([(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h), (x0, y0)], dxfattribs={"layer": "OUTLINE"})
    lines = [
        (f"DWG NO: {dwg_no}", x0 + 5, y0 + 28),
        (title, x0 + 5, y0 + 20),
        ("SHEX-BP-UHEX-54", x0 + 5, y0 + 12),
        (f"REV: {rev}", x0 + 130, y0 + 28),
        ("UNLESS NOTED: mm", x0 + 130, y0 + 12),
        ("MATL: 17-4 PH H900", x0 + 5, y0 + 4),
    ]
    for text, x, y in lines:
        msp.add_text(text, dxfattribs={"layer": "TEXT", "height": 3.5}).set_placement((x, y))


def save_dxf(doc: ezdxf.document.Drawing, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    doc.saveas(str(path))


def _view_title(msp, text: str, x: float, y: float, scale: str | None = None) -> None:
    label = f"{text}  ({scale})" if scale else text
    msp.add_text(label, dxfattribs={"layer": "TEXT", "height": 3.2}).set_placement((x, y))


def _draw_arc_segment(
    msp,
    cx: float,
    cy: float,
    r_in: float,
    r_out: float,
    ang0_deg: float,
    ang1_deg: float,
    layer: str = "OUTLINE",
) -> None:
    msp.add_arc((cx, cy), r_in, ang0_deg, ang1_deg, dxfattribs={"layer": layer})
    msp.add_arc((cx, cy), r_out, ang0_deg, ang1_deg, dxfattribs={"layer": layer})
    a0, a1 = math.radians(ang0_deg), math.radians(ang1_deg)
    msp.add_line((cx + r_in * math.cos(a0), cy + r_in * math.sin(a0)),
                 (cx + r_out * math.cos(a0), cy + r_out * math.sin(a0)), dxfattribs={"layer": layer})
    msp.add_line((cx + r_in * math.cos(a1), cy + r_in * math.sin(a1)),
                 (cx + r_out * math.cos(a1), cy + r_out * math.sin(a1)), dxfattribs={"layer": layer})


def _draw_dim_text(msp, text: str, x: float, y: float, h: float = 2.6) -> None:
    msp.add_text(text, dxfattribs={"layer": "DIM", "height": h}).set_placement((x, y))


def _draw_notes(msp, notes: list[str], x: float, y: float, line_h: float = 6.0) -> None:
    for i, note in enumerate(notes):
        msp.add_text(note, dxfattribs={"layer": "TEXT", "height": 2.5}).set_placement((x, y - i * line_h))


def _draw_stent_zigzag(
    msp,
    x0: float,
    y0: float,
    length: float,
    amplitude: float,
    cells: int,
    layer: str = "OUTLINE",
) -> None:
    """Developed stent strip — zig-zag strut pattern."""
    pitch = length / cells
    pts: list[tuple[float, float]] = [(x0, y0)]
    for i in range(cells):
        x = x0 + (i + 0.5) * pitch
        y = y0 + (amplitude if i % 2 == 0 else -amplitude)
        pts.append((x, y))
        pts.append((x0 + (i + 1) * pitch, y0))
    msp.add_lwpolyline(pts, dxfattribs={"layer": layer})


def _draw_stent_sleeve_sheet(
    *,
    dwg_no: str,
    title: str,
    filename: str,
    part_no: str,
    length_in: float,
    od_run_in: float,
    od_set_in: float,
    id_in: float,
    wall_in: float,
    cells: int,
    rings: int,
    actuator_note: str,
    extra_notes: list[str] | None = None,
) -> Path:
    """Shared layout for laser-cut expansion stent sleeves (DWG-009 class)."""
    doc = new_drawing(filename)
    msp = doc.modelspace()
    title_block(doc, dwg_no, title)

    length = in_to_mm(length_in)
    od_run = in_to_mm(od_run_in)
    od_set = in_to_mm(od_set_in)
    wall = in_to_mm(wall_in)
    scale = 0.12

    ox, oy = 35, 165
    _view_title(msp, "VIEW 1 — SIDE (SET)", ox, oy + od_set / 2 * scale + 18, "SCALE 1:3")
    ro = od_set / 2 * scale
    ri = ro - wall * scale * 3
    draw_len = length * scale * 0.55
    msp.add_lwpolyline([
        (ox, oy + ri), (ox + draw_len, oy + ri), (ox + draw_len, oy + ro),
        (ox, oy + ro * 0.55), (ox, oy + ri),
    ], dxfattribs={"layer": "OUTLINE"})
    _draw_stent_zigzag(msp, ox + 5, oy + (ri + ro) / 2, draw_len - 10, (ro - ri) * 0.35, cells)
    _draw_dim_text(msp, f"L {length:.1f}", ox + draw_len * 0.3, oy - 8)
    _draw_dim_text(msp, f"OD {od_set:.1f} SET", ox + draw_len + 4, oy + ro * 0.6, 2.3)

    px, py = 35, 75
    _view_title(msp, "VIEW 2 — RUN-IN / SET TABLE", px, py + 22)
    rows = [
        ("RUN-IN OD", f"{od_run:.1f} mm ({od_run_in:.3f} IN)"),
        ("SET OD", f"{in_to_mm(od_set_in):.1f} mm ({od_set_in:.3f} IN)"),
        ("ID", f"{in_to_mm(id_in):.1f} mm ({id_in:.3f} IN)"),
        ("WALL", f"{wall:.2f} mm ({wall_in:.3f} IN)"),
        ("CELLS x RINGS", f"{cells} x {rings}"),
    ]
    for i, (k, v) in enumerate(rows):
        msp.add_text(f"{k}: {v}", dxfattribs={"layer": "TEXT", "height": 2.5}).set_placement((px, py - i * 7))

    # Developed strip hint
    sx, sy = 170, 165
    _view_title(msp, "VIEW 3 — DEVELOPED STRUT STRIP (SCHEMATIC)", sx, sy + 18)
    strip_l = draw_len * 1.4
    _draw_stent_zigzag(msp, sx, sy, strip_l, 4.5, cells * 2, layer="HIDDEN")
    _draw_dim_text(msp, "LASER CUT FROM FLAT PATTERN", sx, sy - 8, 2.3)

    notes = [
        f"PART NO: {part_no}",
        "LASER CUT TUBE | CRIMPED ON MANDREL AT RUN-IN",
        actuator_note,
        f"{cells} CELLS x {rings} RINGS TYP",
    ]
    if extra_notes:
        notes.extend(extra_notes)
    _draw_notes(msp, notes, 170, 95)

    path = OUT / "dxf" / filename
    save_dxf(doc, path)
    return path


def draw_iris_segment() -> Path:
    doc = new_drawing("iris_segment")
    msp = doc.modelspace()
    title_block(doc, "DWG-001", "STAGE 3 IRIS SEGMENT")

    r_in = in_to_mm(5.750 / 2 + 0.080)
    r_out = in_to_mm(8.650 / 2 - 0.015)
    t = in_to_mm(0.187)
    axial = in_to_mm(2.750)
    span_deg = 22.5

    ax, ay = 55, 195
    _view_title(msp, "VIEW A — RADIAL END", ax, ay + 58, "SCALE 1:2")
    _draw_centerline(msp, ax - 8, ax + r_out + 18, ay)
    msp.add_line((ax, ay - 8), (ax, ay + r_out + 12), dxfattribs={"layer": "CENTER", "linetype": "CENTER"})
    _draw_arc_segment(msp, ax, ay, r_in, r_out, 0, span_deg)
    tip = math.radians(span_deg)
    for r, sign in ((r_out, 1), (r_in, -1)):
        px, py = ax + r * math.cos(tip), ay + r * math.sin(tip)
        msp.add_line((px, py), (px - 2.5, py + sign * 2.5), dxfattribs={"layer": "OUTLINE"})
    _draw_dim_text(msp, f"R {r_in:.1f}", ax + r_in * 0.55, ay + r_in * 0.45)
    _draw_dim_text(msp, f"R {r_out:.1f}", ax + r_out * 0.7, ay + r_out * 0.25)
    _draw_dim_text(msp, f"{span_deg} DEG", ax + 6, ay + 8)

    bx, by = 55, 115
    _view_title(msp, "VIEW B — AXIAL SECTION", bx, by + 38, "SCALE 1:2")
    msp.add_lwpolyline([
        (bx, by), (bx + axial, by), (bx + axial, by + t),
        (bx, by + t), (bx, by),
    ], dxfattribs={"layer": "OUTLINE"})
    msp.add_line((bx, by + t * 0.15), (bx + axial, by + t * 0.15), dxfattribs={"layer": "HIDDEN", "linetype": "DASHED"})
    msp.add_line((bx, by + t * 0.85), (bx + axial, by + t * 0.85), dxfattribs={"layer": "HIDDEN", "linetype": "DASHED"})
    _draw_dim_text(msp, f"{axial:.2f}", bx + axial / 2 - 8, by - 8)
    _draw_dim_text(msp, f"{t:.2f}", bx + axial + 4, by + t / 2)
    _draw_dim_text(msp, f"RAD {r_in:.1f}-{r_out:.1f}", bx, by + t + 6, 2.3)

    cx, cy = 200, 175
    _view_title(msp, "DETAIL C — ROOT / TOE", cx, cy + 28, "SCALE 3:1")
    fillet_r = in_to_mm(0.030)
    cham = in_to_mm(0.25)
    msp.add_line((cx, cy), (cx + cham, cy), dxfattribs={"layer": "OUTLINE"})
    msp.add_line((cx + cham, cy), (cx + cham + 8, cy + 8), dxfattribs={"layer": "OUTLINE"})
    msp.add_arc((cx + fillet_r, cy + 8 - fillet_r), fillet_r, 90, 180, dxfattribs={"layer": "OUTLINE"})
    msp.add_line((cx, cy + 8), (cx, cy + t * 3), dxfattribs={"layer": "OUTLINE"})
    msp.add_line((cx + cham + 8, cy + 8), (cx + cham + 8, cy + t * 3), dxfattribs={"layer": "OUTLINE"})
    _draw_dim_text(msp, f"R{fillet_r:.2f} MIN", cx + 2, cy + 14, 2.2)
    _draw_dim_text(msp, f"{cham:.2f} x 45 DEG", cx + 4, cy - 6, 2.2)

    hx, hy = 200, 115
    _view_title(msp, "DETAIL D — HELIX SLOT", hx, hy + 22, "SCALE 2:1")
    slot_l = in_to_mm(0.625)
    slot_w = in_to_mm(0.125)
    msp.add_lwpolyline([
        (hx, hy), (hx + slot_l, hy), (hx + slot_l, hy + slot_w),
        (hx, hy + slot_w), (hx, hy),
    ], dxfattribs={"layer": "OUTLINE"})
    _draw_dim_text(msp, f"{slot_l:.2f}", hx + slot_l / 2 - 6, hy - 6, 2.2)
    _draw_dim_text(msp, f"{slot_w:.2f}", hx - 18, hy + slot_w / 2, 2.2)

    _draw_notes(msp, [
        "PART NO: SHEX-001",
        "QTY: 16 PER IRIS MODULE",
        "MATL: 17-4 PH H900",
        "FINISH: ELECTROPOLISH",
        "BREAK SHARP EDGES 0.25 MAX",
        "ANGULARITY: +/- 0.5 DEG TO MODULE C/L",
    ], 10, 95)

    path = OUT / "dxf" / "DWG-001_iris_segment.dxf"
    save_dxf(doc, path)
    return path


def draw_iris_module() -> Path:
    doc = new_drawing("iris_module")
    msp = doc.modelspace()
    title_block(doc, "DWG-002", "STAGE 3 IRIS MODULE ASSY")

    length = in_to_mm(7.5)
    od_coll = in_to_mm(5.750)
    od_dep = in_to_mm(8.650)
    id_bore = in_to_mm(5.750)
    stroke = in_to_mm(4.0)

    ox, oy = 35, 175
    lx_s, od_s = 0.28, 0.10
    L = length * lx_s
    ro_coll = od_coll / 2 * od_s
    ro_dep = od_dep / 2 * od_s
    ri = id_bore / 2 * od_s
    _view_title(msp, "VIEW 1 — MODULE HALF-SECTION (SET)", ox, oy + ro_dep + 22, f"L 1:{1/lx_s:.0f}  OD 1:{1/od_s:.0f}")
    _draw_centerline(msp, ox - 8, ox + L + 8, oy)

    x_stroke = ox + L * 0.42
    x_end = ox + L
    msp.add_lwpolyline([
        (ox, oy), (x_stroke, oy), (x_end, oy),
        (x_end, oy + ro_dep), (x_stroke, oy + ro_dep),
        (ox, oy + ro_coll), (ox, oy),
    ], dxfattribs={"layer": "OUTLINE"})
    msp.add_line((ox, oy + ri), (x_end, oy + ri), dxfattribs={"layer": "HIDDEN", "linetype": "DASHED"})

    for zx, lbl in [
        (ox + L * 0.12, "COLLAPSED POCKET"),
        (x_stroke + L * 0.08, "HELIX ACTUATION"),
        (x_end - L * 0.12, "LOCK LAND"),
    ]:
        msp.add_text(lbl, dxfattribs={"layer": "TEXT", "height": 2.2}).set_placement((zx, oy + ro_coll + 6))

    _draw_dim_text(msp, f"L {length:.1f}", ox + L / 2 - 10, oy - 10)
    _draw_dim_text(msp, f"OD {od_coll:.1f} COLL", ox - 5, oy + ro_coll + 2, 2.3)
    _draw_dim_text(msp, f"OD {od_dep:.1f} DEP", x_end - 30, oy + ro_dep + 2, 2.3)
    _draw_dim_text(msp, f"STROKE {stroke:.1f}", x_stroke, oy - 18, 2.3)

    px, py = 35, 75
    _view_title(msp, "VIEW 2 — SECTION B-B (DEPLOYED)", px, py + od_dep / 2 + 18, "SCALE 1:4")
    pcx, pcy = px + od_dep / 2 + 5, py + od_dep / 2 + 5
    msp.add_circle((pcx, pcy), od_dep / 2, dxfattribs={"layer": "OUTLINE"})
    msp.add_circle((pcx, pcy), id_bore / 2, dxfattribs={"layer": "HIDDEN"})
    for i in range(16):
        a0 = i * 22.5 + 0.6
        a1 = (i + 1) * 22.5 - 0.6
        _draw_arc_segment(msp, pcx, pcy, id_bore / 2 + 2, od_dep / 2 - 1, a0, a1)
    msp.add_circle((pcx, pcy), 2.0, dxfattribs={"layer": "CENTER"})
    _draw_dim_text(msp, "16 SEG @ 22.5 DEG", px, py - 6)

    hx, hy = 200, 155
    _view_title(msp, "VIEW 3 — HELIX GUIDE", hx, hy + 28)
    helix_l = in_to_mm(7.5) * 0.35
    msp.add_line((hx, hy), (hx + helix_l, hy), dxfattribs={"layer": "OUTLINE"})
    msp.add_line((hx, hy + 6), (hx + helix_l, hy + 6), dxfattribs={"layer": "OUTLINE"})
    pts1, pts2 = [], []
    turns = 2
    for i in range(25):
        t = i / 24
        x = hx + t * helix_l
        pts1.append((x, hy + 3 + 2.5 * math.sin(t * turns * 2 * math.pi)))
        pts2.append((x, hy + 3 + 2.5 * math.sin(t * turns * 2 * math.pi + math.pi)))
    msp.add_lwpolyline(pts1, dxfattribs={"layer": "HIDDEN", "linetype": "DASHED"})
    msp.add_lwpolyline(pts2, dxfattribs={"layer": "HIDDEN", "linetype": "DASHED"})
    _draw_dim_text(msp, "IN718 DOUBLE START", hx, hy - 8, 2.3)
    _draw_dim_text(msp, "LEAD 4.0 IN (101.6)", hx + helix_l * 0.25, hy + 12, 2.3)

    _draw_notes(msp, [
        "ASSY: 16 x SHEX-001 + HELIX GUIDE + RETAINER",
        "COLLAPSED OD 5.750 IN | DEPLOYED OD 8.650 IN",
        "ACTUATION: SETTING TOOL ROTARY + AXIAL 4 IN",
        "SEGMENT THK 0.187 IN (PRODUCTION)",
    ], 200, 95)

    path = OUT / "dxf" / "DWG-002_iris_module_assy.dxf"
    save_dxf(doc, path)
    return path


def _draw_centerline(msp, x0: float, x1: float, y: float) -> None:
    msp.add_line((x0, y), (x1, y), dxfattribs={"layer": "CENTER", "linetype": "CENTER"})


def draw_plug_ga() -> Path:
    doc = new_drawing("plug_ga")
    msp = doc.modelspace()
    title_block(doc, "DWG-003", "PLUG 54 IN GENERAL ARRANGEMENT")

    ox, oy = 30, 120
    lx_scale = 0.35
    od_scale = 0.12  # true radial scale for set OD profile
    modules = _module_stack_set()

    msp.add_text("SET CONDITION — BOTTOM (ITEM 1) AT LEFT", dxfattribs={"layer": "TEXT", "height": 3}).set_placement((ox, oy + 55))
    _draw_centerline(msp, ox - 10, ox + in_to_mm(54.0) * lx_scale + 10, oy)
    total_w = _draw_envelope_half_section(msp, ox, oy, modules, lx_scale, od_scale)

    x = ox
    item = 1
    for label, length_in, _od, _id in modules:
        ln = in_to_mm(length_in) * lx_scale
        if length_in >= 4.0:
            msp.add_text(label, dxfattribs={"layer": "TEXT", "height": 2.0}).set_placement((x + 2, oy + in_to_mm(_od) / 2 * od_scale + 6))
        msp.add_text(str(item), dxfattribs={"layer": "DIM", "height": 2.2}).set_placement((x + ln / 2, oy - 8))
        x += ln
        item += 1

    msp.add_text(f"TOTAL LENGTH = {in_to_mm(54.0):.1f} mm (54.0 IN)", dxfattribs={"layer": "DIM", "height": 3.5}).set_placement((ox, oy - 22))
    msp.add_text("RUN OD 1.688 IN | SET MAX OD 8.650 IN | 9-5/8 IN 40# CSG", dxfattribs={"layer": "TEXT", "height": 3}).set_placement((ox, oy - 32))
    msp.add_text(f"LENGTH SCALE 1:{1/lx_scale:.0f}  |  OD SCALE 1:{1/od_scale:.0f} (NOT SAME)", dxfattribs={"layer": "TEXT", "height": 2.5}).set_placement((ox + total_w * 0.35, oy - 32))

    path = OUT / "dxf" / "DWG-003_plug_54in_GA.dxf"
    save_dxf(doc, path)
    return path


def _module_stack_set() -> list[tuple[str, float, float, float]]:
    """(label, length_in, od_in, id_in) bottom to top for SET condition."""
    return [
        ("MANDREL TAIL", 3.0, 1.35, 0.0),
        ("BOTTOM SUB", 2.0, 1.688, 0.75),
        ("LOWER SLIPS", 4.5, 8.72, 1.55),
        ("STG1 INNER", 4.0, 3.375, 1.45),
        ("STG2 MIDDLE", 5.0, 5.750, 3.375),
        ("STG3 IRIS", 7.5, 8.650, 5.750),
        ("SEAL LAND 1", 4.5, 8.720, 1.55),
        ("SEAL LAND 2", 4.5, 8.720, 1.55),
        ("SEAL LAND 3", 4.5, 8.720, 1.55),
        ("SEAL LAND 4", 4.5, 8.720, 1.55),
        ("UPPER MTM", 2.5, 8.800, 8.40),
        ("UPPER SLIPS", 4.5, 8.72, 1.55),
        ("FISH NECK", 3.0, 1.375, 0.0),
    ]


def _run_in_zones() -> list[tuple[str, float, float]]:
    """(label, length_in, od_in) bottom to top for run-in."""
    return [
        ("MANDREL TAIL", 3.0, 1.35),
        ("BOTTOM SUB", 2.0, 1.688),
        ("LOWER SLIPS", 4.5, 1.688),
        ("STG1", 4.0, 1.688),
        ("STG2", 5.0, 1.688),
        ("STG3 IRIS", 7.5, 1.688),
        ("SEAL x4", 18.0, 1.688),
        ("UPPER MTM", 2.5, 1.688),
        ("UPPER SLIPS", 4.5, 1.688),
        ("FISH NECK", 3.0, 1.375),
    ]


def _draw_envelope_half_section(
    msp,
    x: float,
    y: float,
    modules: list[tuple[str, float, float, float]],
    lx_scale: float,
    od_scale: float,
    draw_inner: bool = True,
) -> float:
    """Continuous outer (and inner mandrel) envelope — bottom module at left."""
    outer_pts: list[tuple[float, float]] = []
    inner_pts: list[tuple[float, float]] = []
    xcur = x
    for _label, length_in, od_in, id_in in modules:
        ln = in_to_mm(length_in) * lx_scale
        ro = in_to_mm(od_in) / 2 * od_scale
        ri = in_to_mm(id_in) / 2 * od_scale if id_in > 0 else 0.0
        outer_pts.append((xcur, y + ro))
        outer_pts.append((xcur + ln, y + ro))
        if draw_inner and ri > 0:
            inner_pts.append((xcur, y + ri))
            inner_pts.append((xcur + ln, y + ri))
        xcur += ln

    if outer_pts:
        msp.add_lwpolyline([(x, y), *outer_pts, (xcur, y), (x, y)], dxfattribs={"layer": "OUTLINE"})
    if inner_pts:
        msp.add_lwpolyline(inner_pts, dxfattribs={"layer": "HIDDEN", "linetype": "DASHED"})

    # Module boundary ticks
    xcur = x
    for _label, length_in, _od, _id in modules:
        ln = in_to_mm(length_in) * lx_scale
        msp.add_line((xcur, y - 3), (xcur, y + 3), dxfattribs={"layer": "CENTER", "linetype": "CENTER"})
        xcur += ln
    msp.add_line((xcur, y - 3), (xcur, y + 3), dxfattribs={"layer": "CENTER", "linetype": "CENTER"})
    return xcur - x


def _draw_half_section(msp, x: float, y: float, length: float, od: float, id_: float = 0) -> float:
    """Draw upper half cross-section; return od/2 for dimensioning."""
    ro = od / 2
    ri = id_ / 2 if id_ > 0 else 0
    pts = [(x, y), (x + length, y), (x + length, y + ro), (x, y + ro), (x, y)]
    msp.add_lwpolyline(pts, dxfattribs={"layer": "OUTLINE"})
    if ri > 0:
        msp.add_line((x, y + ri), (x + length, y + ri), dxfattribs={"layer": "HIDDEN", "linetype": "DASHED"})
    return ro


def draw_prototype_detailed() -> Path:
    """DWG-006: Detailed prototype — run-in, set elevation, sections, dim table."""
    doc = new_drawing("prototype_detailed")
    msp = doc.modelspace()
    title_block(doc, "DWG-006", "PROTOTYPE WHOLE TOOL DETAILED")

    lx_scale = 0.35
    od_scale = 0.12
    total_in = 54.0

    # --- VIEW 1: RUN-IN elevation (bottom at left) ---
    ox, oy = 40, 280
    run_stack: list[tuple[str, float, float, float]] = [
        ("MANDREL TAIL", 3.0, 1.35, 0.0),
        ("BOTTOM SUB", 2.0, 1.688, 0.75),
        ("LOWER SLIPS", 4.5, 1.688, 1.55),
        ("STG1", 4.0, 1.688, 1.55),
        ("STG2", 5.0, 1.688, 1.55),
        ("STG3 IRIS", 7.5, 1.688, 1.55),
        ("SEAL x4", 18.0, 1.688, 1.55),
        ("UPPER MTM", 2.5, 1.688, 1.55),
        ("UPPER SLIPS", 4.5, 1.688, 1.55),
        ("FISH NECK", 3.0, 1.375, 0.0),
    ]

    msp.add_text("VIEW 1 - RUN-IN ELEVATION (THRU-TUBING)", dxfattribs={"layer": "TEXT", "height": 4}).set_placement((ox, oy + 40))
    msp.add_text("BOTTOM (MANDREL TAIL) AT LEFT", dxfattribs={"layer": "TEXT", "height": 2.5}).set_placement((ox, oy + 33))
    _draw_centerline(msp, ox - 10, ox + in_to_mm(total_in) * lx_scale + 10, oy)
    _draw_envelope_half_section(msp, ox, oy, run_stack, lx_scale, od_scale * 0.85)

    x = ox
    item = 1
    for label, length_in, od_in, _id in run_stack:
        ln = in_to_mm(length_in) * lx_scale
        if length_in >= 4.0 or label in {"STG1", "STG2", "STG3 IRIS", "FISH NECK"}:
            msp.add_text(label, dxfattribs={"layer": "TEXT", "height": 2.0}).set_placement((x + 2, oy + in_to_mm(od_in) / 2 * od_scale * 0.85 + 5))
        msp.add_text(str(item), dxfattribs={"layer": "DIM", "height": 2.2}).set_placement((x + ln / 2, oy - 8))
        x += ln
        item += 1

    msp.add_text("OD 42.9 mm (1.688 IN) MAX RUN-IN", dxfattribs={"layer": "DIM", "height": 3}).set_placement((ox, oy - 20))
    msp.add_text(f"L = {in_to_mm(total_in):.1f} mm (54.0 IN)", dxfattribs={"layer": "DIM", "height": 3}).set_placement((ox, oy - 28))

    # --- VIEW 2: SET elevation (bottom at left, continuous envelope) ---
    ox2, oy2 = 40, 170
    set_modules = _module_stack_set()
    msp.add_text("VIEW 2 - SET ELEVATION (9-5/8 IN 40# CSG)", dxfattribs={"layer": "TEXT", "height": 4}).set_placement((ox2, oy2 + 125))
    msp.add_text("BOTTOM (MANDREL TAIL) AT LEFT", dxfattribs={"layer": "TEXT", "height": 2.5}).set_placement((ox2, oy2 + 118))
    _draw_centerline(msp, ox2 - 10, ox2 + in_to_mm(total_in) * lx_scale + 10, oy2)
    _draw_envelope_half_section(msp, ox2, oy2, set_modules, lx_scale, od_scale)

    x = ox2
    item = 1
    for label, length_in, od_in, _id in set_modules:
        ln = in_to_mm(length_in) * lx_scale
        if length_in >= 4.0 or label in {"STG3 IRIS", "FISH NECK", "UPPER MTM"}:
            msp.add_text(label, dxfattribs={"layer": "TEXT", "height": 2.0}).set_placement((x + 2, oy2 + in_to_mm(od_in) / 2 * od_scale + 5))
        msp.add_text(str(item), dxfattribs={"layer": "DIM", "height": 2.2}).set_placement((x + ln / 2, oy2 - 8))
        x += ln
        item += 1

    # Casing drift reference line
    drift_ro = in_to_mm(8.679) / 2 * od_scale
    msp.add_line((ox2, oy2 + drift_ro), (ox2 + in_to_mm(total_in) * lx_scale, oy2 + drift_ro),
                 dxfattribs={"layer": "DIM", "linetype": "DASHDOT"})
    msp.add_text("CSG DRIFT ID 8.679", dxfattribs={"layer": "DIM", "height": 2.5}).set_placement((ox2 + 40, oy2 + drift_ro + 4))
    msp.add_text("MAX SET OD 219.7 mm (8.650 IN)", dxfattribs={"layer": "DIM", "height": 3}).set_placement((ox2, oy2 - 18))

    # --- VIEW 3: SECTION A-A through seal module ---
    ax, ay = 40, 55
    msp.add_text("SECTION A-A  (SEAL + MTM)", dxfattribs={"layer": "TEXT", "height": 3.5}).set_placement((ax, ay + 55))
    seal_od = in_to_mm(8.72) / 2
    seal_id = in_to_mm(1.55) / 2
    msp.add_circle((ax + 40, ay + 25), seal_od, dxfattribs={"layer": "OUTLINE"})
    msp.add_circle((ax + 40, ay + 25), seal_id, dxfattribs={"layer": "HIDDEN"})
    for i in range(8):
        ang = math.radians(i * 45)
        px = ax + 40 + seal_od * 0.92 * math.cos(ang)
        py = ay + 25 + seal_od * 0.92 * math.sin(ang)
        msp.add_line((ax + 40 + seal_id * math.cos(ang), ay + 25 + seal_id * math.sin(ang)), (px, py),
                     dxfattribs={"layer": "OUTLINE"})
    msp.add_text("HNBR + 16 PETALS", dxfattribs={"layer": "TEXT", "height": 2.5}).set_placement((ax, ay))

    # --- VIEW 4: SECTION B-B through iris ---
    bx, by = 160, 55
    msp.add_text("SECTION B-B  (STG3 IRIS)", dxfattribs={"layer": "TEXT", "height": 3.5}).set_placement((bx, by + 55))
    cx, cy = bx + 35, by + 25
    for i in range(16):
        a0 = math.radians(i * 22.5)
        a1 = math.radians((i + 0.85) * 22.5)
        r0 = in_to_mm(5.75) / 2
        r1 = in_to_mm(8.65) / 2
        msp.add_line((cx + r0 * math.cos(a0), cy + r0 * math.sin(a0)),
                     (cx + r1 * math.cos(a1), cy + r1 * math.sin(a1)), dxfattribs={"layer": "OUTLINE"})
    msp.add_circle((cx, cy), r0, dxfattribs={"layer": "CENTER"})
    msp.add_text("16 SEG @ 22.5", dxfattribs={"layer": "TEXT", "height": 2.5}).set_placement((bx, by))

    # --- Dimension table ---
    tx, ty = 320, 250
    msp.add_text("DIMENSION TABLE (in)", dxfattribs={"layer": "TEXT", "height": 4}).set_placement((tx, ty))
    rows = [
        ("ITEM", "LENGTH", "OD", "ID"),
        ("Fish neck", "3.00", "1.375", "-"),
        ("Upper slips", "4.50", "8.72", "1.55"),
        ("Upper MTM", "2.50", "8.80", "8.40"),
        ("Seal land (x4)", "4.50", "8.72", "1.55"),
        ("Stage 3 iris", "7.50", "8.650", "5.750"),
        ("Stage 2 stent", "5.00", "5.750", "3.375"),
        ("Stage 1 stent", "4.00", "3.375", "1.450"),
        ("Lower slips", "4.50", "8.72", "1.55"),
        ("Bottom sub", "2.00", "1.688", "0.75"),
        ("Mandrel tail", "3.00", "1.350", "-"),
        ("TOTAL", "54.00", "1.688 RUN", "8.65 SET"),
    ]
    for i, row in enumerate(rows):
        line = "  ".join(f"{c:>10}" for c in row)
        msp.add_text(line, dxfattribs={"layer": "TEXT", "height": 2.3}).set_placement((tx, ty - 12 - i * 7))

    notes = [
        "NOTES:",
        "1. RUN-IN MAX OD 1.688 IN FOR THRU-TUBING",
        "2. SET IN 9-5/8 IN 40# CSG (DRIFT ID 8.679 IN)",
        "3. STG1/STG2 ACTUATORS INTERNAL (BLADDER/BELLEVILLE)",
        "4. STG3 IRIS: 4.0 IN STROKE FROM SETTING TOOL",
        "5. 3D REF: output/stl/shex_54/40_plug_uhex_54in_assembly_set.stl",
        "6. Z=0 AT MANDREL TAIL; FISHING NECK AT Z=54 IN",
    ]
    for i, n in enumerate(notes):
        msp.add_text(n, dxfattribs={"layer": "TEXT", "height": 2.8}).set_placement((tx, 80 - i * 8))

    path = OUT / "dxf" / "DWG-006_prototype_whole_tool_detailed.dxf"
    save_dxf(doc, path)
    return path


def draw_setting_tool_ga() -> Path:
    doc = new_drawing("setting_tool")
    msp = doc.modelspace()
    title_block(doc, "DWG-004", "SETTING TOOL SHEX-ST-54 GA")

    # Bottom (crossover) at left — matches shex_54 module stack
    lx_s = 0.22
    od_main = in_to_mm(3.625)
    od_xover = in_to_mm(3.375)
    h_main = od_main / 2 * 0.14
    h_xover = od_xover / 2 * 0.14

    modules = [
        ("XOVER", 10.0, od_xover),
        ("RELEASE", 8.0, od_xover),
        ("PRESS", 14.0, od_main),
        ("STROKE", 54.0, od_main),
        ("LOAD", 10.0, od_main),
        ("MOTOR", 30.0, od_main),
        ("BATTERY", 84.0, od_main),
        ("TELEM", 22.0, od_main),
        ("HEAD", 14.0, od_main),
    ]

    ox, oy = 25, 145
    _view_title(msp, "VIEW 1 — MODULE ELEVATION (BOTTOM AT LEFT)", ox, oy + h_main + 28, f"LENGTH 1:{1/lx_s:.0f}")
    _draw_centerline(msp, ox - 8, ox + sum(in_to_mm(m[1]) for m in modules) * lx_s + 8, oy)

    x = ox
    stroke_x0 = stroke_x1 = 0.0
    for name, length_in, od_in in modules:
        ln = in_to_mm(length_in) * lx_s
        h = (od_in / 2 * 0.14)
        msp.add_lwpolyline([
            (x, oy), (x + ln, oy), (x + ln, oy + h), (x, oy + h), (x, oy),
        ], dxfattribs={"layer": "OUTLINE"})
        if length_in >= 14:
            msp.add_text(name, dxfattribs={"layer": "TEXT", "height": 2.2}).set_placement((x + ln * 0.15, oy + h + 4))
        if name == "STROKE":
            stroke_x0, stroke_x1 = x, x + ln
            msp.add_line((x + ln * 0.15, oy + h * 0.35), (x + ln * 0.85, oy + h * 0.65),
                         dxfattribs={"layer": "HIDDEN", "linetype": "DASHED"})
        x += ln

    total_mm = sum(in_to_mm(m[1]) for m in modules)
    _draw_dim_text(msp, f"L {total_mm:.0f} mm ({total_mm / MM / 12:.1f} ft)", ox + 20, oy - 12)
    _draw_dim_text(msp, f"OD {od_main:.1f} mm (3.625 IN)", ox, oy - 22)
    _draw_dim_text(msp, "STROKE 12.0 IN | 55 klbf", ox + 80, oy - 22)

    # Section A-A through stroke
    sx, sy = 25, 55
    _view_title(msp, "VIEW 2 — SECTION A-A (STROKE ZONE)", sx, sy + 38, "SCALE 1:2")
    ro, ri = od_main / 2 * 0.35, in_to_mm(1.55) / 2 * 0.35
    scx = sx + 35
    msp.add_circle((scx, sy + 18), ro, dxfattribs={"layer": "OUTLINE"})
    msp.add_circle((scx, sy + 18), ri, dxfattribs={"layer": "HIDDEN"})
    msp.add_circle((scx, sy + 18), ro - in_to_mm(0.25) * 0.35, dxfattribs={"layer": "OUTLINE"})
    _draw_dim_text(msp, "TELESCOPING SLEEVE", sx, sy)
    _draw_dim_text(msp, "MANDREL BORE 1.55 IN", sx, sy - 8, 2.3)

    _draw_notes(msp, [
        "BOTTOM: 1.375 AMMT TO PLUG FISHING NECK",
        "TOP: CCL / HEAD CONNECTION",
        "STROKE MODULE DRIVES STG3 IRIS + SEALS + SLIPS",
    ], 200, 145)

    path = OUT / "dxf" / "DWG-004_setting_tool_SHEX-ST-54.dxf"
    save_dxf(doc, path)
    return path


def draw_mtm_ring() -> Path:
    doc = new_drawing("mtm_ring")
    msp = doc.modelspace()
    title_block(doc, "DWG-005", "MTM RING SEGMENT")

    ro = in_to_mm(8.800 / 2)
    ri = in_to_mm(8.400 / 2)
    radial_w = ro - ri
    h = in_to_mm(0.45)
    span_deg = 30.0  # 12 segments per ring

    # VIEW A: radial end
    ax, ay = 50, 175
    _view_title(msp, "VIEW A — RADIAL END", ax, ay + ro * 0.35 + 20, "SCALE 1:4")
    _draw_arc_segment(msp, ax, ay, ri, ro, 0, span_deg)
    _draw_dim_text(msp, f"{span_deg} DEG", ax + 5, ay + 5)
    _draw_dim_text(msp, f"Ri {ri:.1f}", ax + ri * 0.5, ay + ri * 0.35, 2.3)
    _draw_dim_text(msp, f"Ro {ro:.1f}", ax + ro * 0.65, ay + ro * 0.2, 2.3)

    # VIEW B: axial section
    bx, by = 50, 95
    _view_title(msp, "VIEW B — AXIAL SECTION", bx, by + 28, "SCALE 2:1")
    msp.add_lwpolyline([
        (bx, by), (bx + h, by), (bx + h, by + radial_w),
        (bx, by + radial_w), (bx, by),
    ], dxfattribs={"layer": "OUTLINE"})
    groove = in_to_mm(0.12)
    msp.add_line((bx + h * 0.35, by + radial_w * 0.2), (bx + h * 0.35, by + radial_w * 0.8),
                 dxfattribs={"layer": "HIDDEN", "linetype": "DASHED"})
    _draw_dim_text(msp, f"H {h:.2f}", bx + h + 3, by + radial_w / 2)
    _draw_dim_text(msp, f"W {radial_w:.2f}", bx - 22, by + radial_w / 2)

    # VIEW C: stack context
    cx, cy = 170, 140
    _view_title(msp, "VIEW C — 3-RING STACK IN MODULE", cx, cy + 35)
    stack_h = in_to_mm(2.5) * 0.45
    for i in range(3):
        y = cy + i * stack_h * 0.38
        msp.add_lwpolyline([
            (cx, y), (cx + stack_h, y), (cx + stack_h, y + radial_w * 0.25),
            (cx, y + radial_w * 0.25), (cx, y),
        ], dxfattribs={"layer": "OUTLINE"})
    _draw_dim_text(msp, "UPPER MTM MODULE L 2.5 IN", cx, cy - 10, 2.3)

    _draw_notes(msp, [
        "PART NO: SHEX-003",
        "QTY: 12 (3 RINGS x 4 SEG/RING)",
        "MATL: 17-4 PH H900",
        "DOVETAIL ENGAGES SEAL LAND OD 8.720",
    ], 10, 75)

    path = OUT / "dxf" / "DWG-005_mtm_ring_segment.dxf"
    save_dxf(doc, path)
    return path


def draw_seal_land() -> Path:
    doc = new_drawing("seal_land")
    msp = doc.modelspace()
    title_block(doc, "DWG-007", "SEAL LAND MODULE")

    length = in_to_mm(4.5)
    od = in_to_mm(8.720)
    mandrel = in_to_mm(1.55)
    lx_s, od_s = 0.35, 0.08
    L = length * lx_s
    ro, ri = od / 2 * od_s, mandrel / 2 * od_s

    ox, oy = 40, 165
    _view_title(msp, "VIEW 1 — HALF-SECTION", ox, oy + ro + 18, "SCALE 1:4")
    _draw_centerline(msp, ox - 5, ox + L + 5, oy)
    # HNBR cup profile
    msp.add_lwpolyline([
        (ox, oy + ri), (ox + L * 0.82, oy + ri), (ox + L * 0.82, oy + ro * 0.92),
        (ox + L, oy + ro), (ox + L, oy), (ox, oy), (ox, oy + ri),
    ], dxfattribs={"layer": "OUTLINE"})
    _draw_dim_text(msp, f"L {length:.1f}", ox + L / 2 - 8, oy - 10)
    _draw_dim_text(msp, f"OD {od:.1f}", ox + L + 3, oy + ro * 0.5, 2.3)

    # Plan section — petals
    px, py = 40, 55
    _view_title(msp, "VIEW 2 — SECTION A-A (PETALS)", px, py + od / 2 * od_s + 18, "SCALE 1:6")
    pcx, pcy = px + od / 2 * od_s + 5, py + od / 2 * od_s + 5
    msp.add_circle((pcx, pcy), ro, dxfattribs={"layer": "OUTLINE"})
    msp.add_circle((pcx, pcy), ri, dxfattribs={"layer": "HIDDEN"})
    for i in range(16):
        ang = math.radians(i * 22.5)
        r0 = ri + in_to_mm(0.12) * od_s
        r1 = ro * 0.92
        msp.add_line((pcx + r0 * math.cos(ang), pcy + r0 * math.sin(ang)),
                     (pcx + r1 * math.cos(ang), pcy + r1 * math.sin(ang)), dxfattribs={"layer": "OUTLINE"})
    _draw_dim_text(msp, "16 PETALS 0.55 x 1.4 IN", px, py - 6)

    _draw_notes(msp, [
        "PART NO: SHEX-004 (ELASTOMER) + SHEX-005 (PETAL)",
        "QTY: 4 SEAL LANDS PER PLUG",
        "HNBR 90 DURO | PETALS 17-4 PH",
    ], 200, 165)

    path = OUT / "dxf" / "DWG-007_seal_land_module.dxf"
    save_dxf(doc, path)
    return path


def draw_slip_segment() -> Path:
    doc = new_drawing("slip_segment")
    msp = doc.modelspace()
    title_block(doc, "DWG-008", "SLIP SEGMENT")

    od = in_to_mm(8.720)
    mandrel = in_to_mm(1.55)
    height = in_to_mm(4.5)
    contact_r = od / 2
    mandrel_r = mandrel / 2
    span_deg = 45.0  # 8 segments

    ax, ay = 50, 160
    _view_title(msp, "VIEW A — RADIAL (1 OF 8)", ax, ay + contact_r * 0.15 + 20, "SCALE 1:6")
    msp.add_arc((ax, ay), contact_r, 0, span_deg, dxfattribs={"layer": "OUTLINE"})
    msp.add_arc((ax, ay), mandrel_r, 0, span_deg, dxfattribs={"layer": "HIDDEN"})
    # wedge block
    mid_ang = math.radians(span_deg / 2)
    mid_r = (mandrel_r + contact_r) / 2
    wx, wy = ax + mid_r * math.cos(mid_ang), ay + mid_r * math.sin(mid_ang)
    w_len = (contact_r - mandrel_r) * 0.75
    w_wid = math.pi * contact_r * (span_deg / 360) * 0.45
    msp.add_lwpolyline([
        (wx - w_len / 2, wy - w_wid / 2), (wx + w_len / 2, wy - w_wid / 2),
        (wx + w_len / 2, wy + w_wid / 2), (wx - w_len / 2, wy + w_wid / 2),
        (wx - w_len / 2, wy - w_wid / 2),
    ], dxfattribs={"layer": "OUTLINE"})
    _draw_dim_text(msp, f"{span_deg} DEG", ax + 4, ay + 4)

    bx, by = 50, 75
    _view_title(msp, "VIEW B — SIDE (SET)", bx, by + 22, "SCALE 1:4")
    msp.add_lwpolyline([
        (bx, by), (bx + height * 0.25, by), (bx + height * 0.25, by + w_len * 0.25),
        (bx, by + w_len * 0.25), (bx, by),
    ], dxfattribs={"layer": "OUTLINE"})
    _draw_dim_text(msp, f"H {height:.1f}", bx + height * 0.25 + 4, by + 8, 2.3)

    _draw_notes(msp, [
        "PART NO: SHEX-006 / SHEX-007",
        "QTY: 8 UPPER + 8 LOWER",
        "CASE HARDENED TEETH AT OD",
        "SET AGAINST 9-5/8 IN 40# CSG",
    ], 170, 160)

    path = OUT / "dxf" / "DWG-008_slip_segment.dxf"
    save_dxf(doc, path)
    return path


def draw_stage1_stent() -> Path:
    return _draw_stent_sleeve_sheet(
        dwg_no="DWG-009",
        title="STAGE 1 STENT SLEEVE",
        filename="DWG-009_stage1_stent_sleeve.dxf",
        part_no="SHEX-008",
        length_in=4.0,
        od_run_in=1.688,
        od_set_in=3.375,
        id_in=1.45,
        wall_in=0.035,
        cells=12,
        rings=6,
        actuator_note="INTERNAL BLADDER ACTUATOR (STG1)",
    )


def draw_stage2_stent() -> Path:
    return _draw_stent_sleeve_sheet(
        dwg_no="DWG-011",
        title="STAGE 2 MIDDLE STENT SLEEVE",
        filename="DWG-011_stage2_stent_sleeve.dxf",
        part_no="SHEX-009",
        length_in=5.0,
        od_run_in=1.688,
        od_set_in=5.750,
        id_in=3.375,
        wall_in=0.040,
        cells=14,
        rings=4,
        actuator_note="INTERNAL BELLEVILLE WEDGE ACTUATOR (STG2)",
        extra_notes=["EXPANDS AFTER STG1 SET | 5.0 IN MODULE AXIAL"],
    )


def draw_stage3_iris_sleeve() -> Path:
    """Stage 3 fixed support sleeve — iris segments mount on OD."""
    doc = new_drawing("stage3_iris_sleeve")
    msp = doc.modelspace()
    title_block(doc, "DWG-012", "STAGE 3 IRIS SUPPORT SLEEVE")

    length = in_to_mm(7.5)
    od_run = in_to_mm(1.688)
    od_set = in_to_mm(5.750)
    id_in = in_to_mm(3.375)
    wall = in_to_mm(0.050)
    lx_s, od_s = 0.22, 0.10
    L = length * lx_s
    ro = od_set / 2 * od_s
    ri = id_in / 2 * od_s

    ox, oy = 35, 170
    _view_title(msp, "VIEW 1 — HALF-SECTION (SET)", ox, oy + ro + 20, f"SCALE L 1:{1/lx_s:.0f}")
    _draw_centerline(msp, ox - 5, ox + L + 5, oy)
    msp.add_lwpolyline([
        (ox, oy + ri), (ox + L, oy + ri), (ox + L, oy + ro), (ox, oy + ro), (ox, oy + ri),
    ], dxfattribs={"layer": "OUTLINE"})
    # helix guide groove
    for i in range(3):
        gx = ox + L * (0.25 + i * 0.22)
        msp.add_line((gx, oy + ro - wall * od_s * 0.4), (gx + L * 0.06, oy + ro - wall * od_s * 0.8),
                     dxfattribs={"layer": "HIDDEN", "linetype": "DASHED"})
    _draw_dim_text(msp, f"L {length:.1f}", ox + L / 2 - 10, oy - 10)
    _draw_dim_text(msp, f"OD {od_set:.1f}", ox + L + 3, oy + ro * 0.55, 2.3)

    px, py = 35, 70
    _view_title(msp, "VIEW 2 — SECTION A-A (SEGMENT GUIDES)", px, py + ro + 18, "SCALE 1:5")
    pcx, pcy = px + ro + 8, py + ro + 8
    msp.add_circle((pcx, pcy), ro, dxfattribs={"layer": "OUTLINE"})
    msp.add_circle((pcx, pcy), ri, dxfattribs={"layer": "HIDDEN"})
    for i in range(16):
        ang = math.radians(i * 22.5 + 1.5)
        ang2 = math.radians(i * 22.5 + 20.5)
        r0, r1 = ro * 0.96, ro * 1.02
        msp.add_line((pcx + r0 * math.cos(ang), pcy + r0 * math.sin(ang)),
                     (pcx + r1 * math.cos(ang2), pcy + r1 * math.sin(ang2)), dxfattribs={"layer": "OUTLINE"})
    _draw_dim_text(msp, "16 GUIDE SLOTS FOR SHEX-001", px, py - 6)

    tx, ty = 175, 170
    _view_title(msp, "VIEW 3 — RUN-IN / SET TABLE", tx, ty + 5)
    rows = [
        ("RUN-IN OD", f"{od_run:.1f} mm (CRIMPED)"),
        ("SET OD (SUBSTRATE)", f"{od_set:.1f} mm"),
        ("BORE ID", f"{id_in:.1f} mm"),
        ("WALL", f"{wall:.2f} mm"),
        ("IRIS DEPLOYED OD", f"{in_to_mm(8.650):.1f} mm (VIA SEGMENTS)"),
    ]
    for i, (k, v) in enumerate(rows):
        msp.add_text(f"{k}: {v}", dxfattribs={"layer": "TEXT", "height": 2.5}).set_placement((tx, ty - 12 - i * 7))

    _draw_notes(msp, [
        "PART NO: SHEX-010",
        "FIXED SLEEVE — DOES NOT EXPAND WITH IRIS",
        "IRIS SEGMENTS: SEE DWG-001 (16 OFF)",
        "MODULE ASSY: SEE DWG-002",
        "HELIX GUIDE: SHEX-002 (IN718)",
    ], 175, 95)

    path = OUT / "dxf" / "DWG-012_stage3_iris_support_sleeve.dxf"
    save_dxf(doc, path)
    return path


def draw_fishing_neck() -> Path:
    doc = new_drawing("fishing_neck")
    msp = doc.modelspace()
    title_block(doc, "DWG-010", "FISHING NECK / TOP SUB")

    length = in_to_mm(3.0)
    od_top = in_to_mm(1.375)
    od_bot = in_to_mm(1.688)
    lx_s = 0.55

    ox, oy = 50, 130
    _view_title(msp, "VIEW 1 — HALF-SECTION", ox, oy + od_top / 2 * lx_s + 18, "SCALE 1:1")
    L = length * lx_s
    rt, rb = od_top / 2 * lx_s, od_bot / 2 * lx_s
    msp.add_lwpolyline([
        (ox, oy), (ox + L, oy), (ox + L, oy + rb),
        (ox + L * 0.35, oy + rt), (ox, oy + rt * 0.85), (ox, oy),
    ], dxfattribs={"layer": "OUTLINE"})
    # AMMT thread zone
    msp.add_line((ox + L * 0.08, oy + rt * 0.7), (ox + L * 0.3, oy + rt * 0.7),
                 dxfattribs={"layer": "HIDDEN", "linetype": "DASHED"})
    _draw_dim_text(msp, f"L {length:.1f}", ox + L / 2 - 8, oy - 10)
    _draw_dim_text(msp, "1.375 AMMT", ox + 4, oy + rt + 4, 2.3)

    _draw_notes(msp, [
        "PART NO: SHEX-012",
        "MATL: 4140 HT",
        "INTERFACE TO SHEX-ST-54 SETTING TOOL",
    ], 50, 55)

    path = OUT / "dxf" / "DWG-010_fishing_neck.dxf"
    save_dxf(doc, path)
    return path


def write_bom() -> Path:
    rows = [
        ["Item", "Part No", "Description", "Material", "Qty", "Notes"],
        ["1", "SHEX-001", "Iris segment", "17-4 PH H900", "16", "DWG-001, t=0.187"],
        ["2", "SHEX-002", "Helix guide mandrel", "Inconel 718", "1", "Double-start 4in lead"],
        ["3", "SHEX-003", "MTM ring segment", "17-4 PH H900", "12", "DWG-005"],
        ["4", "SHEX-004", "HNBR seal land", "HNBR 90 duro", "4", "DWG-007, 4.5in axial each"],
        ["5", "SHEX-005", "Petal backup", "17-4 PH", "64", "DWG-007, 16 per seal land"],
        ["6", "SHEX-006", "Upper slip segment", "17-4 PH", "8", "DWG-008, 9-5/8 casing"],
        ["7", "SHEX-007", "Lower slip segment", "17-4 PH", "8", "DWG-008, 9-5/8 casing"],
        ["8", "SHEX-008", "Stage 1 stent sleeve", "17-4 PH", "1", "DWG-009, laser cut"],
        ["9", "SHEX-009", "Stage 2 stent sleeve", "17-4 PH", "1", "DWG-011, laser cut"],
        ["10", "SHEX-010", "Stage 3 iris support sleeve", "17-4 PH", "1", "DWG-012"],
        ["11", "SHEX-011", "Inner mandrel", "17-4 PH", "1", "Through bore"],
        ["12", "SHEX-012", "Top sub / fishing neck", "4140", "1", "DWG-010, 1.375 AMMT"],
        ["13", "SHEX-013", "Bottom equalizing sub", "4140", "1", "Ported"],
        ["14", "SHEX-014", "Expansion bladder", "HNBR", "1", "Stage 1"],
        ["15", "SHEX-015", "Belleville stack", "Inconel 718", "1", "Stage 2"],
        ["16", "ST-001", "Setting tool assembly", "4140/17-4", "1", "DWG-004, per run"],
    ]
    path = OUT / "BOM-001.csv"
    with path.open("w", newline="") as f:
        csv.writer(f).writerows(rows)
    return path


def write_drawing_index(files: list[str]) -> None:
    index = OUT / "DRAWING_INDEX.md"
    content = """# Machine Drawing Package - SHEX-BP-UHEX-54

## Drawing list

| DWG NO | File | Description |
|--------|------|-------------|
| DWG-001 | `dxf/DWG-001_iris_segment.dxf` | Stage 3 iris segment (production) |
| DWG-002 | `dxf/DWG-002_iris_module_assy.dxf` | Stage 3 iris module assembly |
| DWG-003 | `dxf/DWG-003_plug_54in_GA.dxf` | Plug 54" general arrangement |
| DWG-004 | `dxf/DWG-004_setting_tool_SHEX-ST-54.dxf` | Setting tool general arrangement |
| DWG-005 | `dxf/DWG-005_mtm_ring_segment.dxf` | MTM ring segment |
| DWG-007 | `dxf/DWG-007_seal_land_module.dxf` | Seal land module (HNBR + petals) |
| DWG-008 | `dxf/DWG-008_slip_segment.dxf` | Slip segment (upper/lower) |
| DWG-009 | `dxf/DWG-009_stage1_stent_sleeve.dxf` | Stage 1 stent sleeve |
| DWG-010 | `dxf/DWG-010_fishing_neck.dxf` | Fishing neck / top sub |
| DWG-011 | `dxf/DWG-011_stage2_stent_sleeve.dxf` | Stage 2 middle stent sleeve |
| DWG-012 | `dxf/DWG-012_stage3_iris_support_sleeve.dxf` | Stage 3 iris support sleeve |
| **DWG-006** | **`dxf/DWG-006_prototype_whole_tool_detailed.dxf`** | **Detailed prototype whole tool (run-in + set + sections)** |
| **PROTOTYPE** | **`PROTOTYPE_DRAWING_SHEET.md`** | **Readable prototype spec with all dimensions** |
| BOM-001 | `BOM-001.csv` | Bill of materials |

## How to open

- **AutoCAD / BricsCAD / DraftSight:** Open `.dxf` files directly
- **Fusion 360:** Upload DXF to sketch plane
- **SolidWorks:** File > Open > DXF/DWG

## Tolerances (unless noted)

| Feature | Tolerance |
|---------|-----------|
| Machined bore | +/- 0.001 in |
| Segment thickness | +/- 0.001 in |
| Root fillet | R0.030 in min |
| Angular (segment pitch) | +/- 0.5 deg |
| Seal land OD | +0.010 / -0.000 in |

## Related FEA package

See `export/ansys/README_ANSYS_IMPORT.md` for STEP solids and mesh import.
"""
    index.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    files = []
    for fn in [draw_iris_segment, draw_iris_module, draw_plug_ga, draw_prototype_detailed, draw_setting_tool_ga, draw_mtm_ring,
               draw_seal_land, draw_slip_segment, draw_stage1_stent, draw_stage2_stent, draw_stage3_iris_sleeve, draw_fishing_neck]:
        p = fn()
        files.append(str(p))
        print(f"  ok {p.name}")

    # Setting tool individual module drawings
    from export.drawings.generate_setting_tool_drawings import main as draw_st_modules
    for p in draw_st_modules():
        files.append(str(p))

    bom = write_bom()
    print(f"  ok {bom.name}")
    write_drawing_index(files)
    (OUT / "manifest.json").write_text(json.dumps({"drawings": files, "bom": str(bom)}, indent=2))
    print(f"\nDone — drawings in {OUT}")


if __name__ == "__main__":
    main()
