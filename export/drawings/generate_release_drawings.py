"""SHEX-BP-UHEX-54 release shop drawings — dimensioned DXF + PDF per part.

One B-size (17 x 11 in) sheet per manufactured part. Geometry is drawn in
inches in modelspace at a per-view scale; dimension `dimlfac` compensates so
dimension text always reads true part inches.

Authority: export/drawings/part_specs/*.md as amended by DCN-1..DCN-6
(see export/release/RELEASE_NOTES.md).

Run:  .venv\\Scripts\\python export/drawings/generate_release_drawings.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import ezdxf
from ezdxf.enums import TextEntityAlignment

ROOT = Path(__file__).resolve().parents[2]
OUT_DXF = ROOT / "export" / "release" / "drawings" / "dxf"
OUT_PDF = ROOT / "export" / "release" / "drawings" / "pdf"

SHEET_W, SHEET_H = 17.0, 11.0
MARGIN = 0.4

GENERAL_TOL = [
    "UNLESS OTHERWISE SPECIFIED:",
    "  DIMENSIONS ARE IN INCHES",
    "  .XX  +/-0.010   .XXX +/-0.005",
    "  ANGLES +/-0.5 DEG",
    "  BREAK SHARP EDGES 0.010 MAX",
]


# ---------------------------------------------------------------------------
# sheet scaffolding
# ---------------------------------------------------------------------------


class Sheet:
    def __init__(self, dwg_no: str, title: str, part_no: str, material: str,
                 qty: str, rev: str = "A") -> None:
        self.doc = ezdxf.new("R2010", setup=True)
        self.doc.header["$INSUNITS"] = 1  # inches
        self.msp = self.doc.modelspace()
        for name, color, lt in (
            ("BORDER", 7, "CONTINUOUS"), ("GEOM", 7, "CONTINUOUS"),
            ("CENTER", 1, "CENTER"), ("HIDDEN", 8, "DASHED"),
            ("DIM", 4, "CONTINUOUS"), ("TEXT", 7, "CONTINUOUS"),
            ("HATCH", 9, "CONTINUOUS"),
        ):
            if name not in self.doc.layers:
                self.doc.layers.add(name, color=color, linetype=lt)
        st = self.doc.dimstyles.get("EZDXF")
        st.dxf.dimtxt = 0.11
        st.dxf.dimasz = 0.10
        st.dxf.dimexo = 0.04
        st.dxf.dimexe = 0.06
        st.dxf.dimdec = 3
        st.dxf.dimgap = 0.03
        self._border(dwg_no, title, part_no, material, qty, rev)

    # -- frame ---------------------------------------------------------------
    def _border(self, dwg_no, title, part_no, material, qty, rev) -> None:
        m = MARGIN
        self.msp.add_lwpolyline(
            [(m, m), (SHEET_W - m, m), (SHEET_W - m, SHEET_H - m), (m, SHEET_H - m), (m, m)],
            dxfattribs={"layer": "BORDER"},
        )
        # title block
        x0, y0 = SHEET_W - m - 5.4, m
        self.msp.add_lwpolyline(
            [(x0, y0), (SHEET_W - m, y0), (SHEET_W - m, y0 + 1.7), (x0, y0 + 1.7), (x0, y0)],
            dxfattribs={"layer": "BORDER"},
        )
        rows = [
            ("SHEX-BP-UHEX-54  HIGH-EXPANSION BRIDGE PLUG", 0.14, 1.48),
            (title, 0.17, 1.18),
            (f"DWG NO: {dwg_no}    REV {rev}", 0.13, 0.92),
            (f"PART NO: {part_no}    QTY/PLUG: {qty}", 0.12, 0.70),
            (f"MATL: {material}", 0.11, 0.50),
            ("UNITS: INCH   PROJECTION: THIRD ANGLE   SIZE B", 0.10, 0.30),
            ("GENERATED FROM cad/release_solids.py PARAMETRIC MODEL", 0.08, 0.12),
        ]
        for text, h, dy in rows:
            self.msp.add_text(
                text, dxfattribs={"layer": "TEXT", "height": h},
            ).set_placement((x0 + 0.1, y0 + dy))
        # general tolerance block (bottom-left)
        ty = m + 0.12
        for line in reversed(GENERAL_TOL):
            self.msp.add_text(line, dxfattribs={"layer": "TEXT", "height": 0.09}).set_placement(
                (m + 0.1, ty)
            )
            ty += 0.16

    def notes(self, lines: list[str], x: float, y: float, h: float = 0.10) -> None:
        self.msp.add_text("NOTES:", dxfattribs={"layer": "TEXT", "height": h * 1.2}).set_placement((x, y))
        yy = y - 0.22
        for i, line in enumerate(lines, 1):
            self.msp.add_text(f"{i}. {line}", dxfattribs={"layer": "TEXT", "height": h}).set_placement((x, yy))
            yy -= 0.18

    def label(self, text: str, x: float, y: float, h: float = 0.12) -> None:
        self.msp.add_text(text, dxfattribs={"layer": "TEXT", "height": h}).set_placement((x, y))

    def label_c(self, text: str, x: float, y: float, h: float = 0.12) -> None:
        self.msp.add_text(text, dxfattribs={"layer": "TEXT", "height": h}).set_placement(
            (x, y), align=TextEntityAlignment.MIDDLE_CENTER
        )

    # -- dimensions ------------------------------------------------------------
    def hdim(self, p1, p2, dist: float, scale: float, text: str | None = None) -> None:
        dim = self.msp.add_linear_dim(
            base=(p1[0], dist), p1=p1, p2=p2, angle=0,
            override={"dimlfac": 1.0 / scale}, dxfattribs={"layer": "DIM"},
            text=text or "<>",
        )
        dim.render()

    def vdim(self, p1, p2, dist: float, scale: float, text: str | None = None) -> None:
        dim = self.msp.add_linear_dim(
            base=(dist, p1[1]), p1=p1, p2=p2, angle=90,
            override={"dimlfac": 1.0 / scale}, dxfattribs={"layer": "DIM"},
            text=text or "<>",
        )
        dim.render()

    def leader(self, text: str, tip, anchor, h: float = 0.10) -> None:
        self.msp.add_lwpolyline([tip, anchor, (anchor[0] + 0.25, anchor[1])],
                                dxfattribs={"layer": "DIM"})
        for i, line in enumerate(text.split("\n")):
            self.msp.add_text(line, dxfattribs={"layer": "TEXT", "height": h}).set_placement(
                (anchor[0] + 0.3, anchor[1] - h / 2 - i * (h + 0.05))
            )

    def save(self, stem: str) -> Path:
        OUT_DXF.mkdir(parents=True, exist_ok=True)
        p = OUT_DXF / f"{stem}.dxf"
        self.doc.saveas(p)
        return p


# ---------------------------------------------------------------------------
# view helpers
# ---------------------------------------------------------------------------


def turned_half_section(sh: Sheet, profile: list[tuple[float, float]], bore: list[tuple[float, float]],
                        x0: float, y0: float, s: float) -> None:
    """Symmetric turned part: outer profile (z, r) mirrored about centreline,
    optional bore profile. Draw at origin (x0, y0=centreline), scale s."""

    def xy(z: float, r: float) -> tuple[float, float]:
        return (x0 + z * s, y0 + r * s)

    for sign in (1, -1):
        pts = [(x0 + z * s, y0 + sign * r * s) for z, r in profile]
        sh.msp.add_lwpolyline(pts, dxfattribs={"layer": "GEOM"})
        if bore:
            ptsb = [(x0 + z * s, y0 + sign * r * s) for z, r in bore]
            sh.msp.add_lwpolyline(ptsb, dxfattribs={"layer": "HIDDEN" if sign > 0 else "GEOM"})
    # end faces
    z_first, r_first = profile[0]
    z_last, r_last = profile[-1]
    rb_first = bore[0][1] if bore else 0.0
    rb_last = bore[-1][1] if bore else 0.0
    for sign in (1, -1):
        sh.msp.add_line(xy(z_first, sign * rb_first), (x0 + z_first * s, y0 + sign * r_first * s),
                        dxfattribs={"layer": "GEOM"})
        sh.msp.add_line(xy(z_last, sign * rb_last), (x0 + z_last * s, y0 + sign * r_last * s),
                        dxfattribs={"layer": "GEOM"})
    # centreline
    sh.msp.add_line((x0 - 0.3, y0), (x0 + z_last * s + 0.3, y0), dxfattribs={"layer": "CENTER"})


def sector_end_view(sh: Sheet, r1: float, r2: float, half_deg: float,
                    cx: float, cy: float, s: float) -> None:
    """End view of an arc-sector profile part, bisector vertical (up)."""
    a0 = math.radians(90 - half_deg)
    a1 = math.radians(90 + half_deg)

    def pt(r: float, a: float) -> tuple[float, float]:
        return (cx + r * s * math.cos(a), cy + r * s * math.sin(a))

    sh.msp.add_arc((cx, cy), r1 * s, 90 - half_deg, 90 + half_deg, dxfattribs={"layer": "GEOM"})
    sh.msp.add_arc((cx, cy), r2 * s, 90 - half_deg, 90 + half_deg, dxfattribs={"layer": "GEOM"})
    sh.msp.add_line(pt(r1, a0), pt(r2, a0), dxfattribs={"layer": "GEOM"})
    sh.msp.add_line(pt(r1, a1), pt(r2, a1), dxfattribs={"layer": "GEOM"})
    # centre mark + bisector centreline
    sh.msp.add_line((cx - 0.15, cy), (cx + 0.15, cy), dxfattribs={"layer": "CENTER"})
    sh.msp.add_line((cx, cy - 0.15), (cx, cy + r2 * s + 0.3), dxfattribs={"layer": "CENTER"})


def rect_view(sh: Sheet, w: float, h: float, x0: float, y0: float, s: float) -> None:
    sh.msp.add_lwpolyline(
        [(x0, y0), (x0 + w * s, y0), (x0 + w * s, y0 + h * s), (x0, y0 + h * s), (x0, y0)],
        dxfattribs={"layer": "GEOM"},
    )


# ---------------------------------------------------------------------------
# part sheets
# ---------------------------------------------------------------------------


def dwg_001_iris_segment() -> Path:
    sh = Sheet("DWG-001-SHP", "STAGE 3 IRIS SEGMENT", "SHEX-001",
               "17-4 PH H900 (H1150M)", "16")
    s = 1.2
    cx, cy = 4.6, 2.4
    sector_end_view(sh, 2.955, 4.318, 11.25, cx, cy, s)
    sh.label("VIEW A — RADIAL PROFILE (DEPLOYED GEOMETRY)  SCALE 1.2:1", 1.2, 8.6)
    sh.leader("R1 2.955 +/-.005", (cx, cy + 2.955 * s), (cx + 1.4, cy + 2.0))
    sh.leader("R2 4.318 +/-.005", (cx, cy + 4.318 * s), (cx + 1.8, cy + 5.9))
    sh.label_c("22.5 DEG +/-0.5 SPAN", cx, cy + 4.318 * s + 0.45, 0.12)
    sh.label_c("RADIAL WIDTH 1.363 REF", cx, cy + (2.955 + 0.68) * s, 0.10)

    # side view (axial section): L 2.750 x t 0.187 with follower tab
    x0, y0 = 10.6, 4.4
    s2 = 1.6
    rect_view(sh, 2.750, 0.187, x0, y0, s2)
    # tab below mid-length
    tx = x0 + (2.750 / 2 - 0.625 / 2) * s2
    sh.msp.add_lwpolyline(
        [(tx, y0), (tx, y0 - 0.080 * s2), (tx + 0.625 * s2, y0 - 0.080 * s2), (tx + 0.625 * s2, y0)],
        dxfattribs={"layer": "GEOM"},
    )
    sh.label("VIEW B — AXIAL SECTION  SCALE 1.6:1", 10.2, 6.2)
    sh.hdim((x0, y0 + 0.187 * s2), (x0 + 2.750 * s2, y0 + 0.187 * s2), y0 + 1.0, s2)
    sh.vdim((x0 + 2.750 * s2, y0), (x0 + 2.750 * s2, y0 + 0.187 * s2), x0 + 2.750 * s2 + 0.7, s2,
            text="0.187 +/-.005")
    sh.hdim((tx, y0 - 0.080 * s2), (tx + 0.625 * s2, y0 - 0.080 * s2), y0 - 0.8, s2)
    sh.leader("FOLLOWER TAB 0.625 x 0.125 x 0.080 HIGH\nAT MID-LENGTH, ON BISECTOR (INNER FACE)",
              (tx + 0.3 * s2, y0 - 0.080 * s2), (x0 + 0.4, y0 - 1.5))

    sh.notes([
        "WIRE EDM OR CNC PROFILE FROM PLATE — NOT A TURNED OD.",
        "DEPLOYED ARC RADII SHOWN; MODULE NESTED + CRIMPED TO 1.688 OD AT ASSY.",
        "ROOT FILLET R0.030 MIN (INNER CORNERS); OUTER TOE CHAMFER 0.025 x 45 BOTH FACES.",
        "TAB WIDTH 0.125 +/-.003 MATCHES SHEX-002 HELIX GROOVE (DCN-1).",
        "FINISH: ELECTROPOLISH ALL EXPOSED FACES.",
        "VERIFY RADIAL TRAVEL 1.363 IN SET ASSY (DWG-002-SET).",
    ], 1.0, 4.2)
    return sh.save("DWG-001-SHP_SHEX-001_iris_segment")


def dwg_002a_helix_guide() -> Path:
    sh = Sheet("DWG-002A-SHP", "IRIS HELIX GUIDE INSERT", "SHEX-002",
               "INCONEL 718 (AMS 5662)", "1")
    s = 2.2
    # half section: ring OD 1.555 / ID 1.282 x L 4.0 with 2 internal grooves
    x0, y0 = 3.0, 5.6
    prof = [(0, 1.555 / 2), (4.0, 1.555 / 2)]
    bore = [(0, 1.282 / 2), (4.0, 1.282 / 2)]
    turned_half_section(sh, prof, bore, x0, y0, s)
    # groove cuts (schematic on section: show 4 crossings per side)
    for z in (0.5, 1.5, 2.5, 3.5):
        for sign in (1, -1):
            gy = y0 + sign * (1.282 / 2) * s
            sh.msp.add_lwpolyline(
                [(x0 + (z - 0.0625) * s, gy), (x0 + (z - 0.0625) * s, gy + sign * 0.080 * s),
                 (x0 + (z + 0.0625) * s, gy + sign * 0.080 * s), (x0 + (z + 0.0625) * s, gy)],
                dxfattribs={"layer": "GEOM"},
            )
    sh.label("VIEW A — HALF SECTION  SCALE 2.2:1", 2.6, 8.2)
    sh.hdim((x0, y0 + (1.555 / 2) * s), (x0 + 4.0 * s, y0 + (1.555 / 2) * s), y0 + 2.6, s,
            text="4.000 +/-.005")
    sh.vdim((x0, y0 - (1.555 / 2) * s), (x0, y0 + (1.555 / 2) * s), x0 - 0.8, s,
            text="OD 1.555 +.000/-.002")
    sh.vdim((x0 + 4.0 * s, y0 - (1.282 / 2) * s), (x0 + 4.0 * s, y0 + (1.282 / 2) * s),
            x0 + 4.0 * s + 0.8, s, text="ID 1.282 +.003/-.000 (DCN-1)")
    sh.leader("2-START HELIX GROOVE 0.125 +/-.005 W x 0.080 +/-.003 DP\nLEAD 4.000 +/-.010, STARTS 180 DEG APART, ROOT R0.015 MIN",
              (x0 + 1.5 * s, y0 + (1.282 / 2 + 0.08) * s), (x0 + 2.2 * s, y0 + 2.0))

    # developed view (one start unwrap)
    x1, y1 = 11.4, 2.0
    sw, shh = 4.0, 2.6
    sh.msp.add_lwpolyline([(x1, y1), (x1 + sw, y1), (x1 + sw, y1 + shh), (x1, y1 + shh), (x1, y1)],
                          dxfattribs={"layer": "GEOM"})
    sh.msp.add_line((x1, y1), (x1 + sw, y1 + shh), dxfattribs={"layer": "CENTER"})
    sh.label("VIEW B — DEVELOPED HELIX (ONE START)", x1 - 0.2, y1 + shh + 0.5)
    sh.label("CIRCUMFERENCE (PI x 1.282) -> LEAD 4.000/REV", x1 - 0.2, y1 + shh + 0.25, 0.09)

    sh.notes([
        "DCN-1: ID CHANGED 1.552 -> 1.282 SO 0.080 GROOVES HAVE WALL (WAS 0.0015 WALL).",
        "MATES: SHEX-010 POCKET DIA 1.558 (PRESS/SLIP); SHEX-011 NECKED DRIVE ZONE.",
        "MANUFACTURE: EDM OR 5-AXIS FOR HELIX GROOVES.",
        "ANTI-ROTATION PIN DIA 0.062 THROUGH SLEEVE + INSERT, 1 PLACE, AT ASSY.",
        "FUNCTIONAL TEST IN SHEX-010 POCKET WITH MANDREL + 1 SEGMENT.",
        "RUN-IN MODULE PART — NOT FOR SET OD 5.750/8.650.",
    ], 1.0, 3.6)
    return sh.save("DWG-002A-SHP_SHEX-002_helix_guide")


def dwg_005_mtm_segment() -> Path:
    sh = Sheet("DWG-005-SHP", "UPPER MTM RING SEGMENT", "SHEX-003",
               "17-4 PH H900", "12 (3 RINGS x 4)")
    s = 0.85
    cx, cy = 4.8, 2.2
    sector_end_view(sh, 4.200, 4.400, 44.0, cx, cy, s)
    sh.label("VIEW A — RADIAL PROFILE (DEPLOYED)  SCALE 0.85:1", 1.2, 8.4)
    sh.leader("R1 4.200 +/-.005", (cx, cy + 4.200 * s), (cx + 1.2, cy + 2.6))
    sh.leader("R2 4.400 +/-.005 (OD 8.800 SET)", (cx, cy + 4.400 * s), (cx + 1.8, cy + 4.6))
    sh.label_c("88 DEG SEGMENT (90 DEG PITCH, 2 DEG GAP)", cx, cy + 4.400 * s + 0.45, 0.11)

    x0, y0 = 11.6, 4.6
    s2 = 2.0
    rect_view(sh, 0.750, 0.200, x0, y0, s2)
    sh.label("VIEW B — AXIAL SECTION  SCALE 2:1", 11.2, 6.0)
    sh.hdim((x0, y0 + 0.2 * s2), (x0 + 0.75 * s2, y0 + 0.2 * s2), y0 + 1.0, s2, text="0.750 +/-.005")
    sh.vdim((x0 + 0.75 * s2, y0), (x0 + 0.75 * s2, y0 + 0.2 * s2), x0 + 0.75 * s2 + 0.7, s2,
            text="0.200 +/-.005")

    sh.notes([
        "WIRE EDM FROM PLATE; DEPLOYED RADII SHOWN — NESTED AT 1.688 OD AT RUN-IN.",
        "3 RINGS x 4 SEGMENTS, RING JOINTS STAGGERED 30 DEG AT ASSEMBLY.",
        "METAL-TO-METAL BACKUP — PRELOADED BY SHEX-011 LOAD LAND DIA 1.558 (SPEC 12.7).",
        "SET OD 8.800 AGAINST 9-5/8 40# CASING ID 8.835.",
        "PASSIVATE PER AMS 2700 AFTER EDM.",
    ], 1.0, 3.6)
    return sh.save("DWG-005-SHP_SHEX-003_mtm_ring_segment")


def dwg_007b_hnbr_preform() -> Path:
    sh = Sheet("DWG-007B-SHP", "HNBR SEAL LAND LINER PREFORM", "SHEX-004",
               "HNBR 90 SHORE A", "4")
    s = 5.0
    x0, y0 = 4.0, 5.2
    prof = [(0, 0.831), (0.550, 0.831)]
    bore = [(0, 0.781), (0.550, 0.781)]
    turned_half_section(sh, prof, bore, x0, y0, s)
    sh.label("VIEW A — SECTION (MOLDED RING)  SCALE 5:1", 2.6, 8.6)
    sh.hdim((x0, y0 + 0.831 * s), (x0 + 0.550 * s, y0 + 0.831 * s), y0 + 0.831 * s + 0.7, s,
            text="0.550 +/-.010")
    sh.vdim((x0, y0 - 0.831 * s), (x0, y0 + 0.831 * s), x0 - 0.9, s, text="RO 0.831 +/-.005")
    sh.vdim((x0 + 0.55 * s, y0 - 0.781 * s), (x0 + 0.55 * s, y0 + 0.781 * s), x0 + 0.55 * s + 0.9, s,
            text="RI 0.781 +.005/-.000")
    sh.leader("WALL 0.050 +/-.005", (x0 + 0.275 * s, y0 + 0.806 * s), (x0 + 2.2, y0 + 2.2))

    sh.notes([
        "MOLD THE RUN-IN PREFORM ONLY — NOT THE SET OD 8.720 CUP (IN-WELL ENVELOPE).",
        "CONTINUOUS 360 DEG RING; 4 PER PLUG (SEAL LANDS, ITEMS 7-10).",
        "PARTING LINE MID-THICKNESS TYP; DRAFT 1 DEG MIN; FLASH 0.010 MAX.",
        "MECHANICAL GRIP IN CARRIER — NO BOND TO PETAL FACES.",
        "POST-MOLD TRIM FLASH; NO MOLD RELEASE IN SEAL ZONE.",
        "SET CONTACT OD 8.720 AFTER PETAL DEPLOYMENT + MANDREL RAMP COMPRESSION.",
    ], 9.6, 7.6)
    return sh.save("DWG-007B-SHP_SHEX-004_hnbr_preform")


def dwg_007a_petal() -> Path:
    sh = Sheet("DWG-007A-SHP", "SEAL LAND PETAL BACKUP", "SHEX-005",
               "17-4 PH H900 (H1150M)", "64 (16 x 4 LANDS)")
    s = 1.05
    cx, cy = 4.8, 2.6
    sector_end_view(sh, 0.895, 4.011, 11.25, cx, cy, s)
    sh.label("VIEW A — RADIAL PROFILE (DEPLOYED)  SCALE 1.05:1", 1.2, 8.6)
    sh.leader("R1 0.895 +/-.005", (cx, cy + 0.895 * s), (cx + 1.5, cy + 0.4))
    sh.leader("R2 4.011 +/-.005", (cx, cy + 4.011 * s), (cx + 1.8, cy + 5.2))
    sh.label_c("22.5 DEG +/-0.5 SPAN", cx, cy + 4.011 * s + 0.45, 0.12)

    x0, y0 = 11.6, 4.6
    s2 = 2.4
    rect_view(sh, 0.550, 0.110, x0, y0, s2)
    sh.label("VIEW B — AXIAL SECTION  SCALE 2.4:1", 11.2, 5.8)
    sh.hdim((x0, y0 + 0.110 * s2), (x0 + 0.550 * s2, y0 + 0.110 * s2), y0 + 0.9, s2,
            text="0.550 +/-.010")
    sh.vdim((x0 + 0.55 * s2, y0), (x0 + 0.55 * s2, y0 + 0.110 * s2), x0 + 0.55 * s2 + 0.7, s2,
            text="0.110 REF")

    sh.notes([
        "WIRE EDM OR CNC FROM PLATE — NOT A TURNED OD.",
        "DEPLOYED BACKUP RADII SHOWN — SEAL PACK NESTED AT 1.688 OD AT RUN-IN.",
        "ROOT FILLET R0.015 MIN; OUTER TOE CHAMFER 0.015 x 45 BOTH FACES.",
        "ANTI-EXTRUSION RIB BEHIND SHEX-004 HNBR LINER; REACTS ON SHEX-011 RAMPS (12.6).",
        "PASSIVATE PER SPEC; BREAK SHARP EDGES 0.010 MAX.",
    ], 1.0, 4.0)
    return sh.save("DWG-007A-SHP_SHEX-005_petal_backup")


def dwg_008_slip(upper: bool) -> Path:
    pn = "SHEX-006" if upper else "SHEX-007"
    nm = "UPPER SLIP SEGMENT" if upper else "LOWER SLIP SEGMENT"
    dn = "DWG-008A-SHP" if upper else "DWG-008B-SHP"
    sh = Sheet(dn, nm, pn, "17-4 PH H900, TEETH CASE HARDENED 55 HRC MIN", "8")
    s = 0.95
    cx, cy = 4.8, 2.4
    sector_end_view(sh, 3.560, 4.360, 20.5, cx, cy, s)
    sh.label("VIEW A — RADIAL PROFILE (DEPLOYED)  SCALE 0.95:1", 1.2, 8.4)
    sh.leader("R1 3.560 +/-.005", (cx, cy + 3.560 * s), (cx + 1.4, cy + 2.4))
    sh.leader("R2 4.360 +/-.005 (SET OD 8.720)", (cx, cy + 4.360 * s), (cx + 1.8, cy + 4.9))
    sh.label_c("41 DEG SEGMENT (45 DEG PITCH, 4 DEG GAP)", cx, cy + 4.360 * s + 0.45, 0.11)

    # side: L 2.000 with 3 tooth grooves on OD
    x0, y0 = 11.2, 4.2
    s2 = 1.5
    rect_view(sh, 2.000, 0.800, x0, y0, s2)
    for i in range(3):
        zg = 0.35 + i * 0.55
        gx = x0 + zg * s2
        sh.msp.add_lwpolyline(
            [(gx, y0 + 0.8 * s2), (gx, y0 + (0.8 - 0.060) * s2),
             (gx + 0.120 * s2, y0 + (0.8 - 0.060) * s2), (gx + 0.120 * s2, y0 + 0.8 * s2)],
            dxfattribs={"layer": "GEOM"},
        )
    sh.label("VIEW B — AXIAL SECTION  SCALE 1.5:1", 10.8, 6.0)
    sh.hdim((x0, y0 + 0.8 * s2), (x0 + 2.0 * s2, y0 + 0.8 * s2), y0 + 0.8 * s2 + 0.8, s2,
            text="2.000 +/-.010")
    sh.leader("3x TOOTH GROOVE 0.120 W x 0.060 DP\nPITCH 0.550, FIRST AT 0.350 FROM BTM",
              (x0 + 0.41 * s2, y0 + 0.74 * s2), (x0 + 0.6, y0 - 0.8))

    sh.notes([
        "WIRE EDM PROFILE FROM PLATE; TEETH CUT BEFORE CASE HARDEN.",
        "DEPLOYED RADII SHOWN — NESTED AT 1.688 OD AT RUN-IN (CASCADE).",
        "BORE FACE RIDES SHEX-011 EXPANDER CONE (12 DEG INCL) — SPEC 12.3 / 12.8.",
        "TEETH: CASE HARDEN 55 HRC MIN, 0.020-0.030 CASE DEPTH; CORE 28-32 HRC.",
        "SET AGAINST 9-5/8 40# CASING (ID 8.835 / DRIFT 8.679).",
        "UPPER AND LOWER SEGMENTS IDENTICAL PROFILE; TOOTH RAKE OPPOSES LOAD DIRECTION." if upper
        else "LOWER SEGMENT — TOOTH RAKE MIRRORED VS SHEX-006 (HOLDS FROM BELOW).",
    ], 1.0, 4.0)
    return sh.save(f"{dn}_{pn}_slip_segment")


def _stent_sheet(pn: str, dn: str, name: str, length: float, cells: int, rings: int,
                 set_od: float, wall: float) -> Path:
    sh = Sheet(dn, name, pn, "17-4 PH H900 TUBE, LASER CUT + ELECTROPOLISH", "1")
    s = 1.5
    x0, y0 = 2.6, 5.4
    prof = [(0, 1.688 / 2), (length, 1.688 / 2)]
    bore = [(0, 1.562 / 2), (length, 1.562 / 2)]
    turned_half_section(sh, prof, bore, x0, y0, s)
    # kerf slot ticks on the elevation
    margin = 0.06 * length
    band = (length - 2 * margin) / rings
    for ring_i in range(rings):
        zc = margin + (ring_i + 0.5) * band
        for sign in (1, -1):
            yv = y0 + sign * (1.688 / 2) * s
            sh.msp.add_line((x0 + (zc - 0.05) * s, yv), (x0 + (zc + 0.05) * s, yv),
                            dxfattribs={"layer": "HIDDEN"})
    sh.label(f"VIEW A — TUBE BLANK + KERF RING PLANES  SCALE 1.5:1", 2.2, 8.3)
    sh.hdim((x0, y0 + (1.688 / 2) * s), (x0 + length * s, y0 + (1.688 / 2) * s), y0 + 2.0, s,
            text=f"{length:.3f} +/-.010")
    sh.vdim((x0, y0 - (1.688 / 2) * s), (x0, y0 + (1.688 / 2) * s), x0 - 0.8, s,
            text="OD 1.688 +.000/-.005")
    sh.vdim((x0 + length * s, y0 - (1.562 / 2) * s), (x0 + length * s, y0 + (1.562 / 2) * s),
            x0 + length * s + 0.8, s, text="ID 1.562 +.003/-.000")

    # developed pattern panel
    x1, y1 = 9.8, 2.9
    circ = math.pi * 1.688
    sd = 0.85
    sh.msp.add_lwpolyline(
        [(x1, y1), (x1 + length * sd * 1.6, y1), (x1 + length * sd * 1.6, y1 + circ * sd),
         (x1, y1 + circ * sd), (x1, y1)], dxfattribs={"layer": "GEOM"})
    pitch_c = circ / cells
    for ring_i in range(rings):
        zc = (margin + (ring_i + 0.5) * band) * 1.6
        stagger = 0.5 if ring_i % 2 else 0.0
        slot_l = pitch_c * 0.70
        for c in range(cells):
            yc = ((c + stagger) % cells) * pitch_c + pitch_c / 2
            sh.msp.add_lwpolyline(
                [(x1 + (zc - 0.01) * sd * 1.0, y1 + (yc - slot_l / 2) * sd),
                 (x1 + (zc + 0.01) * sd * 1.0, y1 + (yc - slot_l / 2) * sd),
                 (x1 + (zc + 0.01) * sd * 1.0, y1 + (yc + slot_l / 2) * sd),
                 (x1 + (zc - 0.01) * sd * 1.0, y1 + (yc + slot_l / 2) * sd),
                 (x1 + (zc - 0.01) * sd * 1.0, y1 + (yc - slot_l / 2) * sd)],
                dxfattribs={"layer": "GEOM"})
    sh.label("VIEW B — DEVELOPED LASER PATTERN (FLAT)", x1, y1 + circ * sd + 0.35)
    sh.label(f"{cells} SLOTS/RING x {rings} RINGS, STAGGERED 1/2 PITCH; KERF 0.008", x1,
             y1 + circ * sd + 0.15, 0.09)

    sh.notes([
        f"LASER CUT ON TUBE OD 1.688 x WALL 0.063; SLOT LENGTH 0.70 x CIRC PITCH.",
        f"DEPLOYS TO OD {set_od:.3f} (SET); RUN-IN PATTERN IS CLOSED-CELL.",
        "DXF FLAT PATTERN AUTHORITY: export/stent/developed_dxf/ (KERF-COMPENSATED).",
        "HEAT TREAT H900 AFTER CUTTING; ELECTROPOLISH; NO BURRS, NO SLAG.",
        "ACTUATOR: " + ("INTERNAL BLADDER (SHEX-014)." if pn == "SHEX-008"
                        else "INTERNAL BELLEVILLE WEDGE (SHEX-015)."),
        "FORESHORTENING AT DEPLOY ~22 PERCENT — VERIFY ON FIRST ARTICLE.",
    ], 1.0, 3.4)
    return sh.save(f"{dn}_{pn}_stent_sleeve")


def dwg_012_support_sleeve() -> Path:
    sh = Sheet("DWG-012-SHP", "STAGE 3 IRIS SUPPORT SLEEVE", "SHEX-010",
               "17-4 PH H900 (H1150M)", "1")
    s = 1.05
    x0, y0 = 2.2, 5.6
    prof = [(0, 1.688 / 2), (7.5, 1.688 / 2)]
    bore = [(0, 1.562 / 2), (3.25, 1.562 / 2), (3.25, 1.558 / 2), (7.25, 1.558 / 2),
            (7.25, 1.562 / 2), (7.5, 1.562 / 2)]
    turned_half_section(sh, prof, bore, x0, y0, s)
    # guide slot zone (hidden) Z' 1.0-3.75
    for sign in (1, -1):
        yv = y0 + sign * (1.562 / 2 + 0.055) * s
        sh.msp.add_line((x0 + 1.0 * s, yv), (x0 + 3.75 * s, yv), dxfattribs={"layer": "HIDDEN"})
    sh.label("VIEW A — HALF SECTION  SCALE 1.05:1", 1.8, 8.4)
    sh.hdim((x0, y0 + (1.688 / 2) * s), (x0 + 7.5 * s, y0 + (1.688 / 2) * s), y0 + 1.7, s,
            text="7.500 +/-.010")
    sh.hdim((x0 + 3.25 * s, y0 - (1.558 / 2) * s), (x0 + 7.25 * s, y0 - (1.558 / 2) * s),
            y0 - 1.9, s, text="HELIX POCKET 4.000 (Z' 3.250-7.250)")
    sh.vdim((x0, y0 - (1.688 / 2) * s), (x0, y0 + (1.688 / 2) * s), x0 - 0.8, s,
            text="OD 1.688 +.000/-.005")
    sh.vdim((x0 + 7.5 * s, y0 - (1.562 / 2) * s), (x0 + 7.5 * s, y0 + (1.562 / 2) * s),
            x0 + 7.5 * s + 0.8, s, text="ID 1.562 +.003/-.000")
    sh.leader("POCKET ID 1.558 +.003/-.000", (x0 + 5.2 * s, y0 + (1.558 / 2) * s),
              (x0 + 5.6 * s, y0 + 1.3))
    sh.leader("RETAINING RING GROOVE 0.030 x 0.040 AT Z' 7.200",
              (x0 + 7.2 * s, y0 - (1.558 / 2) * s), (x0 + 4.6 * s, y0 - 1.4))

    # end view with 16 slots
    cx, cy = 13.6, 6.4
    s2 = 1.6
    sh.msp.add_circle((cx, cy), 1.688 / 2 * s2, dxfattribs={"layer": "GEOM"})
    sh.msp.add_circle((cx, cy), 1.562 / 2 * s2, dxfattribs={"layer": "GEOM"})
    for i in range(16):
        a = math.radians(i * 22.5)
        r1, r2 = 1.562 / 2 * s2, (1.562 / 2 + 0.055) * s2
        w = 0.060 * s2
        ca, sa = math.cos(a), math.sin(a)
        px, py = -sa, ca
        pts = [
            (cx + r1 * ca - w * px, cy + r1 * sa - w * py),
            (cx + r2 * ca - w * px, cy + r2 * sa - w * py),
            (cx + r2 * ca + w * px, cy + r2 * sa + w * py),
            (cx + r1 * ca + w * px, cy + r1 * sa + w * py),
        ]
        sh.msp.add_lwpolyline(pts + [pts[0]], dxfattribs={"layer": "GEOM"})
    sh.label("VIEW B — SECTION AT Z' 2.375", 12.5, 8.5)
    sh.label("16x GUIDE SLOT 0.120 +/-.005 W x 0.055 +.005/-.000 DP x 2.750 LG", 11.0, 8.3, 0.10)
    sh.label("EQ SPACED 22.5 DEG, SLOT #1 AT 0 DEG DATUM", 11.0, 8.12, 0.10)

    sh.notes([
        "MANUFACTURING PART — RUN-IN OD 1.688 MAX (NOT THE 5.750 SET ENVELOPE).",
        "FIXED SLEEVE — DOES NOT EXPAND WITH IRIS.",
        "BOTTOM/TOP FACES FLAT, RA 32; PILOT Z' 0-0.750 MATES STAGE 2 STENT TOP.",
        "SLOT CENTRES AT Z' 2.375 (PLUG Z 20.875); DEBURR — NO BURRS IN HELIX POCKET.",
        "TOP LOCK LAND Z' 7.250-7.500; OPTIONAL ID STEP 1.540 FOR RETAINER.",
        "MATES: SHEX-002 INSERT IN POCKET; 16x SHEX-001 IN SLOTS; SHEX-011 BORE.",
    ], 1.0, 3.6)
    return sh.save("DWG-012-SHP_SHEX-010_support_sleeve")


def dwg_011b_mandrel() -> Path:
    sh = Sheet("DWG-011B-SHP", "INNER MANDREL", "SHEX-011",
               "17-4 PH H900 (H1150M)", "1", rev="E.1")
    # full elevation at small scale
    s = 0.28
    x0, y0 = 1.0, 7.6
    prof = [
        (0, 0.675), (5.0, 0.675), (5.0, 0.775), (6.25, 0.775), (7.75, 0.810),
        (9.375, 0.810), (9.5, 0.775), (10.3, 0.775), (10.4, 0.635), (25.9, 0.635),
        (26.0, 0.775), (27.125, 0.775), (28.5, 0.791), (28.56, 0.775),
        (31.625, 0.775), (33.0, 0.791), (33.06, 0.775),
        (34.75, 0.775), (34.75, 0.779), (35.25, 0.779), (35.25, 0.775),
        (36.125, 0.775), (37.5, 0.791), (37.56, 0.775),
        (40.625, 0.775), (42.0, 0.791), (42.06, 0.775),
        (48.25, 0.775), (49.75, 0.810), (50.0, 0.775), (50.5, 0.775),
        (50.5, 0.6875), (51.5, 0.6875), (51.5, 0.650), (52.0, 0.650),
    ]
    turned_half_section(sh, prof, [], x0, y0, s)
    # helix rib zone hatch marks (DCN-9: Z 18.15-21.75)
    for z in (18.4, 19.4, 20.4, 21.3):
        sh.msp.add_line((x0 + z * s, y0 + 0.635 * s), (x0 + (z + 0.4) * s, y0 + 0.715 * s),
                        dxfattribs={"layer": "HIDDEN"})
    sh.label("VIEW A — ELEVATION  SCALE 0.28:1 (FINISHED LENGTH 52.000 — DCN-3/7)", 1.0, 9.6)
    sh.hdim((x0, y0 + 0.9), (x0 + 52.0 * s, y0 + 0.9), y0 + 1.5, s, text="52.000 +/-.010")
    sh.hdim((x0, y0 - 0.675 * s), (x0 + 5.0 * s, y0 - 0.675 * s), y0 - 1.2, s,
            text="TAIL 5.000 (DCN-5)")
    sh.hdim((x0 + 10.4 * s, y0 - 0.635 * s), (x0 + 25.9 * s, y0 - 0.635 * s), y0 - 1.6, s,
            text="NECK 15.500 (DCN-1/9)")
    sh.leader("TAIL DIA 1.350 +.000/-.002", (x0 + 1.5 * s, y0 + 0.675 * s), (x0 + 0.4, y0 + 2.6))
    sh.leader("BODY DIA 1.550 +.000/-.002", (x0 + 5.0 * s, y0 + 0.775 * s), (x0 + 2.6, y0 + 3.0))
    sh.leader("LOWER SLIP TAPER DIA 1.550->1.620 x 1.500 (12 DEG INCL)",
              (x0 + 7.0 * s, y0 + 0.793 * s), (x0 + 4.8, y0 + 3.4))
    sh.leader("HELIX NECK DIA 1.270; 2-START DRIVE RIBS Z 18.15-21.75,\nLEAD 4.000, PEAK DIA 1.429, PHASE 324 DEG (DCN-1/9)",
              (x0 + 20.0 * s, y0 + 0.635 * s), (x0 + 5.4, y0 - 2.6))
    sh.leader("4x SEAL RAMP DIA 1.550->1.582 x 1.375 (3 DEG INCL)\nAT Z 27.125 / 31.625 / 36.125 / 40.625",
              (x0 + 28.0 * s, y0 + 0.791 * s), (x0 + 8.4, y0 + 3.0))
    sh.leader("MTM LAND DIA 1.558 x 0.500 AT Z 34.75 (DCN-9)", (x0 + 35.0 * s, y0 + 0.779 * s),
              (x0 + 10.6, y0 + 2.5))
    sh.leader("UPPER SLIP TAPER 1.550->1.620 AT Z 48.25", (x0 + 49.0 * s, y0 + 0.80 * s),
              (x0 + 12.0, y0 + 3.2))

    # detail: top joint (DCN-6/7)
    xd, yd = 10.8, 4.9
    sd = 1.7
    prof_d = [(49.9, 0.775), (50.5, 0.775), (50.5, 0.6875), (51.5, 0.6875),
              (51.5, 0.650), (52.0, 0.650)]
    turned_half_section(sh, prof_d := [(z - 49.9, r) for z, r in prof_d], [], xd, yd, sd)
    # face groove at end (Parker 2-211: OD 1.085 / ID 0.800 x 0.103 DP)
    for sign in (1, -1):
        sh.msp.add_lwpolyline(
            [(xd + 2.1 * sd, yd + sign * (1.085 / 2) * sd), (xd + (2.1 - 0.103) * sd, yd + sign * (1.085 / 2) * sd),
             (xd + (2.1 - 0.103) * sd, yd + sign * (0.800 / 2) * sd), (xd + 2.1 * sd, yd + sign * (0.800 / 2) * sd)],
            dxfattribs={"layer": "GEOM"})
    sh.label("DETAIL B — TOP JOINT (DCN-6/7)  SCALE 1.7:1", 10.6, 7.0)
    sh.leader("1-3/8-12 UNF-2A x 1.000 (Z 50.5-51.5)", (xd + 1.0 * sd, yd + 0.69 * sd),
              (xd + 0.0, yd + 1.7))
    sh.leader("PLAIN SEAL NOSE DIA 1.300 x 0.500", (xd + 1.75 * sd, yd + 0.65 * sd),
              (xd + 2.6, yd + 1.3))
    sh.leader("FACE GROOVE: OD 1.085 / ID 0.800 x 0.103 DP\nPARKER 2-211 VITON 90 (FACE SEAL)",
              (xd + 2.05 * sd, yd + 0.47 * sd), (xd + 2.9, yd + 0.4))
    sh.leader("SHOULDER FACE Z 50.5, FLAT 0.001 FIM, RA 32",
              (xd + 0.6 * sd, yd - 0.775 * sd), (xd - 0.2, yd - 1.7))

    sh.notes([
        "FINISHED LENGTH 52.000: BODY TO SHOULDER Z=50.5 + PIN 1.500 (DCN-3/6/7).",
        "OD STEP LEDGER PER SPEC SHEX-011 SECT 12.10, AMENDED BY DCN-1/9 NECK 10.4-25.9.",
        "STRAIGHTNESS 0.005 PER 12 IN; RA 32 ON ALL MODULE TRAVEL ZONES Z 3-50.5.",
        "THREAD 1-3/8-12 UNF-2A x 1.000; RELIEF 0.030 x 45 AT Z 50.5 (DCN-7).",
        "DRILL DIA 0.125 CROSS PIN AT Z 51.0 AFTER NECK MAKEUP, TORQUE 250 FT-LB MIN.",
        "DRIVE RIBS: ROUND FORM 0.115 W x 0.080 H, 2-START, LEAD 4.000 — MATE SHEX-002.",
        "RIB PHASE REFERENCE FLAT AT Z 18.15 START, PHASE 324 DEG TO INSERT (DCN-9).",
        "NO THROUGH BORE — SOLID BAR.",
    ], 1.0, 3.2)
    return sh.save("DWG-011B-SHP_SHEX-011_inner_mandrel")


def dwg_011a_tail_sleeve() -> Path:
    sh = Sheet("DWG-011A-SHP", "MANDREL TAIL SLEEVE", "SHEX-011A",
               "4140 HT (AMS 6415) 28-32 HRC", "1", rev="B")
    s = 2.2
    x0, y0 = 4.4, 5.4
    prof = [(0, 0.775), (3.0, 0.775)]
    bore = [(0, 0.676), (3.0, 0.676)]
    turned_half_section(sh, prof, bore, x0, y0, s)
    sh.label("VIEW A — SECTION  SCALE 2.2:1", 4.0, 8.0)
    sh.hdim((x0, y0 + 0.775 * s), (x0 + 3.0 * s, y0 + 0.775 * s), y0 + 2.4, s, text="3.000 +/-.010")
    sh.vdim((x0, y0 - 0.775 * s), (x0, y0 + 0.775 * s), x0 - 0.8, s, text="OD 1.550 +/-.005 (DCN-2)")
    sh.vdim((x0 + 3.0 * s, y0 - 0.676 * s), (x0 + 3.0 * s, y0 + 0.676 * s), x0 + 3.0 * s + 0.8, s,
            text="ID 1.352 +.002/-.000")
    sh.notes([
        "DCN-2: SPEC OD/ID WERE TRANSPOSED (OD 1.350 < ID 1.352 IMPOSSIBLE).",
        "SLIP FIT OVER SHEX-011 TAIL DIA 1.350 (Z 0-3); FLUSH AT Z=0.",
        "BOTTOM GUIDE BELOW SHEX-013 — INSTALL AFTER EQUALIZING SUB BODY (DCN-5).",
        "CHAMFER BOTTOM 0.040 x 45, TOP 0.030 x 45.",
    ], 1.0, 3.4)
    return sh.save("DWG-011A-SHP_SHEX-011A_tail_sleeve")


def dwg_010_fishing_neck() -> Path:
    sh = Sheet("DWG-010-SHP", "FISHING NECK / TOP SUB (GS PROFILE)", "SHEX-012",
               "4140 HT (AMS 6415) 28-32 HRC", "1", rev="E")
    s = 1.15
    x0, y0 = 2.6, 5.6
    prof = [(0, 0.775), (0.5, 0.775), (0.5, 0.725), (4.5, 0.725),
            (4.6, 0.5935), (5.3, 0.5935), (5.45, 0.6875), (6.35, 0.6875),
            (6.5, 0.620)]
    bore = [(0, 1.297 / 2), (1.0, 1.297 / 2), (1.0, 0.6525), (1.5, 0.6525),
            (1.5, 0.375), (5.5, 0.375), (5.5, 0.4375), (6.5, 0.4375)]
    turned_half_section(sh, prof, bore, x0, y0, s)
    sh.label("VIEW A — HALF SECTION  SCALE 1.15:1", 2.2, 8.3)
    sh.hdim((x0, y0 + 0.9), (x0 + 6.5 * s, y0 + 0.9), y0 + 1.8, s, text="6.500 +/-.010")
    sh.hdim((x0 + 5.45 * s, y0 - 0.6875 * s), (x0 + 6.35 * s, y0 - 0.6875 * s), y0 - 1.5, s,
            text="HEAD 0.900")
    sh.vdim((x0, y0 - 0.775 * s), (x0, y0 + 0.775 * s), x0 - 0.8, s,
            text="PILOT OD 1.550 -.002/-.004 x 0.500")
    sh.vdim((x0 + 6.35 * s, y0 - 0.6875 * s), (x0 + 6.35 * s, y0 + 0.6875 * s),
            x0 + 6.35 * s + 0.8, s, text="FISH HEAD DIA 1.375 +/-.003 (GS)")
    sh.leader("1-3/8-12 UNF-2B x 1.000 FROM BOTTOM FACE (DCN-7)",
              (x0 + 0.5 * s, y0 + (1.297 / 2) * s), (x0 + 0.8, y0 + 2.2))
    sh.leader("SEAL BORE DIA 1.305 +.005/-.000 x 0.500 (Z' 1.0-1.5)\nFLOOR SEATS 2-211 FACE SEAL (DCN-7)",
              (x0 + 1.25 * s, y0 + 0.6525 * s), (x0 + 2.6, y0 + 2.6))
    sh.leader("BODY DIA 1.450 +.000/-.003 — KIT SHOE ID 1.470 PASSES OVER",
              (x0 + 2.5 * s, y0 + 0.725 * s), (x0 + 3.4, y0 + 2.2))
    sh.leader("GS NECK GROOVE DIA 1.187 +/-.005 x 0.700",
              (x0 + 4.95 * s, y0 + 0.5935 * s), (x0 + 5.6, y0 + 1.6))
    sh.leader("TOP BOX 1.000-8 UN-2B x 1.000 (KIT SHEAR STUD ST-103)",
              (x0 + 6.0 * s, y0 + 0.4375 * s), (x0 + 6.6, y0 + 2.4))
    sh.leader("THROUGH BORE DIA 0.750 +.002/-.000",
              (x0 + 3.6 * s, y0 + 0.375 * s), (x0 + 4.6, y0 - 2.0))

    sh.notes([
        "REV E (DCN-7): NECK DOWNSIZED + GS-PROFILE FISH HEAD SO THE SETTING-KIT",
        "  SLEEVE (ID 1.470) PASSES OVER THE BODY TO REACH THE SLIP CARRIER FACE.",
        "  REV D OD 1.688 BODY WAS UN-SETTABLE BY ANY ADAPTER-KIT TOOL.",
        "BOTTOM FACE SEATS ON SHEX-011 SHOULDER AT PLUG Z=50.5; TORQUE 250 FT-LB MIN.",
        "DRILL DIA 0.125 ANTIROTATION PIN AT PLUG Z=51.0 AFTER MAKEUP.",
        "FISH HEAD: 1.375 GS-CLASS PROFILE — GAUGE WITH GS PULLING TOOL BEFORE SHIP.",
        "PLUG OVERALL WITH THIS NECK: 57.0 IN (DCN-4); NECK SPANS PLUG Z 50.5-57.0.",
        "PILOT Z' 0-0.5 RIDES THE UPPER SLIP CARRIER BORE DIA 1.562.",
    ], 9.8, 4.4)
    return sh.save("DWG-010-SHP_SHEX-012_fishing_neck")


def dwg_013_equalizing_sub() -> Path:
    sh = Sheet("DWG-013-SHP", "BOTTOM EQUALIZING SUB (BODY + SLEEVE)", "SHEX-013 / SHEX-013S",
               "4140 HT (AMS 6415) 28-32 HRC", "1 + 1", rev="C")
    s = 2.0
    # body half-section
    x0, y0 = 2.4, 6.6
    prof = [(0, 0.844), (2.0, 0.844)]
    bore = [(0, 0.738), (2.0, 0.738)]
    turned_half_section(sh, prof, bore, x0, y0, s)
    # ports
    for sign in (1, -1):
        sh.msp.add_lwpolyline(
            [(x0 + (1.0 - 0.031) * s, y0 + sign * 0.738 * s), (x0 + (1.0 - 0.031) * s, y0 + sign * 0.844 * s),
             (x0 + (1.0 + 0.031) * s, y0 + sign * 0.844 * s), (x0 + (1.0 + 0.031) * s, y0 + sign * 0.738 * s)],
            dxfattribs={"layer": "GEOM"})
    # internal gland grooves
    for zg in (0.30, 2.0 - 0.398):
        for sign in (1, -1):
            sh.msp.add_lwpolyline(
                [(x0 + zg * s, y0 + sign * 0.738 * s), (x0 + zg * s, y0 + sign * 0.783 * s),
                 (x0 + (zg + 0.098) * s, y0 + sign * 0.783 * s), (x0 + (zg + 0.098) * s, y0 + sign * 0.738 * s)],
                dxfattribs={"layer": "GEOM"})
    sh.label("VIEW A — BODY HALF SECTION  SCALE 2:1", 2.0, 9.2)
    sh.hdim((x0, y0 + 0.844 * s), (x0 + 2.0 * s, y0 + 0.844 * s), y0 + 2.15, s, text="2.000 +/-.005")
    sh.vdim((x0, y0 - 0.844 * s), (x0, y0 + 0.844 * s), x0 - 0.8, s, text="OD 1.688 +.000/-.005")
    sh.vdim((x0 + 2.0 * s, y0 - 0.738 * s), (x0 + 2.0 * s, y0 + 0.738 * s), x0 + 2.0 * s + 0.8, s,
            text="ID 1.476 +.003/-.000 (DCN-5)")
    sh.leader("4x PORT DIA 0.062 AT Z' 1.000, 90 DEG APART",
              (x0 + 1.0 * s, y0 + 0.844 * s), (x0 + 2.8, y0 + 2.2))
    sh.leader("2x INTERNAL GLAND: GROOVE DIA 1.566 x 0.098 W (0.045 DP)\nVITON 90 CS 0.070 (-016 CLASS); STRADDLE PORTS",
              (x0 + 0.35 * s, y0 - 0.76 * s), (x0 + 2.0, y0 - 2.3))

    # sleeve half-section
    x1, y1 = 2.4, 2.6
    prof2 = [(0, 0.735), (1.2, 0.735)]
    bore2 = [(0, 0.677), (1.2, 0.677)]
    turned_half_section(sh, prof2, bore2, x1, y1, s)
    for sign in (1, -1):
        sh.msp.add_lwpolyline(
            [(x1 + (0.9 - 0.031) * s, y1 + sign * 0.677 * s), (x1 + (0.9 - 0.031) * s, y1 + sign * 0.735 * s),
             (x1 + (0.9 + 0.031) * s, y1 + sign * 0.735 * s), (x1 + (0.9 + 0.031) * s, y1 + sign * 0.677 * s)],
            dxfattribs={"layer": "GEOM"})
    sh.label("VIEW B — SLIDING SLEEVE SHEX-013S  SCALE 2:1", 2.0, 4.85)
    sh.hdim((x1, y1 + 0.735 * s), (x1 + 1.2 * s, y1 + 0.735 * s), y1 + 2.0, s, text="1.200 +/-.005")
    sh.vdim((x1, y1 - 0.735 * s), (x1, y1 + 0.735 * s), x1 - 0.8, s, text="OD 1.470 +.000/-.002")
    sh.vdim((x1 + 1.2 * s, y1 - 0.677 * s), (x1 + 1.2 * s, y1 + 0.677 * s), x1 + 1.2 * s + 0.8, s,
            text="ID 1.354 +.003/-.000")
    sh.leader("4x PORT DIA 0.062, ALIGN BODY PORTS WHEN OPEN",
              (x1 + 0.9 * s, y1 - 0.735 * s), (x1 + 3.2, y1 - 1.7))

    sh.notes([
        "DCN-5: RADIAL STACK REBUILT — SPEC SLEEVE OD 1.680 COULD NOT ENTER BODY ID 1.562,",
        "  AND SPEC 0.070-DP GROOVES CUT THROUGH EVERY AVAILABLE WALL.",
        "NEW STACK: MANDREL TAIL DIA 1.350 EXTENDED TO Z=5.0; SLEEVE 1.470/1.354;",
        "  BODY 1.688/1.476 WITH SEALS IN BODY GLANDS RIDING SLEEVE OD.",
        "SLEEVE TRAVEL 0.375 MIN WITHOUT BINDING; PORTS ALIGNED = OPEN (RUN-IN).",
        "PRESSURE-CONTAINING — 100 PERCENT PT ALL PORTS AFTER MACHINING.",
        "ANTI-ROTATION PIN DIA 0.093 x 0.250 DP AT Z' 0.500, RIDES SLEEVE SLOT.",
        "FUNCTIONAL TEST: FLOW OPEN (ALIGNED); BLOCKED CLOSED (SHIFTED +0.375).",
    ], 9.0, 6.6)
    return sh.save("DWG-013-SHP_SHEX-013_equalizing_sub")


def main() -> None:
    OUT_DXF.mkdir(parents=True, exist_ok=True)
    OUT_PDF.mkdir(parents=True, exist_ok=True)
    sheets = [
        dwg_001_iris_segment(),
        dwg_002a_helix_guide(),
        dwg_005_mtm_segment(),
        dwg_007b_hnbr_preform(),
        dwg_007a_petal(),
        dwg_008_slip(True),
        dwg_008_slip(False),
        _stent_sheet("SHEX-008", "DWG-009-SHP", "STAGE 1 STENT SLEEVE", 4.0, 12, 6, 3.375, 0.063),
        _stent_sheet("SHEX-009", "DWG-011-SHP", "STAGE 2 STENT SLEEVE", 5.0, 14, 4, 5.750, 0.063),
        dwg_012_support_sleeve(),
        dwg_011b_mandrel(),
        dwg_011a_tail_sleeve(),
        dwg_010_fishing_neck(),
        dwg_013_equalizing_sub(),
    ]
    for p in sheets:
        print(f"  ok {p.name}")

    # PDF rendering
    import matplotlib
    matplotlib.use("Agg")
    from ezdxf.addons.drawing import RenderContext, Frontend
    from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
    import matplotlib.pyplot as plt

    for p in sheets:
        doc = ezdxf.readfile(p)
        msp = doc.modelspace()
        fig = plt.figure(figsize=(17, 11), dpi=200)
        ax = fig.add_axes([0, 0, 1, 1])
        ctx = RenderContext(doc)
        backend = MatplotlibBackend(ax)
        Frontend(ctx, backend).draw_layout(msp, finalize=True)
        out = OUT_PDF / (p.stem + ".pdf")
        fig.savefig(out, facecolor="white")
        plt.close(fig)
        print(f"  pdf {out.name}")


if __name__ == "__main__":
    main()
