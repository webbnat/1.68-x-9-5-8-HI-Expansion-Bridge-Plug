"""Assemble complete bridge plug in run-in and set configurations."""

from __future__ import annotations

import cadquery as cq

from cad.parts import (
    backup_petal,
    bottom_equalizing_sub,
    centralizer_ring,
    expansion_bladder,
    inner_mandrel,
    outer_sheath,
    retrieval_cone,
    seal_element,
    setting_piston,
    slip_segment,
    top_sub,
)
from cad.stent_sleeve import StentParams, build_stent_sleeve
from cad.units import in_to_mm


def _place(part: cq.Workplane, x_mm: float = 0, y_mm: float = 0, z_mm: float = 0) -> cq.Workplane:
    return part.translate((x_mm, y_mm, z_mm))


def build_assembly_run_in() -> cq.Workplane:
    """Collapsed run-in configuration — stent crimped on mandrel inside sheath."""
    z = 0.0
    asm = _place(inner_mandrel(), z_mm=z)
    z += in_to_mm(14.0)

    stent = build_stent_sleeve(StentParams(), state="collapsed")
    stent = stent.translate((0, 0, in_to_mm(4.5)))
    asm = asm.union(stent)

    sheath = outer_sheath().translate((0, 0, in_to_mm(4.2)))
    asm = asm.union(sheath)

    asm = asm.union(top_sub().translate((0, 0, in_to_mm(12.5))))
    asm = asm.union(bottom_equalizing_sub())
    return asm


def build_assembly_set() -> cq.Workplane:
    """Set configuration — expanded stent, seal, slips, backups against casing."""
    base_z = in_to_mm(2.0)

    asm = _place(bottom_equalizing_sub(), z_mm=0)
    asm = asm.union(setting_piston().translate((0, 0, in_to_mm(1.5))))

    stent = build_stent_sleeve(StentParams(), state="expanded")
    asm = asm.union(stent.translate((0, 0, base_z)))

    bladder = expansion_bladder().translate((0, 0, base_z + in_to_mm(0.15)))
    asm = asm.union(bladder)

    seal = seal_element().translate((0, 0, base_z + in_to_mm(3.1)))
    asm = asm.union(seal)

    for i in range(8):
        angle = i * 45
        petal = (
            backup_petal()
            .rotate((0, 0, 0), (0, 0, 1), angle)
            .translate((in_to_mm(1.55), 0, base_z + in_to_mm(3.0)))
        )
        asm = asm.union(petal)

    for i in range(6):
        angle = i * 60 + 30
        slip = (
            slip_segment()
            .rotate((0, 0, 0), (0, 0, 1), angle)
            .translate((in_to_mm(1.85), 0, base_z + in_to_mm(4.9)))
        )
        asm = asm.union(slip)

    asm = asm.union(centralizer_ring().translate((0, 0, base_z + in_to_mm(4.6))))
    asm = asm.union(retrieval_cone().translate((0, 0, base_z + in_to_mm(5.2))))
    asm = asm.union(top_sub().translate((0, 0, base_z + in_to_mm(6.8))))
    return asm


def build_assembly_alt_2125() -> cq.Workplane:
    """Alternate 2.125\" OD variant assembly (higher pressure rating envelope)."""
    params = StentParams(collapsed_od_in=2.125, expanded_od_in=4.050)
    asm = bottom_equalizing_sub(od_in=2.05)
    stent = build_stent_sleeve(params, state="collapsed")
    asm = asm.union(stent.translate((0, 0, in_to_mm(3.0))))
    asm = asm.union(top_sub(od_in=2.05, neck_od_in=1.5).translate((0, 0, in_to_mm(8.0))))
    return asm
