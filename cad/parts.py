"""Mechanical bridge plug components (non-stent parts)."""

from __future__ import annotations

import cadquery as cq


def inner_mandrel(od_in: float = 1.35, length_in: float = 14.0) -> cq.Workplane:
    """Delivery mandrel — catheter core analog."""
    return cq.Workplane("XY").circle(od_in / 2).extrude(length_in)


def outer_sheath(id_in: float = 1.72, od_in: float = 1.82, length_in: float = 5.0) -> cq.Workplane:
    """Run-in protective sheath over collapsed stent."""
    return (
        cq.Workplane("XY")
        .circle(od_in / 2)
        .circle(id_in / 2)
        .extrude(length_in)
    )


def expansion_bladder(
    collapsed_od_in: float = 1.40,
    expanded_od_in: float = 3.85,
    length_in: float = 3.0,
    wall_in: float = 0.06,
) -> cq.Workplane:
    """Elastomer bladder — balloon catheter analog (shown as expanded form)."""
    return (
        cq.Workplane("XY")
        .circle(expanded_od_in / 2)
        .circle(expanded_od_in / 2 - wall_in)
        .extrude(length_in)
    )


def seal_element(
    od_in: float = 3.95,
    id_in: float = 1.55,
    length_in: float = 1.75,
) -> cq.Workplane:
    """HNBR sealing cup (expanded set condition)."""
    return (
        cq.Workplane("XY")
        .circle(od_in / 2)
        .circle(id_in / 2)
        .extrude(length_in)
        .faces(">Z")
        .workplane()
        .circle(od_in / 2 - 0.05)
        .extrude(-0.35)
    )


def backup_petal(
    length_in: float = 1.4,
    width_in: float = 0.55,
    thickness_in: float = 0.08,
) -> cq.Workplane:
    """Single petal-style anti-extrusion backup (Interwell HEX inspired)."""
    return (
        cq.Workplane("XZ")
        .moveTo(0, 0)
        .lineTo(width_in, 0)
        .lineTo(width_in * 0.35, length_in)
        .lineTo(0, length_in * 0.85)
        .close()
        .extrude(thickness_in)
    )


def slip_segment(
    height_in: float = 0.85,
    base_width_in: float = 0.65,
    thickness_in: float = 0.45,
) -> cq.Workplane:
    """Casing slip wedge segment."""
    return (
        cq.Workplane("XZ")
        .moveTo(0, 0)
        .lineTo(base_width_in, 0)
        .lineTo(base_width_in * 0.55, height_in)
        .lineTo(0, height_in * 0.9)
        .close()
        .extrude(thickness_in)
    )


def setting_piston(od_in: float = 1.30, length_in: float = 2.5) -> cq.Workplane:
    """Axial setting piston driven by wireline/CT jar or hydraulic setting tool."""
    return (
        cq.Workplane("XY")
        .circle(od_in / 2)
        .extrude(length_in)
        .faces(">Z")
        .workplane()
        .circle(od_in / 2 - 0.08)
        .extrude(-0.4)
    )


def top_sub(
    od_in: float = 1.65,
    length_in: float = 2.0,
    neck_od_in: float = 1.375,
) -> cq.Workplane:
    """Top connector / fishing neck sub."""
    body = cq.Workplane("XY").circle(od_in / 2).extrude(length_in)
    neck = (
        cq.Workplane("XY")
        .workplane(offset=length_in)
        .circle(neck_od_in / 2)
        .extrude(1.2)
    )
    return body.union(neck)


def bottom_equalizing_sub(od_in: float = 1.65, length_in: float = 1.5) -> cq.Workplane:
    """Bottom sub with equalizing port representation."""
    body = cq.Workplane("XY").circle(od_in / 2).extrude(length_in)
    port = (
        cq.Workplane("YZ")
        .workplane(offset=od_in / 2 - 0.15)
        .center(0, length_in * 0.45)
        .circle(0.18)
        .extrude(-0.35)
    )
    return body.cut(port)


def retrieval_cone(
    top_od_in: float = 1.55,
    bottom_od_in: float = 1.05,
    length_in: float = 1.8,
) -> cq.Workplane:
    """Cone that collapses stent sleeve on retrieval pull."""
    return (
        cq.Workplane("XY")
        .circle(top_od_in / 2)
        .workplane(offset=length_in)
        .circle(bottom_od_in / 2)
        .loft(combine=True)
    )


def centralizer_ring(od_in: float = 3.90, thickness_in: float = 0.25, height_in: float = 0.35) -> cq.Workplane:
    return (
        cq.Workplane("XY")
        .circle(od_in / 2)
        .circle(od_in / 2 - thickness_in)
        .extrude(height_in)
    )
