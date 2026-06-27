"""Setting-tool (SHEX-AK-20) manual figures.

Dimensions mirror cad/setting_kit_solids.py and the plug DCN-7/8 top joint.
2D sections: tool axis horizontal (plug Z, inches), radius vertical (inches).
Market figures are data-driven from web-verified tool specs (see WORKING_LOG).
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

OUT = Path(__file__).parent / "figures"
OUT.mkdir(exist_ok=True)

C = {
    "tool": "#37485e",
    "sleeve": "#d9822b",     # ST-101
    "rod": "#4f9d69",        # ST-102
    "stud": "#c0504d",       # ST-103
    "spacer": "#c9a227",     # ST-104
    "neck": "#666f7a",       # SHEX-012 Rev E
    "mandrel": "#8898aa",
    "carrier": "#d8c8b8",
    "plug": "#9aa7b4",
}

# --- kit constants (cad/setting_kit_solids.py) ---
SHOE_OD, SHOE_ID = 1.900, 1.470
SLEEVE_TOP_OD, SLEEVE_BOX_ID = 3.750, 3.250
ROD_OD, ROD_TOP_PIN = 1.250, 1.500
STUD_BODY, STUD_PIN, STUD_NECK = 1.000, 0.870, 0.640
Z_SHOE_FOOT, Z_STUD_BOT, Z_ROD_BOT, Z_ROD_TOP = 51.0, 56.0, 58.15, 73.25


def mirrored(ax, prof, color, z_off=0.0, alpha=1.0, ec="black", lw=0.5, zorder=2,
             label=None):
    for sgn in (1, -1):
        xs = [z + z_off for z, _ in prof] + [prof[-1][0] + z_off, prof[0][0] + z_off]
        ys = [sgn * r for _, r in prof] + [0, 0]
        ax.add_patch(Polygon(list(zip(xs, ys)), closed=True, fc=color, ec=ec,
                             lw=lw, alpha=alpha, zorder=zorder,
                             label=label if sgn == 1 else None))


def tube(ax, prof, bore, color, z_off=0.0, alpha=1.0, ec="black", lw=0.5, zorder=2,
         label=None):
    """Hollow body: prof (outer upper outline) + bore (inner upper outline)."""
    for sgn in (1, -1):
        xs = [z + z_off for z, _ in prof] + [z + z_off for z, _ in reversed(bore)]
        ys = [sgn * r for _, r in prof] + [sgn * r for _, r in reversed(bore)]
        ax.add_patch(Polygon(list(zip(xs, ys)), closed=True, fc=color, ec=ec,
                             lw=lw, alpha=alpha, zorder=zorder,
                             label=label if sgn == 1 else None))


def ring(ax, z0, z1, r_in, r_out, color, z_off=0.0, alpha=1.0, ec="black", lw=0.5,
         zorder=3, label=None):
    for sgn in (1, -1):
        y = (r_in if sgn > 0 else -r_out)
        ax.add_patch(Rectangle((z0 + z_off, y), z1 - z0, r_out - r_in, fc=color,
                               ec=ec, lw=lw, alpha=alpha, zorder=zorder,
                               label=label if sgn > 0 else None))


def callout(ax, text, xy, xytext, fs=8.0):
    ax.annotate(text, xy=xy, xytext=xytext, fontsize=fs,
                arrowprops=dict(arrowstyle="-", lw=0.7, color="0.25"),
                ha="left", va="center", zorder=20,
                bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="0.6", lw=0.5))


def axis_line(ax, z0, z1):
    ax.plot([z0, z1], [0, 0], color="0.4", lw=0.7, ls=(0, (12, 3, 2, 3)), zorder=1)


# ---------------------------------------------------------------------------
def _draw_plug_top(ax, dz_outer=0.0):
    """Plug top reference. dz_outer shifts the OUTER stack (carrier) for the
    SET illustration; mandrel + neck stay fixed in plug coordinates."""
    # mandrel stub 44 -> 52 with DCN-7 pin
    mprof = [(44.0, 0.775), (44.75, 0.779), (45.25, 0.775), (48.25, 0.775),
             (49.75, 0.810), (50.0, 0.775), (50.5, 0.775), (50.5, 0.6875),
             (51.5, 0.6875), (51.5, 0.650), (52.0, 0.650)]
    mirrored(ax, mprof, C["mandrel"], label="plug mandrel (held up)")
    # upper slip carrier (outer stack) 46.5-51, moves with dz_outer
    ring(ax, 46.5, 51.0, 1.562 / 2, 1.688 / 2, C["carrier"], z_off=dz_outer,
         label="upper slip carrier (outer stack)")
    # Rev E fishing neck box-down: pilot 1.550, body 1.450, fish head 1.375
    nprof = [(50.5, 0.775), (51.0, 0.775), (51.0, 0.725), (56.0, 0.725),
             (57.0, 0.6875)]
    nbore = [(50.5, 0.6875), (51.5, 0.6875), (51.5, 0.435), (56.0, 0.435),
             (56.0, 0.500), (57.0, 0.500)]
    tube(ax, nprof, nbore, C["neck"], label="SHEX-012 Rev E fishing neck")


def _draw_kit(ax, dz_string=0.0, sheared=False):
    """Kit + tool lower end. dz_string lifts the whole string (rod+sleeve+tool)
    on release."""
    # ST-101 setting sleeve/shoe (moves with tool crosslink sleeve = string)
    s_prof = [(51.0, 0.950), (62.0, 0.950), (63.5, 1.875), (66.0, 1.875)]
    s_bore = [(51.0, 0.735), (62.5, 0.735), (65.0, 1.625), (66.0, 1.625)]
    tube(ax, s_prof, s_bore, C["sleeve"], z_off=dz_string,
         label="ST-101 setting sleeve/shoe")
    # ST-102 tension rod (fixed to tool setting mandrel = string)
    r_prof = [(58.15, 0.625), (72.0, 0.625), (72.0, 0.750), (73.25, 0.750)]
    r_bore = [(58.15, 0.4375), (59.20, 0.4375)]
    tube(ax, r_prof, r_bore, C["rod"], z_off=dz_string, label="ST-102 tension rod")
    # ST-103 shear stud
    if not sheared:
        st = [(56.0, STUD_PIN / 2), (57.0, STUD_PIN / 2), (57.0, STUD_BODY / 2),
              (57.45, STUD_BODY / 2), (57.50, STUD_NECK / 2), (57.70, STUD_NECK / 2),
              (57.75, STUD_BODY / 2), (58.20, STUD_BODY / 2), (58.20, STUD_PIN / 2),
              (59.20, STUD_PIN / 2)]
        mirrored(ax, st, C["stud"], zorder=5, label="ST-103 shear stud (45 klbf)")
    else:
        # bottom half stays in neck box
        bot = [(56.0, STUD_PIN / 2), (57.0, STUD_PIN / 2), (57.0, STUD_BODY / 2),
               (57.45, STUD_BODY / 2), (57.50, STUD_NECK / 2), (57.60, STUD_NECK / 2)]
        mirrored(ax, bot, C["stud"], zorder=5, label="ST-103 lower (stays)")
        top = [(57.60, STUD_NECK / 2), (57.70, STUD_NECK / 2), (57.75, STUD_BODY / 2),
               (58.20, STUD_BODY / 2), (58.20, STUD_PIN / 2), (59.20, STUD_PIN / 2)]
        mirrored(ax, top, C["stud"], z_off=dz_string, zorder=5,
                 label="ST-103 upper (leaves)")
    # tool lower end (schematic): crosslink sleeve (moving) + setting mandrel socket
    ring(ax, 66.0, 74.0, 1.30, 1.90, C["tool"], z_off=dz_string,
         label="tool crosslink sleeve (moving)")
    ring(ax, 72.0, 75.0, 0.0, 1.20, C["tool"], z_off=dz_string,
         label="tool setting mandrel (fixed)")


def fig_interface(state: str) -> None:
    sheared = state == "released"
    dz = 2.0 if sheared else 0.0
    fig, ax = plt.subplots(figsize=(15, 4.6), dpi=140)
    _draw_plug_top(ax, dz_outer=(-0.0))  # outer stack shift shown in sequence fig
    _draw_kit(ax, dz_string=dz, sheared=sheared)
    axis_line(ax, 43, 76 + dz)
    if not sheared:
        callout(ax, "shoe foot lands on carrier face\nat plug Z=51 (pushes outer stack down)",
                (51.0, 0.95), (44.5, 2.6))
        callout(ax, "shear stud ties plug neck to rod\n(holds mandrel up through the neck)",
                (57.6, 0.32), (53.5, -2.6))
        callout(ax, "tool stroke 10.0 in drives sleeve\ndown relative to rod = SET (DCN-8)",
                (66.0, 1.6), (60.0, 2.7))
        ttl = "SHEX-AK-20 interface — RIGGED (stroke 0): stud made up, shoe on carrier"
    else:
        callout(ax, "stud parted at neck Ø0.640\n(45 klbf): lower half stays in plug",
                (57.6, 0.32), (52.0, -2.6))
        callout(ax, "string (tool+rod+sleeve+stud top)\npulls free; GS fish head remains",
                (66.0, 1.6), (60.0, 2.7))
        ttl = "SHEX-AK-20 interface — RELEASED: stud sheared, string lifted"
    ax.set_title(ttl, fontsize=10.5)
    ax.set_xlabel("Plug Z (in)")
    ax.set_ylabel("R (in)")
    ax.set_xlim(43, 76 + dz + 1)
    ax.set_ylim(-3.4, 3.4)
    ax.set_aspect("equal")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=4, fontsize=7.4,
              frameon=False)
    ax.grid(alpha=0.15, lw=0.4)
    fig.tight_layout()
    fname = f"fig_kit_interface_{state}.png"
    fig.savefig(OUT / fname, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  ok {fname}")


def fig_string_ga() -> None:
    """Full run string, two conveyances. Schematic blocks (not to scale length)."""
    fig, axes = plt.subplots(2, 1, figsize=(15, 6.4), dpi=140)
    strings = [
        ("E-LINE", "electric wireline", [
            ("cable head\n/ CCL", 16, "#2b3a4a"),
            ("firing head\n+ charge", 14, "#7a2d2d"),
            ("Baker E-4 No. 20 WLPSA\n10.777 in stroke, 55 klbf, gas-generating", 80, C["tool"]),
        ]),
        ("COILED TUBING", "CT + pump pressure", [
            ("CT\nconnector", 16, "#2b3a4a"),
            ("ball-drop\n/ circ sub", 14, "#3a5a3a"),
            ("Baker Model J No. 20  (or B-20 / HST-425)\nhydraulic, multi-piston", 80, C["tool"]),
        ]),
    ]
    for ax, (mode, conv, blocks) in zip(axes, strings):
        x = 0.0
        # common lower end: adapter kit + plug
        seq = blocks + [
            ("SHEX-AK-20\nadapter kit", 18, "#d9822b"),
            ("SHEX-BP-UHEX-54 plug\nØ1.688 run-in, 57 in", 60, C["plug"]),
        ]
        total = sum(L for _, L, _ in seq)
        for name, L, col in seq:
            ax.add_patch(Rectangle((x, -0.5), L, 1.0, fc=col, ec="black", lw=0.6))
            ax.text(x + L / 2, 0.0, name, ha="center", va="center", fontsize=6.8,
                    color="white" if col not in (C["plug"], "#d9822b") else "black",
                    rotation=0, wrap=True)
            x += L
        ax.annotate(f"{mode}  ({conv})", xy=(0, 1.2), fontsize=10, fontweight="bold")
        ax.annotate("↓ downhole", xy=(total * 0.985, 1.05), fontsize=8, ha="right",
                    color="0.3")
        ax.set_xlim(-3, total + 3)
        ax.set_ylim(-1.4, 1.8)
        ax.set_axis_off()
    fig.suptitle("Run string — one #20 adapter kit serves both conveyances "
                 "(Model J uses the same kits as the E-4)", fontsize=11)
    fig.tight_layout()
    fig.savefig(OUT / "fig_string_ga.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  ok fig_string_ga.png")


def fig_two_stroke() -> None:
    """The two-actuator architecture: first (internal) then secondary (tool)."""
    fig, ax = plt.subplots(figsize=(15, 6.0), dpi=140)
    steps = [
        (0, "RUN IN", "Ø1.688 collapsed;\nEQ ports open;\nactuators armed", 1.688),
        (1, "FIRST stroke\n(internal)", "burst disk fires\nstage-1 bladder,\nthen stage-2\nBelleville —\nNO tool stroke", 5.75),
        (2, "SECONDARY\n0-4 in", "tool stroke\nbegins: stage-3\niris screws out", 8.636),
        (3, "SECONDARY\n4-10 in", "seals energize,\nslips bite,\nMTM preloads", 8.80),
        (4, "RELEASE", "45 klbf shears\nST-103 stud;\ntool pulls free\n— plug SET", 8.80),
    ]
    n = len(steps)
    dx = 3.4
    scale = 3.4 / (8.835 / 2)   # max plug half-height ~3.4
    for i, lbl, desc, od in steps:
        xc = i * dx
        for yy in (-3.95, 3.7):
            ax.add_patch(Rectangle((xc - 1.2, yy), 2.4, 0.22, fc="#b0b0b0", ec="none"))
        rr = od / 2 * scale
        ax.add_patch(Rectangle((xc - 0.62, -rr), 1.24, 2 * rr, fc=C["plug"], ec="black",
                               lw=0.5, zorder=3))
        ax.add_patch(Rectangle((xc - 0.13, -3.85), 0.26, 7.55, fc=C["mandrel"],
                               ec="none", zorder=2))
        ax.text(xc, 4.25, lbl, ha="center", va="bottom", fontsize=8.6,
                fontweight="bold")
        ax.text(xc, rr + 0.12, f"Ø{od:.3f}", ha="center", va="bottom", fontsize=6.8,
                color="0.3", zorder=5)
        ax.text(xc, -4.25, desc, ha="center", va="top", fontsize=7.2)
        if i < n - 1:
            ax.annotate("", xy=(xc + 1.55, 0), xytext=(xc + 0.75, 0),
                        arrowprops=dict(arrowstyle="-|>", lw=1.4, color="0.3"))
    # bracket the two stroke regimes (high, clear of titles)
    ax.annotate("", xy=(0.4, 6.0), xytext=(dx + 0.6, 6.0),
                arrowprops=dict(arrowstyle="|-|", lw=1.0, color="#7a2d2d"))
    ax.text((0.4 + dx + 0.6) / 2, 6.2, "FIRST — internal, self-powered", ha="center",
            fontsize=8, color="#7a2d2d")
    ax.annotate("", xy=(2 * dx - 0.6, 6.0), xytext=(4 * dx + 0.6, 6.0),
                arrowprops=dict(arrowstyle="|-|", lw=1.0, color="#1f4e79"))
    ax.text((2 * dx - 0.6 + 4 * dx + 0.6) / 2, 6.2,
            "SECONDARY — setting tool 10.0 in (E-4 #20 / Model J #20)", ha="center",
            fontsize=8, color="#1f4e79")
    ax.set_xlim(-1.8, 4 * dx + 1.8)
    ax.set_ylim(-6.2, 7.0)
    ax.set_aspect("equal")
    ax.set_axis_off()
    ax.set_title("Two-actuator setting architecture — the 10-in tool stroke is a SECONDARY "
                 "stroke after the internal first stroke", fontsize=11)
    fig.tight_layout()
    fig.savefig(OUT / "fig_two_stroke.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  ok fig_two_stroke.png")


def fig_market() -> None:
    """OD vs setting force, with tubing/casing passage lines — shows the conflict."""
    tools = [
        # name, od, force, stroke, kind, label dx, label dy
        ("E-4 #05", 1.718, 10.0, 5.879, "e-line", -0.30, 3.2),
        ("B105 (thru-tbg)", 1.810, 10.0, 6.0, "CT", 0.07, -3.5),
        ("E-4 #10", 2.750, 35.0, 5.707, "e-line", 0.07, 2.2),
        ("E-4 #20", 3.800, 55.0, 10.777, "e-line", -0.62, 2.6),
        ("Model J #20 / B-20", 3.800, 50.0, 11.0, "CT", 0.10, 1.2),
        ("HST 425", 3.800, 50.0, 11.0, "CT", 0.10, -3.0),
    ]
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=140)
    for name, od, force, stroke, kind, ldx, ldy in tools:
        col = "#1f4e79" if kind == "e-line" else "#3a7d3a"
        mk = "o" if kind == "e-line" else "s"
        ax.scatter(od, force, s=90, c=col, marker=mk, zorder=5, edgecolor="black",
                   linewidth=0.5)
        ax.annotate(f"{name}\n{stroke:.1f}in stroke", (od, force),
                    xytext=(od + ldx, force + ldy), fontsize=7.2,
                    ha="left" if ldx >= 0 else "right")
    # passage drift lines
    for x, lbl in [(1.995, '2-3/8" tbg drift 1.995'),
                   (2.441, '2-7/8" tbg drift 2.441'),
                   (3.833, '4-1/2" tbg drift 3.833')]:
        ax.axvline(x, ls="--", lw=0.9, color="0.5")
        ax.text(x, 60, lbl, rotation=90, va="top", ha="right", fontsize=7, color="0.4")
    # plug demand line
    ax.axhline(45, ls="-.", lw=1.1, color="#c0504d")
    ax.text(1.55, 46, "plug demand ≈ 45 klbf (release)", fontsize=8, color="#c0504d")
    ax.fill_betweenx([45, 60], 1.5, 1.995, alpha=0.12, color="#c0504d")
    ax.text(1.75, 30, "thru-tubing\n+ high force\n= empty\n(no market tool)",
            fontsize=8.5, ha="center", color="#7a2d2d")
    ax.set_xlabel("Tool OD (in)")
    ax.set_ylabel("Max setting force (klbf)")
    ax.set_xlim(1.5, 4.4)
    ax.set_ylim(0, 60)
    ax.set_title("Market setting tools: the OD-vs-force conflict\n"
                 "(circles = e-line E-4; squares = CT hydraulic; all use #20 adapter kits)",
                 fontsize=10.5)
    ax.grid(alpha=0.2, lw=0.4)
    fig.tight_layout()
    fig.savefig(OUT / "fig_market_conflict.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  ok fig_market_conflict.png")


def fig_stroke_budget() -> None:
    fig, ax = plt.subplots(figsize=(11, 4.4), dpi=140)
    demand = [("stage-3 iris", 4.0), ("seal lands x4", 4.0),
              ("slip set", 1.5), ("release overtravel", 0.5)]
    left = 0.0
    cols = ["#e0a800", "#3f7fbf", "#c0504d", "#888888"]
    for (lbl, w), col in zip(demand, cols):
        ax.barh(0, w, left=left, color=col, edgecolor="black", height=0.5)
        ax.text(left + w / 2, 0, f"{lbl}\n{w:.1f}", ha="center", va="center",
                fontsize=7.5, color="white")
        left += w
    ax.text(left + 0.1, 0, f"demand = {left:.2f} in", va="center", fontsize=9,
            fontweight="bold")
    tools = [("E-4 #20 (10.777)", 10.777, 0.9), ("Model J #20 / HST 425 (11.0)", 11.0, 1.4),
             ("E-4 #10 (5.707) — too short", 5.707, 1.9)]
    for lbl, val, y in tools:
        ok = val >= left
        ax.plot([0, val], [y, y], lw=6, color="#3a7d3a" if ok else "#b03030",
                solid_capstyle="butt", alpha=0.7)
        ax.plot([val, val], [y - 0.18, y + 0.18], lw=1.5, color="black")
        ax.text(val + 0.1, y, lbl, va="center", fontsize=8)
    ax.axvline(left, ls="--", color="#c0504d", lw=1.0)
    ax.set_xlim(0, 12.5)
    ax.set_ylim(-0.6, 2.4)
    ax.set_yticks([])
    ax.set_xlabel("Stroke (in)")
    ax.set_title("Setting stroke budget (secondary/tool stroke only — stages 1-2 are internal)",
                 fontsize=10.5)
    ax.grid(axis="x", alpha=0.2, lw=0.4)
    fig.tight_layout()
    fig.savefig(OUT / "fig_stroke_budget.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  ok fig_stroke_budget.png")


def main() -> None:
    fig_string_ga()
    fig_interface("rigged")
    fig_interface("released")
    fig_two_stroke()
    fig_market()
    fig_stroke_budget()


if __name__ == "__main__":
    main()
