"""SHEX-BP-UHEX-54 — Stage 1/2 internal actuator B-rep STEP geometry (Gmsh OCC).

The internal "first stroke" actuators that expand the plug 1.688 -> 5.750 in
radially BEFORE the setting tool applies its 10-in axial secondary stroke.
Sizing authority: export/analysis/actuator_design.py (+ .json).

Architecture (DCN-10 / DCN-11):
  DCN-10  Stent sleeves SHEX-008/009 re-specified from 17-4 PH H900 to a
          DUCTILE expandable alloy (annealed 316L or Ni alloy) so the laser-cut
          mesh can plastically hinge ~2x without cracking. H900 is too brittle.
  DCN-11  Stage-2 prime mover changed from a Belleville/swage wedge to a SECOND
          INFLATABLE BLADDER. A rigid cone/wedge starting <= stent ID 1.562
          cannot grow to back a 5.624 OD stent (geometrically impossible in the
          0.146-in annulus). The Belleville stack is retained ONLY as a
          hold-open / anti-recoil axial preload.
  DCN-12  First-stroke INITIATION + SEQUENCING re-architected (see
          export/analysis/FIRST_STROKE_TRIGGER.md, SHEX-EM-001). A passive
          hydrostatic-referenced burst disk fires during run-in (no position
          control), so it is replaced by: (a) energy from the well, (b) a
          position-correct COMMAND (CT applied differential + ball seat, or
          e-line EFI gate), (c) COMPLETION-gated sequencing where each stent's
          bottom-out pressure shifts an arming sleeve that uncovers the next
          stage's feed. New sub SHEX-017 houses the gate / ball seat / reference
          piston / arming sleeve / manifold; the EQ pilot (SHEX-016A) is
          interlocked to close SHEX-013 first.

Both stages: a reinforced HNBR bladder in the mandrel-neck annulus (Ø1.270)
is pressurised through a burst disk (wellbore hydrostatic or applied CT
pressure), inflates, and plastically deploys the laser-cut mesh stent. A
body-lock ratchet ring backs up each deployed stage; the Belleville stack
preloads the stack against recoil. An equalizing pilot piston closes the
SHEX-013 sub first.

Coordinates: plug Z (inches), bottom of plug = 0. STEP output mm. Bladders are
elastomer envelopes shown at run-in (folded) and deployed (inflated) volumes;
thread/seal forms not modelled (standard for STEP release).
"""

from __future__ import annotations

import math

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
    build_shex_008_stage1_stent,
    build_shex_009_stage2_stent,
)

# --- key dimensions (in) — from actuator_design.py -------------------------
NECK_OD = 1.270             # mandrel helix neck through stage 1/2 zones
STENT_ID = 1.562
STENT_OD = 1.688
STENT_WALL = 0.063
GLAND_OD = 1.550            # bladder end gland / swage ring OD
LOCK_OD = 1.500            # body-lock ratchet ring OD
BLADDER_RUN_OD = 1.462      # folded bladder OD at run-in
BLADDER_ID = 1.290          # bladder bore (over a thin neck liner)

# stage zones (plug Z)
S1_Z0, S1_Z1 = 9.5, 13.5
S2_Z0, S2_Z1 = 13.5, 18.5
S1_DEPLOY_OD = 3.375
S2_DEPLOY_OD = 5.750
S1_BLADDER_DEP_OD = S1_DEPLOY_OD - 2 * STENT_WALL   # 3.249
S2_BLADDER_DEP_OD = S2_DEPLOY_OD - 2 * STENT_WALL   # 5.624

CHARGE_SUB_OD = 0.500
PILOT_OD = 1.450

# sequence / initiation sub (SHEX-017, DCN-12)
SEQ_SUB_OD = 1.550
SEQ_BORE = 1.300
ARM_SLEEVE_OD = 1.290
ARM_SLEEVE_ID = 1.050

# Toggle the DCN-12 sequence sub. Set False to reconstruct the pre-DCN-12
# revision (Rev A) of the assembled tool; True (default) is the current Rev B.
INCLUDE_SEQ_SUB = True


# ---------------------------------------------------------------------------
# machined parts (datum z0 = bottom face)
# ---------------------------------------------------------------------------


def build_shex_014a_gland_ring(m: Model, z0: float = 0.0) -> list[tuple[int, int]]:
    """SHEX-014A bladder end gland / swage ring. OD 1.550 / ID 1.270 x 0.350.
    Internal crimp groove anchors the bladder end; used at both stage bladder
    ends (4 per plug)."""
    body = annulus(z0, 0.350, NECK_OD / 2, GLAND_OD / 2)
    # crimp groove on the OD face that the bladder lip swages into
    groove = annulus(z0 + 0.12, 0.110, GLAND_OD / 2 - 0.040, GLAND_OD / 2 + 0.05)
    return cut(body, groove)


def build_shex_014b_lock_ring(m: Model, z0: float = 0.0) -> list[tuple[int, int]]:
    """SHEX-014B body-lock ratchet ring. OD 1.500 / ID 1.270 x 0.400 with
    internal saw-tooth ratchet (one-way) that walks up the mandrel ratchet
    band and holds the deployed stage against recoil. (Also SHEX-015D.)"""
    body = annulus(z0, 0.400, NECK_OD / 2, LOCK_OD / 2)
    # 3 internal ratchet teeth (modelled as bore grooves)
    tools = []
    for i in range(3):
        zt = z0 + 0.07 + i * 0.11
        tools.append(annulus(zt, 0.045, NECK_OD / 2 - 0.001, NECK_OD / 2 + 0.028)[0])
    # axial expansion slot (split ring) — single radial gap
    o = gmsh.model.occ
    slot = o.addBox(mm(NECK_OD / 2 - 0.05), -mm(0.020), mm(z0 - 0.05),
                    mm(LOCK_OD), mm(0.040), mm(0.500))
    tools.append((3, slot))
    return cut(body, tools)


def build_shex_014c_charge_sub(m: Model, z0: float = 0.0) -> list[tuple[int, int]]:
    """SHEX-014C burst-disk charge sub (stage 1). OD 0.500 x 0.550 threaded
    plug; counterbore holds a COTS burst disk; cross-drilled to the bladder
    inflation passage. (SHEX-015E identical with a metering orifice.)"""
    body = cyl(z0, 0.550, CHARGE_SUB_OD / 2)
    tools = [
        cyl(z0 - 0.05, 0.25, 0.300 / 2),                 # disk counterbore
        cyl(z0 + 0.30, 0.30, 0.125 / 2),                 # inflation passage
    ]
    # hex socket for makeup
    o = gmsh.model.occ
    hexp = o.addCylinder(0, 0, mm(z0 + 0.45), 0, 0, mm(0.12), mm(0.110))
    tools.append((3, hexp))
    return cut([body], tools)


def build_shex_015b_belleville(m: Model, z0: float = 0.0) -> list[tuple[int, int]]:
    """SHEX-015B Belleville hold washer (disc spring). OD 1.540 / ID 1.290,
    coned 0.100 free height, 0.050 stock. HOLD/anti-recoil preload only
    (DCN-11). Stacked in series; qty set by preload requirement."""
    cone_h = 0.100
    t = 0.050
    big = conez(z0, cone_h, GLAND_OD / 2 - 0.01, STENT_ID / 2 - 0.04)
    small = conez(z0 + t, cone_h, GLAND_OD / 2 - 0.01, STENT_ID / 2 - 0.04)
    bore = cyl(z0 - 0.05, cone_h + t + 0.1, BLADDER_ID / 2)
    return cut([big], [small, bore])


def build_shex_015c_belleville_housing(m: Model, z0: float = 0.0) -> list[tuple[int, int]]:
    """SHEX-015C Belleville housing / preload retainer sleeve.
    OD 1.550 / ID 1.290 x 1.200, internal counterbore Ø1.460 x 0.95 holds the
    disc-spring stack; shoulder reacts the preload."""
    body = annulus(z0, 1.200, BLADDER_ID / 2, GLAND_OD / 2)
    bore = annulus(z0 + 0.20, 0.95, BLADDER_ID / 2 - 0.01, 1.460 / 2)
    return cut(body, bore)


def build_shex_016_charge_chamber(m: Model, z0: float = 0.0) -> list[tuple[int, int]]:
    """SHEX-016 charge / atmospheric-reference chamber sleeve.
    OD 1.550 / ID 1.300 x 2.000, 2 radial pilot ports, end shoulder seals the
    reference volume that arms the burst-disk differential."""
    body = annulus(z0, 2.000, 1.300 / 2, GLAND_OD / 2)
    o = gmsh.model.occ
    tools = []
    for ang in (0.0, 180.0):
        a = math.radians(ang)
        c = o.addCylinder(0, 0, mm(z0 + 1.0),
                          math.cos(a) * mm(1.0), math.sin(a) * mm(1.0), 0,
                          mm(0.062 / 2))
        tools.append((3, c))
    return cut(body, tools)


def build_shex_016a_pilot_piston(m: Model, z0: float = 0.0) -> list[tuple[int, int]]:
    """SHEX-016A equalizing pilot piston. OD 1.450 seal land x 0.30; stem
    Ø1.000 x 0.70; nose Ø0.700 x 0.30 that shifts the SHEX-013S sleeve closed
    first (lowest cracking pressure). 2 OD O-ring grooves."""
    parts = [
        cyl(z0, 0.30, PILOT_OD / 2),
        cyl(z0 + 0.30, 0.70, 1.000 / 2),
        cyl(z0 + 1.00, 0.30, 0.700 / 2),
    ]
    body = fuse(parts)
    grooves = [
        annulus(z0 + 0.07, 0.080, PILOT_OD / 2 - 0.05, PILOT_OD / 2 + 0.01)[0],
        annulus(z0 + 0.19, 0.080, PILOT_OD / 2 - 0.05, PILOT_OD / 2 + 0.01)[0],
    ]
    return cut(body, grooves)


# ---------------------------------------------------------------------------
# sequence / initiation sub (SHEX-017, DCN-12)
# ---------------------------------------------------------------------------


def build_shex_017_sequence_sub(m: Model, z0: float = 0.0) -> list[tuple[int, int]]:
    """SHEX-017 sequence / initiation sub HOUSING. OD 1.550 / bore 1.300 x 1.50.
    Common gate for both conveyances: a top EFI/pilot port (e-line igniter or CT
    pilot pressure), a reference-piston bore with two seal-groove lands, and the
    radial FEED MANIFOLD that routes to the stage-1 and stage-2 bladder lines.
    DCN-12 replaces the passive hydrostatic burst disk (no position control)."""
    o = gmsh.model.occ
    body = annulus(z0, 1.50, SEQ_BORE / 2, SEQ_SUB_OD / 2)
    tools = [
        cyl(z0 + 1.50 - 0.32, 0.37, 0.200 / 2),          # EFI / pilot port counterbore
    ]
    # two radial manifold feed ports (to stage-1 and stage-2 lines)
    for zc, ang in ((z0 + 0.55, 0.0), (z0 + 0.95, 180.0)):
        a = math.radians(ang)
        c = o.addCylinder(0, 0, mm(zc), math.cos(a) * mm(1.0), math.sin(a) * mm(1.0),
                          0, mm(0.094 / 2))
        tools.append((3, c))
    # metering orifice (small radial, 90 deg off the feeds)
    mo = o.addCylinder(0, 0, mm(z0 + 0.75), 0, mm(1.0), 0, mm(0.040 / 2))
    tools.append((3, mo))
    # reference-piston seal-groove lands in the bore
    tools.append(annulus(z0 + 0.20, 0.080, SEQ_BORE / 2 - 0.01, SEQ_BORE / 2 + 0.045)[0])
    tools.append(annulus(z0 + 0.35, 0.080, SEQ_BORE / 2 - 0.01, SEQ_BORE / 2 + 0.045)[0])
    return cut([body] if isinstance(body, tuple) else body, tools)


def build_shex_017a_arming_sleeve(m: Model, z0: float = 0.0) -> list[tuple[int, int]]:
    """SHEX-017A stage1->2 arming sleeve (shuttle). OD 1.290 / ID 1.050 x 0.60,
    held by a calibrated shear pin. When stage 1 bottoms out the pressure climb
    shears the pin and shifts this sleeve to UNCOVER the stage-2 feed port —
    completion-gated sequencing (DCN-12), not a pressure/time threshold."""
    o = gmsh.model.occ
    body = annulus(z0, 0.60, ARM_SLEEVE_ID / 2, ARM_SLEEVE_OD / 2)
    tools = []
    fp = o.addCylinder(0, 0, mm(z0 + 0.32), mm(1.0), 0, 0, mm(0.094 / 2))   # feed port
    tools.append((3, fp))
    sp = o.addCylinder(0, 0, mm(z0 + 0.10), 0, mm(1.0), 0, mm(0.093 / 2))   # shear pin
    tools.append((3, sp))
    return cut(body, tools)


def build_shex_017b_reference_piston(m: Model, z0: float = 0.0) -> list[tuple[int, int]]:
    """SHEX-017B reference / ball-seat piston. Seal land OD 1.290 x 0.30 + stem
    Ø1.000 x 0.60; central Ø0.50 flow bore with a tapered ball seat. On CT it
    responds to the APPLIED differential (CT bore vs annulus), so depth/
    hydrostatic cancel and it cannot trip during run-in; a dropped ball lands on
    the seat to positively arm the gate. 2 OD O-ring grooves."""
    o = gmsh.model.occ
    body = fuse([cyl(z0, 0.30, ARM_SLEEVE_OD / 2), cyl(z0 + 0.30, 0.60, 1.000 / 2)])
    tools = [cyl(z0 - 0.05, 1.05, 0.500 / 2)]                       # flow bore
    seat = o.addCone(0, 0, mm(z0 + 0.16), 0, 0, mm(0.13), mm(0.90 / 2), mm(0.50 / 2))
    tools.append((3, seat))                                        # tapered ball seat
    tools.append(annulus(z0 + 0.07, 0.060, ARM_SLEEVE_OD / 2 - 0.05, ARM_SLEEVE_OD / 2 + 0.01)[0])
    tools.append(annulus(z0 + 0.18, 0.060, ARM_SLEEVE_OD / 2 - 0.05, ARM_SLEEVE_OD / 2 + 0.01)[0])
    return cut(body, tools)


# ---------------------------------------------------------------------------
# elastomer bladder envelopes (run-in folded vs deployed inflated)
# ---------------------------------------------------------------------------


def build_bladder(z0: float, length: float, deployed_od: float,
                  state: str) -> list[tuple[int, int]]:
    """Reinforced HNBR bladder envelope. state 'run_in' (folded ~Ø1.462) or
    'deployed' (inflated to just under the stent ID)."""
    od = deployed_od if state == "deployed" else BLADDER_RUN_OD
    wall = 0.060 if state == "run_in" else max(0.045, (od - BLADDER_ID) / 2 * 0.08)
    return annulus(z0, length, BLADDER_ID / 2, od / 2)


# ---------------------------------------------------------------------------
# reference bodies (mandrel neck stub + stent representations)
# ---------------------------------------------------------------------------


def _ref_mandrel_stub(m: Model) -> None:
    """Mandrel neck reference over the stage 1/2 region (Z 8.5-19.5):
    Ø1.270 neck with short blends to Ø1.550 body at the ends; a ratchet band
    for the lock rings is implied (shown plain)."""
    parts = [
        cyl(8.5, 0.4, 1.550 / 2),
        conez(8.9, 0.15, 1.550 / 2, NECK_OD / 2),
        cyl(9.05, 10.30, NECK_OD / 2),               # neck 9.05-19.35
        conez(19.35, 0.15, NECK_OD / 2, 1.550 / 2),
        cyl(19.50, 0.40, 1.550 / 2),
    ]
    m.register("REF_mandrel_neck", "ductile mandrel (ref)", fuse(parts))


def _stent(z0: float, z1: float, od: float, state: str,
           builder) -> list[tuple[int, int]]:
    """Run-in: the real laser-cut sleeve. Deployed: expanded thin annulus
    (wall thins as the mesh stretches)."""
    if state == "run_in":
        return builder(None, z0)
    wall = 0.045
    return annulus(z0, z1 - z0, od / 2 - wall, od / 2)


# ---------------------------------------------------------------------------
# stage 1/2 actuator assembly
# ---------------------------------------------------------------------------


def add_actuator_hardware(m: Model, bladder_state: str, dz: float = 0.0) -> None:
    """Register the SHEX-014/015/016 actuator hardware (no stents, no mandrel
    reference). All parts are mandrel-mounted, so pass dz = mandrel stroke to
    shift them with the mandrel group (e.g. dz = SET_STROKE in the set state).
    bladder_state: 'run_in' (folded) or 'deployed' (inflated)."""
    def reg(name: str, mat: str, tags: list[tuple[int, int]]) -> None:
        if dz:
            gmsh.model.occ.translate(tags, 0, 0, mm(dz))
        m.register(name, mat, tags)

    # stage 1 bladder actuator (SHEX-014)
    reg("SHEX-014_stage1_bladder", "HNBR + ply",
        build_bladder(S1_Z0 + 0.45, 3.10, S1_BLADDER_DEP_OD, bladder_state))
    reg("SHEX-014A_gland_lower", "17-4 PH H1075",
        build_shex_014a_gland_ring(m, S1_Z0 + 0.05))
    reg("SHEX-014A_gland_upper", "17-4 PH H1075",
        build_shex_014a_gland_ring(m, S1_Z1 - 0.40))
    reg("SHEX-014B_lock_ring_s1", "17-4 PH H1075",
        build_shex_014b_lock_ring(m, S1_Z0 - 0.30))
    reg("SHEX-014C_charge_sub_s1", "4140 HT + burst disk",
        build_shex_014c_charge_sub(m, S1_Z0 - 0.95))

    # stage 2 bladder actuator + hold (SHEX-015)
    reg("SHEX-015_stage2_bladder", "HNBR + ply",
        build_bladder(S2_Z0 + 0.45, 4.10, S2_BLADDER_DEP_OD, bladder_state))
    reg("SHEX-015A_gland_lower", "17-4 PH H1075",
        build_shex_014a_gland_ring(m, S2_Z0 + 0.05))
    reg("SHEX-015A_gland_upper", "17-4 PH H1075",
        build_shex_014a_gland_ring(m, S2_Z1 - 0.40))
    for i in range(4):
        reg(f"SHEX-015B_belleville_{i+1}", "Inconel 718",
            build_shex_015b_belleville(m, S2_Z1 + 0.05 + i * 0.055))
    reg("SHEX-015C_belleville_housing", "4140 HT",
        build_shex_015c_belleville_housing(m, S2_Z1 + 0.35))
    reg("SHEX-015D_lock_ring_s2", "17-4 PH H1075",
        build_shex_014b_lock_ring(m, S2_Z0 - 0.30))
    reg("SHEX-015E_charge_sub_s2", "4140 HT + burst disk + orifice",
        build_shex_014c_charge_sub(m, S2_Z0 - 0.55))

    # shared charge / trigger module (SHEX-016)
    reg("SHEX-016_charge_chamber", "4140 HT",
        build_shex_016_charge_chamber(m, S1_Z0 - 3.10))
    reg("SHEX-016A_pilot_piston", "17-4 PH H1075",
        build_shex_016a_pilot_piston(m, S1_Z0 - 1.60))

    # sequence / initiation sub (SHEX-017, DCN-12) — gate + reference piston sit
    # below the charge module; the stage1->2 arming sleeve sits at the stage-2
    # feed so its shift uncovers the stage-2 line on stage-1 completion.
    if INCLUDE_SEQ_SUB:
        reg("SHEX-017_sequence_sub", "4140 HT",
            build_shex_017_sequence_sub(m, S1_Z0 - 4.85))
        reg("SHEX-017B_reference_piston", "17-4 PH H1075",
            build_shex_017b_reference_piston(m, S1_Z0 - 4.75))
        reg("SHEX-017A_arming_sleeve", "17-4 PH H1075",
            build_shex_017a_arming_sleeve(m, S2_Z0 - 0.95))


def build_actuator_assembly(m: Model, state: str) -> None:
    """state: 'run_in' (collapsed, bladders folded) or 'deployed'
    (stage 1 -> 3.375, stage 2 -> 5.750, bladders inflated)."""
    _ref_mandrel_stub(m)

    # --- stents (run-in real mesh, or deployed expanded annulus) -----------
    m.register("SHEX-008_stage1_stent", "ductile alloy (DCN-10)",
               _stent(S1_Z0, S1_Z1, S1_DEPLOY_OD, state, build_shex_008_stage1_stent))
    m.register("SHEX-009_stage2_stent", "ductile alloy (DCN-10)",
               _stent(S2_Z0, S2_Z1, S2_DEPLOY_OD, state, build_shex_009_stage2_stent))

    bstate = "deployed" if state in ("deployed", "set") else "run_in"
    add_actuator_hardware(m, bstate, dz=0.0)
