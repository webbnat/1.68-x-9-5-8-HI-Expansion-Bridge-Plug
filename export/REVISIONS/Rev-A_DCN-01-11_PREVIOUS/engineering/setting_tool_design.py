#!/usr/bin/env python3
"""
SHEX-ST-54 setting tool design analysis.

Custom long-stroke electro-mechanical tool for 54" UHEX plug.
Sized to fit standard 35 ft wireline lubricator with 54" plug (27.2 ft total string).
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class PlugStrokeDemand:
    stage3_iris_in: float = 4.0
    seal_compression_in: float = 5.5  # 4 lands x ~1.4" effective
    slip_set_in: float = 1.5
    release_overtravel_in: float = 0.5
    # Stages 1-2 internal — NOT on setting tool


@dataclass
class SettingToolSpec:
    name: str = "SHEX-ST-54"
    od_in: float = 3.625
    total_length_ft: float = 20.5
    stroke_in: float = 12.0
    max_force_klbf: float = 55
    max_temp_f: float = 350
    pressure_rating_psi: float = 20_000
    top_connection: str = "1.4375-20 UNEF rope socket / cable head"
    bottom_connection: str = "1.375 AMMT to plug fishing neck"
    power: str = "Li-ion battery pack, non-explosive"
    sensors: list[str] = None

    def __post_init__(self):
        if self.sensors is None:
            self.sensors = [
                "axial load (klbf)",
                "linear displacement (in)",
                "downhole pressure (psi)",
                "downhole temperature (F)",
                "battery voltage",
            ]


def module_breakdown() -> list[dict]:
    """Top to bottom module stack."""
    return [
        {"name": "Cable head / CCL sub", "length_in": 12.0, "od_in": 3.625, "function": "Wireline connection + CCL"},
        {"name": "Telemetry & memory", "length_in": 24.0, "od_in": 3.625, "function": "QA recording, real-time surface readout (optional)"},
        {"name": "Battery pack (2x module)", "length_in": 84.0, "od_in": 3.625, "function": "Power for motor; rig-safe non-explosive"},
        {"name": "Motor / gearbox", "length_in": 28.0, "od_in": 3.625, "function": "High-torque low-speed linear drive"},
        {"name": "Load cell section", "length_in": 8.0, "od_in": 3.625, "function": "Axial force measurement"},
        {"name": "Stroke actuator (ball screw)", "length_in": 54.0, "od_in": 3.625, "function": "11.6\" linear travel, 55 klbf push"},
        {"name": "Pressure balance / compensation", "length_in": 10.0, "od_in": 3.625, "function": "Hydrostatic compensation, 20 ksi rating"},
        {"name": "Release collet", "length_in": 6.0, "od_in": 3.375, "function": "Shear-pin release at set force + overtravel"},
        {"name": "Bottom crossover (AMMT)", "length_in": 8.0, "od_in": 3.375, "function": "Interface to plug fishing neck"},
    ]


def stroke_budget() -> dict:
    d = PlugStrokeDemand()
    tool = SettingToolSpec()
    required = d.stage3_iris_in + d.seal_compression_in + d.slip_set_in + d.release_overtravel_in
    return {
        "stage3_iris": d.stage3_iris_in,
        "seal_compression": d.seal_compression_in,
        "slip_set": d.slip_set_in,
        "overtravel": d.release_overtravel_in,
        "total_required_in": required,
        "tool_stroke_in": tool.stroke_in,
        "margin_in": tool.stroke_in - required,
        "stages_1_2_internal": "5\" + 5\" bladder/Belleville — not on setting tool",
    }


def force_budget() -> dict:
    """Force allocation during set sequence."""
    return {
        "stage3_iris_deploy": {"force_klbf": 12, "stroke_in": 4.0, "note": "Overcome friction + radial deployment"},
        "seal_land_1": {"force_klbf": 8, "stroke_in": 1.5, "note": "First HNBR land"},
        "seal_land_2": {"force_klbf": 10, "stroke_in": 1.5, "note": "Increasing resistance"},
        "seal_land_3": {"force_klbf": 12, "stroke_in": 1.5, "note": "MTM ring preload begins"},
        "seal_land_4": {"force_klbf": 15, "stroke_in": 1.5, "note": "Final seal + upper MTM"},
        "slip_set": {"force_klbf": 18, "stroke_in": 1.5, "note": "Dual slip wedge"},
        "peak_total": {"force_klbf": 55, "stroke_in": 11.5, "note": "Peak at final slip set"},
    }


def ct_adapter_option() -> dict:
    return {
        "name": "SHEX-ST-54-CT",
        "description": "CT hydraulic setting adapter — replaces motor/battery with CT string pressure",
        "length_ft": 8.0,
        "od_in": 2.875,
        "stroke_in": "unlimited (CT pump)",
        "force_klbf": 60,
        "bottom_connection": "1.375 AMMT",
        "use_when": "Wireline stroke insufficient or re-set required",
    }


def print_design() -> None:
    tool = SettingToolSpec()
    stroke = stroke_budget()
    forces = force_budget()

    print("=" * 76)
    print("  SHEX-ST-54 SETTING TOOL DESIGN")
    print("=" * 76)
    print(f"""
  OVERVIEW
    Companion setting tool for 54\" SHEX-BP-UHEX-54 plug (9-5/8\" 40#)
    Non-explosive electro-mechanical (Halliburton DPU / SLB ReSOLVE class)

  KEY DIMENSIONS
    Tool OD:              {tool.od_in}\"
    Total length:         {tool.total_length_ft} ft ({tool.total_length_ft * 12:.0f}\")
    Linear stroke:        {tool.stroke_in}\"
    Max setting force:    {tool.max_force_klbf} klbf
    Pressure rating:      {tool.pressure_rating_psi:,} psi
    Temperature:          {tool.max_temp_f} F
    Top connection:       {tool.top_connection}
    Bottom connection:    {tool.bottom_connection}

  SURFACE STRING (with 54\" plug)
    Setting tool:         {tool.total_length_ft * 12:.0f}\"
    Plug:                  54\"
    Adapters:              18\"
    TOTAL:                {tool.total_length_ft * 12 + 54 + 18:.0f}\" ({(tool.total_length_ft * 12 + 54 + 18)/12:.1f} ft)
    Standard 35 ft lube:  {(35*12) - (tool.total_length_ft * 12 + 54 + 18):.0f}\" margin
""")

    print("  MODULE STACK (top to bottom)")
    print(f"  {'Module':<32} {'Length':>8} {'OD':>6}")
    print("  " + "-" * 50)
    total = 0
    for m in module_breakdown():
        total += m["length_in"]
        print(f"  {m['name']:<32} {m['length_in']:>6.1f}\" {m['od_in']:>5.3f}\"")
    print(f"  {'TOTAL':<32} {total:>6.1f}\"")
    print()

    print("  STROKE BUDGET")
    for k, v in stroke.items():
        print(f"    {k}: {v}")
    print()

    print("  FORCE PROFILE (sequential set)")
    peak = 0
    cum_stroke = 0
    for step, data in forces.items():
        if step == "peak_total":
            continue
        cum_stroke += data["stroke_in"]
        peak = max(peak, data["force_klbf"])
        print(f"    {step:<16} {data['force_klbf']:>3} klbf  {data['stroke_in']:>4.1f}\"  {data['note']}")
    print(f"    Peak force: {forces['peak_total']['force_klbf']} klbf at {forces['peak_total']['stroke_in']}\" cumulative")
    print()

    print("  SETTING SEQUENCE (tool <-> plug interaction)")
    print("""
    1. RUN IN: Tool latched to plug fishing neck (1.375\" AMMT). Stages 1-2 armed, not fired.
    2. AT DEPTH: Confirm internal Stage 1 bladder charged (pressure sensor on plug mandrel).
    3. T-0:   Tool holds tension; internal Stage 1 fires -> 1.69\" to 3.38\" (no tool stroke).
    4. T+30s: Internal Stage 2 Belleville fires -> 3.38\" to 5.75\" (no tool stroke).
    5. T+60s: Tool advances 4.0\" @ 12 klbf -> Stage 3 iris deploys to 8.65\".
    6. T+90s: Tool advances 6.0\" @ ramp 8-15 klbf -> compress 4 seal lands sequentially.
    7. T+120s: Final 1.5\" @ 18 klbf -> set dual slips + MTM ring preload.
    8. T+130s: Release collet shears at 55 klbf + 0.5\" overtravel; tool free to pull.
    9. QA: Surface download force/stroke curve; compare to golden signature.

    RELEASE MECHANISM
      Shear pin collet rated 55 klbf +/- 5%.
      Alternative: hydraulic release for CT variant (SHEX-ST-54-CT).
""")

    ct = ct_adapter_option()
    print("  CT HYDRAULIC VARIANT")
    for k, v in ct.items():
        print(f"    {k}: {v}")


def main() -> None:
    print_design()


if __name__ == "__main__":
    main()
