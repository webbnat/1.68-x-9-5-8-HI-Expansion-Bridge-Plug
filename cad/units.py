"""Unit helpers — internal CAD math uses inches; STL export uses mm."""

MM_PER_IN = 25.4


def in_to_mm(value: float) -> float:
    return value * MM_PER_IN


def mm_to_in(value: float) -> float:
    return value / MM_PER_IN
