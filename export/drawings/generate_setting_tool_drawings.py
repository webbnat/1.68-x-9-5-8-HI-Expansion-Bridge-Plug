#!/usr/bin/env python3
"""Individual setting-tool module drawings (ST-DWG-001 … ST-DWG-010)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from export.drawings.generate_drawings import (
    MM,
    OUT,
    _draw_dim_text,
    _draw_notes,
    _draw_centerline,
    _view_title,
    in_to_mm,
    new_drawing,
    save_dxf,
    title_block,
)

ST_OUT = OUT / "dxf" / "setting_tool"

MODULES = [
    ("ST-DWG-001", "ST-001", "BOTTOM CROSSOVER / AMMT", 10.0, 3.375, 1.375, "4140 HT", [
        "1.375 in AMMT PIN TO PLUG FISHING NECK",
        "O-RING BOSS 2.750 IN OD TYP",
        "FILL PORT 1/4 NPT (PRESSURE BALANCE FEED)",
    ], [
        "O-RINGS: Parker 2-015 Viton (qty 4)",
        "AMMT PIN: CUSTOM PER API 11BR CL 2",
    ]),
    ("ST-DWG-002", "ST-002", "RELEASE COLLET", 8.0, 3.375, 2.75, "17-4 PH H900", [
        "SHEAR PIN BORES 0.125 IN DIA x 8",
        "COLLET FINGERS x 6 @ 60 DEG",
        "RELEASE AT 55 klbf +/- 5%",
    ], [
        "SHEAR PINS: 17-4 PH 0.125 IN DIA (McMaster 90107A195 class)",
        "SPRINGS: Belleville 0.75 x 0.38 x 0.039 (custom stack)",
    ]),
    ("ST-DWG-003", "ST-003", "PRESSURE BALANCE", 14.0, 3.625, 2.875, "17-4 PH", [
        "COMPENSATION PISTON TRAVEL 0.75 IN",
        "20 ksi RATED ANNULUS ISOLATION",
        "SILICONE OIL FILL VOLUME 180 cm3",
    ], [
        "PISTON SEALS: Trelleborg Turcon Variseal (custom groove)",
        "FILL FLUID: Dow Corning 200 50 cSt",
    ]),
    ("ST-DWG-004", "ST-004", "STROKE ACTUATOR", 54.0, 3.625, 2.900, "17-4 PH H900", [
        "BALL SCREW LEAD 0.500 IN",
        "LINEAR TRAVEL 12.0 IN (11.6 IN USABLE)",
        "PUSH ROD OD 1.550 IN (PLUG MANDREL INTERFACE)",
        "OUTER SLEEVE + INNER MANDREL TELESCOPE",
    ], [
        "BALL SCREW: Thomson 6409KAA (custom length) OR Rollon Planetary screw",
        "LINEAR BEARINGS: Thomson 60 Case x 2",
        "WIPERS: Hallite 605 (custom OD)",
    ]),
    ("ST-DWG-005", "ST-005", "LOAD CELL SECTION", 10.0, 3.625, 2.875, "17-4 PH", [
        "TENSION/COMPRESSION IN LOAD PATH",
        "STRAIN GAUGE BRIDGE 350 ohm",
        "CALIBRATION SHIM GROOVE",
    ], [
        "LOAD CELL: Interface 1200 Standard (custom OD trim) OR HBM U10M miniature",
        "AMP: Vishay 2310 signal conditioner (in telemetry module)",
    ]),
    ("ST-DWG-006", "ST-006", "MOTOR / GEARBOX", 30.0, 3.625, 2.875, "17-4 PH / 718", [
        "BLDC MOTOR + 3-STAGE PLANETARY",
        "OUTPUT TORQUE 800 lbf-in @ 55 klbf stall",
        "MAG COUPLER OR DIRECT COUPLING TO SCREW",
    ], [
        "MOTOR: Maxon EC-i 40 (custom winding) + GP 42 planetary",
        "ALT PRODUCTION: Moog brushless slotless (oilfield qualified vendor)",
        "ENCODER: US Digital E5 2048 CPR",
    ]),
    ("ST-DWG-007", "ST-007", "BATTERY HOUSING", 84.0, 3.625, 3.375, "Ti / 17-4 PH", [
        "2x BATTERY MODULES IN SERIES",
        "NON-EXPLOSIVE Li-SOCl2 PRIMARY",
        "FUSE + REDUNDANT ISOLATION",
    ], [
        "CELLS: Saft LS14500 or Tadiran TL-5903 (D size, qty 48 typ)",
        "ALT OILFIELD: Ultralife UBBL08 (wireline pack — vendor qualified)",
        "HOUSING: CUSTOM Ti 6Al-4V per ST-DWG-007",
    ]),
    ("ST-DWG-008", "ST-008", "TELEMETRY CARTRIDGE", 22.0, 3.625, 3.125, "17-4 PH", [
        "MCU + FLASH + RS-485 WIRELINE MODEM",
        "SENSORS: LOAD, STROKE, P, T, BATTERY V",
        "CONNECTOR: Glenair 805 series (top pass-through)",
    ], [
        "MCU: TI MSP430FR5994 (lab) / Curtis-Wright Penny+Giles (production WL)",
        "FLASH: 128 MB industrial SD / SPI flash",
        "PRESSURE: Keller 10LHPX (0-20 ksi) or GE Druck TERPS",
        "TEMP: RTD PT100 Class A",
        "STROKE LVDT: Macro Sensors CD375 (custom length)",
    ]),
    ("ST-DWG-009", "ST-009", "CABLE HEAD / CCL", 14.0, 3.625, 2.875, "4140 HT", [
        "1.4375-20 UNEF ROPE SOCKET",
        "CCL MAGNET MANDREL (optional)",
        "TOP FISH 3.125 IN HEX",
    ], [
        "ROPE SOCKET: Custom per wireline cable size (7/16 in typical)",
        "CCL: Scout Downhole SDCCL-3625 or custom magnet stack",
    ]),
    ("ST-DWG-010", "ST-010", "INNER STROKE MANDREL", 11.6, 1.550, 0.0, "17-4 PH H900", [
        "PUSHES PLUG INNER MANDREL 1.550 IN OD",
        "TRAVELS INSIDE ST-004 STROKE MODULE",
        "HARD CHROME PLATE CONTACT ZONE",
    ], [
        "MATL: 17-4 PH H900, H1150M",
        "CHROME: 0.002 in min per AMS 2460",
    ]),
]


def draw_st_module(
    dwg_no: str,
    part_id: str,
    title: str,
    length_in: float,
    od_in: float,
    id_in: float,
    material: str,
    fab_notes: list[str],
    cots_notes: list[str],
) -> Path:
    doc = new_drawing(part_id)
    msp = doc.modelspace()
    title_block(doc, dwg_no, title)

    lx_s = 0.45 if length_in <= 30 else 0.12
    od_s = 0.35
    L = in_to_mm(length_in) * lx_s
    ro = in_to_mm(od_in) / 2 * od_s
    ri = in_to_mm(id_in) / 2 * od_s if id_in > 0 else ro * 0.35

    ox, oy = 40, 130
    _view_title(msp, "VIEW 1 — HALF-SECTION", ox, oy + ro + 22, f"SCALE L 1:{1/lx_s:.0f}")
    _draw_centerline(msp, ox - 5, ox + L + 5, oy)
    if id_in > 0:
        msp.add_lwpolyline([
            (ox, oy + ri), (ox + L, oy + ri), (ox + L, oy + ro), (ox, oy + ro), (ox, oy + ri),
        ], dxfattribs={"layer": "OUTLINE"})
    else:
        msp.add_lwpolyline([
            (ox, oy), (ox + L, oy), (ox + L, oy + ro), (ox, oy + ro), (ox, oy),
        ], dxfattribs={"layer": "OUTLINE"})
    _draw_dim_text(msp, f"L {in_to_mm(length_in):.1f} mm ({length_in:.1f} IN)", ox + L * 0.2, oy - 10)
    _draw_dim_text(msp, f"OD {in_to_mm(od_in):.1f} mm", ox + L + 4, oy + ro * 0.5, 2.4)
    if id_in > 0:
        _draw_dim_text(msp, f"ID {in_to_mm(id_in):.1f} mm", ox - 28, oy + ri, 2.4)

    _draw_notes(msp, [f"PART NO: {part_id}", f"MATL: {material}", "FABRICATION:"] + fab_notes, 40, 75)
    _draw_notes(msp, ["COTS / PURCHASED:"] + cots_notes, 200, 75)

    path = ST_OUT / f"{dwg_no}_{part_id}_{title.replace(' ', '_').replace('/', '_')[:30]}.dxf"
    save_dxf(doc, path)
    return path


def main() -> list[Path]:
    ST_OUT.mkdir(parents=True, exist_ok=True)
    paths = []
    for args in MODULES:
        p = draw_st_module(*args)
        paths.append(p)
        print(f"  ok {p.name}")
    return paths


if __name__ == "__main__":
    main()
