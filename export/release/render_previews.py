"""Render PNG previews of the release geometry (assemblies + key parts)."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from stl import mesh as stl_mesh

ROOT = Path(__file__).resolve().parents[2]
REL = ROOT / "export" / "release"
PNG = REL / "png"
PNG.mkdir(exist_ok=True)


def render_stl(path: Path, out: Path, elev: float = 18, azim: float = -60,
               stretch_z: bool = False, max_r_mm: float | None = None,
               cut_half: bool = False) -> None:
    m = stl_mesh.Mesh.from_file(str(path))
    v = m.vectors  # (n, 3, 3)
    if max_r_mm is not None:
        rr = np.sqrt(v[:, :, 0] ** 2 + v[:, :, 1] ** 2).min(axis=1)
        v = v[rr < max_r_mm]
    if cut_half:
        v = v[v[:, :, 1].mean(axis=1) < 0.5]
    fig = plt.figure(figsize=(14, 6) if stretch_z else (8, 8), dpi=110)
    ax = fig.add_subplot(111, projection="3d")
    # z along the horizontal for long tools
    pts = v.reshape(-1, 3)
    zmin, zmax = pts[:, 2].min(), pts[:, 2].max()
    rmax = max(abs(pts[:, 0]).max(), abs(pts[:, 1]).max())
    # swap axes so tool axis is X for display
    vv = v[:, :, [2, 0, 1]]
    coll = Poly3DCollection(vv, alpha=0.95, linewidths=0.05)
    coll.set_facecolor((0.62, 0.66, 0.72))
    coll.set_edgecolor((0.25, 0.28, 0.33, 0.25))
    ax.add_collection3d(coll)
    ax.set_xlim(zmin, zmax)
    ax.set_ylim(-rmax, rmax)
    ax.set_zlim(-rmax, rmax)
    if stretch_z:
        ax.set_box_aspect((zmax - zmin, 2 * rmax * 3, 2 * rmax * 3))
    else:
        ax.set_box_aspect((zmax - zmin, 2 * rmax, 2 * rmax))
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()
    fig.tight_layout(pad=0)
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  ok {out.name}")


def mesh_step_to_stl(step: Path, out_stl: Path, size_mm: float = 1.5) -> None:
    import gmsh
    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 0)
    gmsh.merge(str(step))
    gmsh.option.setNumber("Mesh.MeshSizeMax", size_mm)
    gmsh.option.setNumber("Mesh.MeshSizeMin", size_mm / 6)
    gmsh.model.mesh.generate(2)
    gmsh.write(str(out_stl))
    gmsh.finalize()


def main() -> None:
    # assemblies
    run_stl = REL / "stl" / "SHEX-BP-UHEX-54_RUN-IN.stl"
    set_stl = REL / "stl" / "SHEX-BP-UHEX-54_SET.stl"
    if run_stl.exists():
        render_stl(run_stl, PNG / "SHEX-BP-UHEX-54_RUN-IN.png", elev=14, azim=-55)
        render_stl(run_stl, PNG / "SHEX-BP-UHEX-54_RUN-IN_section.png",
                   elev=10, azim=-90, cut_half=True)
    if set_stl.exists():
        # exclude the casing reference body (r > 110 mm) so the tool is visible
        render_stl(set_stl, PNG / "SHEX-BP-UHEX-54_SET.png", elev=14, azim=-55,
                   max_r_mm=112.0)
        render_stl(set_stl, PNG / "SHEX-BP-UHEX-54_SET_section.png",
                   elev=10, azim=-90, max_r_mm=112.0, cut_half=True)

    # key parts
    parts = [
        ("SHEX-011_inner_mandrel", 1.5),
        ("SHEX-002_helix_guide", 0.7),
        ("SHEX-010_support_sleeve", 0.8),
        ("SHEX-001_iris_segment", 0.8),
        ("SHEX-008_stage1_stent_runin", 0.6),
        ("SHEX-012_fishing_neck", 0.8),
        ("SHEX-013_equalizing_sub_body", 0.5),
    ]
    tmp = REL / "stl" / "_tmp"
    tmp.mkdir(exist_ok=True)
    for pname, sz in parts:
        step = REL / "step" / "parts" / f"{pname}.stp"
        if not step.exists():
            continue
        s = tmp / f"{pname}.stl"
        try:
            mesh_step_to_stl(step, s, sz)
            render_stl(s, PNG / f"{pname}.png", elev=20, azim=-60)
        except Exception as e:  # noqa: BLE001
            print(f"  FAIL {pname}: {e}")


if __name__ == "__main__":
    main()
