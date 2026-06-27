"""Stage 1/2 internal actuator (SHEX-014/015/016) manual figures.

2D sections: tool axis horizontal (plug Z, inches), radius vertical (inches).
Dimensions mirror cad/actuator_solids.py and export/analysis/actuator_design.py.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUT = Path(__file__).parent / "figures"
OUT.mkdir(exist_ok=True)
ANALYSIS = Path(__file__).resolve().parents[2] / "analysis" / "actuator_design.json"

C = {
    "mandrel": "#8898aa",
    "stent": "#9aa7b4",
    "bladder": "#b5651d",
    "gland": "#5f7d8c",
    "lock": "#c0504d",
    "belle": "#4f9d69",
    "charge": "#37485e",
    "pilot": "#c9a227",
}

NECK_OD = 1.270
STENT_ID, STENT_OD = 1.562, 1.688
S1 = (9.5, 13.5)
S2 = (13.5, 18.5)
S1_DEP, S2_DEP = 3.375, 5.750


def ring(ax, z0, z1, r_in, r_out, color, alpha=1.0, ec="black", lw=0.5, z=3,
         label=None):
    for sgn in (1, -1):
        y = r_in if sgn > 0 else -r_out
        ax.add_patch(Rectangle((z0, y), z1 - z0, r_out - r_in, fc=color, ec=ec,
                               lw=lw, alpha=alpha, zorder=z,
                               label=label if sgn > 0 else None))


def callout(ax, x, y, text, xt, yt, color="black", fs=8):
    ax.annotate(text, xy=(x, y), xytext=(xt, yt), fontsize=fs, color=color,
                ha="center", va="center",
                arrowprops=dict(arrowstyle="-", lw=0.7, color=color))


def axis_line(ax, z0, z1):
    ax.plot([z0, z1], [0, 0], "k-.", lw=0.5, alpha=0.5, zorder=1)


# ---------------------------------------------------------------------------


def fig_section(state: str) -> None:
    fig, ax = plt.subplots(figsize=(13, 5.4), dpi=140)
    axis_line(ax, 6.0, 21.0)
    # mandrel neck
    ring(ax, 8.7, 19.3, 0.0, NECK_OD / 2, C["mandrel"], z=2, label="mandrel neck Ø1.270")
    ring(ax, 6.0, 8.9, 0.0, 1.550 / 2, C["mandrel"], z=2)
    ring(ax, 19.1, 21.0, 0.0, 1.550 / 2, C["mandrel"], z=2)

    if state == "run_in":
        # stents collapsed at 1.688
        ring(ax, *S1, STENT_ID / 2, STENT_OD / 2, C["stent"], z=4,
             label="stent sleeve (mesh)")
        ring(ax, *S2, STENT_ID / 2, STENT_OD / 2, C["stent"], z=4)
        # bladders folded in the annulus
        ring(ax, S1[0] + 0.45, S1[1] - 0.40, NECK_OD / 2, 1.462 / 2, C["bladder"],
             z=3, label="bladder (folded)")
        ring(ax, S2[0] + 0.45, S2[1] - 0.40, NECK_OD / 2, 1.462 / 2, C["bladder"], z=3)
        title = "Stage 1/2 actuators — RUN-IN (Ø1.688, bladders folded in the annulus)"
    else:
        ring(ax, *S1, S1_DEP / 2 - 0.045, S1_DEP / 2, C["stent"], z=4,
             label="stent (deployed)")
        ring(ax, *S2, S2_DEP / 2 - 0.045, S2_DEP / 2, C["stent"], z=4)
        ring(ax, S1[0] + 0.45, S1[1] - 0.40, NECK_OD / 2, (S1_DEP - 0.126) / 2,
             C["bladder"], z=3, alpha=0.85, label="bladder (inflated)")
        ring(ax, S2[0] + 0.45, S2[1] - 0.40, NECK_OD / 2, (S2_DEP - 0.126) / 2,
             C["bladder"], z=3, alpha=0.85)
        callout(ax, (S1[0] + S1[1]) / 2, S1_DEP / 2, "stage 1\nØ3.375",
                (S1[0] + S1[1]) / 2, S1_DEP / 2 + 0.5)
        callout(ax, (S2[0] + S2[1]) / 2, S2_DEP / 2, "stage 2\nØ5.750",
                (S2[0] + S2[1]) / 2, S2_DEP / 2 + 0.4)
        title = "Stage 1/2 actuators — DEPLOYED (first stroke complete, before tool stroke)"

    # glands, lock rings, charge subs, belleville, pilot, chamber (both states)
    for z0 in (S1[0] + 0.05, S1[1] - 0.40, S2[0] + 0.05, S2[1] - 0.40):
        ring(ax, z0, z0 + 0.35, NECK_OD / 2, 1.550 / 2, C["gland"], z=5)
    ring(ax, S1[0] - 0.30, S1[0] - 0.30 + 0.40, NECK_OD / 2, 1.500 / 2, C["lock"], z=5,
         label="body-lock ratchet")
    ring(ax, S2[0] - 0.30, S2[0] - 0.30 + 0.40, NECK_OD / 2, 1.500 / 2, C["lock"], z=5)
    for i in range(4):
        ring(ax, S2[1] + 0.05 + i * 0.055, S2[1] + 0.05 + i * 0.055 + 0.05,
             1.290 / 2, 1.540 / 2, C["belle"], z=6,
             label="Belleville hold" if i == 0 else None)
    ring(ax, S2[1] + 0.35, S2[1] + 0.35 + 1.20, 1.460 / 2, 1.550 / 2, C["charge"], z=4)
    # charge chamber + pilot piston below stage 1
    ring(ax, S1[0] - 3.10, S1[0] - 1.10, 1.300 / 2, 1.550 / 2, C["charge"], z=4,
         label="charge / ref chamber")
    ring(ax, S1[0] - 1.60, S1[0] - 1.30, 0.0, 1.450 / 2, C["pilot"], z=5,
         label="EQ pilot piston")
    ring(ax, S1[0] - 0.95, S1[0] - 0.40, 0.0, 0.500 / 2, "#222", z=6,
         label="burst-disk charge sub")
    ring(ax, S2[0] - 0.55, S2[0] - 0.05, 0.0, 0.500 / 2, "#222", z=6)

    ax.set_xlim(6.0, 21.5)
    ax.set_ylim(-3.2, 3.4)
    ax.set_aspect("equal")
    ax.set_xlabel("Plug Z (in)")
    ax.set_ylabel("R (in)")
    ax.set_title(title, fontsize=11)
    ax.legend(loc="lower right", fontsize=6.6, ncol=2, framealpha=0.9)
    fig.tight_layout()
    fig.savefig(OUT / f"fig_act_section_{state}.png", facecolor="white")
    plt.close(fig)
    print(f"  ok fig_act_section_{state}.png")


def fig_sequence() -> None:
    fig, ax = plt.subplots(figsize=(14, 5.6), dpi=140)
    steps = [
        ("RUN-IN", "Ø1.688 collapsed;\nEQ ports OPEN;\ngate ARMED (DCN-12)", 1.688, "#8898aa"),
        ("EQ CLOSE", "by COMMAND (CT dP+ball\n/ e-line EFI): pilot closes\nSHEX-013 -> arms S1", 1.688, "#c9a227"),
        ("STAGE 1", "S1 bladder inflates ->\nstent 1; bottom-out shift\narms stage 2", 3.375, "#b5651d"),
        ("STAGE 2", "S2 bladder inflates ->\nstent 2 -> 'ready'\nsignature", 5.750, "#b5651d"),
        ("HAND OFF", "lock rings hold;\nBelleville preload;\ntool 10-in stroke next", 5.750, "#4f9d69"),
    ]
    n = len(steps)
    dx = 3.2
    scale = 3.0 / (5.750 / 2)
    for i, (lbl, desc, od, col) in enumerate(steps):
        xc = i * dx
        for yy in (-3.35, 3.15):
            ax.add_patch(Rectangle((xc - 1.2, yy), 2.4, 0.2, fc="#b0b0b0", ec="none"))
        rr = od / 2 * scale
        ax.add_patch(Rectangle((xc - 0.55, -rr), 1.1, 2 * rr, fc=col, ec="black",
                               lw=0.5, zorder=3))
        ax.add_patch(Rectangle((xc - 0.11, -3.25), 0.22, 6.4, fc="#6b7580",
                               ec="none", zorder=2))
        ax.text(xc, 3.55, lbl, ha="center", va="bottom", fontsize=9, fontweight="bold")
        ax.text(xc, rr + 0.1, f"Ø{od:.3f}", ha="center", va="bottom", fontsize=6.8,
                color="0.3", zorder=5)
        ax.text(xc, -3.6, desc, ha="center", va="top", fontsize=7.2)
        if i < n - 1:
            ax.annotate("", xy=(xc + 1.45, 0), xytext=(xc + 0.7, 0),
                        arrowprops=dict(arrowstyle="-|>", lw=1.4, color="0.3"))
    ax.annotate("", xy=(1 * dx - 0.6, 4.7), xytext=(3 * dx + 0.6, 4.7),
                arrowprops=dict(arrowstyle="|-|", lw=1.0, color="#7a2d2d"))
    ax.text(2 * dx, 4.9, "FIRST STROKE — internal, pressure-driven (no setting-tool stroke)",
            ha="center", fontsize=8.5, color="#7a2d2d")
    ax.set_xlim(-1.7, 4 * dx + 1.7)
    ax.set_ylim(-5.0, 5.4)
    ax.set_aspect("equal")
    ax.set_axis_off()
    ax.set_title("Internal first-stroke sequence — Ø1.688 → Ø5.750 before the tool ever strokes",
                 fontsize=11)
    fig.tight_layout()
    fig.savefig(OUT / "fig_act_sequence.png", facecolor="white")
    plt.close(fig)
    print("  ok fig_act_sequence.png")


def fig_pressure() -> None:
    d = json.loads(ANALYSIS.read_text()) if ANALYSIS.exists() else {}
    s1_dep = d.get("Stage 1_deploy_psi", 941)
    s1_hold = d.get("Stage 1_hold_psi", 470)
    s2_dep = d.get("Stage 2_deploy_psi", 470)
    s2_hold = d.get("Stage 2_hold_psi", 276)
    rating = d.get("stage1_bladder_rating_psi", 2500)
    fig, ax = plt.subplots(figsize=(11, 5.6), dpi=140)
    cats = ["Stage 1\ndeploy", "Stage 1\nhold", "Stage 2\ndeploy", "Stage 2\nhold"]
    vals = [s1_dep, s1_hold, s2_dep, s2_hold]
    ax.bar(cats, vals, color=["#b5651d", "#d4a373", "#b5651d", "#d4a373"],
           edgecolor="black", zorder=3)
    for x, v in zip(cats, vals):
        ax.text(x, v + 30, f"{v:.0f}", ha="center", fontsize=8)
    for ft, ppg, ls in ((8000, 9.0, "-"), (3000, 9.0, "--")):
        p = 0.052 * ppg * ft
        ax.axhline(p, color="#1f4e79", ls=ls, lw=1.2, zorder=2)
        ax.text(3.4, p + 30, f"hydrostatic @ {ft} ft, {ppg:.0f} ppg = {p:.0f} psi",
                ha="right", fontsize=7.4, color="#1f4e79")
    ax.axhline(rating, color="#c0504d", ls="-.", lw=1.2)
    ax.text(0.0, rating + 30, f"bladder design rating {rating} psi", fontsize=7.4,
            color="#c0504d")
    ax.set_ylabel("Pressure (psi)")
    ax.set_ylim(0, max(rating, 4200) + 400)
    ax.set_title("Bladder pressure budget — required deploy/hold vs available "
                 "hydrostatic (first-order)", fontsize=10.5)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "fig_act_pressure.png", facecolor="white")
    plt.close(fig)
    print("  ok fig_act_pressure.png")


def fig_why_bladder() -> None:
    fig, ax = plt.subplots(figsize=(11, 5.0), dpi=140)
    # annulus budget bar + impossibility of rigid swage
    ax.barh(["available annulus\n(radial)"], [0.146], color="#4f9d69",
            edgecolor="black", zorder=3)
    ax.text(0.146 + 0.02, 0, "0.146 in", va="center", fontsize=9)
    ax.set_xlim(0, 2.6)
    ax.set_xlabel("Radial dimension (in)")
    ax.set_title("Why both stages are inflatable bladders (DCN-11)", fontsize=11)
    txt = ("A rigid swage / Belleville-wedge must start ≤ stent ID 1.562 (r 0.781)\n"
           "yet reach r 2.812 to back the Ø5.624 deployed stent — it cannot grow\n"
           "1.27 → 5.62 inside a 0.146-in annulus. Only a folded element that\n"
           "inflates can. ⇒ Stage 2 = second bladder; Belleville = hold-only.")
    ax.text(0.6, -0.42, txt, fontsize=9, va="top", ha="left",
            bbox=dict(boxstyle="round", fc="#f5efe6", ec="#b5651d"))
    fig.tight_layout()
    fig.savefig(OUT / "fig_act_why_bladder.png", facecolor="white")
    plt.close(fig)
    print("  ok fig_act_why_bladder.png")


def fig_trigger_interlock() -> None:
    """DCN-12: why the passive trigger fails (left) and the commanded /
    completion-gated architecture that replaces it (right)."""
    fig, (axl, axr) = plt.subplots(1, 2, figsize=(14, 6.0), dpi=140,
                                   gridspec_kw={"width_ratios": [1, 1.5]})

    # --- left: passive hydrostatic trigger fires during run-in --------------
    axl.set_title("Passive hydrostatic burst disk — FAILS", fontsize=10.5,
                  color="#7a2d2d")
    axl.plot([0, 0], [0, 12000], color="0.6", lw=8, solid_capstyle="butt",
             alpha=0.5)
    axl.annotate("", xy=(0, 11500), xytext=(0, 200),
                 arrowprops=dict(arrowstyle="-|>", lw=1.6, color="#37485e"))
    axl.text(0.18, 11000, "run-in\n(depth increases,\nhydrostatic rises)",
             fontsize=8, va="top")
    for p, lbl in ((941, "p1 crack = 941 psi\n-> FIRES at ~1810 ft"),
                   (470, "p2 crack = 470 psi\n-> FIRES at ~905 ft")):
        depth = p / (0.052 * 9.0)
        axl.axhline(depth, color="#c0504d", ls="--", lw=1.1)
        axl.text(0.18, depth, lbl, fontsize=7.6, va="center", color="#c0504d")
    axl.text(0, -900, "both disks fire on the way DOWN,\nnot at target depth — no position control",
             fontsize=8, ha="center", va="top", color="#7a2d2d")
    axl.set_ylim(12200, -2200)
    axl.set_xlim(-0.5, 1.6)
    axl.set_ylabel("Depth (ft)")
    axl.set_xticks([])

    # --- right: DCN-12 commanded + completion-gated chain -------------------
    axr.set_title("DCN-12 — commanded initiation + completion-gated sequence",
                  fontsize=10.5, color="#1f5e3a")
    chain = [
        ("COMMAND", "CT applied dP (+1500 psi)\n+ ball seat  OR  e-line EFI", "#c9a227"),
        ("GATE OPEN", "SHEX-017 admits the well\n(CT fluid / hydrostatic)", "#37485e"),
        ("EQ CLOSE", "pilot strokes first ->\nSHEX-013 ports shut", "#6a8caf"),
        ("STAGE 1", "bladder -> Ø3.375;\nbottom-out shifts 017A", "#b5651d"),
        ("STAGE 2", "feed uncovered ->\nbladder -> Ø5.750", "#b5651d"),
        ("READY", "ratchets hold; hand off to\nthe tool's 10-in stroke", "#4f9d69"),
    ]
    y = 9
    for i, (lbl, desc, col) in enumerate(chain):
        yc = y - i * 1.55
        axr.add_patch(Rectangle((0.2, yc - 0.55), 2.0, 1.05, fc=col, ec="black",
                                lw=0.6, alpha=0.92))
        axr.text(1.2, yc, lbl, ha="center", va="center", fontsize=9,
                 fontweight="bold", color="white")
        axr.text(2.45, yc, desc, ha="left", va="center", fontsize=8)
        if i < len(chain) - 1:
            axr.annotate("", xy=(1.2, yc - 1.0), xytext=(1.2, yc - 0.6),
                         arrowprops=dict(arrowstyle="-|>", lw=1.5, color="0.3"))
    axr.text(1.2, y + 1.15, "position-correct, run-in-safe; order is MECHANICAL",
             ha="center", fontsize=8.4, color="#1f5e3a")
    axr.set_xlim(0, 7.2)
    axr.set_ylim(0.2, 11)
    axr.set_axis_off()

    fig.suptitle("First-stroke trigger & equalizing interlock (SHEX-EM-001 / DCN-12)",
                 fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(OUT / "fig_act_trigger.png", facecolor="white")
    plt.close(fig)
    print("  ok fig_act_trigger.png")


def main() -> None:
    fig_section("run_in")
    fig_section("deployed")
    fig_sequence()
    fig_pressure()
    fig_why_bladder()
    fig_trigger_interlock()


if __name__ == "__main__":
    main()
