"""SHEX-AK-20 setting adapter kit — B-rep STEP geometry (Gmsh OCC).

Adapter kit mating the SHEX-BP-UHEX-54 plug to a Baker E-4 No. 20 wireline
pressure setting assembly, a Baker Model J-20 coiled-tubing hydraulic
setting tool, or any #20-class clone (Model B / BST / Owen / Fury style)
that carries the standard #20 bottom interface. The Model J uses the same
adapter kits as the E-4 (Baker Hughes product literature), so one kit
serves both conveyances.

Working principle (relative motion only): the kit SLEEVE threads onto the
tool's moving crosslink sleeve and lands on the plug's upper slip carrier
face at plug Z=51; the kit ROD threads onto the tool's fixed setting
mandrel and holds the plug fishing neck through the calibrated SHEAR STUD.
Tool stroke drives the sleeve down 10.0 in relative to the rod -> the plug
outer stack displaces -10.0 relative to the plug mandrel = SET (DCN-8).
At 45 klbf the stud parts at its neck and the string pulls free (DCN-7
GS-profile head remains for re-latch / retrieval).

Coordinates: plug Z (inches), bottom of plug = 0. STEP output mm.
Interface thread callouts modelled at nominal major/minor diameter —
thread forms are not modelled (standard practice for STEP release).

ST-DCN-1  Kit sized to DCN-7 plug top: shoe OD 1.900 / ID 1.470 passes
          over the O1.450 neck body and bears on the carrier face annulus
          O1.562-1.688 at Z=51.
ST-DCN-2  Shear stud neck O0.640 x 0.30 -> 45 klbf +/-5% in 4140 HT
          (125-145 ksi UTS lot-calibrated; proof batch required).
ST-DCN-3  Tool-side threads assumed: crosslink sleeve box 3.250-8 UN,
          setting mandrel 1.500-12 UNF box. VERIFY against the specific
          tool make before cutting (clone vendors vary).
"""

from __future__ import annotations

import gmsh

from cad.release_solids import (
    Model,
    annulus,
    conez,
    cut,
    cyl,
    fuse,
    mm,
    session,
)

# --- key interface dimensions (in) ----------------------------------------
SHOE_OD = 1.900
SHOE_ID = 1.470
SLEEVE_TOP_OD = 3.750
SLEEVE_BOX_ID = 3.250      # 3.250-8 UN 2B box (ST-DCN-3) shown at major
ROD_OD = 1.250
ROD_TOP_PIN_OD = 1.500     # 1.500-12 UNF-2A shown at major
STUD_BODY_OD = 1.000       # 1.000-8 UN ends shown at body
STUD_PIN_OD = 0.870        # modelled at ~thread minor so it nests in tap bores
STUD_NECK_OD = 0.640       # ST-DCN-2 -> 45 klbf
KIT_STROKE = 10.0          # DCN-8 net set stroke (tool capability 10.777)

# rigged-state Z stations (plug coordinates)
Z_SHOE_FOOT = 51.0         # carrier face (DCN-7)
Z_SLEEVE_TOP = 66.0
Z_STUD_BOT = 56.0          # stud pin enters neck top box (plug 56-57)
Z_ROD_BOT = 58.15
Z_ROD_TOP = 73.25


# ---------------------------------------------------------------------------
# kit parts (each built at its own datum z0 = bottom face unless noted)
# ---------------------------------------------------------------------------


def build_st101_setting_sleeve(m: Model, z0: float = 0.0) -> list[tuple[int, int]]:
    """ST-101 setting sleeve / shoe. L 15.000.
    Foot OD 1.900 / ID 1.470 tube x 11.0; cone to O3.750; box top.
    z0 = foot (bottom) face."""
    parts = [
        cyl(z0 + 0.0, 11.0, SHOE_OD / 2),
        conez(z0 + 11.0, 1.5, SHOE_OD / 2, SLEEVE_TOP_OD / 2),
        cyl(z0 + 12.5, 2.5, SLEEVE_TOP_OD / 2),
    ]
    body = fuse(parts)
    tools = [
        cyl(z0 - 0.1, 11.6, SHOE_ID / 2),                       # shoe bore
        conez(z0 + 11.5, 1.5, SHOE_ID / 2, SLEEVE_BOX_ID / 2),  # transition bore
        cyl(z0 + 13.0, 2.0 + 0.1, SLEEVE_BOX_ID / 2),           # 3.250-8 UN box zone
    ]
    return cut(body, tools)


def build_st102_tension_rod(m: Model, z0: float = 0.0) -> list[tuple[int, int]]:
    """ST-102 tension rod. L 15.100. O1.250 body; bottom box 1.000-8 UN
    (tap bore O0.875 x 1.05); top pin 1.500-12 UNF x 1.25 (upset head).
    z0 = bottom face."""
    parts = [
        cyl(z0 + 0.0, 13.85, ROD_OD / 2),
        cyl(z0 + 13.85, 1.25, ROD_TOP_PIN_OD / 2),
    ]
    body = fuse(parts)
    tools = [cyl(z0 - 0.1, 1.05 + 0.1, 0.875 / 2)]   # bottom box tap bore
    return cut(body, tools)


def build_st103_shear_stud(m: Model, z0: float = 0.0) -> list[tuple[int, int]]:
    """ST-103 calibrated shear stud. L 3.200.
    Pin x 1.0 each end (O0.870 at minor), O1.000 bodies, shear neck
    O0.640 x 0.30 at centre (ST-DCN-2: 45 klbf +/-5%). z0 = bottom face."""
    parts = [
        cyl(z0 + 0.0, 1.0, STUD_PIN_OD / 2),
        cyl(z0 + 1.0, 0.45, STUD_BODY_OD / 2),
        conez(z0 + 1.45, 0.05, STUD_BODY_OD / 2, STUD_NECK_OD / 2),
        cyl(z0 + 1.50, 0.20, STUD_NECK_OD / 2),
        conez(z0 + 1.70, 0.05, STUD_NECK_OD / 2, STUD_BODY_OD / 2),
        cyl(z0 + 1.75, 0.45, STUD_BODY_OD / 2),
        cyl(z0 + 2.20, 1.0, STUD_PIN_OD / 2),
    ]
    return fuse(parts)


def build_st104_spacer(m: Model, z0: float = 0.0) -> list[tuple[int, int]]:
    """ST-104 stroke spacer ring OD 1.900 / ID 1.480 x 0.250 (kit of 2,
    fit between sleeve box face and tool sleeve to tune stud preload)."""
    return annulus(z0, 0.250, 1.480 / 2, SHOE_OD / 2)


# ---------------------------------------------------------------------------
# reference bodies (tool lower end + plug top) for the interface assembly
# ---------------------------------------------------------------------------


def _ref_tool_lower(m: Model) -> None:
    """Generic #20-class tool lower end: crosslink sleeve (moving, mates the
    kit sleeve box) + fixed setting mandrel socket (mates the rod pin)."""
    # crosslink sleeve: pin 3.250 x 2.0 into kit box, body O3.800 above
    pin = cyl(64.0, 2.0, SLEEVE_BOX_ID / 2)
    body = cyl(66.0, 8.0, 3.800 / 2)
    sleeve = fuse([pin, body])
    # hollow it so the rod / setting mandrel pass through
    sleeve = cut(sleeve, [cyl(63.9, 10.2, 2.600 / 2)])
    m.register("REF_tool_crosslink_sleeve", "reference (tool vendor)", sleeve)
    # fixed setting mandrel: socket over the rod top pin
    sock = cut([cyl(Z_ROD_TOP - 1.30, 3.55, 2.400 / 2)],
               [cyl(Z_ROD_TOP - 1.35, 1.30, ROD_TOP_PIN_OD / 2 + 0.005),
                cyl(Z_ROD_TOP - 0.05, 1.0, 0.700 / 2)])
    m.register("REF_tool_setting_mandrel", "reference (tool vendor)", sock)


def _ref_plug_top(m: Model) -> None:
    """Plug top reference: mandrel stub (Z 44-50.5 + DCN-7 pin), upper slip
    carrier, and the Rev E fishing neck."""
    from cad import release_solids as rs

    # mandrel stub with DCN-7 top joint
    parts = [
        cyl(44.0, 0.75, 1.550 / 2),
        cyl(44.75, 0.50, 1.558 / 2),
        cyl(45.25, 3.0, 1.550 / 2),
        conez(48.25, 1.50, 1.550 / 2, 1.620 / 2),
        conez(49.75, 0.25, 1.620 / 2, 1.550 / 2),
        cyl(50.0, 0.5, 1.550 / 2),
        cyl(50.5, 1.0, 1.375 / 2),
        cyl(51.5, 0.5, 1.300 / 2),
    ]
    m.register("REF_plug_mandrel_stub", "17-4 PH H900 (ref)", fuse(parts))
    m.register("REF_upper_slip_carrier", "17-4 PH H900 (ref)",
               annulus(46.5, 4.5, 1.562 / 2, 1.688 / 2))
    m.register("SHEX-012_fishing_neck_RevE", "4140 HT",
               rs.build_shex_012_fishing_neck(m, 50.5))


# ---------------------------------------------------------------------------
# interface assembly
# ---------------------------------------------------------------------------


def build_kit_assembly(m: Model, state: str) -> None:
    """state: 'rigged' (stud made up, stroke 0) or 'released'
    (post-set pull-off: stud sheared, string lifted +2.0)."""
    dz = 2.0 if state == "released" else 0.0

    def shift(tags: list[tuple[int, int]]) -> list[tuple[int, int]]:
        if dz:
            gmsh.model.occ.translate(tags, 0, 0, mm(dz))
        return tags

    _ref_plug_top(m)

    # kit
    m.register("ST-101_setting_sleeve", "4140 HT (AMS 6415)",
               shift(build_st101_setting_sleeve(m, Z_SHOE_FOOT)))
    m.register("ST-102_tension_rod", "4140 HT (AMS 6415)",
               shift(build_st102_tension_rod(m, Z_ROD_BOT)))
    if state == "rigged":
        m.register("ST-103_shear_stud", "4140 HT calibrated",
                   build_st103_shear_stud(m, Z_STUD_BOT))
    else:
        # stud parted at the neck centre (Z 57.6): bottom half stays in the
        # plug neck box, top half leaves with the rod
        bot = [
            cyl(Z_STUD_BOT + 0.0, 1.0, STUD_PIN_OD / 2),
            cyl(Z_STUD_BOT + 1.0, 0.45, STUD_BODY_OD / 2),
            conez(Z_STUD_BOT + 1.45, 0.05, STUD_BODY_OD / 2, STUD_NECK_OD / 2),
            cyl(Z_STUD_BOT + 1.50, 0.10, STUD_NECK_OD / 2),
        ]
        m.register("ST-103_shear_stud_lower", "4140 HT calibrated", fuse(bot))
        top = [
            cyl(Z_STUD_BOT + 1.60, 0.10, STUD_NECK_OD / 2),
            conez(Z_STUD_BOT + 1.70, 0.05, STUD_NECK_OD / 2, STUD_BODY_OD / 2),
            cyl(Z_STUD_BOT + 1.75, 0.45, STUD_BODY_OD / 2),
            cyl(Z_STUD_BOT + 2.20, 1.0, STUD_PIN_OD / 2),
        ]
        m.register("ST-103_shear_stud_upper", "4140 HT calibrated",
                   shift(fuse(top)))

    _shift_refs = state == "released"
    # tool reference bodies move with the string on pull-off
    before = len(m.bodies)
    _ref_tool_lower(m)
    if _shift_refs:
        for body in m.bodies[before:]:
            gmsh.model.occ.translate(body.dimtags, 0, 0, mm(dz))
