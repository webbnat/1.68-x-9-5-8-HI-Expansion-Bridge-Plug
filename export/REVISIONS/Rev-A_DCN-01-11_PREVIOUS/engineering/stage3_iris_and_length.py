#!/usr/bin/env python3
"""
Stage 3 iris mechanism deep-dive + optimal tool length vs wireline/CT surface envelope.

References (public):
  - SLB ReSOLVE setting tool: ~21 ft length, 10.4-11.4 in stroke, 55-78 klbf
  - Halliburton DPU-I-LS: long-stroke electro-mechanical (TTEBP high-expansion class)
  - SLB Hi-Ex / Weatherford ISO-Flex: segmented-ring radial expansion (~80% ID expansion)
  - 30 CFR 250.620: lubricator must contain tool string under pressure
  - PROBUS/NXL lubricator sections: 4, 6, 8, 10 ft modular
"""

from __future__ import annotations

import math
from dataclasses import dataclass


# --- Casing target ---
RUN_OD = 1.688
STAGE3_IN_OD = 5.750
STAGE3_OUT_OD = 8.650
SET_DRIFT = 8.679


@dataclass
class SurfaceEnvelope:
    name: str
    setting_tool_ft: float
    setting_stroke_in: float
    max_setting_force_klbf: float
    lubricator_ft: float
    bop_stack_ft: float
    adapters_ft: float
    notes: str

    @property
    def max_total_string_ft(self) -> float:
        """Lubricator must exceed tool string; use 3 ft minimum margin."""
        return self.lubricator_ft - 3.0

    @property
    def max_plug_length_in(self) -> float:
        return max(0, (self.max_total_string_ft - self.setting_tool_ft - self.adapters_ft) * 12)


SURFACE_CONFIGS = [
    SurfaceEnvelope(
        "Wireline — standard platform",
        setting_tool_ft=21.2,
        setting_stroke_in=11.4,
        max_setting_force_klbf=55,
        lubricator_ft=35,
        bop_stack_ft=6,
        adapters_ft=1.5,
        notes="ReSOLVE-class; 2x10ft + 1x8ft lubricator typical",
    ),
    SurfaceEnvelope(
        "Wireline — extended onshore",
        setting_tool_ft=21.2,
        setting_stroke_in=11.4,
        max_setting_force_klbf=55,
        lubricator_ft=45,
        bop_stack_ft=6,
        adapters_ft=1.5,
        notes="3x10ft + 1x6ft lubricator sections",
    ),
    SurfaceEnvelope(
        "Wireline — DPU-I-LS long stroke",
        setting_tool_ft=22.0,
        setting_stroke_in=22.0,
        max_setting_force_klbf=60,
        lubricator_ft=45,
        bop_stack_ft=6,
        adapters_ft=1.5,
        notes="Halliburton TTEBP high-expansion class (stroke est. from product pairing)",
    ),
    SurfaceEnvelope(
        "Coiled tubing — standard CTU",
        setting_tool_ft=8.0,
        setting_stroke_in=999,
        max_setting_force_klbf=60,
        lubricator_ft=25,
        bop_stack_ft=8,
        adapters_ft=2.0,
        notes="Hydraulic setting via CT pump; stroke not tool-limited",
    ),
    SurfaceEnvelope(
        "Coiled tubing — extended lubricator",
        setting_tool_ft=8.0,
        setting_stroke_in=999,
        max_setting_force_klbf=60,
        lubricator_ft=40,
        bop_stack_ft=8,
        adapters_ft=2.0,
        notes="Extra riser sections or spacer bar deployment",
    ),
]


@dataclass
class IrisSegment:
    """One segment of sliding segmented-ring iris (Hi-Ex / ISO-Flex class)."""
    count: int
    thickness_in: float
    axial_length_in: float
    arc_deg: float
    inner_radius_in: float
    outer_radius_deployed_in: float


def stage3_iris_geometry() -> dict:
    """Stage 3: 5.75\" body expands to 8.65\" against 9-5/8\" 40# drift."""
    r_in = STAGE3_IN_OD / 2
    r_out = STAGE3_OUT_OD / 2
    radial_travel = r_out - r_in
    expansion_ratio = STAGE3_OUT_OD / STAGE3_IN_OD

    segments = 16
    arc = 360 / segments * 0.82  # overlap factor
    seg = IrisSegment(
        count=segments,
        thickness_in=0.125,
        axial_length_in=2.75,
        arc_deg=arc,
        inner_radius_in=r_in + 0.08,
        outer_radius_deployed_in=r_out - 0.015,
    )

    petal_tip_chord = math.sqrt(r_out**2 - r_in**2) * 2 * math.sin(math.radians(arc / 2))

    return {
        "expansion_ratio": expansion_ratio,
        "radial_travel_in": radial_travel,
        "segment_count": segments,
        "segment_thickness_in": seg.thickness_in,
        "segment_axial_in": seg.axial_length_in,
        "segment_arc_deg": arc,
        "tip_chord_in": petal_tip_chord,
        "module_length_in": 7.5,  # segments + actuator + guide rings
        "actuation_stroke_in": 4.0,
    }


def internal_stroke_budget(seal_length_in: float, seal_elements: int) -> dict:
    """Axial travel consumed inside plug during full set sequence."""
    return {
        "stage1_bladder_in": 5.0,
        "stage2_wedge_in": 5.0,
        "stage3_iris_in": stage3_iris_geometry()["actuation_stroke_in"],
        "seal_compression_in": seal_elements * 0.45,
        "slip_set_in": 1.5,
        "total_in": 5.0 + 5.0 + 4.0 + seal_elements * 0.45 + 1.5,
    }


def tool_length_options() -> list[dict]:
    """Candidate plug lengths with module breakdown."""
    return [
        {
            "name": "Minimum viable (48\")",
            "total_in": 48,
            "seal_in": 12,
            "seal_elements": 3,
            "mtm_rings": 8,
            "notes": "1500-2500 psi; tight wireline envelope",
        },
        {
            "name": "OPTIMAL — dual conveyance (54\")",
            "total_in": 54,
            "seal_in": 18,
            "seal_elements": 4,
            "mtm_rings": 12,
            "notes": "3000-5000 psi MTM-primary; fits standard WL + CT",
        },
        {
            "name": "Extended wireline (60\")",
            "total_in": 60,
            "seal_in": 24,
            "seal_elements": 6,
            "mtm_rings": 12,
            "notes": "5000 psi; needs 45ft lubricator",
        },
        {
            "name": "Maximum (72\")",
            "total_in": 72,
            "seal_in": 36,
            "seal_elements": 9,
            "mtm_rings": 16,
            "notes": "CT-preferred; marginal on standard WL",
        },
    ]


def print_iris_design() -> None:
    g = stage3_iris_geometry()
    print("=" * 76)
    print("  STAGE 3 IRIS — MECHANICAL DESIGN (SHEX-BP-UHEX)")
    print("=" * 76)
    print(f"""
  FUNCTION
    Expand scaffold from Stage 2 envelope ({STAGE3_IN_OD}\") to casing contact ({STAGE3_OUT_OD}\")
    prior to seal compression and slip set. This is the ONLY stage that touches 9-5/8\" wall.

  RECOMMENDED MECHANISM: 16-segment sliding ring iris
    (SLB Hi-Ex / Weatherford ISO-Flex segmented-ring class — NOT a literal camera iris)

  Why segmented ring vs alternatives:
    | Mechanism           | Pros                          | Cons @ 8.65\" OD        |
    |---------------------|-------------------------------|------------------------|
    | Segmented ring      | Proven HP; controlled recovery| Machining precision    |
    | Scissor iris        | High radial throw             | Bind risk; heavy       |
    | Simple petals       | Easy prototype                | Tip stress; gap at 5x  |
    | Balloon/stent only  | Simple                        | Cannot bridge 1.45\"     |

  GEOMETRY
    Stage 2 incoming OD:     {STAGE3_IN_OD:.3f}\"
    Stage 3 deployed OD:       {STAGE3_OUT_OD:.3f}\"  (0.029\" under {SET_DRIFT}\" drift)
    Radial travel per side:    {g['radial_travel_in']:.3f}\"
    Diameter expansion ratio:  {g['expansion_ratio']:.2f}x  (modest — this stage is feasible)

  SEGMENT DESIGN
    Segment count:             {g['segment_count']}  (22.5 deg arc each, 18% overlap)
    Segment thickness:         {g['segment_thickness_in']:.3f}\"  (17-4 PH H900)
    Segment axial length:      {g['segment_axial_in']:.2f}\"
    Tip chord (approx):        {g['tip_chord_in']:.2f}\"
    Module envelope:           {g['module_length_in']:.1f}\" axial

  ACTUATION (key design)
    Segments ride on double-start Acme helix guide slots on mandrel.
    Axial push ({g['actuation_stroke_in']:.1f}\") rotates segments 12-15 deg -> radial lockout.
    Final 0.5\" stroke: segment toes wedge against casing micro-ramps (metal preload).

    Sequence position in tool:
      Stage 1 bladder fires (internal, 5\" stroke) — no setting tool travel
      Stage 2 wedge fires (internal, 5\" stroke) — no setting tool travel
      Stage 3 iris: {g['actuation_stroke_in']:.1f}\" AXIAL from setting tool OR internal CT hydraulic
      Seal + slips: remaining setting-tool stroke

  RETRIEVAL
    Pull mandrel: helix reverses, segments nest inside {STAGE3_IN_OD}\" envelope.
    Segment toes feature breakaway ramp (2 deg) so pull force < 15 klbf to collapse.
    Outer stent (Stage 3 lattice) provides scaffold during retrieval until iris nested.

  MATERIALS
    Segments: 17-4 PH H900, electropolished contact face
    Helix guide: Inconel 718 (galling resistance)
    Optional casing-facing insert: tungsten carbide pad at toe (washout tolerance)
""")


def print_surface_envelope() -> None:
    print("=" * 76)
    print("  SURFACE ENVELOPE — WIRELINE / CT LUBRICATOR & SETTING TOOLS")
    print("=" * 76)
    print(f"\n  {'Configuration':<38} {'Lube':>6} {'Stroke':>8} {'Max plug':>10}")
    print("  " + "-" * 68)
    for c in SURFACE_CONFIGS:
        plug = c.max_plug_length_in
        stroke = "hydraulic" if c.setting_stroke_in > 100 else f'{c.setting_stroke_in:.1f}"'
        print(f"  {c.name:<38} {c.lubricator_ft:>5.0f}ft {stroke:>8} {plug:>8.0f}\"")
        print(f"    {c.notes}")

    print("""
  RULES OF THUMB (industry)
    - Lubricator length > entire tool string + 2-3 ft (30 CFR 250.620 offshore)
    - Standard lubricator sections: 4, 6, 8, 10 ft (stacked)
    - ReSOLVE / e-line setting tool alone: ~21 ft — dominates string length
    - CT: tool OD passes stripper; length limited by lubricator below injector (~25-40 ft)
    - BHA longer than riser: CT deployment/spacer bar hangs upper BHA at surface
""")


def print_stroke_analysis() -> None:
    print("=" * 76)
    print("  INTERNAL STROKE vs SETTING TOOL STROKE")
    print("=" * 76)
    for opt in tool_length_options():
        s = internal_stroke_budget(opt["seal_in"] / max(opt["seal_elements"], 1), opt["seal_elements"])
        print(f"\n  {opt['name']} ({opt['total_in']}\")")
        print(f"    Internal travel required: {s['total_in']:.1f}\"")
        print(f"    ReSOLVE stroke (11.4\"):   {'INSUFFICIENT — use internal actuators' if s['total_in'] > 11.4 else 'OK'}")
        print(f"    DPU-I-LS (~22\"):          {'MARGINAL' if s['total_in'] > 22 else 'OK with internal staging'}")


def print_optimal_recommendation() -> None:
    print("=" * 76)
    print("  OPTIMAL TOOL LENGTH RECOMMENDATION")
    print("=" * 76)
    print("""
  RECOMMENDED: 54 inches (4.5 ft) — plug body only

  MODULE BREAKDOWN (top to bottom):
    Fishing neck / top sub ..............  3.0\"
    Upper slips (8-seg, 9-5/8\") ........  4.5\"
    Upper MTM ring stack ................  2.5\"
    Seal module (MTM-primary) ........... 18.0\"  (4 x 4.5\" HNBR lands + 16 petals each)
    STAGE 3 IRIS MODULE .................  7.5\"  (16-segment sliding ring)
    Stage 2 middle stent/wedge ..........  5.0\"
    Stage 1 inner stent/bladder .........  4.0\"
    Lower slips .........................  4.5\"
    Bottom equalizing sub ...............  2.0\"
    Setting mandrel tail ................  3.0\"
    ----------------------------------------
    TOTAL ............................... 54.0\"

  TOTAL SURFACE STRING (wireline):
    ReSOLVE setting tool ...... 21.2 ft (254\")
    Crossovers / CCL ........... 1.5 ft ( 18\")
    Plug ....................... 4.5 ft ( 54\")
    ----------------------------------------
    TOTAL ...................... 27.2 ft  -> fits 35 ft lubricator with 8 ft margin

  WHY NOT 72\"?
    - 72\" plug + 21 ft setting tool = 33 ft -> only 2 ft margin in standard 35 ft lube
    - Offshore platform handling limit often ~30 ft rig-up height without special riser
    - 54\" with MTM-primary achieves same 3000-5000 psi as 72\" elastomer-heavy design
    - Retrieval friction scales with seal length — 36\" seal is high hang-up risk in 9-5/8\"

  WHY NOT 48\"?
    - Seal module shrinks to 12\" -> pressure margin thin for 5000 psi target
    - Stage modules compressed -> maintenance / FEA access harder

  CT CONVEYANCE:
    54\" plug + ~8 ft CT BHA = ~12.5 ft -> easily fits 25 ft lubricator
    CT preferred for SETTING (unlimited hydraulic stroke) if internal actuators fail
    Can run longer 60-66\" variant on CT if 5000+ psi qualification needed

  STROKE ARCHITECTURE (critical):
    Do NOT rely on setting-tool stroke for Stages 1-2.
    Use INTERNAL stored-energy actuators:
      Stage 1: bladder + burst disk (5\" travel)
      Stage 2: Belleville wedge stack (5\" travel)
      Stage 3 iris: partial setting-tool stroke (4\") OR CT hydraulic
      Seal/slips: remaining 6-7\" of ReSOLVE / DPU stroke

    This decouples 5x expansion from lubricator-length limits.
""")


def main() -> None:
    print_iris_design()
    print_surface_envelope()
    print_stroke_analysis()
    print_optimal_recommendation()


if __name__ == "__main__":
    main()
