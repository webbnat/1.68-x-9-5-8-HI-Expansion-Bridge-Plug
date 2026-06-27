"""Manual figures for SHEX-BP-UHEX-54 — generated from release dimensions.

Every dimension here mirrors cad/release_solids.py (the release geometry
authority). Figures are schematic-accurate 2D cross sections: the tool axis
is horizontal (Z, inches), radius vertical (inches), full section (mirrored).
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Polygon, Rectangle

OUT = Path(__file__).parent / "figures"
OUT.mkdir(exist_ok=True)

# palette (colorblind-friendly-ish)
C = {
    "mandrel": "#8898aa",
    "neck": "#5b7fa6",
    "tail_sleeve": "#c9a227",
    "eq_body": "#7a5fa0",
    "eq_sleeve": "#b08fd0",
    "slip": "#c0504d",
    "carrier": "#d8c8b8",
    "stent1": "#4f9d69",
    "stent2": "#2e7d54",
    "sleeve10": "#d9822b",
    "insert02": "#946b2d",
    "iris": "#e0a800",
    "petal": "#3f7fbf",
    "hnbr": "#222222",
    "mtm": "#aa3377",
    "neck12": "#666f7a",
    "casing": "#b0b0b0",
    "seal": "#111111",
}

MANDREL_PROF = [
    (0, 0.675), (5.0, 0.675), (5.0, 0.775), (6.25, 0.775), (7.75, 0.810),
    (9.375, 0.810), (9.5, 0.775), (10.3, 0.775), (10.4, 0.635), (25.9, 0.635),
    (26.0, 0.775), (27.125, 0.775), (28.5, 0.791), (28.56, 0.775),
    (31.625, 0.775), (33.0, 0.791), (33.06, 0.775),
    (34.75, 0.775), (34.75, 0.779), (35.25, 0.779), (35.25, 0.775),
    (36.125, 0.775), (37.5, 0.791), (37.56, 0.775),
    (40.625, 0.775), (42.0, 0.791), (42.06, 0.775),
    (48.25, 0.775), (49.75, 0.810), (50.0, 0.775), (50.5, 0.775),
    (50.5, 0.6875), (51.5, 0.6875), (51.5, 0.650), (52.0, 0.650),
]

# SHEX-012 Rev E (DCN-7): pilot, body, GS neck groove, fish head
NECK12_PROF = [(0, 0.775), (0.5, 0.775), (0.5, 0.725), (4.5, 0.725),
               (4.6, 0.5935), (5.3, 0.5935), (5.45, 0.6875), (6.35, 0.6875),
               (6.5, 0.620)]
NECK12_BORE = [(0, 0.6485), (1.0, 0.6485), (1.0, 0.6525), (1.5, 0.6525),
               (1.5, 0.375), (5.5, 0.375), (5.5, 0.4375), (6.5, 0.4375)]

MODULE_Z = {
    "mandrel_tail": (0.0, 3.0), "bottom_sub": (3.0, 5.0),
    "lower_slips": (5.0, 9.5), "stage1": (9.5, 13.5), "stage2": (13.5, 18.5),
    "stage3_iris": (18.5, 26.0), "seal_land_1": (26.0, 30.5),
    "seal_land_2": (30.5, 35.0), "seal_land_3": (35.0, 39.5),
    "seal_land_4": (39.5, 44.0), "upper_mtm": (44.0, 46.5),
    "upper_slips": (46.5, 51.0), "fishing_neck": (50.5, 57.0),
}
STROKE = 10.0  # DCN-8
RB, RO = 0.781, 0.844  # module bore R / run-in outer R
CASING_IR, CASING_OR = 8.835 / 2, 9.625 / 2


def mirrored(ax, prof, color, z_off=0.0, alpha=1.0, ec="black", lw=0.4, zorder=2,
             label=None):
    """prof: list of (z, r) tracing the upper outline left->right. Closes along
    the axis. Drawn twice (r and -r)."""
    for sgn in (1, -1):
        xs = [z + z_off for z, _ in prof] + [prof[-1][0] + z_off, prof[0][0] + z_off]
        ys = [sgn * r for _, r in prof] + [0, 0]
        ax.add_patch(Polygon(list(zip(xs, ys)), closed=True, fc=color, ec=ec,
                             lw=lw, alpha=alpha, zorder=zorder,
                             label=label if sgn == 1 else None))


def ring(ax, z0, z1, r_in, r_out, color, z_off=0.0, alpha=1.0, ec="black",
         lw=0.4, zorder=3, label=None, hatch=None):
    for sgn in (1, -1):
        ax.add_patch(Rectangle((z0 + z_off, sgn * r_in if sgn > 0 else -r_out),
                               z1 - z0, r_out - r_in, fc=color, ec=ec, lw=lw,
                               alpha=alpha, zorder=zorder, hatch=hatch,
                               label=label if sgn > 0 else None))


def callout(ax, text, xy, xytext, fs=8.0):
    ax.annotate(text, xy=xy, xytext=xytext, fontsize=fs,
                arrowprops=dict(arrowstyle="-", lw=0.7, color="0.25"),
                ha="left", va="center", zorder=20,
                bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="0.6", lw=0.5))


def axis_line(ax, z0, z1):
    ax.plot([z0, z1], [0, 0], color="0.4", lw=0.7, ls=(0, (12, 3, 2, 3)), zorder=1)


def draw_static_stack(ax, state: str) -> None:
    """All non-mandrel-group modules (identical Z in both states)."""
    # equalizing sub
    z0, _ = MODULE_Z["bottom_sub"]
    ring(ax, z0, z0 + 2.0, 0.738, RO, C["eq_body"], label="SHEX-013 eq. sub body")
    ring(ax, z0 + 0.1, z0 + 1.3, 0.677, 0.735, C["eq_sleeve"],
         label="SHEX-013S sliding sleeve")
    # slips
    for mod in ("lower_slips", "upper_slips"):
        z0, z1 = MODULE_Z[mod]
        zc = (z0 + z1) / 2 - 1.0
        lbl_s = "SHEX-006/007 slips (x8 ea)" if mod == "lower_slips" else None
        lbl_c = "Slip carriers" if mod == "lower_slips" else None
        if state == "set":
            ring(ax, zc, zc + 2.0, 3.560, 4.360, C["slip"], label=lbl_s, zorder=4)
            ring(ax, z0, z1, RB, 1.780, C["carrier"], label=lbl_c)
        else:
            ring(ax, zc, zc + 2.0, RB + 0.002, RO - 0.002, C["slip"], label=lbl_s,
                 zorder=4)
            ring(ax, z0, zc, RB, RO, C["carrier"], label=lbl_c)
            ring(ax, zc + 2.0, z1, RB, RO, C["carrier"])
    # stents
    z0, z1 = MODULE_Z["stage1"]
    if state == "set":
        ring(ax, z0, z1, 3.375 / 2 - 0.063, 3.375 / 2, C["stent1"],
             label="SHEX-008 stage-1 stent")
    else:
        ring(ax, z0, z1, RB, RO, C["stent1"], label="SHEX-008 stage-1 stent",
             hatch="////")
    z0, z1 = MODULE_Z["stage2"]
    if state == "set":
        ring(ax, z0, z1, 5.750 / 2 - 0.063, 5.750 / 2, C["stent2"],
             label="SHEX-009 stage-2 stent")
    else:
        ring(ax, z0, z1, RB, RO, C["stent2"], label="SHEX-009 stage-2 stent",
             hatch="\\\\\\\\")
    # stage-3 iris module
    z0, z1 = MODULE_Z["stage3_iris"]
    ring(ax, z0, z1, RB, RO, C["sleeve10"], label="SHEX-010 support sleeve")
    ring(ax, z0 + 3.25, z0 + 7.25, 0.641, 0.7775, C["insert02"],
         label="SHEX-002 helix guide")
    if state == "set":
        ring(ax, z0 + 1.0, z0 + 3.75, 2.955, 4.318, C["iris"],
             label="SHEX-001 iris segments (x16)", zorder=4)
    else:
        ring(ax, z0 + 0.40, z0 + 3.15, 0.720, 0.778, C["iris"],
             label="SHEX-001 iris segments (x16)", zorder=4)
    # seal lands
    for i in range(1, 5):
        z0, z1 = MODULE_Z[f"seal_land_{i}"]
        lbl_p = "SHEX-005 petal backups (x16/land)" if i == 1 else None
        lbl_h = "SHEX-004 HNBR liner" if i == 1 else None
        lbl_c = "Seal carriers" if i == 1 else None
        if state == "set":
            ring(ax, z0, z0 + 0.4, RB, RO, C["carrier"], label=lbl_c)
            ring(ax, z0 + 0.4, z1 - 0.4, RB, 4.360, C["hnbr"], alpha=0.85,
                 label=lbl_h)
            ring(ax, z0 + 1.70, z0 + 2.25, 0.895, 4.011, C["petal"], label=lbl_p,
                 zorder=4)
        else:
            ring(ax, z0, z1, RB, RO, C["carrier"], label=lbl_c)
            ring(ax, z0 + 2.25, z0 + 2.80, RB, 0.831, C["hnbr"], alpha=0.85,
                 label=lbl_h, zorder=4)
            ring(ax, z0 + 1.70, z0 + 2.25, RB, 0.831, C["petal"], label=lbl_p,
                 zorder=4)
    # upper MTM
    z0, z1 = MODULE_Z["upper_mtm"]
    if state == "set":
        for ring_i in range(3):
            zr = z0 + 0.05 + ring_i * 0.80
            ring(ax, zr, zr + 0.75, 4.200, 4.400, C["mtm"],
                 label="SHEX-003 MTM rings (3x4 seg)" if ring_i == 0 else None,
                 zorder=4)
    else:
        ring(ax, z0 + 0.25, z0 + 2.25, RB + 0.002, RO - 0.002, C["mtm"],
             label="SHEX-003 MTM rings (3x4 seg)", zorder=4)


def draw_mandrel_group(ax, dz: float) -> None:
    mirrored(ax, MANDREL_PROF, C["mandrel"], z_off=dz, zorder=2,
             label="SHEX-011 inner mandrel")
    # drive ribs (sectioned at phase 0/180: lobes every lead/2 = 2.0)
    for zr in (18.15 + 0.0, 18.15 + 2.0, 18.15 + 3.3):
        for sgn in (1, -1):
            ax.add_patch(Rectangle((zr + dz, sgn * 0.635 if sgn > 0 else -(0.715)),
                                   0.30, 0.080, fc=C["neck"], ec="black", lw=0.3,
                                   zorder=3))
    ring(ax, 0, 3.0, 0.676, 0.775, C["tail_sleeve"], z_off=dz,
         label="SHEX-011A tail sleeve")
    prof = [(z + 50.5, r) for z, r in NECK12_PROF]
    mirrored(ax, prof, C["neck12"], z_off=dz, zorder=2,
             label="SHEX-012 fishing neck")


def fig_ga(state: str, fname: str, title: str) -> None:
    dz = STROKE if state == "set" else 0.0
    fig, ax = plt.subplots(figsize=(16, 5.4 if state == "set" else 3.4), dpi=140)
    draw_static_stack(ax, state)
    draw_mandrel_group(ax, dz)
    if state == "set":
        top = 57.0 + dz + 4.0
        ring(ax, -4.0, top, CASING_IR, CASING_OR, C["casing"], alpha=0.55,
             label='9-5/8" 40# casing (ref)')
        axis_line(ax, -5, top + 1)
        ax.set_xlim(-5.5, top + 1.5)
        ax.set_ylim(-5.2, 5.2)
    else:
        axis_line(ax, -1, 58)
        ax.set_xlim(-1.5, 58.5)
        ax.set_ylim(-2.6, 2.6)

    # module band annotations under the axis
    yb = -1.35 if state != "set" else -5.05
    for name, (z0, z1) in MODULE_Z.items():
        ax.annotate("", xy=(z0, yb), xytext=(z1, yb),
                    arrowprops=dict(arrowstyle="|-|,widthA=0.18,widthB=0.18",
                                    lw=0.7, color="0.35"))
        short = {
            "mandrel_tail": "tail", "bottom_sub": "eq sub",
            "lower_slips": "lower slips", "stage1": "stage 1",
            "stage2": "stage 2", "stage3_iris": "stage 3 iris",
            "seal_land_1": "seal 1", "seal_land_2": "seal 2",
            "seal_land_3": "seal 3", "seal_land_4": "seal 4",
            "upper_mtm": "MTM", "upper_slips": "upper slips",
            "fishing_neck": "fishing neck",
        }[name]
        ax.text((z0 + z1) / 2, yb - (0.28 if state != "set" else 0.42), short,
                ha="center", va="top", fontsize=7.4, rotation=0 if state == "set" else 30)

    if state == "set":
        callout(ax, "iris segments deployed\nto OD 8.636 (16x SHEX-001)",
                (20.9, 4.25), (12.0, 4.6))
        callout(ax, "HNBR liner + petals energized\non mandrel seal ramps",
                (32.0, 4.2), (30.0, 4.85))
        callout(ax, "slips bite casing (OD 8.720)", (7.0, 4.2), (-4.0, 4.7))
        callout(ax, "MTM rings preloaded by\nmandrel land Ø1.558 (OD 8.800)",
                (45.6, 4.3), (47.5, 4.85))
        callout(ax, f"mandrel group stroked +{STROKE:.0f} in",
                (57.0 + dz, 0.7), (58.0, 2.4))
    else:
        callout(ax, "Ø1.688 max envelope", (36.0, 0.85), (33.0, 1.9))
        callout(ax, "helix neck Ø1.270 (DCN-1)", (16.5, 0.64), (13.5, 1.9))
        callout(ax, "fishing neck 1.375 pin / 1in AMT", (56.0, 0.69), (50.5, 1.9))
        callout(ax, "equalizing ports open", (4.0, 0.84), (1.0, 1.9))

    ax.set_title(title, fontsize=11, pad=10)
    ax.set_xlabel("Plug Z (in)")
    ax.set_ylabel("R (in)")
    ax.set_aspect("equal")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.30 if state != "set" else -0.22),
              ncol=5, fontsize=7.2, frameon=False)
    ax.grid(alpha=0.15, lw=0.4)
    fig.tight_layout()
    fig.savefig(OUT / fname, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  ok {fname}")


def fig_mandrel() -> None:
    fig, ax = plt.subplots(figsize=(15, 3.6), dpi=140)
    mirrored(ax, MANDREL_PROF, C["mandrel"])
    for zr in (18.15, 20.15, 21.45):
        for sgn in (1, -1):
            ax.add_patch(Rectangle((zr, sgn * 0.635 if sgn > 0 else -0.715),
                                   0.30, 0.080, fc=C["neck"], ec="black", lw=0.3,
                                   zorder=3))
    axis_line(ax, -1, 53.5)
    zones = [
        (0, 5.0, "tail Ø1.350\n(DCN-5)"), (6.25, 9.375, "lower slip\ntaper/land Ø1.620"),
        (10.4, 25.9, "helix neck Ø1.270 — drive ribs Z 18.15–21.75\n2-start, lead 4.000, peak Ø1.429 (DCN-1/9)"),
        (27.125, 42.06, "4x seal ramps Ø1.550→1.582 (3°)\n@ 27.125 / 31.625 / 36.125 / 40.625"),
        (48.25, 50.0, "upper slip\ntaper Ø1.620"),
        (50.5, 52.0, "pin Ø1.375\n(DCN-6/7)"),
    ]
    for z0, z1, txt in zones:
        ax.annotate("", xy=(z0, -1.15), xytext=(z1, -1.15),
                    arrowprops=dict(arrowstyle="|-|,widthA=0.16,widthB=0.16",
                                    lw=0.7, color="0.3"))
        ax.text((z0 + z1) / 2, -1.32, txt, ha="center", va="top", fontsize=7.4)
    ax.annotate("MTM land Ø1.558 @ 34.75 (DCN-9)", xy=(35.0, 0.78), xytext=(33.0, 1.15),
                fontsize=7.4, arrowprops=dict(arrowstyle="-", lw=0.6, color="0.3"))
    ax.text(2.5, 1.05, "body Ø1.550 elsewhere", fontsize=8, color="0.25")
    ax.set_xlim(-1.5, 54.5)
    ax.set_ylim(-2.6, 1.4)
    ax.set_aspect("equal")
    ax.set_title("SHEX-011 inner mandrel — functional zone ledger (finished length 52.500)",
                 fontsize=11)
    ax.set_xlabel("Plug Z (in)")
    ax.grid(alpha=0.15, lw=0.4)
    fig.tight_layout()
    fig.savefig(OUT / "fig_mandrel_zones.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  ok fig_mandrel_zones.png")


def fig_helix_detail() -> None:
    fig, ax = plt.subplots(figsize=(11, 5.6), dpi=140)
    z0, z1 = 17.5, 26.5
    # mandrel neck + transitions
    prof = [(17.5, 0.775)] + [(z, r) for z, r in MANDREL_PROF if 17.5 < z < 26.5] \
        + [(26.5, 0.775)]
    prof = [(17.5, 0.775), (22.9, 0.635), (23.0, 0.775), (26.5, 0.775)]
    prof = [(17.5, 0.635), (22.9, 0.635), (23.0, 0.775), (26.5, 0.775)]
    mirrored(ax, prof, C["mandrel"], label="SHEX-011 mandrel (helix neck Ø1.270)")
    # ribs: 2-start lead 4 -> section lobes every 2.0 in
    for zr in (19.25, 21.25, 22.85):
        for sgn in (1, -1):
            y = 0.635 if sgn > 0 else -0.715
            ax.add_patch(Rectangle((zr, y), 0.30, 0.080, fc=C["neck"], ec="black",
                                   lw=0.5, zorder=4,
                                   label="drive ribs 0.115W x 0.080H (2-start)"
                                   if (zr == 19.25 and sgn > 0) else None))
    # support sleeve 18.5-26 with pocket 21.75-25.75 and slots
    sleeve = [(18.5, 0.844), (26.0, 0.844)]
    ring(ax, 18.5, 26.0, 0.781, 0.844, C["sleeve10"], label="SHEX-010 support sleeve")
    ring(ax, 21.75, 25.75, 0.779, 0.781, "white", ec="none", zorder=3.5)
    # helix insert 21.75-25.75
    ring(ax, 21.75, 25.75, 0.641, 0.7775, C["insert02"],
         label="SHEX-002 helix guide (ID Ø1.282)")
    # grooves in insert (lead 4, 2-start: crossings every 1.0 at alternating sides)
    for zg in (22.25, 23.25, 24.25, 25.25):
        for sgn in (1, -1):
            ax.add_patch(Rectangle((zg - 0.0625, (0.641 if sgn > 0 else -0.721)),
                                   0.125, 0.080, fc="white", ec="black", lw=0.5,
                                   zorder=4,
                                   label="helix grooves 0.125W x 0.080DP, lead 4.000"
                                   if (zg == 22.25 and sgn > 0) else None))
    # iris segments stowed 18.9-21.65
    ring(ax, 18.90, 21.65, 0.720, 0.778, C["iris"],
         label="SHEX-001 iris segments (stowed)")
    # follower tab on segment mid-length
    for sgn in (1, -1):
        ax.add_patch(Rectangle((20.0, (0.640 if sgn > 0 else -0.720)), 0.625, 0.080,
                               fc=C["iris"], ec="black", lw=0.5, zorder=4,
                               label="segment follower tab (rides grooves)"
                               if sgn > 0 else None))
    axis_line(ax, z0, z1)
    callout(ax, "SET stroke: mandrel moves +11 in →\nribs sweep through insert grooves,\ninsert+segments rotate & climb",
            (21.0, -0.675), (18.0, -1.45))
    callout(ax, "anti-rotation pin Ø0.062\nthrough sleeve + insert", (25.4, 0.81),
            (24.6, 1.35))
    ax.set_xlim(17.0, 27.2)
    ax.set_ylim(-1.85, 1.75)
    ax.set_aspect("equal")
    ax.set_title("DCN-1 — stage-3 iris helix drive (run-in position, section at rib phase)",
                 fontsize=11)
    ax.set_xlabel("Plug Z (in)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=3, fontsize=7.4,
              frameon=False)
    ax.grid(alpha=0.15, lw=0.4)
    fig.tight_layout()
    fig.savefig(OUT / "fig_helix_drive.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  ok fig_helix_drive.png")


def fig_eq_sub() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.6), dpi=140, sharey=True)
    for ax, shifted in zip(axes, (False, True)):
        dz_sleeve = 0.375 if shifted else 0.0
        # mandrel tail Ø1.350 through zone (DCN-5)
        mirrored(ax, [(0, 0.675), (5.0, 0.675), (5.0, 0.775), (6.5, 0.775)],
                 C["mandrel"], label="SHEX-011 tail Ø1.350")
        ring(ax, 0, 3.0, 0.676, 0.775, C["tail_sleeve"], label="SHEX-011A sleeve")
        # body with glands and ports
        ring(ax, 3.0, 5.0, 0.738, 0.844, C["eq_body"], label="SHEX-013 body")
        for zg in (3.30, 4.602):
            for sgn in (1, -1):
                ax.add_patch(Rectangle((zg, 0.738 if sgn > 0 else -0.783),
                                       0.098, 0.045, fc="white", ec="black", lw=0.5,
                                       zorder=4))
                # o-ring dot
                ax.add_patch(plt.Circle((zg + 0.049, (0.755 if sgn > 0 else -0.755)),
                                        0.030, fc=C["seal"], ec="none", zorder=5))
        # ports at Z=4.0
        for sgn in (1, -1):
            ax.add_patch(Rectangle((4.0 - 0.031, 0.738 if sgn > 0 else -0.844),
                                   0.062, 0.106, fc="white", ec="black", lw=0.5,
                                   zorder=4))
        # sleeve
        z0s = 3.1 + dz_sleeve
        ring(ax, z0s, z0s + 1.2, 0.677, 0.735, C["eq_sleeve"],
             label="SHEX-013S sleeve")
        for sgn in (1, -1):
            ax.add_patch(Rectangle((z0s + 0.9 - 0.031, 0.677 if sgn > 0 else -0.735),
                                   0.062, 0.058, fc="white", ec="black", lw=0.5,
                                   zorder=4))
        axis_line(ax, -0.5, 6.5)
        ax.set_xlim(-0.5, 6.6)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect("equal")
        ax.grid(alpha=0.15, lw=0.4)
        ax.set_xlabel("Plug Z (in)")
        if not shifted:
            ax.set_title("OPEN (run-in): sleeve port @ Z 4.0 aligned with body ports",
                         fontsize=9.5)
            callout(ax, "flow path:\nbore ↔ annulus", (4.0, 0.79), (4.9, 1.25))
        else:
            ax.set_title("CLOSED (set): sleeve shifted +0.375, O-rings straddle ports",
                         fontsize=9.5)
            callout(ax, "ports blanked by\nsleeve wall between glands", (4.0, 0.79),
                    (4.9, 1.25))
    axes[0].legend(loc="upper center", bbox_to_anchor=(1.05, -0.16), ncol=5,
                   fontsize=7.6, frameon=False)
    fig.suptitle("DCN-5 — bottom equalizing sub radial stack (body glands, sliding sleeve)",
                 fontsize=11)
    fig.tight_layout()
    fig.savefig(OUT / "fig_equalizing_sub.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  ok fig_equalizing_sub.png")


def fig_top_joint() -> None:
    fig, ax = plt.subplots(figsize=(10, 5.2), dpi=140)
    # mandrel: body to shoulder + pin
    mprof = [(49.5, 0.775), (51.0, 0.775), (51.0, 0.750), (52.5, 0.750)]
    mirrored(ax, mprof, C["mandrel"], label="SHEX-011 mandrel (pin up)")
    # thread zone marks on pin 51-52
    for zt in (51.05, 51.25, 51.45, 51.65, 51.85):
        for sgn in (1, -1):
            ax.plot([zt, zt + 0.08], [sgn * 0.750, sgn * 0.720], color="black",
                    lw=0.6, zorder=5)
    # face groove in nose
    for sgn in (1, -1):
        ax.add_patch(Rectangle((52.414, (1.087 / 2 if sgn > 0 else -1.181 / 2)),
                               0.086, (1.181 - 1.087) / 2, fc="white", ec="black",
                               lw=0.6, zorder=5))
        ax.add_patch(plt.Circle((52.46, sgn * (1.134 / 2)), 0.030, fc=C["seal"],
                                zorder=6))
    # fishing neck female
    prof = [(z + 51.0, r) for z, r in NECK12_PROF]
    bore = [(z + 51.0, r) for z, r in NECK12_BORE]
    for sgn in (1, -1):
        xs = [z for z, _ in prof] + [z for z, _ in reversed(bore)]
        ys = [sgn * r for _, r in prof] + [sgn * r for _, r in reversed(bore)]
        ax.add_patch(Polygon(list(zip(xs, ys)), closed=True, fc=C["neck12"],
                             ec="black", lw=0.5, alpha=0.9, zorder=3,
                             label="SHEX-012 fishing neck (box down)" if sgn > 0 else None))
    # thread marks female 51-52
    for zt in (51.10, 51.30, 51.50, 51.70, 51.90):
        for sgn in (1, -1):
            ax.plot([zt, zt + 0.08], [sgn * 0.7112, sgn * 0.745], color="black",
                    lw=0.6, zorder=5)
    axis_line(ax, 49, 57.5)
    callout(ax, "shoulder face Z=51.0\n(flat 0.001 FIM, RA 32)", (51.0, 0.79), (49.2, 1.35))
    callout(ax, "1-1/2-12 UNF-2A x 1.000\n(relief 0.030 x 45°)", (51.5, 0.74), (49.6, -1.45))
    callout(ax, "seal bore Ø1.530 x 0.5\nover plain nose Ø1.500", (52.25, 0.765), (52.6, 1.4))
    callout(ax, "Parker 2-216 face seal\nin pin nose end face", (52.46, 0.567), (53.6, 0.95))
    callout(ax, "Ø0.125 cross pin @ Z 51.5\nafter 250 ft-lb makeup", (51.5, -0.75), (52.8, -1.45))
    callout(ax, "1 in AMT top connection", (56.5, 0.688), (55.6, 1.3))
    ax.set_xlim(48.8, 57.8)
    ax.set_ylim(-1.85, 1.8)
    ax.set_aspect("equal")
    ax.set_title("DCN-6 — top joint: SHEX-011 pin into SHEX-012 box (section)", fontsize=11)
    ax.set_xlabel("Plug Z (in)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=2, fontsize=8,
              frameon=False)
    ax.grid(alpha=0.15, lw=0.4)
    fig.tight_layout()
    fig.savefig(OUT / "fig_top_joint.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  ok fig_top_joint.png")


def fig_setting_sequence() -> None:
    """4-panel cartoon of the setting cascade."""
    stages = [
        ("1. RUN-IN  (Ø1.688)", 0.0, dict()),
        ("2. STROKE 0→4 in: slips ride tapers,\nstage-1 stent deploys", 4.0,
         dict(slips=0.55, s1=1.0)),
        ("3. STROKE 4→8 in: stage-2 stent +\niris segments screw outward", 8.0,
         dict(slips=1.0, s1=1.0, s2=1.0, iris=0.6)),
        ("4. STROKE 11 in: iris under seals, ramps\nenergize HNBR, MTM preloaded — SET", 11.0,
         dict(slips=1.0, s1=1.0, s2=1.0, iris=1.0, seal=1.0, mtm=1.0)),
    ]
    fig, axes = plt.subplots(4, 1, figsize=(13, 11), dpi=130, sharex=True)
    for ax, (title, dz, f) in zip(axes, stages):
        fr = {k: f.get(k, 0.0) for k in ("slips", "s1", "s2", "iris", "seal", "mtm")}
        ring(ax, -4, 72, CASING_IR, CASING_OR, C["casing"], alpha=0.5)
        # static modules with interpolated radii
        for mod in ("lower_slips", "upper_slips"):
            z0, z1 = MODULE_Z[mod]
            zc = (z0 + z1) / 2 - 1.0
            r1 = RB + fr["slips"] * (3.560 - RB)
            r2 = RO + fr["slips"] * (4.360 - RO)
            ring(ax, zc, zc + 2.0, r1, r2, C["slip"], zorder=4)
            ring(ax, z0, z1, RB, RO, C["carrier"])
        z0, z1 = MODULE_Z["stage1"]
        r = RO + fr["s1"] * (3.375 / 2 - RO)
        ring(ax, z0, z1, max(r - 0.30, RB), r, C["stent1"])  # display wall exaggerated
        z0, z1 = MODULE_Z["stage2"]
        r = RO + fr["s2"] * (5.750 / 2 - RO)
        ring(ax, z0, z1, max(r - 0.30, RB), r, C["stent2"])
        z0, z1 = MODULE_Z["stage3_iris"]
        ring(ax, z0, z1, RB, RO, C["sleeve10"])
        ri1 = 0.720 + fr["iris"] * (2.955 - 0.720)
        ri2 = 0.778 + fr["iris"] * (4.318 - 0.778)
        ring(ax, z0 + 0.7, z0 + 3.45, ri1, ri2, C["iris"], zorder=4)
        for i in range(1, 5):
            z0, z1 = MODULE_Z[f"seal_land_{i}"]
            rs = 0.831 + fr["seal"] * (4.360 - 0.831)
            rp2 = 0.831 + fr["seal"] * (4.011 - 0.831)
            rp1 = RB + fr["seal"] * (0.895 - RB)
            ring(ax, z0, z1, RB, RO, C["carrier"])
            ring(ax, z0 + 0.4, z1 - 0.4, RB, rs, C["hnbr"], alpha=0.8, zorder=3.6)
            ring(ax, z0 + 1.7, z0 + 2.25, rp1, rp2, C["petal"], zorder=4)
        z0, z1 = MODULE_Z["upper_mtm"]
        rm1 = RB + fr["mtm"] * (4.200 - RB)
        rm2 = RO + fr["mtm"] * (4.400 - RO)
        ring(ax, z0 + 0.2, z1 - 0.2, rm1, rm2, C["mtm"], zorder=4)
        draw_mandrel_group(ax, dz)
        axis_line(ax, -4, 71)
        ax.set_xlim(-5, 72)
        ax.set_ylim(-5.1, 5.1)
        ax.set_aspect("equal")
        ax.set_ylabel("R (in)")
        ax.text(0.01, 0.96, title, transform=ax.transAxes, fontsize=9.5,
                va="top", ha="left",
                bbox=dict(boxstyle="round,pad=0.3", fc="#f4f4f4", ec="0.5"))
        ax.grid(alpha=0.12, lw=0.4)
    axes[-1].set_xlabel("Plug Z (in)")
    fig.suptitle("SHEX-BP-UHEX-54 setting cascade (mandrel stroke +11 in, 55 klbf setting tool)",
                 fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.98))
    fig.savefig(OUT / "fig_setting_sequence.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  ok fig_setting_sequence.png")


def fig_exploded() -> None:
    """Assembly-order exploded diagram (schematic half-sections, axial gaps)."""
    fig, ax = plt.subplots(figsize=(16, 6.2), dpi=140)
    items = [
        # (length, prof builder as list of (z, r) or ring (r_in, r_out), color, label)
        ("SHEX-011\nmandrel", 8.0, ("prof", [(0, 0.675), (1.2, 0.675), (1.2, 0.775),
                                             (6.2, 0.775), (6.2, 0.75), (8.0, 0.75)]),
         C["mandrel"], "1"),
        ("SHEX-013S\nsleeve", 1.2, ("ring", 0.677, 0.735), C["eq_sleeve"], "2"),
        ("SHEX-013\nbody", 2.0, ("ring", 0.738, 0.844), C["eq_body"], "3"),
        ("SHEX-011A\ntail sleeve", 3.0, ("ring", 0.676, 0.775), C["tail_sleeve"], "4"),
        ("SHEX-007 x8 +\ncarrier (lower)", 4.5, ("ring", 0.781, 0.844), C["slip"], "5"),
        ("SHEX-008\nstage-1 stent", 4.0, ("ring", 0.781, 0.844), C["stent1"], "6"),
        ("SHEX-009\nstage-2 stent", 5.0, ("ring", 0.781, 0.844), C["stent2"], "7"),
        ("SHEX-001 x16\niris segments", 2.75, ("ring", 0.720, 0.778), C["iris"], "8"),
        ("SHEX-002\nhelix guide", 4.0, ("ring", 0.641, 0.7775), C["insert02"], "9"),
        ("SHEX-010\nsupport sleeve", 7.5, ("ring", 0.781, 0.844), C["sleeve10"], "10"),
        ("4x seal lands\n(004+005 x16)", 9.0, ("ring", 0.781, 0.844), C["petal"], "11"),
        ("SHEX-003 x12\nMTM rings", 2.5, ("ring", 0.781, 0.844), C["mtm"], "12"),
        ("SHEX-006 x8 +\ncarrier (upper)", 4.5, ("ring", 0.781, 0.844), C["slip"], "13"),
        ("SHEX-012\nfishing neck", 6.0, ("prof", [(0, 0.844), (4.5, 0.844),
                                                  (4.62, 0.6875), (6.0, 0.6875)]),
         C["neck12"], "14"),
    ]
    z = 0.0
    gap = 1.6
    for label, ln, geom, color, num in items:
        if geom[0] == "prof":
            mirrored(ax, [(zz + z, r) for zz, r in geom[1]], color)
        else:
            ring(ax, z, z + ln, geom[1], geom[2], color)
        ax.text(z + ln / 2, 1.15, num, ha="center", va="bottom", fontsize=10,
                fontweight="bold",
                bbox=dict(boxstyle="circle,pad=0.25", fc="white", ec="0.3"))
        ax.text(z + ln / 2, -1.05, label, ha="center", va="top", fontsize=7.6)
        z += ln + gap
    axis_line(ax, -1, z)
    ax.annotate("install order →", xy=(z * 0.45, 1.9), fontsize=11, color="0.3")
    ax.set_xlim(-1.5, z + 0.5)
    ax.set_ylim(-2.0, 2.2)
    ax.set_aspect("auto")  # schematic: radii exaggerated for legibility
    ax.set_axis_off()
    ax.set_title("Assembly order — components slide onto the mandrel from the top (pin) end "
                 "after the bottom group (2–4) is captured at the tail", fontsize=11)
    fig.tight_layout()
    fig.savefig(OUT / "fig_exploded_order.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  ok fig_exploded_order.png")


def main() -> None:
    fig_ga("run_in", "fig_ga_runin.png",
           "SHEX-BP-UHEX-54 — general arrangement, RUN-IN (full section, Ø1.688 envelope, OAL 57.0)")
    fig_ga("set", "fig_ga_set.png",
           'SHEX-BP-UHEX-54 — general arrangement, SET in 9-5/8" 40# casing (full section)')
    fig_mandrel()
    fig_helix_detail()
    fig_eq_sub()
    fig_top_joint()
    fig_setting_sequence()
    fig_exploded()


if __name__ == "__main__":
    main()
