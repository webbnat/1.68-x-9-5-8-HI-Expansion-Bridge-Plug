"""Stage 1/2 actuator (SHEX-014/015/016) — dimensioned shop drawings (DXF+PDF).

Reuses the Sheet scaffolding from generate_release_drawings.py.
Authority: cad/actuator_solids.py + export/analysis/actuator_design.py
(DCN-10 ductile stent, DCN-11 second bladder / Belleville hold-only).

Run:  .venv\\Scripts\\python export/drawings/generate_actuator_drawings.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from generate_release_drawings import (  # noqa: E402
    OUT_DXF,
    OUT_PDF,
    Sheet,
    turned_half_section,
)


def dwg_014a_gland() -> Path:
    sh = Sheet("ACT-DWG-014A", "BLADDER END GLAND / SWAGE RING", "SHEX-014A",
               "17-4 PH H1075", "4/PLUG")
    s = 4.6
    x0, y0 = 3.0, 6.0
    prof = [(0, 0.775), (0.35, 0.775)]
    bore = [(0, 0.635), (0.35, 0.635)]
    turned_half_section(sh, prof, bore, x0, y0, s)
    sh.label("VIEW A — HALF SECTION  SCALE 4.6:1", 2.0, 9.0)
    sh.hdim((x0, y0 + 0.775 * s), (x0 + 0.35 * s, y0 + 0.775 * s), y0 + 2.2, s,
            text="0.350 +/-.005")
    sh.vdim((x0 + 0.18 * s, y0 - 0.775 * s), (x0 + 0.18 * s, y0 + 0.775 * s),
            x0 - 1.0, s, text="OD 1.550 / ID 1.270")
    sh.leader("OD CRIMP GROOVE 0.110 W x 0.040 DEEP —\nBLADDER LIP SWAGES IN (RETAINS + SEALS END)",
              (x0 + 0.18 * s, y0 + 0.74 * s), (x0 + 4.2, y0 + 2.6))
    sh.leader("BORE 1.270 SLIP FIT OVER MANDREL NECK",
              (x0 + 0.30 * s, y0 + 0.635 * s), (x0 + 3.6, y0 - 2.2))
    sh.notes([
        "USED AT BOTH ENDS OF STAGE-1 AND STAGE-2 BLADDERS (4/PLUG).",
        "BORE CONCENTRIC TO OD 0.002 FIM; FACES SQUARE 0.002 FIM.",
        "DEBURR + LIGHT POLISH BLADDER CONTACT FACE (NO ELASTOMER NICKS).",
    ], 1.0, 3.6)
    return sh.save("ACT-DWG-014A_gland_ring")


def dwg_014b_lock() -> Path:
    sh = Sheet("ACT-DWG-014B", "BODY-LOCK RATCHET RING (STAGE 1/2)",
               "SHEX-014B / 015D", "17-4 PH H1075", "2/PLUG")
    s = 4.2
    x0, y0 = 3.0, 6.0
    prof = [(0, 0.750), (0.40, 0.750)]
    bore = [(0, 0.635), (0.40, 0.635)]
    turned_half_section(sh, prof, bore, x0, y0, s)
    sh.label("VIEW A — HALF SECTION  SCALE 4.2:1", 2.0, 9.0)
    sh.hdim((x0, y0 + 0.750 * s), (x0 + 0.40 * s, y0 + 0.750 * s), y0 + 2.2, s,
            text="0.400 +/-.005")
    sh.vdim((x0 + 0.20 * s, y0 - 0.750 * s), (x0 + 0.20 * s, y0 + 0.750 * s),
            x0 - 1.0, s, text="OD 1.500 / ID 1.270 (FREE)")
    sh.leader("3x INTERNAL SAW-TOOTH RATCHET 0.028 DEEP @ 0.110 PITCH —\n"
              "ONE-WAY: WALKS UP MANDREL RATCHET BAND, HOLDS DEPLOYED STAGE",
              (x0 + 0.20 * s, y0 + 0.66 * s), (x0 + 4.4, y0 + 2.8))
    sh.leader("0.040 AXIAL SPLIT (C-RING) — RADIAL\nCOLLAPSE/EXPAND OVER THE BAND",
              (x0 + 0.40 * s, y0 - 0.69 * s), (x0 + 4.2, y0 - 2.4))
    sh.notes([
        "ANTI-RECOIL: HOLDS THE PLASTICALLY-EXPANDED MESH STENT OPEN AFTER",
        "  BLADDER PRESSURE BLEEDS OFF (NOT A LOAD-BEARING SEAL).",
        "TEETH HARDER THAN MANDREL BAND; STRESS-RELIEVE AFTER EDM.",
        "RETRIEVAL: RING RELEASES WHEN STAGE COLLAPSES ON PULL (OPEN ITEM).",
    ], 1.0, 3.6)
    return sh.save("ACT-DWG-014B_lock_ring")


def dwg_014c_charge() -> Path:
    sh = Sheet("ACT-DWG-014C", "BURST-DISK CHARGE SUB", "SHEX-014C / 015E",
               "4140 HT + COTS BURST DISK", "2/PLUG")
    s = 7.0
    x0, y0 = 3.0, 6.0
    prof = [(0, 0.250), (0.55, 0.250)]
    bore = [(0, 0.150), (0.25, 0.150), (0.25, 0.0625), (0.55, 0.0625)]
    turned_half_section(sh, prof, bore, x0, y0, s)
    sh.label("VIEW A — HALF SECTION  SCALE 7:1", 2.0, 9.2)
    sh.hdim((x0, y0 + 0.250 * s), (x0 + 0.55 * s, y0 + 0.250 * s), y0 + 1.8, s,
            text="0.550 +/-.005")
    sh.vdim((x0 + 0.40 * s, y0 - 0.250 * s), (x0 + 0.40 * s, y0 + 0.250 * s),
            x0 - 1.0, s, text="OD 0.500")
    sh.leader("DISK COUNTERBORE 0.300 x 0.250 —\nCOTS BURST DISK (CRACK p1 STAGE 1, p2 STAGE 2)",
              (x0 + 0.10 * s, y0 + 0.150 * s), (x0 + 3.6, y0 + 2.8))
    sh.leader("INFLATION PASSAGE 0.125 -> BLADDER ANNULUS\n(STAGE 2: ADD METERING ORIFICE FOR ~30 s DELAY)",
              (x0 + 0.45 * s, y0 + 0.0625 * s), (x0 + 4.4, y0 - 2.4))
    sh.notes([
        "CRACK PRESSURE SELECTED VS WELL HYDROSTATIC WINDOW (SEE ANALYSIS).",
        "  STAGE 1 p1 < STAGE 2 p2 SO STAGES FIRE IN ORDER.",
        "THREADS INTO MANDREL CHARGE PORT; HEX SOCKET 0.110 AF MAKEUP.",
        "DESIGN BLADDER RATING 2500 PSI; BURST DISK RATED ACCORDINGLY.",
    ], 1.0, 3.6)
    return sh.save("ACT-DWG-014C_charge_sub")


def dwg_015_belleville() -> Path:
    sh = Sheet("ACT-DWG-015", "BELLEVILLE HOLD WASHER + HOUSING",
               "SHEX-015B / 015C", "INC 718 / 4140 HT", "4 + 1/PLUG")
    # washer view
    s = 5.0
    x0, y0 = 3.0, 6.4
    prof = [(0, 0.770), (0.10, 0.645)]
    bore = [(0, 0.720), (0.10, 0.645)]
    turned_half_section(sh, prof, bore, x0, y0, s)
    sh.label("VIEW A — SHEX-015B DISC SPRING  SCALE 5:1", 1.8, 9.2)
    sh.vdim((x0 + 0.05 * s, y0 - 0.770 * s), (x0 + 0.05 * s, y0 + 0.770 * s),
            x0 - 1.0, s, text="OD 1.540 / ID 1.290")
    sh.leader("FREE HEIGHT 0.100, STOCK 0.050 — CONED DISC SPRING",
              (x0 + 0.06 * s, y0 + 0.70 * s), (x0 + 3.6, y0 + 2.8))
    sh.leader("DCN-11: HOLD / ANTI-RECOIL PRELOAD ONLY\n(NOT A RADIAL DRIVER) — STACK 4 IN SERIES",
              (x0 + 0.05 * s, y0 - 0.70 * s), (x0 + 3.6, y0 - 2.6))
    # housing view
    xs, ys = 11.4, 6.4
    ss = 3.6
    prof2 = [(0, 0.775), (1.20, 0.775)]
    bore2 = [(0, 0.645), (0.20, 0.645), (0.20, 0.730), (1.15, 0.730), (1.15, 0.645),
             (1.20, 0.645)]
    turned_half_section(sh, prof2, bore2, xs, ys, ss)
    sh.label("VIEW B — SHEX-015C HOUSING  SCALE 3.6:1", 10.2, 9.0)
    sh.hdim((xs, ys + 0.775 * ss), (xs + 1.20 * ss, ys + 0.775 * ss), ys + 2.2, ss,
            text="1.200")
    sh.vdim((xs + 0.6 * ss, ys - 0.775 * ss), (xs + 0.6 * ss, ys + 0.775 * ss),
            xs - 0.8, ss, text="OD 1.550 / ID 1.290")
    sh.leader("COUNTERBORE 1.460 x 0.95 HOLDS STACK;\nSHOULDER REACTS PRELOAD",
              (xs + 0.7 * ss, ys + 0.730 * ss), (xs + 2.2, ys + 2.6))
    sh.notes([
        "STACK 4x SHEX-015B IN SERIES -> ~200-300 LBF PRELOAD OVER ~0.2 IN.",
        "INC 718 FOR RELAXATION RESISTANCE AT TEMPERATURE.",
        "PRELOAD SET AT ASSEMBLY VIA SHIM UNDER HOUSING SHOULDER.",
    ], 1.0, 3.4)
    return sh.save("ACT-DWG-015_belleville")


def dwg_016_chamber() -> Path:
    sh = Sheet("ACT-DWG-016", "CHARGE CHAMBER + EQ PILOT PISTON",
               "SHEX-016 / 016A", "4140 HT / 17-4 PH H1075", "1 + 1/PLUG")
    # chamber view
    s = 3.6
    x0, y0 = 3.0, 6.4
    prof = [(0, 0.775), (2.00, 0.775)]
    bore = [(0, 0.650), (2.00, 0.650)]
    turned_half_section(sh, prof, bore, x0, y0, s)
    sh.label("VIEW A — SHEX-016 CHAMBER SLEEVE  SCALE 3.6:1", 1.8, 9.2)
    sh.hdim((x0, y0 + 0.775 * s), (x0 + 2.00 * s, y0 + 0.775 * s), y0 + 2.2, s,
            text="2.000")
    sh.vdim((x0 + 1.0 * s, y0 - 0.775 * s), (x0 + 1.0 * s, y0 + 0.775 * s),
            x0 - 0.9, s, text="OD 1.550 / ID 1.300")
    sh.leader("2x RADIAL PILOT PORT 0.062 — ARMS THE\nBURST-DISK DIFFERENTIAL (ATM REFERENCE)",
              (x0 + 1.0 * s, y0 + 0.775 * s), (x0 + 3.4, y0 + 2.8))
    # pilot piston view
    xs, ys = 11.0, 6.4
    ss = 3.6
    prof2 = [(0, 0.725), (0.30, 0.725), (0.30, 0.500), (1.00, 0.500), (1.00, 0.350),
             (1.30, 0.350)]
    turned_half_section(sh, prof2, [], xs, ys, ss)
    sh.label("VIEW B — SHEX-016A PILOT PISTON  SCALE 3.6:1", 9.8, 9.0)
    sh.hdim((xs, ys + 0.725 * ss), (xs + 1.30 * ss, ys + 0.725 * ss), ys + 2.2, ss,
            text="1.300 OAL")
    sh.leader("SEAL LAND OD 1.450 x 0.30, 2x O-RING GROOVES",
              (xs + 0.15 * ss, ys + 0.725 * ss), (xs + 1.6, ys + 2.6))
    sh.leader("NOSE 0.700 SHIFTS SHEX-013S SLEEVE\nCLOSED FIRST (EQ PORTS) — LOWEST CRACK p",
              (xs + 1.15 * ss, ys + 0.350 * ss), (xs + 2.0, ys - 2.4))
    sh.notes([
        "EQ PILOT FIRES BEFORE STAGE 1 (LOWEST CRACK PRESSURE) -> ISOLATE BELOW.",
        "CHAMBER REFERENCE VOLUME SEALED + ARMED AT SURFACE.",
        "ALL SEAL BORES RA 16; PISTON SEAL LAND RA 16.",
    ], 1.0, 3.6)
    return sh.save("ACT-DWG-016_chamber_pilot")


def dwg_017_sequence() -> Path:
    sh = Sheet("ACT-DWG-017", "SEQUENCE / INITIATION SUB (DCN-12)",
               "SHEX-017 / 017A / 017B", "4140 HT / 17-4 PH H1075", "1+1+1/PLUG")
    # View A — housing
    s = 4.0
    x0, y0 = 2.6, 6.2
    prof = [(0, 0.775), (1.50, 0.775)]
    bore = [(0, 0.650), (1.50, 0.650)]
    turned_half_section(sh, prof, bore, x0, y0, s)
    sh.label("VIEW A — SHEX-017 HOUSING  SCALE 4:1", 1.2, 9.7)
    sh.hdim((x0, y0 + 0.775 * s), (x0 + 1.50 * s, y0 + 0.775 * s), y0 + 1.4, s,
            text="1.500")
    sh.vdim((x0 + 0.75 * s, y0 - 0.775 * s), (x0 + 0.75 * s, y0 + 0.775 * s),
            x0 - 0.9, s, text="OD 1.550 / ID 1.300")
    sh.leader("EFI / PILOT PORT 0.200 — e-line IGNITER OR\nCT PILOT OPENS THE GATE (COMMAND)",
              (x0 + 1.34 * s, y0 + 0.650 * s), (x0 + 1.7, y0 + 2.9))
    sh.leader("2x RADIAL MANIFOLD FEED 0.094 ->\nSTAGE-1 / STAGE-2 BLADDER LINES",
              (x0 + 0.55 * s, y0 + 0.775 * s), (x0 - 0.3, y0 + 1.9))
    sh.leader("METERING ORIFICE 0.040 — PLATEAU\nDAMPING ONLY (NOT THE SEQUENCER)",
              (x0 + 0.75 * s, y0 - 0.775 * s), (x0 + 0.2, y0 - 2.4))
    # View B — arming sleeve
    xs, ys = 11.2, 8.2
    ss = 4.4
    prof2 = [(0, 0.645), (0.60, 0.645)]
    bore2 = [(0, 0.525), (0.60, 0.525)]
    turned_half_section(sh, prof2, bore2, xs, ys, ss)
    sh.label("VIEW B — SHEX-017A ARMING SLEEVE  4.4:1", 9.4, 10.0)
    sh.vdim((xs + 0.3 * ss, ys - 0.645 * ss), (xs + 0.3 * ss, ys + 0.645 * ss),
            xs - 0.8, ss, text="OD 1.290 / ID 1.050")
    sh.leader("SHEAR PIN 0.093 —\nCALIBRATED ~1720 PSI",
              (xs + 0.10 * ss, ys + 0.645 * ss), (xs + 1.9, ys + 1.3))
    sh.leader("FEED PORT 0.094 — UNCOVERS STAGE-2\nLINE WHEN STAGE 1 BOTTOMS OUT",
              (xs + 0.32 * ss, ys - 0.645 * ss), (xs + 1.3, ys - 1.6))
    # View C — reference / ball-seat piston
    xc, yc = 11.2, 4.4
    sc = 4.4
    prof3 = [(0, 0.645), (0.30, 0.645), (0.30, 0.500), (0.90, 0.500)]
    bore3 = [(0, 0.450), (0.13, 0.250), (0.90, 0.250)]
    turned_half_section(sh, prof3, bore3, xc, yc, sc)
    sh.label("VIEW C — SHEX-017B REFERENCE / BALL-SEAT PISTON  4.4:1", 8.5, 6.3)
    sh.hdim((xc, yc + 0.645 * sc), (xc + 0.90 * sc, yc + 0.645 * sc), yc + 1.4, sc,
            text="0.900 OAL")
    sh.leader("TAPERED BALL SEAT 0.90->0.50 —\nDROP BALL TO ARM THE CT GATE",
              (xc + 0.06 * sc, yc - 0.45 * sc), (xc - 1.9, yc - 1.2))
    sh.leader("SEAL LAND OD 1.290, 2x O-RING — RESPONDS\nTO APPLIED dP (CT vs ANNULUS): DEPTH CANCELS",
              (xc + 0.15 * sc, yc + 0.645 * sc), (xc + 1.0, yc + 1.5))
    sh.notes([
        "DCN-12: REPLACES THE PASSIVE HYDROSTATIC BURST-DISK TRIGGER, WHICH HAS",
        "  NO POSITION CONTROL (FIRES DURING RUN-IN). SEE SHEX-EM-001.",
        "INITIATION BY COMMAND: CT APPLIED dP (+~1500 PSI) + BALL, OR e-line EFI.",
        "SEQUENCING IS COMPLETION-GATED: EQ PILOT (SHEX-016A) CLOSES SHEX-013",
        "  FIRST -> ARMS STAGE 1; STAGE-1 BOTTOM-OUT SHIFTS 017A -> ARMS STAGE 2.",
        "ALL SEAL BORES RA 16; PT ALL PRESSURE PASSAGES AFTER MACHINING.",
    ], 1.0, 3.2)
    return sh.save("ACT-DWG-017_sequence_sub")


def _pdf(stem: str) -> None:
    import ezdxf
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from ezdxf.addons.drawing import Frontend, RenderContext
    from ezdxf.addons.drawing.matplotlib import MatplotlibBackend

    doc = ezdxf.readfile(OUT_DXF / f"{stem}.dxf")
    fig = plt.figure(figsize=(17, 11))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    Frontend(RenderContext(doc), MatplotlibBackend(ax)).draw_layout(
        doc.modelspace(), finalize=True)
    OUT_PDF.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PDF / f"{stem}.pdf", facecolor="white")
    plt.close(fig)
    print(f"  pdf {stem}.pdf")


def main() -> None:
    OUT_DXF.mkdir(parents=True, exist_ok=True)
    stems = []
    for fn in (dwg_014a_gland, dwg_014b_lock, dwg_014c_charge, dwg_015_belleville,
               dwg_016_chamber, dwg_017_sequence):
        p = fn()
        stems.append(p.stem)
        print(f"  ok {p.name}")
    for stem in stems:
        _pdf(stem)


if __name__ == "__main__":
    main()
