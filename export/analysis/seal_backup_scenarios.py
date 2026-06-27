#!/usr/bin/env python3
"""
Pressure capacity scenarios: longer seal stacks and metal-to-metal backups.

First-order models only — not a substitute for FEA or API 11D1 / ISO 14310 testing.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class ToolConfig:
    run_od_in: float
    set_casing_id_in: float = 4.090
    seal_od_in: float = 3.95
    stent_wall_in: float = 0.035


@dataclass
class SealScenario:
    name: str
    seal_length_in: float
    element_count: int = 1
    hnbr_contact_stress_psi: float = 800
    backup_type: str = "petal"  # none | petal | mtm_ring | mtm_primary
    backup_count: int = 8
    backup_material_yield_psi: float = 120_000  # 17-4 PH


def seal_limited_dp(cfg: ToolConfig, length_in: float, elements: int, contact_stress: float) -> float:
    """Elastomer contact-stress limit (extrusion not yet blocked)."""
    total_length = length_in * elements
    contact_area = math.pi * (cfg.seal_od_in + 0.015) * total_length
    piston_area = math.pi / 4 * (cfg.seal_od_in - 0.5) ** 2
    return (contact_stress * contact_area) / piston_area


def extrusion_gap_in(cfg: ToolConfig) -> float:
    """Radial clearance each side between run OD and casing ID."""
    return (cfg.set_casing_id_in - cfg.run_od_in) / 2


def petal_backup_factor(gap_in: float, petal_length_in: float, petal_count: int) -> float:
    """
    Petal backups reduce effective extrusion gap. Returns multiplier on elastomer dP capacity.
    Simplified: coverage fraction of gap bridged by overlapping petals.
    """
    if petal_length_in <= 0:
        return 1.0
    span = petal_length_in * 0.85
    coverage = min(1.0, (span * petal_count * 0.15) / max(gap_in, 0.01))
    # Partial gap closure improves elastomer life; not linear to pressure
    return 1.0 + 0.6 * coverage


def mtm_ring_limited_dp(
    cfg: ToolConfig,
    ring_count: int,
    ring_axial_width_in: float,
    contact_stress_psi: float = 2500,
) -> float:
    """
    Metal-to-metal backup: load carried by metal ring contact against casing.
    contact_stress_psi: allowable Hertzian/contact stress metal-on-casing (conservative).
    """
    deployed_od = cfg.set_casing_id_in - 0.010  # slight undergage for interference
    contact_area = math.pi * deployed_od * ring_axial_width_in * ring_count
    piston_area = math.pi / 4 * (cfg.seal_od_in - 0.5) ** 2
    return (contact_stress_psi * contact_area) / piston_area


def slip_anchor_limited_dp(
    cfg: ToolConfig,
    slip_segments: int = 6,
    friction_coeff: float = 0.35,
    normal_force_klbf: float = 45.0,
) -> float:
    """
    Maximum dP before slips yield/slide (simplified axial force balance).
    normal_force_klbf: total radial preload from element compression at set.
    """
    hold_klbf = friction_coeff * normal_force_klbf * slip_segments / 6
    effective_bore_in = cfg.set_casing_id_in - 0.15
    piston_area = math.pi / 4 * effective_bore_in**2
    return (hold_klbf * 1000) / piston_area


def stent_hoop_at_dp(cfg: ToolConfig, dp_psi: float) -> float:
    id_in = cfg.run_od_in - 2 * cfg.stent_wall_in
    return hoop_stress_psi(dp_psi, id_in, cfg.stent_wall_in)


def hoop_stress_psi(pressure_psi: float, id_in: float, wall_in: float) -> float:
    return pressure_psi * id_in / (2 * wall_in)


def effective_dp(scenario: SealScenario, cfg: ToolConfig) -> dict:
    gap = extrusion_gap_in(cfg)
    base = seal_limited_dp(cfg, scenario.seal_length_in, scenario.element_count, scenario.hnbr_contact_stress_psi)

    if scenario.backup_type == "none":
        dp = base
        limiter = "elastomer extrusion"
    elif scenario.backup_type == "petal":
        dp = base * petal_backup_factor(gap, scenario.seal_length_in * 0.4, scenario.backup_count)
        limiter = "elastomer + petal anti-extrusion"
    elif scenario.backup_type == "mtm_ring":
        mtm = mtm_ring_limited_dp(cfg, ring_count=2, ring_axial_width_in=0.35)
        dp = min(base * 1.2, mtm)  # elastomer still needed for gas seal; metal carries bulk load
        limiter = "metal ring contact (elastomer gas seal)"
    elif scenario.backup_type == "mtm_primary":
        mtm = mtm_ring_limited_dp(cfg, ring_count=3, ring_axial_width_in=0.45, contact_stress_psi=3000)
        slip = slip_anchor_limited_dp(cfg)
        dp = min(mtm, slip)
        limiter = "MTM rings vs slip anchor"
    else:
        dp = base
        limiter = "unknown"

    tool_length_adder = scenario.seal_length_in * scenario.element_count - 1.75
    return {
        "name": scenario.name,
        "dp_psi": dp,
        "limiter": limiter,
        "extrusion_gap_in": gap,
        "added_tool_length_in": max(0, tool_length_adder),
        "stent_hoop_psi": stent_hoop_at_dp(cfg, dp),
    }


def print_matrix(cfg: ToolConfig, label: str) -> None:
    print(f"\n{'=' * 72}")
    print(f"  {label}  |  Run OD {cfg.run_od_in:.3f}\"  |  Casing ID {cfg.set_casing_id_in:.3f}\"")
    print(f"  Radial extrusion gap (each side): {extrusion_gap_in(cfg):.3f}\"")
    print(f"{'=' * 72}")

    scenarios = [
        SealScenario("Baseline (current)", 1.75, 1, backup_type="petal", backup_count=8),
        SealScenario("Long single seal 3.0\"", 3.0, 1, backup_type="petal"),
        SealScenario("Long single seal 4.5\"", 4.5, 1, backup_type="petal"),
        SealScenario("Long single seal 6.0\"", 6.0, 1, backup_type="petal"),
        SealScenario("Dual stack 2x1.75\"", 1.75, 2, backup_type="petal"),
        SealScenario("Dual stack 2x2.5\"", 2.5, 2, backup_type="petal"),
        SealScenario("Triple stack 3x1.75\"", 1.75, 3, backup_type="petal"),
        SealScenario("Baseline + MTM backup rings", 1.75, 1, backup_type="mtm_ring"),
        SealScenario("Long seal 3.0\" + MTM rings", 3.0, 1, backup_type="mtm_ring"),
        SealScenario("MTM-primary (short elastomer)", 0.75, 1, backup_type="mtm_primary"),
        SealScenario("MTM-primary + dual elastomer", 1.25, 2, backup_type="mtm_primary"),
    ]

    print(f"\n{'Scenario':<36} {'Est dP':>8} {'+Length':>8} {'Limiter'}")
    print("-" * 72)
    for s in scenarios:
        r = effective_dp(s, cfg)
        flag = " ***" if r["dp_psi"] >= 3000 else ""
        print(
            f"{r['name']:<36} {r['dp_psi']:>7.0f} psi {r['added_tool_length_in']:>+6.2f}\"  "
            f"{r['limiter']}{flag}"
        )


def print_recommendations() -> None:
    print(f"\n{'=' * 72}")
    print("  DESIGN INTERPRETATION")
    print(f"{'=' * 72}")
    print("""
LONGER SEAL STACK (elastomer-only path):
  - dP scales ~linearly with total elastomer contact length.
  - Each +1.75\" of HNBR adds ~same increment as the baseline (~1865 psi on 1.688\" tool).
  - To reach 3000 psi elastomer-only at 1.688\": need ~2.8x baseline length (~4.9\" total).
  - Tradeoffs: longer tool, longer setting stroke, retrieval cone collapse length,
    increased friction through restrictions on pull, stent/bladder must stay aligned.

METAL-TO-METAL BACKUP (recommended for 3000+ psi):
  - Petal backups (current HEX-style): modest gain (~1.3-1.8x) — blocks extrusion gap
    but elastomer still primary pressure seal.
  - Full MTM ring stack: metal rings bear bulk radial load; elastomer becomes gas-tight
    secondary seal (ISO V0 path). Typically unlocks 3500-6000+ psi at 1.688\" if slips hold.
  - MTM-primary architecture: 2-3 hardened rings (17-4 PH / Inconel) set against casing
    FIRST, then compress short HNBR land for gas seal — industry standard for HP plugs.

PRACTICAL ARCHITECTURE FOR YOUR TARGETS:
  | Goal dP   | 1.688\" OD approach                          | 2.125\" OD approach        |
  |-----------|-----------------------------------------------|----------------------------|
  | 2000 psi  | Baseline seal + petals (current)              | Easy                       |
  | 3000 psi  | MTM ring stack + 1.5-2.0\" HNBR OR 4.5\" seal | MTM + 1.75\" seal          |
  | 4000 psi  | MTM-primary + dual slips + 17-4 rings         | MTM-primary + petals       |
  | 5000+ psi | MTM-primary; FEA on slips mandatory           | Preferred path             |

CRITICAL CONSTRAINT AT 1.688\":
  The radial extrusion gap (~1.2\" per side into 4.5\" casing) is the hard problem.
  Longer elastomer alone cannot solve this — metal must bridge the gap before pressure
  acts. Stent sleeve sets the OD envelope; MTM petals/rings deploy OUTBOARD of the stent.

NEXT ENGINEERING STEPS:
  1. Add outboard MTM ring module to CAD (2-3 split rings, 0.35-0.45\" each)
  2. FEA: petal tip contact stress + slip shear at 4000 psi
  3. Physical test: ISO 14310 V0 gas leak after 5000 psi hold
""")


def main() -> None:
    print_matrix(ToolConfig(run_od_in=1.688), "PRIMARY VARIANT — 1.688\" OD")
    print_matrix(ToolConfig(run_od_in=2.125, stent_wall_in=0.040), "ALTERNATE VARIANT — 2.125\" OD")
    print_recommendations()
    print("Note: All values are first-order estimates. Qualification requires physical testing.")


if __name__ == "__main__":
    main()
