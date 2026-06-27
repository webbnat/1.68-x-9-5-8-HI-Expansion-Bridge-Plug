"""Brief setting-sequence animation (run-in -> full set) for SHEX-BP-UHEX-54.

Driven by the real tool geometry (cad/release_solids MODULE_Z + deployed ODs):
each module expands in the true setting order, the mandrel makes its 10-in
secondary stroke, and the result is written as an animated GIF.

Rendered with matplotlib 3D surfaces (no per-frame meshing) for speed/robustness.
Run:  .venv\\Scripts\\python export/full_tool/animate_setting.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

OUT = Path(__file__).parent
GIF = OUT / "SHEX-BP-UHEX-54_setting_sequence.gif"

RUN_OD = 1.688
SET_STROKE = 10.0

# module Z map (plug coords) — mirrors cad/release_solids.MODULE_Z
MOD = {
    "mandrel_tail": (0.0, 3.0),
    "bottom_sub": (3.0, 5.0),
    "lower_slips": (5.0, 9.5),
    "stage1": (9.5, 13.5),
    "stage2": (13.5, 18.5),
    "stage3_iris": (18.5, 26.0),
    "seal_land_1": (26.0, 30.5),
    "seal_land_2": (30.5, 35.0),
    "seal_land_3": (35.0, 39.5),
    "seal_land_4": (39.5, 44.0),
    "upper_mtm": (44.0, 46.5),
    "upper_slips": (46.5, 51.0),
}

# deployed OD + expansion window (global progress p) + colour, in setting order
SET_OD = {
    "lower_slips": (8.720, 0.74, 0.88, "#b08d57"),
    "stage1": (3.375, 0.12, 0.26, "#b5651d"),
    "stage2": (5.750, 0.26, 0.42, "#b5651d"),
    "stage3_iris": (8.650, 0.42, 0.58, "#6a8caf"),
    "seal_land_1": (8.720, 0.58, 0.74, "#c0504d"),
    "seal_land_2": (8.720, 0.58, 0.74, "#c0504d"),
    "seal_land_3": (8.720, 0.58, 0.74, "#c0504d"),
    "seal_land_4": (8.720, 0.58, 0.74, "#c0504d"),
    "upper_mtm": (8.800, 0.74, 0.88, "#c9a227"),
    "upper_slips": (8.720, 0.74, 0.88, "#b08d57"),
}
STATIC = {  # never expand
    "mandrel_tail": ("#555a61", 1.350),
    "bottom_sub": ("#7d8893", RUN_OD),
}

PHASES = [
    (0.00, 0.12, "RUN IN  —  Ø1.688, equalizing ports open"),
    (0.12, 0.26, "FIRST STROKE (internal): Stage 1 bladder  →  Ø3.375"),
    (0.26, 0.42, "FIRST STROKE (internal): Stage 2 bladder  →  Ø5.750"),
    (0.42, 0.58, "SECONDARY STROKE (tool): Stage 3 iris  →  Ø8.650"),
    (0.58, 0.74, "SECONDARY STROKE (tool): 4 seal lands energize  →  Ø8.720"),
    (0.74, 0.88, "SECONDARY STROKE (tool): slips bite + MTM  →  Ø8.800"),
    (0.88, 1.01, "FULL SET  —  anchored & sealed; tool releases"),
]


def smooth(a: float, b: float, p: float) -> float:
    if p <= a:
        return 0.0
    if p >= b:
        return 1.0
    t = (p - a) / (b - a)
    return t * t * (3 - 2 * t)


def caption(p: float) -> str:
    for a, b, txt in PHASES:
        if a <= p < b:
            return txt
    return PHASES[-1][2]


def cylinder(ax, z0, z1, r, color, ntheta=28, alpha=1.0):
    theta = np.linspace(0, 2 * np.pi, ntheta)
    x = np.array([z0, z1])
    th, xx = np.meshgrid(theta, x)
    yy = r * np.cos(th)
    zz = r * np.sin(th)
    ax.plot_surface(xx, yy, zz, color=color, alpha=alpha, linewidth=0,
                    antialiased=True, shade=True, zorder=2)
    # end cap at the larger face for solidity
    tt = np.linspace(0, 2 * np.pi, ntheta)
    rr = np.linspace(0, r, 2)
    TT, RR = np.meshgrid(tt, rr)
    for xc in (z0, z1):
        ax.plot_surface(np.full_like(TT, xc), RR * np.cos(TT), RR * np.sin(TT),
                        color=color, alpha=alpha, linewidth=0, shade=True)


def draw_frame(p: float):
    fig = plt.figure(figsize=(11, 3.6), dpi=110)
    ax = fig.add_subplot(111, projection="3d")
    dz = SET_STROKE * smooth(0.42, 0.88, p)   # mandrel secondary stroke

    # central mandrel (rides +dz) — thin, mostly hidden, visible at the pin
    cylinder(ax, 0.0 + dz, 52.0 + dz, 1.550 / 2, "#4c5158", alpha=1.0)
    # fishing neck pin (extends as it strokes out)
    cylinder(ax, 51.0 + dz, 57.0 + dz, 1.375 / 2, "#3f444a", alpha=1.0)

    # static modules
    for name, (color, od) in STATIC.items():
        z0, z1 = MOD[name]
        cylinder(ax, z0, z1, od / 2, color)

    # expanding modules
    for name, (set_od, a, b, color) in SET_OD.items():
        z0, z1 = MOD[name]
        od = RUN_OD + (set_od - RUN_OD) * smooth(a, b, p)
        cylinder(ax, z0, z1, od / 2, color)

    # faint casing ID rings (top/bottom wireframe) so expansion reads to-casing
    cid = 8.835 / 2
    for ang in np.linspace(0, 2 * np.pi, 60):
        pass
    ax.plot([0, 67], [cid, cid], [0, 0], color="0.7", lw=0.6, ls="--")
    ax.plot([0, 67], [-cid, -cid], [0, 0], color="0.7", lw=0.6, ls="--")

    ax.set_xlim(0, 67)
    ax.set_ylim(-cid - 0.3, cid + 0.3)
    ax.set_zlim(-cid - 0.3, cid + 0.3)
    ax.set_box_aspect((67, 2 * cid, 2 * cid))
    ax.view_init(elev=16, azim=-62)
    ax.set_axis_off()
    # progress bar + caption
    fig.text(0.5, 0.93, "SHEX-BP-UHEX-54  —  setting sequence", ha="center",
             fontsize=11, weight="bold")
    fig.text(0.5, 0.86, caption(p), ha="center", fontsize=9, color="#7a2d2d")
    ax2 = fig.add_axes([0.12, 0.06, 0.76, 0.03])
    ax2.barh([0], [p], color="#37485e", height=1.0)
    ax2.barh([0], [1.0], color="#dddddd", height=1.0, zorder=0)
    ax2.set_xlim(0, 1)
    ax2.set_axis_off()
    fig.canvas.draw()
    w, h = fig.canvas.get_width_height()
    img = Image.frombuffer("RGBA", (w, h), fig.canvas.buffer_rgba(), "raw",
                           "RGBA", 0, 1).convert("RGB")
    plt.close(fig)
    return img


def main():
    # ramp up, brief hold at full set
    ps = list(np.linspace(0.0, 1.0, 40)) + [1.0] * 6
    frames = [draw_frame(p) for p in ps]
    frames[0].save(GIF, save_all=True, append_images=frames[1:], duration=110,
                   loop=0, optimize=True)
    print(f"  ok  {GIF}  ({len(frames)} frames)")


if __name__ == "__main__":
    main()
