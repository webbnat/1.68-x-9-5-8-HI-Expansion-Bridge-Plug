"""
Developed (flat) open-cell diamond stent pattern for laser-cut thin-wall tubes.

Design method
-------------
1. Target SET envelope defines cell count N and mean circumferential pitch at deploy.
2. Run-in developed width W_run = pi * d_mean_run fixes the cut pattern on the tube.
3. Out-of-phase crown rows + diagonal struts form diamond cells that close at run-in
   and open when circumferential pitch scales ~ OD_set / d_mean_run.
4. Foreshortening estimated from inextensible strut edges (validation, not cut change).

Manufacturing output is always the RUN-IN developed pattern; SET is a validated envelope.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

State = Literal["run_in", "set"]


@dataclass(frozen=True)
class StentStageSpec:
    part_no: str
    od_run_in: float
    id_run_in: float
    od_set_in: float
    id_set_in: float
    length_in: float
    cells_around: int
    rings: int
    strut_width_in: float = 0.045
    kerf_in: float = 0.008
    end_margin_frac: float = 0.06
    drawing: str = ""

    @property
    def d_mean_run(self) -> float:
        return (self.od_run_in + self.id_run_in) / 2.0

    @property
    def d_mean_set(self) -> float:
        return (self.od_set_in + self.id_set_in) / 2.0

    @property
    def w_run(self) -> float:
        return math.pi * self.d_mean_run

    @property
    def w_set(self) -> float:
        return math.pi * self.d_mean_set

    @property
    def pitch_run(self) -> float:
        return self.w_run / float(self.cells_around)

    @property
    def pitch_set(self) -> float:
        return self.w_set / float(self.cells_around)

    @property
    def od_expansion_ratio(self) -> float:
        return self.od_set_in / self.od_run_in

    @property
    def pitch_expansion_ratio(self) -> float:
        return self.pitch_set / self.pitch_run


@dataclass
class StentPattern:
    spec: StentStageSpec
    state: State
    row_y: list[float]
    # Each cell: 4 corners CCW — top, right, bottom, left (developed x,y inches)
    diamonds: list[tuple[tuple[float, float], ...]]
    strut_segments: list[tuple[tuple[float, float], tuple[float, float]]] = field(default_factory=list)
    aperture_polygons: list[list[tuple[float, float]]] = field(default_factory=list)


@dataclass
class StentValidation:
    spec: StentStageSpec
    pitch_run_in: float
    pitch_at_set_target: float
    circumferential_stretch_ratio: float
    axial_pitch_run_in: float
    axial_pitch_after_deploy: float
    length_run_in: float
    length_after_deploy: float
    foreshortening_in: float
    foreshortening_pct: float
    strut_length_in: float
    closes_at_run_in: bool
    notes: list[str]


def _row_positions(length_in: float, rings: int, margin_frac: float) -> list[float]:
    margin = length_in * margin_frac
    usable = length_in - 2.0 * margin
    if rings <= 1:
        return [length_in / 2.0]
    pitch = usable / float(rings - 1)
    return [margin + i * pitch for i in range(rings)]


def _wrap_x(x: float, width: float) -> float:
    return x % width


def _diamond_corners(
    x_center: float,
    y_top: float,
    y_bottom: float,
    half_width: float,
) -> tuple[tuple[float, float], tuple[float, float], tuple[float, float], tuple[float, float]]:
    y_mid = (y_top + y_bottom) / 2.0
    top = (x_center, y_top)
    right = (x_center + half_width, y_mid)
    bottom = (x_center, y_bottom)
    left = (x_center - half_width, y_mid)
    return top, right, bottom, left


def _inset_aperture(
    corners: tuple[tuple[float, float], ...],
    strut_half: float,
) -> list[tuple[float, float]]:
    """Shrink diamond toward centroid for laser aperture (leave strut land)."""
    cx = sum(p[0] for p in corners) / 4.0
    cy = sum(p[1] for p in corners) / 4.0
    out = []
    for x, y in corners:
        dx, dy = x - cx, y - cy
        mag = math.hypot(dx, dy)
        if mag < 1e-9:
            out.append((x, y))
            continue
        scale = max(0.0, 1.0 - strut_half / mag)
        out.append((cx + dx * scale, cy + dy * scale))
    return out


def build_pattern(spec: StentStageSpec, state: State = "run_in") -> StentPattern:
    """
    Build developed diamond mesh.

    run_in: pitch = pitch_run (laser cut authority)
    set:    pitch = pitch_set (deployed envelope check / illustration)
    """
    if state == "run_in":
        pitch = spec.pitch_run
        width = spec.w_run
        row_y = _row_positions(spec.length_in, spec.rings, spec.end_margin_frac)
    else:
        pitch = spec.pitch_set
        width = spec.w_set
        row_y_base = _row_positions(spec.length_in, spec.rings, spec.end_margin_frac)
        v = validate_pattern(spec)
        if spec.rings > 1 and v.axial_pitch_after_deploy > 0:
            margin = spec.length_in * spec.end_margin_frac
            row_y = [margin + i * v.axial_pitch_after_deploy for i in range(spec.rings)]
        else:
            row_y = row_y_base

    half_w = pitch / 2.0
    diamonds: list[tuple[tuple[float, float], ...]] = []
    segments: list[tuple[tuple[float, float], tuple[float, float]]] = []
    apertures: list[list[tuple[float, float]]] = []

    for j in range(len(row_y) - 1):
        y_top = row_y[j]
        y_bot = row_y[j + 1]
        phase = (pitch / 2.0) if (j % 2) else 0.0
        for i in range(spec.cells_around):
            x_c = phase + (i + 0.5) * pitch
            corners = _diamond_corners(x_c, y_top, y_bot, half_w)
            diamonds.append(corners)
            for k in range(4):
                p0 = corners[k]
                p1 = corners[(k + 1) % 4]
                segments.append((p0, p1))
            apertures.append(_inset_aperture(corners, spec.strut_width_in / 2.0))

    # Duplicate seam cells so pattern tiles at x=0 / x=width
    seam_apertures: list[list[tuple[float, float]]] = []
    for ap in apertures:
        shifted = [(_wrap_x(x + width, width), y) for x, y in ap]
        if shifted[0][0] < spec.strut_width_in:
            seam_apertures.append(shifted)

    return StentPattern(
        spec=spec,
        state=state,
        row_y=row_y,
        diamonds=diamonds,
        strut_segments=segments,
        aperture_polygons=apertures + seam_apertures,
    )


def validate_pattern(spec: StentStageSpec) -> StentValidation:
    """Check run-in pattern against SET envelope via pitch stretch + strut kinematics."""
    row_y = _row_positions(spec.length_in, spec.rings, spec.end_margin_frac)
    notes: list[str] = []

    if spec.rings < 2:
        return StentValidation(
            spec=spec,
            pitch_run_in=spec.pitch_run,
            pitch_at_set_target=spec.pitch_set,
            circumferential_stretch_ratio=spec.pitch_expansion_ratio,
            axial_pitch_run_in=0.0,
            axial_pitch_after_deploy=0.0,
            length_run_in=spec.length_in,
            length_after_deploy=spec.length_in,
            foreshortening_in=0.0,
            foreshortening_pct=0.0,
            strut_length_in=0.0,
            closes_at_run_in=True,
            notes=["Single ring — validation limited"],
        )

    dy_run = row_y[1] - row_y[0]
    half_dx_run = spec.pitch_run / 2.0
    strut_len = math.hypot(half_dx_run, dy_run / 2.0)
    half_dx_set = spec.pitch_set / 2.0

    if half_dx_set >= strut_len:
        notes.append(
            "WARNING: SET half-pitch exceeds strut length — increase rings, reduce cells, or shorten deploy pitch"
        )
        dy_set = 0.0
    else:
        dy_set = 2.0 * math.sqrt(strut_len * strut_len - half_dx_set * half_dx_set)

    margin = spec.length_in * spec.end_margin_frac
    length_deploy = 2.0 * margin + (spec.rings - 1) * dy_set
    foreshort = spec.length_in - length_deploy
    foreshort_pct = 100.0 * foreshort / spec.length_in if spec.length_in else 0.0

    # Closure: aperture circumferential gap at run-in vs strut width
    run_pattern = build_pattern(spec, "run_in")
    min_gap = float("inf")
    for ap in run_pattern.aperture_polygons:
        xs = [p[0] for p in ap]
        gap = min(xs[i + 1] - xs[i] for i in range(len(xs) - 1)) if len(xs) > 1 else float("inf")
        min_gap = min(min_gap, abs(gap))

    closes = spec.pitch_run > spec.strut_width_in * 1.5
    if not closes:
        notes.append("WARNING: circumferential pitch may be tight for strut width at run-in")

    notes.append(
        "Circumferential stretch run->SET mean pitch: %.3f× (OD ratio %.3f×)"
        % (spec.pitch_expansion_ratio, spec.od_expansion_ratio)
    )
    notes.append(
        "Estimated deploy length: %.3f in (foreshorten %.3f in, %.1f%%)"
        % (length_deploy, foreshort, foreshort_pct)
    )

    return StentValidation(
        spec=spec,
        pitch_run_in=spec.pitch_run,
        pitch_at_set_target=spec.pitch_set,
        circumferential_stretch_ratio=spec.pitch_expansion_ratio,
        axial_pitch_run_in=dy_run,
        axial_pitch_after_deploy=dy_set,
        length_run_in=spec.length_in,
        length_after_deploy=length_deploy,
        foreshortening_in=foreshort,
        foreshortening_pct=foreshort_pct,
        strut_length_in=strut_len,
        closes_at_run_in=closes,
        notes=notes,
    )


def map_developed_to_cylinder(
    x: float,
    y: float,
    spec: StentStageSpec,
    z_base: float = 0.0,
) -> tuple[float, float, float]:
    """Map developed (x,y) on run-in mean diameter to Cartesian (X,Y,Z)."""
    r = spec.d_mean_run / 2.0
    theta = 2.0 * math.pi * _wrap_x(x, spec.w_run) / spec.w_run
    return (r * math.cos(theta), r * math.sin(theta), z_base + y)


def load_spec_from_yaml(part_key: str, yaml_path: str | Path | None = None) -> StentStageSpec:
    import yaml

    path = Path(yaml_path) if yaml_path else Path(__file__).resolve().parents[1] / "config" / "stent_patterns.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    defaults = data.get("defaults", {})
    part = data[part_key]
    merged = {**defaults, **part}
    return StentStageSpec(
        part_no=merged["part_no"],
        od_run_in=float(merged["od_run_in"]),
        id_run_in=float(merged["id_run_in"]),
        od_set_in=float(merged["od_set_in"]),
        id_set_in=float(merged["id_set_in"]),
        length_in=float(merged["length_in"]),
        cells_around=int(merged["cells_around"]),
        rings=int(merged["rings"]),
        strut_width_in=float(merged.get("strut_width_in", 0.045)),
        kerf_in=float(merged.get("kerf_in", 0.008)),
        end_margin_frac=float(merged.get("end_margin_frac", 0.06)),
        drawing=str(merged.get("drawing", "")),
    )


def format_validation_report(v: StentValidation) -> str:
    s = v.spec
    lines = [
        "%s (%s) — developed diamond pattern" % (s.part_no, s.drawing or "stent"),
        "",
        "RUN-IN (laser authority)",
        "  OD %.3f / bore ID %.3f / L %.3f" % (s.od_run_in, s.id_run_in, s.length_in),
        "  Developed W %.3f / pitch %.3f / %d cells × %d rings"
        % (s.w_run, v.pitch_run_in, s.cells_around, s.rings),
        "  Strut width %.3f / kerf %.3f" % (s.strut_width_in, s.kerf_in),
        "",
        "SET envelope (validation target)",
        "  OD %.3f / bore ID %.3f" % (s.od_set_in, s.id_set_in),
        "  Target pitch %.3f (%.3f× circumferential stretch)"
        % (v.pitch_at_set_target, v.circumferential_stretch_ratio),
        "  Deploy length ~%.3f (foreshorten %.3f in, %.1f%%)"
        % (v.length_after_deploy, v.foreshortening_in, v.foreshortening_pct),
        "  Strut edge length (run-in) %.4f in" % v.strut_length_in,
        "",
    ]
    lines.extend("  " + n for n in v.notes)
    return "\n".join(lines)
