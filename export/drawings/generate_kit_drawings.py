"""SHEX-AK-20 setting adapter kit — dimensioned shop drawings (DXF + PDF).

Reuses the Sheet scaffolding from generate_release_drawings.py.
Authority: cad/setting_kit_solids.py (ST-DCN-1..3) + DCN-7/8.

Run:  .venv\\Scripts\\python export/drawings/generate_kit_drawings.py
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


def dwg_st101_sleeve() -> Path:
    sh = Sheet("ST-DWG-101", "SETTING SLEEVE / SHOE", "ST-101",
               "4140 HT (AMS 6415) 28-32 HRC", "1/KIT")
    s = 0.62
    x0, y0 = 2.2, 5.8
    prof = [(0, 0.950), (11.0, 0.950), (12.5, 1.875), (15.0, 1.875)]
    bore = [(0, 0.735), (11.5, 0.735), (13.0, 1.625), (15.0, 1.625)]
    turned_half_section(sh, prof, bore, x0, y0, s)
    sh.label("VIEW A — HALF SECTION  SCALE 0.62:1  (FOOT AT LEFT = DOWNHOLE)", 1.6, 8.6)
    sh.hdim((x0, y0 + 1.875 * s), (x0 + 15.0 * s, y0 + 1.875 * s), y0 + 2.0, s,
            text="15.000 +/-.015")
    sh.hdim((x0, y0 - 0.950 * s), (x0 + 11.0 * s, y0 - 0.950 * s), y0 - 1.8, s,
            text="SHOE TUBE 11.000")
    sh.vdim((x0, y0 - 0.950 * s), (x0, y0 + 0.950 * s), x0 - 0.8, s,
            text="SHOE OD 1.900 +/-.005")
    sh.vdim((x0 + 14.6 * s, y0 - 1.875 * s), (x0 + 14.6 * s, y0 + 1.875 * s),
            x0 + 15.0 * s + 0.9, s, text="OD 3.750 +/-.010")
    sh.leader("SHOE BORE DIA 1.470 +.005/-.000 x 11.5\nPASSES SHEX-012 REV E BODY DIA 1.450 (DCN-7)",
              (x0 + 5.0 * s, y0 + 0.735 * s), (x0 + 3.6, y0 + 1.9))
    sh.leader("FOOT FACE: BEARS ON UPPER SLIP CARRIER\nANNULUS 1.562-1.688 AT PLUG Z=51 — SQUARE 0.002 FIM, RA 32",
              (x0, y0 + 0.85 * s), (x0 - 1.2, y0 + 3.1))
    sh.leader("BOX 3.250-8 UN-2B x 2.000 — TOOL CROSSLINK\nSLEEVE (ST-DCN-3: VERIFY VS TOOL MAKE)",
              (x0 + 14.0 * s, y0 + 1.625 * s), (x0 + 9.6, y0 + 3.3))
    sh.leader("CONE BORE 30 DEG INCL, BLEND R0.25", (x0 + 12.2 * s, y0 + 1.1 * s),
              (x0 + 9.0, y0 - 2.2))
    sh.notes([
        "MATES: BAKER E-4 No.20 / MODEL J-20 CROSSLINK SLEEVE (AND #20 CLONES).",
        "ST-DCN-3: CONFIRM CROSSLINK SLEEVE THREAD ON THE SPECIFIC TOOL BEFORE CUTTING.",
        "SHOE TUBE IS A COLUMN AT 45 KLBF — NO NICKS/TOOL MARKS DEEPER THAN 0.005.",
        "4x MILLED FLATS 0.75 W AT TOP OD FOR MAKEUP WRENCH.",
        "2x ST-104 SPACER RINGS FIT BETWEEN BOX FACE AND TOOL SLEEVE TO TUNE STAND-OFF.",
        "MPI AFTER MACHINING; NO LINEAR INDICATIONS.",
    ], 1.0, 3.4)
    return sh.save("ST-DWG-101_setting_sleeve")


def dwg_st102_rod() -> Path:
    sh = Sheet("ST-DWG-102", "TENSION ROD", "ST-102",
               "4140 HT (AMS 6415) 28-32 HRC", "1/KIT")
    s = 0.72
    x0, y0 = 2.2, 5.8
    prof = [(0, 0.625), (13.85, 0.625), (13.85, 0.750), (15.10, 0.750)]
    bore = [(0, 0.4375), (1.05, 0.4375)]
    turned_half_section(sh, prof, bore, x0, y0, s)
    sh.label("VIEW A — HALF SECTION  SCALE 0.72:1  (BOTTOM AT LEFT)", 1.6, 8.4)
    sh.hdim((x0, y0 + 0.78 * s), (x0 + 15.10 * s, y0 + 0.78 * s), y0 + 1.9, s,
            text="15.100 +/-.015")
    sh.vdim((x0 + 6.0 * s, y0 - 0.625 * s), (x0 + 6.0 * s, y0 + 0.625 * s), x0 - 0.8, s,
            text="BODY DIA 1.250 +/-.003")
    sh.leader("BOTTOM BOX 1.000-8 UN-2B x 1.000\n(TAKES ST-103 SHEAR STUD TOP PIN)",
              (x0 + 0.5 * s, y0 + 0.4375 * s), (x0 + 0.6, y0 + 2.2))
    sh.leader("TOP PIN 1.500-12 UNF-2A x 1.250 — TOOL SETTING\nMANDREL BOX (ST-DCN-3: VERIFY VS TOOL MAKE)",
              (x0 + 14.5 * s, y0 + 0.750 * s), (x0 + 9.2, y0 + 2.6))
    sh.leader("WRENCH FLATS 2x 1.000 AF x 1.5 AT MID-BODY",
              (x0 + 7.5 * s, y0 - 0.625 * s), (x0 + 5.2, y0 - 2.0))
    sh.notes([
        "FULL TENSION MEMBER AT 45 KLBF: MIN SECTION 1.227 IN2 — 37 KSI NOMINAL.",
        "RUNOUT BODY TO THREADS 0.003 FIM MAX.",
        "RADIUS ALL SHOULDERS R0.06 MIN (FATIGUE).",
        "MPI AFTER MACHINING.",
    ], 1.0, 3.6)
    return sh.save("ST-DWG-102_tension_rod")


def dwg_st103_stud() -> Path:
    sh = Sheet("ST-DWG-103", "CALIBRATED SHEAR STUD + SPACER", "ST-103 / ST-104",
               "4140 HT 125-145 KSI LOT", "1 + 2/KIT")
    s = 2.6
    x0, y0 = 2.6, 6.2
    prof = [(0, 0.435), (1.0, 0.435), (1.0, 0.500), (1.45, 0.500), (1.50, 0.320),
            (1.70, 0.320), (1.75, 0.500), (2.20, 0.500), (2.20, 0.435), (3.20, 0.435)]
    turned_half_section(sh, prof, [], x0, y0, s)
    sh.label("VIEW A — ST-103 SHEAR STUD  SCALE 2.6:1", 1.8, 9.2)
    sh.hdim((x0, y0 + 0.52 * s), (x0 + 3.20 * s, y0 + 0.52 * s), y0 + 2.2, s,
            text="3.200 +/-.010")
    sh.hdim((x0 + 1.50 * s, y0 - 0.32 * s), (x0 + 1.70 * s, y0 - 0.32 * s), y0 - 2.0, s,
            text="NECK 0.200 +/-.005")
    sh.vdim((x0 + 1.6 * s, y0 - 0.32 * s), (x0 + 1.6 * s, y0 + 0.32 * s), x0 - 0.9, s,
            text="NECK DIA 0.640 +/-.002 (ST-DCN-2)")
    sh.leader("THREAD 1.000-8 UN-2A x 1.000 BOTH ENDS\n(BOTTOM: SHEX-012 TOP BOX; TOP: ST-102 BOX)",
              (x0 + 0.5 * s, y0 + 0.435 * s), (x0 + 0.6, y0 + 1.9))
    sh.leader("BODY DIA 1.000; HEX SOCKET 0.500 AF\nIN TOP END FACE FOR MAKEUP",
              (x0 + 2.0 * s, y0 + 0.50 * s), (x0 + 6.2, y0 + 1.7))
    sh.leader("45 DEG NECK SHOULDERS, ROOT R0.015 MAX\n(CONTROLLED BREAK — NO POLISH)",
              (x0 + 1.72 * s, y0 + 0.42 * s), (x0 + 6.6, y0 + 0.2))
    # ST-104 spacer view
    xs, ys = 11.6, 5.6
    ss = 2.6
    turned_half_section(sh, [(0, 0.950), (0.25, 0.950)], [(0, 0.740), (0.25, 0.740)],
                        xs, ys, ss)
    sh.label("VIEW B — ST-104 STROKE SPACER  SCALE 2.6:1", 10.8, 8.2)
    sh.vdim((xs, ys - 0.95 * ss), (xs, ys + 0.95 * ss), xs - 0.8, ss,
            text="OD 1.900 / ID 1.480")
    sh.hdim((xs, ys + 0.95 * ss), (xs + 0.25 * ss, ys + 0.95 * ss), ys + 2.8, ss,
            text="0.250 +/-.002")
    sh.notes([
        "ST-DCN-2: NECK 0.640 x 0.200 -> PARTS AT 45 KLBF +/-5% IN 125-145 KSI 4140.",
        "LOT CALIBRATION MANDATORY: PULL 3 STUDS PER HEAT LOT TO FAILURE,",
        "  RECORD BREAK LOAD; ACCEPT LOT IF ALL 3 WITHIN 42.75-47.25 KLBF.",
        "STAMP LOT NO + BREAK LOAD ON BOTH BODY FLANKS.",
        "DO NOT SHOT-PEEN, PLATE, OR POLISH THE NECK.",
        "ST-104 SPACERS TUNE TOOL-SLEEVE STAND-OFF; FIT 0/1/2 AT RIG-UP.",
    ], 1.0, 3.4)
    return sh.save("ST-DWG-103_shear_stud_spacer")


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
    for fn in (dwg_st101_sleeve, dwg_st102_rod, dwg_st103_stud):
        p = fn()
        stems.append(p.stem)
        print(f"  ok {p.name}")
    for stem in stems:
        _pdf(stem)


if __name__ == "__main__":
    main()
