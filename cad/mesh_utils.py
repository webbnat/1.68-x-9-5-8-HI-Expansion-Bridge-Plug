"""Pure-Python mesh generation for STL export (no OpenCASCADE required)."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from stl import mesh


@dataclass
class MeshData:
    vertices: np.ndarray  # (N, 3)
    faces: np.ndarray  # (M, 3) int indices

    def to_stl_mesh(self) -> mesh.Mesh:
        data = np.zeros(len(self.faces), dtype=mesh.Mesh.dtype)
        for i, (a, b, c) in enumerate(self.faces):
            tri = self.vertices[[a, b, c]]
            data["vectors"][i] = tri
        return mesh.Mesh(data, remove_empty_areas=False)


def _append(meshes: list[MeshData], other: MeshData) -> None:
    if len(other.vertices) == 0:
        return
    offset = len(meshes[-1].vertices) if meshes else 0
    if not meshes:
        meshes.append(other)
        return
    base = meshes[0]
    v = np.vstack([base.vertices, other.vertices])
    f = np.vstack([base.faces, other.faces + offset])
    meshes[0] = MeshData(v, f)


def merge(*parts: MeshData) -> MeshData:
    if not parts:
        return MeshData(np.empty((0, 3)), np.empty((0, 3), dtype=int))
    v = parts[0].vertices
    f = parts[0].faces
    for p in parts[1:]:
        off = len(v)
        v = np.vstack([v, p.vertices])
        f = np.vstack([f, p.faces + off])
    return MeshData(v, f)


def cylinder(
    radius: float,
    height: float,
    segments: int = 48,
    center: tuple[float, float, float] = (0, 0, 0),
) -> MeshData:
    cx, cy, cz = center
    angles = np.linspace(0, 2 * math.pi, segments, endpoint=False)
    bottom = np.column_stack([radius * np.cos(angles), radius * np.sin(angles), np.zeros(segments)])
    top = bottom.copy()
    top[:, 2] = height
    verts = np.vstack([bottom, top, [[0, 0, 0], [0, 0, height]]])
    b_center, t_center = 2 * segments, 2 * segments + 1
    faces = []
    for i in range(segments):
        j = (i + 1) % segments
        bi, bj = i, j
        ti, tj = i + segments, j + segments
        faces.append([bi, bj, ti])
        faces.append([ti, bj, tj])
        faces.append([b_center, bj, bi])
        faces.append([t_center, ti, tj])
    v = verts + np.array([cx, cy, cz])
    return MeshData(v, np.array(faces, dtype=int))


def tube(
    outer_r: float,
    inner_r: float,
    height: float,
    segments: int = 48,
    center: tuple[float, float, float] = (0, 0, 0),
) -> MeshData:
    outer = cylinder(outer_r, height, segments)
    inner = cylinder(inner_r, height, segments)
    # Flip inner normals by reversing winding
    inner.faces = inner.faces[:, [0, 2, 1]]
    return merge(outer, inner)


def cone(
    r_bottom: float,
    r_top: float,
    height: float,
    segments: int = 48,
    center: tuple[float, float, float] = (0, 0, 0),
) -> MeshData:
    cx, cy, cz = center
    angles = np.linspace(0, 2 * math.pi, segments, endpoint=False)
    bot = np.column_stack([r_bottom * np.cos(angles), r_bottom * np.sin(angles), np.zeros(segments)])
    top = np.column_stack([r_top * np.cos(angles), r_top * np.sin(angles), np.full(segments, height)])
    verts = np.vstack([bot, top, [[0, 0, 0], [0, 0, height]]])
    bc, tc = 2 * segments, 2 * segments + 1
    faces = []
    for i in range(segments):
        j = (i + 1) % segments
        bi, bj, ti, tj = i, j, i + segments, j + segments
        faces.append([bi, bj, ti])
        faces.append([ti, bj, tj])
        if r_bottom > 0:
            faces.append([bc, bj, bi])
        if r_top > 0:
            faces.append([tc, ti, tj])
    return MeshData(verts + np.array([cx, cy, cz]), np.array(faces, dtype=int))


def box(
    lx: float,
    ly: float,
    lz: float,
    center: tuple[float, float, float] = (0, 0, 0),
) -> MeshData:
    cx, cy, cz = center
    hx, hy, hz = lx / 2, ly / 2, lz / 2
    corners = np.array(
        [
            [-hx, -hy, -hz],
            [hx, -hy, -hz],
            [hx, hy, -hz],
            [-hx, hy, -hz],
            [-hx, -hy, hz],
            [hx, -hy, hz],
            [hx, hy, hz],
            [-hx, hy, hz],
        ]
    ) + np.array([cx, cy, cz])
    faces = [
        [0, 1, 2],
        [0, 2, 3],
        [4, 6, 5],
        [4, 7, 6],
        [0, 4, 5],
        [0, 5, 1],
        [2, 6, 7],
        [2, 7, 3],
        [0, 3, 7],
        [0, 7, 4],
        [1, 5, 6],
        [1, 6, 2],
    ]
    return MeshData(corners, np.array(faces, dtype=int))


def rotate_z(data: MeshData, angle_deg: float) -> MeshData:
    a = math.radians(angle_deg)
    c, s = math.cos(a), math.sin(a)
    m = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    return MeshData(data.vertices @ m.T, data.faces.copy())


def translate(data: MeshData, dx: float, dy: float, dz: float) -> MeshData:
    return MeshData(data.vertices + np.array([dx, dy, dz]), data.faces.copy())


def stent_lattice(
    od: float,
    wall: float,
    length: float,
    cells: int = 12,
    rings: int = 8,
    strut_w: float = 0.045,
) -> MeshData:
    """Zig-zag ring stent pattern as merged thin boxes."""
    outer_r = od / 2
    inner_r = outer_r - wall
    base = tube(outer_r, inner_r, length, segments=64)

    parts = [base]
    margin = length * 0.06
    pitch = (length - 2 * margin) / max(rings - 1, 1)
    strut_t = wall * 0.85

    for ring in range(rings):
        z = margin + ring * pitch
        phase = 0 if ring % 2 == 0 else math.pi / cells
        for i in range(cells):
            a0 = phase + 2 * math.pi * i / cells
            a1 = phase + 2 * math.pi * (i + 0.5) / cells
            r0 = outer_r * (1.0 if i % 2 == 0 else 0.88)
            r1 = outer_r * (0.88 if i % 2 == 0 else 1.0)
            x0, y0 = r0 * math.cos(a0), r0 * math.sin(a0)
            x1, y1 = r1 * math.cos(a1), r1 * math.sin(a1)
            mx, my = (x0 + x1) / 2, (y0 + y1) / 2
            seg = math.hypot(x1 - x0, y1 - y0)
            angle = math.degrees(math.atan2(y1 - y0, x1 - x0))
            b = box(seg, strut_w, strut_t, center=(mx, my, z))
            b = rotate_z(b, angle)
            parts.append(b)

        if ring < rings - 1:
            z2 = margin + (ring + 1) * pitch
            zm = (z + z2) / 2
            for c in range(cells // 2):
                ang = 2 * math.pi * c / cells + (math.pi / cells if ring % 2 else 0)
                x, y = outer_r * math.cos(ang), outer_r * math.sin(ang)
                conn = box(strut_w * 0.8, strut_w * 0.8, (z2 - z) * 0.6, center=(x, y, zm))
                parts.append(conn)

    return merge(*parts)


def wedge_profile(
    base_w: float,
    height: float,
    thickness: float,
    center: tuple[float, float, float] = (0, 0, 0),
) -> MeshData:
    """Triangular wedge (slip / petal)."""
    cx, cy, cz = center
    v = np.array(
        [
            [0, 0, 0],
            [base_w, 0, 0],
            [base_w * 0.55, height, 0],
            [0, height * 0.9, 0],
            [0, 0, thickness],
            [base_w, 0, thickness],
            [base_w * 0.55, height, thickness],
            [0, height * 0.9, thickness],
        ]
    ) + np.array([cx, cy, cz])
    faces = [
        [0, 1, 2],
        [0, 2, 3],
        [4, 6, 5],
        [4, 7, 6],
        [0, 4, 5],
        [0, 5, 1],
        [1, 5, 6],
        [1, 6, 2],
        [2, 6, 7],
        [2, 7, 3],
        [3, 7, 4],
        [3, 4, 0],
    ]
    return MeshData(v, np.array(faces, dtype=int))


def export_mesh(data: MeshData, path: str, scale: float = 25.4) -> None:
    """Export mesh; coordinates assumed inches, STL in mm."""
    m = data.to_stl_mesh()
    m.vectors *= scale
    m.save(path)
