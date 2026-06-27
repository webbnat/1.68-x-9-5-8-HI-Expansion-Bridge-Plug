"""SHEX-BP-UHEX-54 release solids — manufacturing-grade B-rep STEP geometry.

Built on the Gmsh OpenCASCADE kernel. All input dimensions in inches;
STEP output in millimetres. Z axis: bottom of tool at z=0, increasing uphole.

This module supersedes the envelope geometry in cad/solid_cad.py for release.
It implements the part_specs/*.md shop dimensions and resolves the spec
contradictions recorded as DCN-1..DCN-5 (see export/release/RELEASE_NOTES.md):

  DCN-1  Helix drive re-architected as a 2-start lead screw: the mandrel is
         necked to O1.270 over Z 10.4-23.0 (so the fixed SHEX-002 insert is
         never over O1.550 body at any stroke position) with 2-start helical
         drive ribs at Z 19-23 (peak O1.429); SHEX-002 ID changed
         1.552 -> O1.282 so the 0.080-deep grooves have wall to live in
         (groove root O1.442).
  DCN-2  SHEX-011A tail sleeve: ID 1.352 over the O1.350 tail, OD 1.550
         (spec had OD 1.350 < ID 1.352, impossible).
  DCN-3  Mandrel finished length 52.500: body to the joint shoulder at Z=51
         plus the O1.500 x 1.5 pin stub; the spec's Z 51-54 O1.550 stub
         cannot coexist with the SHEX-012 O0.750 bore.
  DCN-4  Plug overall length 57.0 in with SHEX-012 Rev D 6.000 neck.
  DCN-5  SHEX-013 radial stack rebuilt so the sliding sleeve actually fits
         and the O-ring glands have wall to live in: mandrel O1.350 tail
         extended through the sub zone (step moves Z 3.0 -> 5.0); body
         OD 1.688 / ID 1.476 with 2 internal gland grooves (0.045 deep)
         straddling the ports; sleeve OD 1.470 / ID 1.354 (spec sleeve
         OD 1.680 could not enter the O1.562 body bore, and 0.070-deep
         grooves cut through every wall in the spec stack).
  DCN-6  Top joint re-sequenced so thread, seal and shoulder can all mate:
         mandrel shoulder @ Z=51.0; pin (thread at base, plain seal nose,
         face O-ring groove in the nose end face); SHEX-012 female: thread
         at mouth 0-1.0, seal bore 1.0-1.5.
  DCN-7  Settability (adapter-kit interface): with the Rev D O1.688 neck no
         setting sleeve could pass over the neck to react the outer stack —
         the plug could not be set by any tool. Top joint downsized and
         recessed: mandrel shoulder Z 51.0 -> 50.5, pin O1.375 (thread
         1-3/8-12 UNF-2A 50.5-51.5, plain nose O1.300 51.5-52.0, Parker
         2-211 face groove in nose face), finished length 52.000.
         SHEX-012 Rev E: L 6.5 (plug Z 50.5-57.0, OAL still 57.0), pilot
         O1.550 x 0.5 into the carrier bore, body O1.450, GS-profile fish
         head O1.375 with internal 1.000-8 UN box top connection. The kit
         shoe (OD 1.900 / ID 1.470) passes over the O1.450 body and lands
         on the upper slip carrier face at Z=51.
  DCN-8  Net setting stroke re-budgeted 11.0 -> 10.000 in (+0.25 release
         overtravel = 10.25 demand) so the plug sets inside the 10.777-in
         stroke of a Baker E-4 No. 20 e-line tool (0.53 margin) and the
         10.5-in stroke of #20-class CT hydraulic tools (Model J-20 /
         Fury-20 class, 0.25 margin). Release stud calibrated 45 klbf.
         Seal energization is restated as axial stack squeeze from the
         kit setting sleeve (industry standard); the mandrel seal ramps
         provide radial backup under lands 3-4 at full stroke only.
  DCN-9  Iris drive interference fix + re-index: helix neck extended
         10.4-25.9 (was -23.0) - as released, the O1.282 insert sat over
         O1.550 body at Z 23.0-25.75 AT RUN-IN (hard interference);
         drive ribs moved Z 18.15-21.75 (top flush with insert bottom at
         stroke 0, fully meshed at stroke 4.0 = iris deployed; phase
         324 deg); MTM load land moved 44.75 -> 34.75 so at full stroke
         (44.75) it sits under the MTM rings instead of 10 in above them.
         Slip-set kinematics at full stroke (expander leaves the slip
         zone) remain an inherited open item - documented, not resolved.
"""

from __future__ import annotations

import math
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterator

import gmsh

IN_TO_MM = 25.4


def mm(v_in: float) -> float:
    return v_in * IN_TO_MM


# ---------------------------------------------------------------------------
# session helpers
# ---------------------------------------------------------------------------


@dataclass
class Body:
    name: str
    material: str
    dimtags: list[tuple[int, int]] = field(default_factory=list)


class Model:
    def __init__(self, name: str) -> None:
        gmsh.initialize()
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.model.add(name)
        self.name = name
        self.bodies: list[Body] = []

    def close(self) -> None:
        gmsh.finalize()

    def register(self, name: str, material: str, dimtags: list[tuple[int, int]]) -> None:
        self.bodies.append(Body(name, material, list(dimtags)))

    def synchronize(self) -> None:
        gmsh.model.occ.synchronize()

    def name_bodies(self) -> None:
        """Attach body names as physical groups so STEP carries labels."""
        self.synchronize()
        for body in self.bodies:
            tags = [t for d, t in body.dimtags if d == 3]
            if tags:
                pg = gmsh.model.addPhysicalGroup(3, tags)
                gmsh.model.setPhysicalName(3, pg, body.name)

    def purge_strays(self) -> None:
        """Remove dangling curves/surfaces (helix construction wires etc.).

        Entity tags are renumbered on each synchronize, so the boundary set
        is recomputed every pass.
        """
        self.synchronize()
        for _ in range(3):
            vols = gmsh.model.getEntities(3)
            needed: set[tuple[int, int]] = set(vols)
            needed.update((d, abs(t)) for d, t in gmsh.model.getBoundary(
                vols, combined=False, oriented=False, recursive=True))
            removed_any = False
            for dim in (2, 1, 0):
                strays = [e for e in gmsh.model.getEntities(dim) if e not in needed]
                if strays:
                    try:
                        gmsh.model.occ.remove(strays, recursive=False)
                        removed_any = True
                    except Exception:
                        pass
            if not removed_any:
                break
            self.synchronize()

    def write_step(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.purge_strays()
        self.name_bodies()
        gmsh.write(str(path))

    def write_stl(self, path: Path, size_mm: float = 6.0) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.synchronize()
        gmsh.option.setNumber("Mesh.SaveAll", 1)
        gmsh.option.setNumber("Mesh.MeshSizeMax", size_mm)
        gmsh.option.setNumber("Mesh.MeshSizeMin", size_mm / 8)
        gmsh.model.mesh.generate(2)
        gmsh.write(str(path))


@contextmanager
def session(name: str) -> Iterator[Model]:
    model = Model(name)
    try:
        yield model
    finally:
        model.close()


# ---------------------------------------------------------------------------
# primitive helpers (inches in, OCC tags out)
# ---------------------------------------------------------------------------

occ = gmsh.model.occ  # resolved at call time after gmsh.initialize()


def cyl(z0: float, h: float, r: float) -> tuple[int, int]:
    return (3, gmsh.model.occ.addCylinder(0, 0, mm(z0), 0, 0, mm(h), mm(r)))


def conez(z0: float, h: float, r0: float, r1: float) -> tuple[int, int]:
    return (3, gmsh.model.occ.addCone(0, 0, mm(z0), 0, 0, mm(h), mm(r0), mm(r1)))


def annulus(z0: float, h: float, ri: float, ro: float) -> list[tuple[int, int]]:
    if ri <= 1e-9:
        return [cyl(z0, h, ro)]
    out = cyl(z0, h, ro)
    inn = cyl(z0, h, ri)
    res, _ = gmsh.model.occ.cut([out], [inn])
    return res


def cut(target: list[tuple[int, int]], tools: list[tuple[int, int]]) -> list[tuple[int, int]]:
    res, _ = gmsh.model.occ.cut(target, tools)
    return res


def fuse(parts: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if len(parts) == 1:
        return parts
    res, _ = gmsh.model.occ.fuse(parts[:1], parts[1:])
    return res


def radial_hole(z: float, r_hole: float, ang_deg: float, r_extent: float) -> tuple[int, int]:
    """Cylinder pointing radially outward at angle ang_deg, length 2*r_extent."""
    a = math.radians(ang_deg)
    dx, dy = math.cos(a), math.sin(a)
    return (
        3,
        gmsh.model.occ.addCylinder(
            -dx * mm(r_extent) * 0.0, -dy * mm(r_extent) * 0.0, mm(z),
            dx * mm(r_extent), dy * mm(r_extent), 0,
            mm(r_hole),
        ),
    )


def sector_prism(
    r1: float,
    r2: float,
    half_deg: float,
    z0: float,
    length: float,
    rot_deg: float = 0.0,
) -> tuple[int, int]:
    """True arc-bounded sector (annular wedge) extruded along Z."""
    a = math.radians(half_deg)
    z = mm(z0)
    o = gmsh.model.occ
    pc = o.addPoint(0, 0, z)
    p0 = o.addPoint(mm(r1) * math.cos(-a), mm(r1) * math.sin(-a), z)
    p1 = o.addPoint(mm(r2) * math.cos(-a), mm(r2) * math.sin(-a), z)
    p2 = o.addPoint(mm(r2) * math.cos(a), mm(r2) * math.sin(a), z)
    p3 = o.addPoint(mm(r1) * math.cos(a), mm(r1) * math.sin(a), z)
    l0 = o.addLine(p0, p1)
    arc_out = o.addCircleArc(p1, pc, p2)
    l1 = o.addLine(p2, p3)
    arc_in = o.addCircleArc(p3, pc, p0)
    loop = o.addCurveLoop([l0, arc_out, l1, arc_in])
    surf = o.addPlaneSurface([loop])
    ext = o.extrude([(2, surf)], 0, 0, mm(length))
    vols = [(d, t) for d, t in ext if d == 3]
    if rot_deg:
        o.rotate(vols, 0, 0, 0, 0, 0, 1, math.radians(rot_deg))
    return vols[0]


def helix_pipe(
    r_center: float,
    lead: float,
    turns: float,
    z0: float,
    profile_r: float,
    phase_deg: float = 0.0,
    pts_per_turn: int = 24,
) -> tuple[int, int]:
    """Solid swept along a helix — round profile (groove / rib form)."""
    o = gmsh.model.occ
    n = max(8, int(pts_per_turn * turns))
    pts = []
    for i in range(n + 1):
        f = i / n
        ang = math.radians(phase_deg) + 2 * math.pi * turns * f
        x = mm(r_center) * math.cos(ang)
        y = mm(r_center) * math.sin(ang)
        z = mm(z0 + lead * turns * f)
        pts.append(o.addPoint(x, y, z))
    spline = o.addSpline(pts)
    wire = o.addWire([spline])

    # disk at helix start, oriented normal to the start tangent
    a0 = math.radians(phase_deg)
    x0, y0 = mm(r_center) * math.cos(a0), mm(r_center) * math.sin(a0)
    z0mm = mm(z0)
    disk = o.addDisk(x0, y0, z0mm, mm(profile_r), mm(profile_r))
    # start tangent of the helix
    tx = -math.sin(a0)
    ty = math.cos(a0)
    tz = mm(lead) / (2 * math.pi * mm(r_center))
    norm = math.sqrt(tx * tx + ty * ty + tz * tz)
    tx, ty, tz = tx / norm, ty / norm, tz / norm
    # rotate disk normal (+Z) onto tangent
    axx = -ty  # z cross t
    axy = tx
    axz = 0.0
    ax_norm = math.sqrt(axx * axx + axy * axy)
    if ax_norm > 1e-9:
        angle = math.acos(max(-1.0, min(1.0, tz)))
        o.rotate([(2, disk)], x0, y0, z0mm, axx / ax_norm, axy / ax_norm, axz, angle)
    swept = o.addPipe([(2, disk)], wire, "DiscreteTrihedron")
    vols = [(d, t) for d, t in swept if d == 3]
    try:
        o.remove([(1, spline)], recursive=True)
    except Exception:
        pass
    return vols[0]


def face_groove(z_face: float, depth: float, r_in: float, r_out: float) -> tuple[int, int]:
    """Annular groove tool cut downward into a +Z face."""
    out = cyl(z_face - depth, depth, r_out)
    inn = cyl(z_face - depth, depth, r_in)
    res, _ = gmsh.model.occ.cut([out], [inn])
    return res[0]


def bore_groove(z0: float, width: float, r_bore: float, r_groove: float) -> tuple[int, int]:
    """Annular O-ring groove tool cut outward from a bore."""
    out = cyl(z0, width, r_groove)
    inn = cyl(z0, width, r_bore * 0.5)  # generous inner clearance
    res, _ = gmsh.model.occ.cut([out], [inn])
    return res[0]


def od_groove_tool(z0: float, width: float, r_root: float, r_od: float) -> tuple[int, int]:
    """Annular groove tool to cut into an OD (ring from r_root out past OD)."""
    out = cyl(z0, width, r_od + 0.25)
    inn = cyl(z0, width, r_root)
    res, _ = gmsh.model.occ.cut([out], [inn])
    return res[0]


# ---------------------------------------------------------------------------
# design constants (authority: part_specs + design_uhex_54in.yaml + DCNs)
# ---------------------------------------------------------------------------

MANDREL_BODY_OD = 1.550
MANDREL_TAIL_OD = 1.350
RUN_OD = 1.688
BORE_ID = 1.562  # standard module bore over the mandrel
CASING_ID = 8.835       # 9-5/8" 40# nominal ID
CASING_DRIFT = 8.679
CASING_OD = 9.625

# DCN-1 lead-screw helix drive
HELIX_LEAD = 4.0
HELIX_TURNS = 1.0       # each start sweeps 1 turn over the 4.0 zone
HELIX_NECK_OD = 1.270
HELIX_RIB_PROFILE_R = 0.0575   # round-form rib, ~0.115 wide
HELIX_RIB_PEAK_OD = 1.430
SHEX002_OD = 1.555
SHEX002_ID = 1.282      # DCN-1 (was 1.552)
SHEX002_GROOVE_W = 0.125
SHEX002_GROOVE_D = 0.080
SHEX002_LEN = 4.0

# module Z map (run-in, plug coordinates) — 57.0 in overall per DCN-4
MODULE_Z = {
    "mandrel_tail": (0.0, 3.0),
    "bottom_sub": (3.0, 5.0),
    "lower_slips": (5.0, 9.5),
    "stage1": (9.5, 13.5),
    "stage2": (13.5, 18.5),
    "stage3_iris": (18.5, 26.0),
    "seal_land_1": (26.0, 30.5),
    "seal_land_2": (30.5, 35.0),
    "seal_land_3": (35.0, 39.5),
    "seal_land_4": (39.5, 44.0),
    "upper_mtm": (44.0, 46.5),
    "upper_slips": (46.5, 51.0),
    "fishing_neck": (51.0, 57.0),
}

SET_STROKE = 10.0  # mandrel +Z travel, run-in -> set (DCN-8: fits E-4 No.20 10.777)


# ---------------------------------------------------------------------------
# individual parts (each built at its own part datum Z'=0 bottom face)
# ---------------------------------------------------------------------------


def build_shex_001_iris_segment(m: Model, z0: float = 0.0, rot_deg: float = 0.0) -> list[tuple[int, int]]:
    """Iris segment, deployed profile (EDM from plate). R1 2.955 / R2 4.318,
    span 22.5 deg, L 2.750, with helix follower tab on the inner face."""
    seg = sector_prism(2.955, 4.318, 11.25, z0, 2.750, 0.0)
    # follower tab: 0.625 axial x 0.125 circumferential x 0.080 radial inward,
    # centred at mid-length on the bisector plane
    tab_zc = z0 + 2.750 / 2
    o = gmsh.model.occ
    tab = o.addBox(
        mm(2.955 - 0.080), -mm(0.125) / 2, mm(tab_zc - 0.625 / 2),
        mm(0.080 + 0.020), mm(0.125), mm(0.625),
    )
    res = fuse([seg, (3, tab)])
    if rot_deg:
        o.rotate(res, 0, 0, 0, 0, 0, 1, math.radians(rot_deg))
    return res


def build_shex_002_helix_guide(
    m: Model, z0: float = 0.0, phase_deg: float = 0.0
) -> list[tuple[int, int]]:
    """Helix guide insert — DCN-1: OD 1.555 x ID 1.282 x L 4.000 ring with
    2-start internal helical grooves, lead 4.0, groove 0.125 x 0.080."""
    ring = annulus(z0, SHEX002_LEN, SHEX002_ID / 2, SHEX002_OD / 2)
    groove_center_r = SHEX002_ID / 2 + SHEX002_GROOVE_D - SHEX002_GROOVE_W / 2
    tools = []
    for phase in (phase_deg, phase_deg + 180.0):
        tools.append(
            helix_pipe(groove_center_r, HELIX_LEAD, HELIX_TURNS, z0, SHEX002_GROOVE_W / 2, phase)
        )
    return cut(ring, tools)


def build_shex_003_mtm_segment(m: Model, z0: float = 0.0, rot_deg: float = 0.0) -> list[tuple[int, int]]:
    """MTM ring segment — 90 deg arc (minus 2 deg gap), R 4.200-4.400, L 0.750.
    12 per plug = 3 rings x 4 segments."""
    return [sector_prism(4.200, 4.400, 44.0, z0, 0.750, rot_deg)]


def build_shex_004_hnbr_preform(m: Model, z0: float = 0.0) -> list[tuple[int, int]]:
    """HNBR seal liner preform — Ri 0.781 / Ro 0.831 x L 0.550 ring."""
    return annulus(z0, 0.550, 0.781, 0.831)


def build_shex_005_petal_backup(m: Model, z0: float = 0.0, rot_deg: float = 0.0) -> list[tuple[int, int]]:
    """Petal backup, deployed profile. R1 0.895 / R2 4.011, 22.5 deg, L 0.550."""
    return [sector_prism(0.895, 4.011, 11.25, z0, 0.550, rot_deg)]


def build_slip_segment(m: Model, z0: float = 0.0, rot_deg: float = 0.0) -> list[tuple[int, int]]:
    """SHEX-006/007 slip segment, deployed profile. 45 deg sector (minus gap),
    R 3.560-4.360, L 2.000, with 4 tooth serrations on the OD."""
    seg = sector_prism(3.560, 4.360, 20.5, z0, 2.000, 0.0)
    # tooth grooves: annular V-ish notches on OD (rectangular form, 0.060 deep)
    tools = []
    for i in range(3):
        zg = z0 + 0.35 + i * 0.55
        tools.append(od_groove_tool(zg, 0.120, 4.360 - 0.060, 4.360))
    res = cut([seg], tools)
    if rot_deg:
        gmsh.model.occ.rotate(res, 0, 0, 0, 0, 0, 1, math.radians(rot_deg))
    return res


def _stent_sleeve(
    m: Model,
    z0: float,
    length: float,
    od: float,
    wall: float,
    cells_around: int,
    rings: int,
    kerf: float = 0.008,
) -> list[tuple[int, int]]:
    """Laser-cut sleeve at run-in OD: staggered circumferential kerf slots
    (closed-cell at run-in; deploys to diamond mesh)."""
    ro = od / 2
    ri = ro - wall
    tube = annulus(z0, length, ri, ro)
    margin = 0.06 * length
    band = (length - 2 * margin) / rings
    slot_frac = 0.70
    slot_w = 0.020  # modelled kerf slot width (laser kerf 0.008 on drawing)
    tools: list[tuple[int, int]] = []
    o = gmsh.model.occ
    for ring_i in range(rings):
        zc = z0 + margin + (ring_i + 0.5) * band
        stagger = 0.5 if ring_i % 2 else 0.0
        pitch = 360.0 / cells_around
        arc_len = math.pi * od * slot_frac / cells_around  # tangential chord
        for c in range(cells_around):
            ang = math.radians((c + stagger) * pitch)
            # thin box through the wall, tangential orientation
            bx = o.addBox(
                mm(ri - 0.15), -mm(arc_len) / 2, mm(zc - slot_w / 2),
                mm(wall + 0.30), mm(arc_len), mm(slot_w),
            )
            o.rotate([(3, bx)], 0, 0, 0, 0, 0, 1, ang)
            tools.append((3, bx))
    return cut(tube, tools)


def build_shex_008_stage1_stent(m: Model, z0: float = 0.0) -> list[tuple[int, int]]:
    return _stent_sleeve(m, z0, 4.0, RUN_OD, 0.063, 12, 6)


def build_shex_009_stage2_stent(m: Model, z0: float = 0.0) -> list[tuple[int, int]]:
    return _stent_sleeve(m, z0, 5.0, RUN_OD, 0.063, 14, 4)


def build_shex_010_support_sleeve(m: Model, z0: float = 0.0) -> list[tuple[int, int]]:
    """Stage-3 iris support sleeve at manufacturing geometry:
    OD 1.688 x L 7.500, bore O1.562, 16 guide slots, helix pocket, lock land."""
    body = annulus(z0, 7.5, BORE_ID / 2, RUN_OD / 2)
    o = gmsh.model.occ
    tools: list[tuple[int, int]] = []
    # 16 internal guide slots: 0.120 wide x 0.055 deep x 2.750 long, centre Z' 2.375
    slot_z0 = z0 + 2.375 - 2.750 / 2
    for i in range(16):
        ang = math.radians(i * 22.5)
        bx = o.addBox(
            mm(BORE_ID / 2 - 0.020), -mm(0.120) / 2, mm(slot_z0),
            mm(0.055 + 0.020), mm(0.120), mm(2.750),
        )
        o.rotate([(3, bx)], 0, 0, 0, 0, 0, 1, ang)
        tools.append((3, bx))
    # helix pocket: bore opened to O1.558 over Z' 3.250-7.250
    tools.append(annulus(z0 + 3.250, 4.000, BORE_ID / 2 - 0.05, 1.558 / 2)[0])
    # retaining ring groove 0.030 wide x 0.040 deep at Z' 7.200 (in pocket bore)
    tools.append(annulus(z0 + 7.200, 0.030, 1.558 / 2 - 0.01, 1.558 / 2 + 0.040)[0])
    return cut(body, tools)


def build_shex_011_mandrel(m: Model, z0: float = 0.0) -> list[tuple[int, int]]:
    """Inner mandrel, finished length 52.000 (DCN-3/DCN-7), full functional
    zones per spec section 12.10 with DCN-1 lead-screw helix drive zone."""
    parts: list[tuple[int, int]] = []
    # ledger (tail -> head); cones for tapers
    # DCN-5: O1.350 tail extended through the equalizing zone (step @ Z=5.0)
    parts.append(cyl(z0 + 0.0, 5.0, MANDREL_TAIL_OD / 2))                       # tail
    parts.append(cyl(z0 + 5.0, 1.25, MANDREL_BODY_OD / 2))                      # to 6.25
    parts.append(conez(z0 + 6.25, 1.50, MANDREL_BODY_OD / 2, 1.620 / 2))        # lower slip taper
    parts.append(cyl(z0 + 7.75, 1.625, 1.620 / 2))                              # trail land
    parts.append(conez(z0 + 9.375, 0.125, 1.620 / 2, MANDREL_BODY_OD / 2))      # blend @ 9.5
    parts.append(cyl(z0 + 9.5, 0.8, MANDREL_BODY_OD / 2))                       # to 10.3
    # DCN-1/DCN-9 helix drive: long neck (insert never rides O1.550 at any
    # stroke 0-10; release Rev A interfered at run-in over Z 23.0-25.75)
    parts.append(conez(z0 + 10.3, 0.10, MANDREL_BODY_OD / 2, HELIX_NECK_OD / 2))
    parts.append(cyl(z0 + 10.40, 15.50, HELIX_NECK_OD / 2))                     # neck 10.4-25.9
    parts.append(conez(z0 + 25.90, 0.10, HELIX_NECK_OD / 2, MANDREL_BODY_OD / 2))
    # 2-start drive ribs Z 18.15-21.75 (DCN-9: top flush with insert bottom
    # at stroke 0; fully meshed at stroke 4.0), peak O1.429
    rib_center_r = HELIX_NECK_OD / 2 + 0.022
    for phase in (0.0, 180.0):
        parts.append(
            helix_pipe(
                rib_center_r,
                HELIX_LEAD, 0.90, z0 + 18.15, HELIX_RIB_PROFILE_R, phase,
            )
        )
    parts.append(cyl(z0 + 26.0, 1.125, MANDREL_BODY_OD / 2))                    # to 27.125
    # seal ramps x4: 1.550 -> 1.582 over 1.375, flat crest is momentary (ramp
    # peak then 30 deg back-chamfer to 1.550)
    zr = 27.125
    for _ in range(4):
        parts.append(conez(z0 + zr, 1.375, MANDREL_BODY_OD / 2, 1.582 / 2))
        parts.append(conez(z0 + zr + 1.375, 0.060, 1.582 / 2, MANDREL_BODY_OD / 2))
        nxt = zr + 4.5
        parts.append(cyl(z0 + zr + 1.435, nxt - (zr + 1.435), MANDREL_BODY_OD / 2))
        zr = nxt
    # zr now 45.125; previous loop covered to 45.125 via last gap cylinder
    parts.append(cyl(z0 + 45.125, 5.875 - 1.125, MANDREL_BODY_OD / 2))          # to 49.875 base run
    # MTM load land O1.558 x 0.500 @ 34.75-35.25 (DCN-9: arrives under the
    # MTM rings at full stroke 44.75-45.25)
    parts.append(cyl(z0 + 34.75, 0.50, 1.558 / 2))
    # upper slip taper
    parts.append(conez(z0 + 48.25, 1.50, MANDREL_BODY_OD / 2, 1.620 / 2))
    parts.append(conez(z0 + 49.75, 0.25, 1.620 / 2, MANDREL_BODY_OD / 2))
    parts.append(cyl(z0 + 50.0, 0.5, MANDREL_BODY_OD / 2))                      # body to joint @ 50.5
    # DCN-6/DCN-7 top joint (pin up): shoulder @ Z=50.5; pin O1.375 50.5-51.5
    # (thread 1-3/8-12 UNF-2A shown at major dia), plain seal nose O1.300
    # 51.5-52.0; finished length 52.000
    parts.append(cyl(z0 + 50.5, 1.0, 1.375 / 2))
    parts.append(cyl(z0 + 51.5, 0.5, 1.300 / 2))
    body = fuse(parts)
    # DCN-7: face O-ring groove (Parker 2-211) in the pin nose end face @ 52.0
    groove = face_groove(z0 + 52.0, 0.103, 0.800 / 2, 1.085 / 2)
    # thread relief at base of thread (Z=50.5)
    relief = od_groove_tool(z0 + 50.5, 0.060, 1.375 / 2 - 0.030, MANDREL_BODY_OD / 2)
    return cut(body, [groove, relief])


def build_shex_011a_tail_sleeve(m: Model, z0: float = 0.0) -> list[tuple[int, int]]:
    """Tail sleeve — DCN-2: ID 1.352 / OD 1.550 x L 3.000."""
    return annulus(z0, 3.0, 1.352 / 2, MANDREL_BODY_OD / 2)


def build_shex_012_fishing_neck(m: Model, z0: float = 0.0) -> list[tuple[int, int]]:
    """Fishing neck Rev E (DCN-7): L 6.500 (plug Z 50.5-57.0).
    Pilot O1.550 x 0.5 (rides the carrier bore), body O1.450, GS-profile
    fish head O1.375 over a O1.187 neck groove. Bore: 1-3/8-12 UNF-2B box
    at mouth (0-1.0), seal bore O1.305 (1.0-1.5), O0.750 gun-drill, then
    internal 1.000-8 UN box at the top (5.5-6.5) for the kit tension stud."""
    parts = [
        cyl(z0 + 0.0, 0.5, 1.550 / 2),                  # pilot into carrier bore
        cyl(z0 + 0.5, 4.0, 1.450 / 2),                  # body (DCN-7: shoe passes over)
        conez(z0 + 4.5, 0.10, 1.450 / 2, 1.187 / 2),    # into GS neck groove
        cyl(z0 + 4.6, 0.70, 1.187 / 2),                 # neck groove
        conez(z0 + 5.3, 0.15, 1.187 / 2, 1.375 / 2),    # under-head lead
        cyl(z0 + 5.45, 0.90, 1.375 / 2),                # fish head
        conez(z0 + 6.35, 0.15, 1.375 / 2, 1.240 / 2),   # top chamfer
    ]
    body = fuse(parts)
    tools = [
        cyl(z0 - 0.1, 0.1 + 1.0, 1.297 / 2),            # thread zone 0-1.0 (2B minor)
        cyl(z0 + 1.0, 0.500, 1.305 / 2),                # seal/pilot bore 1.0-1.5
        cyl(z0 + 1.4, 4.2, 0.750 / 2),                  # through bore
        cyl(z0 + 5.5, 1.0 + 0.1, 0.875 / 2),            # top box 1.000-8 UN tap bore
    ]
    return cut(body, tools)


def build_shex_013_body(m: Model, z0: float = 0.0) -> list[tuple[int, int]]:
    """Equalizing sub body — DCN-5: OD 1.688 / ID 1.476 x L 2.000,
    4 radial ports O0.062 at Z'=1.000, 2 internal gland grooves
    (O1.566 x 0.098 wide) straddling the port plane."""
    body = annulus(z0, 2.0, 1.476 / 2, RUN_OD / 2)
    tools = [radial_hole(z0 + 1.0, 0.062 / 2, a, 1.2) for a in (0, 90, 180, 270)]
    # internal O-ring gland grooves in the bore (depth 0.045)
    tools.append(annulus(z0 + 0.30, 0.098, 1.476 / 2 - 0.02, 1.566 / 2)[0])
    tools.append(annulus(z0 + 2.0 - 0.398, 0.098, 1.476 / 2 - 0.02, 1.566 / 2)[0])
    return cut(body, tools)


def build_shex_013s_sleeve(m: Model, z0: float = 0.0) -> list[tuple[int, int]]:
    """Equalizing sliding sleeve — DCN-5: OD 1.470 / ID 1.354 x L 1.200,
    4 matching ports; plain OD (seals live in the body glands)."""
    body = annulus(z0, 1.2, 1.354 / 2, 1.470 / 2)
    tools = [radial_hole(z0 + 0.9, 0.062 / 2, a, 1.0) for a in (0, 90, 180, 270)]
    return cut(body, tools)


# ---------------------------------------------------------------------------
# nested (run-in) representations for profile parts
# ---------------------------------------------------------------------------


def nested_arcs(
    z0: float,
    length: float,
    r1: float,
    r2: float,
    count: int,
    gap_deg: float = 2.0,
) -> list[tuple[int, int]]:
    """Thin nested arc shells at run-in (stowed profile parts convention)."""
    out: list[tuple[int, int]] = []
    pitch = 360.0 / count
    half = (pitch - gap_deg) / 2
    for i in range(count):
        out.append(sector_prism(r1, r2, half, z0, length, i * pitch))
    return out


# ---------------------------------------------------------------------------
# assemblies
# ---------------------------------------------------------------------------


def build_assembly(m: Model, state: str) -> None:
    """state: 'run_in' or 'set'. Plug Z map per MODULE_Z; in SET the mandrel
    group (mandrel, tail sleeve, fishing neck) advances +11.0 in."""
    dz = SET_STROKE if state == "set" else 0.0

    def shift(tags: list[tuple[int, int]]) -> list[tuple[int, int]]:
        if dz:
            gmsh.model.occ.translate(tags, 0, 0, mm(dz))
        return tags

    # mandrel group (moves in SET)
    t = build_shex_011_mandrel(m, 0.0)
    m.register("SHEX-011_inner_mandrel", "17-4 PH H900", shift(t))
    t = build_shex_011a_tail_sleeve(m, 0.0)
    m.register("SHEX-011A_tail_sleeve", "4140 HT", shift(t))
    t = build_shex_012_fishing_neck(m, 50.5)
    m.register("SHEX-012_fishing_neck", "4140 HT", shift(t))

    # bottom equalizing sub (stationary stack)
    z0 = MODULE_Z["bottom_sub"][0]
    m.register("SHEX-013_equalizing_sub_body", "4140 HT", build_shex_013_body(m, z0))
    m.register("SHEX-013S_sliding_sleeve", "4140 HT", build_shex_013s_sleeve(m, z0 + 0.1))

    # slips
    for mod, pn in (("lower_slips", "SHEX-007_lower_slip"), ("upper_slips", "SHEX-006_upper_slip")):
        z0, z1 = MODULE_Z[mod]
        zc = (z0 + z1) / 2 - 1.0
        if state == "set":
            tags: list[tuple[int, int]] = []
            for i in range(8):
                tags.extend(build_slip_segment(m, zc, i * 45.0))
            carrier = annulus(z0, z1 - z0, BORE_ID / 2, 3.560 / 2)
        else:
            tags = nested_arcs(zc, 2.0, BORE_ID / 2 + 0.002, RUN_OD / 2 - 0.002, 8, 3.0)
            carrier = annulus(z0, zc - z0, BORE_ID / 2, RUN_OD / 2) + annulus(
                zc + 2.0, z1 - zc - 2.0, BORE_ID / 2, RUN_OD / 2
            )
        m.register(pn + "_x8", "17-4 PH H900", tags)
        m.register(pn + "_carrier", "17-4 PH H900", carrier)

    # stage 1 stent (DCN-10: ductile expandable alloy, not 17-4 PH H900)
    z0, z1 = MODULE_Z["stage1"]
    if state == "set":
        tags = annulus(z0, z1 - z0, 3.375 / 2 - 0.063, 3.375 / 2)
    else:
        tags = build_shex_008_stage1_stent(m, z0)
    m.register("SHEX-008_stage1_stent", "ductile expandable alloy (DCN-10)", tags)

    # stage 2 stent (DCN-10)
    z0, z1 = MODULE_Z["stage2"]
    if state == "set":
        tags = annulus(z0, z1 - z0, 5.750 / 2 - 0.063, 5.750 / 2)
    else:
        tags = build_shex_009_stage2_stent(m, z0)
    m.register("SHEX-009_stage2_stent", "ductile expandable alloy (DCN-10)", tags)

    # stage 3 iris module — helix guide grooves phase-matched to the mandrel
    # drive ribs at run-in (ribs start Z=18.15 phase 0; insert bottom 21.75;
    # offset (21.75-18.15)/4.0*360 = 324 deg per DCN-9)
    z0, z1 = MODULE_Z["stage3_iris"]
    m.register("SHEX-010_support_sleeve", "17-4 PH H900", build_shex_010_support_sleeve(m, z0))
    m.register(
        "SHEX-002_helix_guide", "Inconel 718",
        build_shex_002_helix_guide(m, z0 + 3.250, phase_deg=324.0),
    )
    seg_tags: list[tuple[int, int]] = []
    if state == "set":
        seg_z = z0 + 2.375 - 2.750 / 2
        for i in range(16):
            seg_tags.extend(build_shex_001_iris_segment(m, seg_z, i * 22.5))
    else:
        # stowed segments ride the annulus between the mandrel drive ribs
        # (peak R 0.715) and the sleeve bore (R 0.781), below the insert
        seg_tags = nested_arcs(z0 + 0.40, 2.750, 0.720, 0.778, 16, 3.0)
    m.register("SHEX-001_iris_segment_x16", "17-4 PH H900", seg_tags)

    # seal lands x4 — at run-in petals nest just below the liner (axial offset
    # avoids radial overlap of the stowed bodies)
    for i in range(1, 5):
        z0, z1 = MODULE_Z[f"seal_land_{i}"]
        petal_z = z0 + 1.70
        liner_z = z0 + 2.25
        if state == "set":
            cup = annulus(z0 + 0.4, (z1 - z0) - 0.8, BORE_ID / 2, 8.720 / 2)
            petals: list[tuple[int, int]] = []
            for j in range(16):
                petals.extend(build_shex_005_petal_backup(m, petal_z, j * 22.5))
            carrier = annulus(z0, 0.4, BORE_ID / 2, RUN_OD / 2)
        else:
            cup = annulus(liner_z, 0.550, 0.781, 0.831)
            petals = nested_arcs(petal_z, 0.550, 0.781, 0.831, 16, 3.0)
            carrier = annulus(z0, z1 - z0, BORE_ID / 2, RUN_OD / 2)
            window = annulus(
                petal_z - 0.05, (liner_z + 0.550 + 0.05) - (petal_z - 0.05),
                0.781 - 0.004, RUN_OD / 2 + 0.01,
            )
            carrier = cut(carrier, window)
        m.register(f"SHEX-004_hnbr_liner_{i}", "HNBR 90A", cup)
        m.register(f"SHEX-005_petals_land{i}_x16", "17-4 PH H900", petals)
        m.register(f"seal_carrier_{i}", "17-4 PH H900", carrier)

    # upper MTM stack
    z0, z1 = MODULE_Z["upper_mtm"]
    if state == "set":
        tags = []
        for ring_i in range(3):
            zr = z0 + 0.05 + ring_i * 0.80
            for j in range(4):
                tags.extend(build_shex_003_mtm_segment(m, zr, j * 90.0 + ring_i * 30.0))
    else:
        tags = nested_arcs(z0 + 0.25, 2.0, BORE_ID / 2 + 0.002, RUN_OD / 2 - 0.002, 12, 4.0)
    m.register("SHEX-003_mtm_segments_x12", "17-4 PH H900", tags)

    # stage 1/2 internal actuator hardware (SHEX-014/015/016). The hardware is
    # mandrel-mounted, so it rides the mandrel group (dz). Bladders are shown
    # folded/spent in both end states; the inflated transient lives only in the
    # SHEX-ACT-S12_DEPLOYED sub-assembly. (Local import: avoids a circular
    # import, since actuator_solids imports from this module.)
    from cad import actuator_solids as _acs
    _acs.add_actuator_hardware(m, bladder_state="run_in", dz=dz)

    if state == "set":
        # casing context (reference body): covers tool envelope with margin
        top = MODULE_Z["fishing_neck"][1] + dz + 4.0
        m.register(
            "REF_casing_9625_40lb",
            "L80 casing (reference)",
            annulus(-4.0, top + 4.0, CASING_ID / 2, CASING_OD / 2),
        )
