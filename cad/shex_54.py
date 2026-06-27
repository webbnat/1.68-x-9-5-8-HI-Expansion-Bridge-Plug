"""SHEX-ST-54 setting tool and 54\" plug assembly mesh generation."""

from __future__ import annotations

from cad.mesh_utils import MeshData, cylinder, merge, translate, tube
from cad.plug_visual import MODULES, casing_reference, plug_run_in, plug_set


def setting_tool_assembly() -> "MeshData":
    """SHEX-ST-54 module stack — bottom (crossover) at z=0."""
    z = 0.0
    parts = []

    modules = [
        (10.0, 3.375 / 2, 3.25, "crossover"),
        (8.0, 3.375 / 2, 3.375, "release"),
        (14.0, 3.625 / 2, 3.625, "pressure"),
        (54.0, 3.625 / 2, 3.625, "stroke"),
        (10.0, 3.625 / 2, 3.625, "loadcell"),
        (30.0, 3.625 / 2, 3.625, "motor"),
        (84.0, 3.625 / 2, 3.625, "battery"),
        (22.0, 3.625 / 2, 3.625, "telemetry"),
        (14.0, 3.625 / 2, 3.625, "head"),
    ]

    for length, outer_r, flange_od, _name in modules:
        body = cylinder(outer_r, length, segments=64)
        parts.append(translate(body, 0, 0, z))
        # Joint flange between modules
        parts.append(
            translate(
                tube(flange_od / 2, outer_r - 0.04, 0.35, segments=48),
                0,
                0,
                z + length - 0.35,
            )
        )
        z += length

    # Telescoping stroke detail (inner mandrel visible in stroke section)
    stroke_z = 10 + 8 + 14
    parts.append(translate(tube(3.625 / 2, 1.55 / 2, 11.6, segments=48), 0, 0, stroke_z + 8))
    parts.append(translate(tube(3.625 / 2 - 0.18, 3.625 / 2 - 0.32, 11.6, segments=48), 0, 0, stroke_z + 20))

    return merge(*parts)


def plug_54_assembly() -> "MeshData":
    """Set condition — primary review geometry."""
    return plug_set()


def plug_54_run_in() -> "MeshData":
    return plug_run_in()


def plug_54_set_in_casing() -> "MeshData":
    return merge(plug_set(), casing_reference())


def combined_run_in_string() -> "MeshData":
    """Setting tool + 54\" plug for lubricator length check."""
    plug = plug_run_in()
    tool = setting_tool_assembly()
    return merge(tool, translate(plug, 0, 0, 246.0))


def plug_total_length() -> float:
    return sum(m[1] for m in MODULES)
