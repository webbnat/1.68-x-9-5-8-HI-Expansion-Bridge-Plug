#!/usr/bin/env python3
"""First-order pressure and expansion feasibility estimates (not FEA)."""

from __future__ import annotations

import math


def hoop_stress_psi(pressure_psi: float, id_in: float, wall_in: float) -> float:
    """Thin-wall hoop stress."""
    return pressure_psi * id_in / (2 * wall_in)


def seal_contact_area_sq_in(seal_od_in: float, seal_length_in: float, interference_in: float = 0.015) -> float:
    """Approximate cylindrical contact band."""
    effective_od = seal_od_in + interference_in
    return math.pi * effective_od * seal_length_in


def max_pressure_from_seal(
    seal_od_in: float,
    seal_length_in: float,
    allowable_contact_psi: float = 800,
) -> float:
    """
    Simplified seal pressure limit based on HNBR contact stress.
    Industry elastomer packers typically use 500-1200 psi contact stress limit.
    """
    area = seal_contact_area_sq_in(seal_od_in, seal_length_in)
    # Force balance: P * pi/4 * ID^2 ≈ contact_stress * area (simplified)
    effective_id = seal_od_in - 0.5
    piston_area = math.pi / 4 * effective_id**2
    return (allowable_contact_psi * area) / piston_area


def expansion_ratio(run_od_in: float, set_id_in: float) -> float:
    return set_id_in / run_od_in


def main() -> None:
    variants = [
        ("1.688\" primary", 1.688, 3.95, 1.75, 0.035),
        ("2.125\" alternate", 2.125, 3.95, 1.75, 0.040),
    ]
    set_id = 4.090

    print("=" * 60)
    print("SHEX-BP — Preliminary Pressure & Expansion Analysis")
    print("=" * 60)

    for name, run_od, seal_od, seal_len, wall in variants:
        ratio = expansion_ratio(run_od, set_id)
        p_seal = max_pressure_from_seal(seal_od, seal_len)
        stent_hoop = hoop_stress_psi(p_seal, run_od - 2 * wall, wall)
        print(f"\nVariant: {name}")
        print(f"  Run OD:              {run_od:.3f} in")
        print(f"  Set casing ID:       {set_id:.3f} in")
        print(f"  Expansion ratio:     {ratio:.2f}x diameter")
        print(f"  Est. max dP (seal):  {p_seal:.0f} psi")
        print(f"  Stent hoop @ max dP: {stent_hoop:.0f} psi")
        if p_seal >= 3000:
            print("  >> Meets 3000 psi target (preliminary)")
        else:
            print('  >> Below 3000 psi target; consider 2.125" OD or longer seal')

    print("\nNote: Full API 11D1 / ISO 14310 qualification requires FEA and physical testing.")


if __name__ == "__main__":
    main()
