#!/usr/bin/env python3
"""
Ultra-high expansion analysis: 1.688" run OD sealing in 9-5/8" 40# casing.
Max tool length 72" (6 ft).

9-5/8" 40# API casing:
  Nominal ID: 8.835"
  Drift ID:   8.679"
  Wall:       0.395"
"""

from __future__ import annotations

import math
from dataclasses import dataclass


RUN_OD = 1.688
SET_ID_NOM = 8.835
SET_ID_DRIFT = 8.679
SEAL_OD = 8.720
MAX_TOOL_IN = 72.0
EXPANSION_RATIO = SET_ID_DRIFT / RUN_OD  # ~5.14x diameter


@dataclass
class CascadeStage:
    name: str
    collapsed_od: float
    expanded_od: float
    axial_in: float


CASCADE = [
    CascadeStage("Stage 1 — inner stent", 1.688, 3.375, 4.0),
    CascadeStage("Stage 2 — middle stent", 3.375, 5.750, 5.0),
    CascadeStage("Stage 3 — outer stent/iris", 5.750, 8.650, 6.0),
]


def seal_dp(seal_length_in: float, elements: int = 1, contact_stress: float = 800) -> float:
    area = math.pi * SEAL_OD * seal_length_in * elements
    piston = math.pi / 4 * (SET_ID_DRIFT - 0.15) ** 2
    return (contact_stress * area) / piston


def mtm_dp(ring_count: int, ring_width_in: float, contact_stress: float = 2500) -> float:
    area = math.pi * (SET_ID_NOM - 0.02) * ring_width_in * ring_count
    piston = math.pi / 4 * (SET_ID_DRIFT - 0.15) ** 2
    return (contact_stress * area) / piston


def slip_dp(segments: int = 8, normal_klbf: float = 120.0, mu: float = 0.40, assemblies: int = 2) -> float:
    """Dual slip assemblies in large casing — higher normal force from long seal compression."""
    hold = mu * normal_klbf * assemblies
    piston = math.pi / 4 * (SET_ID_DRIFT - 0.15) ** 2
    return (hold * 1000) / piston


def stent_strut_stress(dp_psi: float, stage: CascadeStage, wall: float = 0.050) -> float:
    """Hoop stress in thinnest (outer) stage at deployed diameter."""
    id_ = stage.expanded_od - 2 * wall
    return dp_psi * id_ / (2 * wall)


def stage_feasible(stage: CascadeStage, max_ratio_per_stage: float = 2.2) -> bool:
    return (stage.expanded_od / stage.collapsed_od) <= max_ratio_per_stage


def length_budget() -> dict[str, float]:
    return {
        "fishing_neck / top sub": 3.0,
        "upper slip assembly": 4.5,
        "equalizing ports": 1.5,
        "MTM ring stack (upper)": 3.0,
        "seal stack (configurable)": 36.0,
        "MTM ring stack (lower)": 3.0,
        "3-stage expansion cascade": 15.0,
        "lower slip assembly": 4.5,
        "bottom sub": 2.0,
        "setting piston / mandrel tail": 2.5,
    }


def print_header() -> None:
    print("=" * 76)
    print("  SHEX-BP ULTRA-HIGH EXPANSION — 9-5/8\" 40# CASING")
    print("=" * 76)
    print(f"  Run OD:           {RUN_OD:.3f}\"")
    print(f"  Set casing:       9-5/8\" 40#  (nom ID {SET_ID_NOM:.3f}\", drift {SET_ID_DRIFT:.3f}\")")
    print(f"  Expansion ratio:  {EXPANSION_RATIO:.2f}x diameter  ({EXPANSION_RATIO:.1f}:1)")
    print(f"  Max tool length:  {MAX_TOOL_IN:.0f}\" ({MAX_TOOL_IN/12:.0f} ft)")
    print(f"  Radial travel:    {(SET_ID_DRIFT - RUN_OD)/2:.2f}\" per side")


def print_cascade() -> None:
    print(f"\n{'-' * 76}")
    print("  MULTI-STAGE EXPANSION CASCADE (required — single stent cannot do 5.14x)")
    print(f"{'-' * 76}")
    cumulative = 1.0
    for s in CASCADE:
        r = s.expanded_od / s.collapsed_od
        cumulative *= r
        ok = "OK" if stage_feasible(s) else "MARGINAL"
        print(
            f"  {s.name}:  {s.collapsed_od:.3f}\" -> {s.expanded_od:.3f}\"  "
            f"({r:.2f}x)  L={s.axial_in:.1f}\"  [{ok}]"
        )
    print(f"  Combined ratio: {cumulative:.2f}x  (target {EXPANSION_RATIO:.2f}x)")


def print_length_budget() -> None:
    print(f"\n{'-' * 76}")
    print("  72\" TOOL LENGTH BUDGET")
    print(f"{'-' * 76}")
    total = 0.0
    for name, ln in length_budget().items():
        total += ln
        print(f"  {name:<35} {ln:>5.1f}\"")
    print(f"  {'TOTAL':<35} {total:>5.1f}\"")


def print_seal_scenarios() -> None:
    print(f"\n{'-' * 76}")
    print("  SEAL / PRESSURE SCENARIOS (large bore — seal OD ~8.72\")")
    print(f"{'-' * 76}")
    print(f"\n  {'Configuration':<42} {'Seal len':>8} {'Est dP':>10} {'Limiter'}")
    print("  " + "-" * 72)

    configs = [
        ("Single 1.75\" land + petals", 1.75, 1, "elastomer"),
        ("12\" seal stack (3x4\")", 4.0, 3, "elastomer"),
        ("24\" seal stack (6x4\")", 4.0, 6, "elastomer"),
        ("36\" seal stack (9x4\") — full budget", 4.0, 9, "elastomer"),
        ("36\" + upper/lower MTM (6 rings)", 4.0, 9, "mtm"),
        ("MTM-primary: 12 rings + 6\" HNBR gas seal", 1.0, 6, "mtm_primary"),
        ("MTM-primary: 16 rings + 8\" HNBR", 1.0, 8, "mtm_primary"),
    ]

    for name, elem_len, count, mode in configs:
        total_seal = elem_len * count
        if mode == "elastomer":
            dp = seal_dp(elem_len, count) * 1.4  # petal factor in large ID
            lim = "elastomer contact"
        elif mode == "mtm":
            el = seal_dp(elem_len, count) * 1.2
            m = mtm_dp(6, 0.45)
            dp = min(el, m)
            lim = "MTM rings + elastomer"
        else:
            m = mtm_dp(12 if "12" in name else 16, 0.45, 3000)
            sl = slip_dp()
            dp = min(m, sl)
            lim = "MTM vs dual slips"
        print(f"  {name:<42} {total_seal:>6.1f}\" {dp:>9.0f} psi  {lim}")


def print_architecture() -> None:
    print(f"\n{'-' * 76}")
    print("  RECOMMENDED ARCHITECTURE — SHEX-BP-UHEX-9625")
    print(f"{'-' * 76}")
    print("""
  TOP (fishing neck)
    |
    |-- Upper slips (8 seg) ...................... anchor in 9-5/8" casing
    |-- Upper MTM ring stack (3 rings x 0.45")
    |
    |-- SEAL MODULE (~36")
    |     9 x 4" HNBR lands, each with 16-petal MTM backup
    |     (alternating set during staged compression)
    |
    |-- Lower MTM ring stack (3 rings)
    |
    |-- 3-STAGE EXPANSION CASCADE (~15")
    |     Stage 1: inner stent  1.69" -> 3.38"  (bladder actuated)
    |     Stage 2: middle stent 3.38" -> 5.75"  (mechanical wedge)
    |     Stage 3: outer iris   5.75" -> 8.65"  (petal/scissor + stent)
    |
    |-- Lower slips (8 seg)
    |-- Bottom equalizing sub
    |
  BOTTOM

  SETTING SEQUENCE (long-stroke ~24"):
    1. Locate at depth; equalize
    2. Stage 1 bladder expands inner stent to 3.38"
    3. Stage 2 wedge drives middle stent to 5.75"
    4. Stage 3 outer iris deploys to 8.65" OD scaffold
    5. Compress 36" seal stack (sequential lands)
    6. Set upper slips -> lower slips -> MTM rings
    7. Release setting tool

  RETRIEVAL: reverse cascade — pull collapses outer->middle->inner stent
""")


def print_limits() -> None:
    print(f"\n{'-' * 76}")
    print("  GOVERNING LIMITS & WHAT 6' LENGTH UNLOCKS")
    print(f"{'-' * 76}")

    dp_36_el = seal_dp(4.0, 9) * 1.4
    dp_mtm = mtm_dp(16, 0.45, 3000)
    dp_slip = slip_dp(8, 120, 0.40, 2)

    print(f"""
  EXPANSION (hardest problem):
    - 5.14x exceeds single-stent medical limit (~2.5-3x per stage)
    - 3-stage cascade is mandatory; similar to NeoWideRange (~5x) commercial tools
    - Stage 3 outer iris/petal is novel — highest engineering risk
    - Setting stroke ~24\" (Halliburton DPU-I-LS long-stroke class)

  PRESSURE (6' length helps enormously):
    - Large bore (8.7\") means huge piston area — need MORE seal length per psi
      OR MTM-primary architecture
    - 36\" elastomer stack:     ~{dp_36_el:.0f} psi (elastomer-limited)
    - 16-ring MTM-primary:      ~{dp_mtm:.0f} psi (metal contact-limited)
    - Dual slip anchor (2x8):   ~{dp_slip:.0f} psi (slip-limited, tunable with set force)

  WHAT IS ACHIEVABLE (preliminary):
    | Target dP  | Architecture                              | Tool use of 72\" |
    |------------|-------------------------------------------|-----------------|
    | 1500 psi   | 12\" seal + 3-stage cascade + dual slips  | ~45\"           |
    | 3000 psi   | 24\" seal + MTM petals + dual slips       | ~55\"           |
    | 5000 psi   | MTM-primary (16 rings) + 8\" HNBR V0 seal | ~60\"           |
    | 5000+ psi  | MTM-primary + FEA slips + 36\" seal backup| full 72\"       |

  COMPARED TO 4.5\" CASING:
    - 2.4x expansion -> 5.14x expansion (2.1x harder geometrically)
    - Seal OD 2.2x larger -> need ~2x seal length for same elastomer dP
    - 72\" budget vs ~18\" baseline — length is your main advantage
    - Dual slip assemblies strongly recommended (bi-directional loads)

  CRITICAL R&D ITEMS:
    1. Stage 3 outer iris mechanism (scissor/petal) — patent landscape similar to ISO-Flex
    2. Stent strut fatigue through 3 sequential plastic expansions
    3. Sequential setting controller (wireline depth correlation + force/stroke QA)
    4. Retrieval without hanging up in 36\" seal stack
    5. Centralization in 9-5/8\" open hole / washed-out ID
""")


def main() -> None:
    print_header()
    print_cascade()
    print_length_budget()
    print_seal_scenarios()
    print_architecture()
    print_limits()
    print("\nNote: Conceptual analysis only. 5x expansion requires prototype testing per stage.")


if __name__ == "__main__":
    main()
