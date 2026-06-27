"""SHEX-BP-UHEX-54 — Stage 1/2 internal actuator design analysis.

First-order engineering sizing for the two internal expansion actuators that
perform the "first stroke" (radial expansion 1.688 -> 5.750 in) BEFORE the
setting tool applies its 10-in axial secondary stroke.

    Stage 1  SHEX-014   inflatable bladder        OD 1.688 -> 3.375
    Stage 2  SHEX-015   swage cone + Belleville    OD 3.375 -> 5.750

These are FIRST-ORDER hand calcs to size geometry and bound the energy/force
budget. They are NOT a substitute for FEA + full-scale test (flagged as an
open item). Run:  .venv\\Scripts\\python export\\analysis\\actuator_design.py
"""

from __future__ import annotations

import json
import math
from pathlib import Path

PSI = 1.0
KSI = 1000.0

# --- geometry (from cad/release_solids.py MODULE_Z + part dims) ------------
MANDREL_NECK_OD = 1.270          # DCN-1 helix neck through stage 1/2 zones
STENT_ID = 1.562
STENT_OD_RUNIN = 1.688
STENT_WALL = 0.063
STAGE1 = {"z0": 9.5, "z1": 13.5, "od_start": 1.688, "od_end": 3.375}
STAGE2 = {"z0": 13.5, "z1": 18.5, "od_start": 3.375, "od_end": 5.750}
CASING_DRIFT = 8.679

# --- material model (CONCEPT: ductile stent, see DCN-10) --------------------
# 17-4 PH H900 (current spec) is too strong/brittle to plastically hinge 2x.
# A balloon/swage-expandable mesh must be a ductile alloy (annealed 316L or a
# Ni alloy). Use annealed 316L properties for the expansion mechanics.
STENT_SY = 30 * KSI              # 316L annealed ~30 ksi yield
LIGAMENT_FRACTION = 0.42         # open-cell mesh: fraction of circumference that is solid strut
FRICTION = 0.15                  # steel-on-steel lubricated swage


def ann_radial(od_id_pair: tuple[float, float]) -> float:
    return 0.0


def stent_expansion_pressure(od_start: float, t: float, sy: float,
                             ligament: float) -> float:
    """Internal pressure to plastically open a thin mesh tube at its SMALLEST
    (hardest) radius. Thin-wall hoop: p = sigma * t_eff / r, t_eff = ligament*t.
    Evaluated at the start radius (worst case for pressure)."""
    r = od_start / 2.0
    t_eff = ligament * t
    return sy * t_eff / r


def hydrostatic_psi(tvd_ft: float, mud_ppg: float = 9.0) -> float:
    return 0.052 * mud_ppg * tvd_ft


def section(title: str) -> None:
    print("\n" + "=" * 74)
    print(title)
    print("=" * 74)


def main() -> None:
    out: dict = {}

    section("1. ANNULUS BUDGET - the space the actuators must live in")
    r_mandrel = MANDREL_NECK_OD / 2
    r_stent_id = STENT_ID / 2
    annulus = r_stent_id - r_mandrel
    print(f"  mandrel neck OD          {MANDREL_NECK_OD:.3f} in  (r {r_mandrel:.3f})")
    print(f"  stent sleeve ID          {STENT_ID:.3f} in  (r {r_stent_id:.3f})")
    print(f"  radial annulus available {annulus:.3f} in  ({2*annulus:.3f} diametral)")
    print(f"  -> bladder wall + fold and piston/cone wall must fit in {annulus:.3f} in")
    out["annulus_radial_in"] = round(annulus, 4)

    section("2. STENT EXPANSION MECHANICS (per stage)")
    for name, st in (("Stage 1", STAGE1), ("Stage 2", STAGE2)):
        dR = (st["od_end"] - st["od_start"]) / 2
        p_open = stent_expansion_pressure(st["od_start"], STENT_WALL,
                                          STENT_SY, LIGAMENT_FRACTION)
        L = st["z1"] - st["z0"]
        # radial force to hold the mesh open at the FINAL OD (contact pressure
        # * projected cylinder area) — drives the swage/piston for stage 2
        r_end = st["od_end"] / 2
        p_hold = stent_expansion_pressure(st["od_end"], STENT_WALL,
                                          STENT_SY, LIGAMENT_FRACTION)
        F_radial = p_hold * math.pi * st["od_end"] * L
        print(f"  {name}: OD {st['od_start']:.3f} -> {st['od_end']:.3f}  "
              f"(dR {dR:.3f}/side, L {L:.1f})")
        print(f"     deploy pressure (worst case, start r) ~ {p_open:8.0f} psi")
        print(f"     hold pressure (final r)               ~ {p_hold:8.0f} psi")
        print(f"     total radial force at final OD        ~ {F_radial:8.0f} lbf")
        out[f"{name}_deploy_psi"] = round(p_open)
        out[f"{name}_hold_psi"] = round(p_hold)
        out[f"{name}_radial_force_lbf"] = round(F_radial)

    section("3. STAGE 1 - INFLATABLE BLADDER (SHEX-014)")
    st = STAGE1
    bladder_run_od = STENT_ID - 0.10        # folded clearance under stent ID
    bladder_dep_id = st["od_end"] - 2 * STENT_WALL   # bladder OD reaches stent ID
    L = st["z1"] - st["z0"]
    # inflated fluid volume ~ annulus between mandrel neck and deployed stent ID
    v_dep = math.pi / 4 * (bladder_dep_id**2 - MANDREL_NECK_OD**2) * L
    v_run = math.pi / 4 * (bladder_run_od**2 - MANDREL_NECK_OD**2) * L
    dV = v_dep - v_run
    p_dep = out["Stage 1_deploy_psi"]
    print(f"  bladder run-in OD (folded)  ~ {bladder_run_od:.3f} in")
    print(f"  bladder deployed OD         ~ {bladder_dep_id:.3f} in (to stent ID)")
    print(f"  inflation fluid dV          ~ {dV:6.2f} in^3 ({dV*16.387:.0f} cc)")
    print(f"  required bladder pressure   ~ {p_dep:.0f} psi (+ reinforcement margin)")
    print(f"  design bladder rating        = {max(2500, p_dep*2):.0f} psi (2x deploy, burst 3x)")
    print("  source: wellbore hydrostatic / applied CT pressure via burst disk")
    print(f"  hydrostatic @ 8000 ft, 9 ppg ~ {hydrostatic_psi(8000):.0f} psi (ample)")
    print(f"  hydrostatic @ 3000 ft, 9 ppg ~ {hydrostatic_psi(3000):.0f} psi")
    out["stage1_bladder_dV_in3"] = round(dV, 2)
    out["stage1_bladder_rating_psi"] = int(max(2500, p_dep * 2))

    section("4. STAGE 2 - WHY A RIGID SWAGE/CONE IS REJECTED (DCN-11)")
    st = STAGE2
    dR = (st["od_end"] - st["od_start"]) / 2
    # a rigid cone/swage must itself reach under the stent at the FINAL OD
    swage_od_needed = st["od_end"] - 2 * STENT_WALL
    print(f"  To back the stent at its FINAL OD {st['od_end']:.3f}, a rigid swage")
    print(f"  must grow to ~ {swage_od_needed:.3f} in OD under the mesh.")
    print(f"  But at run-in every part must be <= stent ID {STENT_ID:.3f}.")
    print(f"  A solid cone/Belleville-wedge starting at <= {STENT_ID:.3f} CANNOT")
    print(f"  grow to {swage_od_needed:.3f} - it is geometrically impossible in this")
    print("  annulus (same class of limit as the setting-tool OD-vs-force).")
    print("  Only an element that FOLDS small and inflates large works.")
    print("  => DECISION (DCN-11): Stage 2 is a SECOND INFLATABLE BLADDER,")
    print("     sequenced after stage 1. The Belleville stack is retained ONLY")
    print("     as a hold-open / anti-recoil axial preload (not a radial driver).")
    # for reference, what the rejected swage would have demanded
    for half_angle in (15,):
        ta = math.tan(math.radians(half_angle))
        axial_travel = dR / ta
        print(f"  (ref: a {half_angle}-deg cone would need {axial_travel:.2f} in axial"
              f" travel and could only lift dR {dR:.3f} from a moving base.)")
    out["stage2_prime_mover"] = "inflatable bladder (DCN-11; swage rejected)"

    section("5. STAGE 2 - SECOND INFLATABLE BLADDER (SHEX-015)")
    bladder_run_od = STENT_ID - 0.10
    bladder_dep_id = st["od_end"] - 2 * STENT_WALL
    L = st["z1"] - st["z0"]
    v_dep = math.pi / 4 * (bladder_dep_id**2 - MANDREL_NECK_OD**2) * L
    v_run = math.pi / 4 * (bladder_run_od**2 - MANDREL_NECK_OD**2) * L
    dV = v_dep - v_run
    p_dep = out["Stage 2_deploy_psi"]
    print(f"  bladder run-in OD (folded)  ~ {bladder_run_od:.3f} in")
    print(f"  bladder deployed OD         ~ {bladder_dep_id:.3f} in (to stent ID)")
    print(f"  inflation fluid dV          ~ {dV:6.2f} in^3 ({dV*16.387:.0f} cc)")
    print(f"  required bladder pressure   ~ {p_dep:.0f} psi (lower than stage 1: larger r)")
    print(f"  design bladder rating        = {max(2500, p_dep*2):.0f} psi")
    print("  Belleville hold stack (annulus-limited, NOT a radial driver):")
    bw_od = STENT_ID - 0.02
    bw_id = MANDREL_NECK_OD + 0.02
    washer_force = 8.0 * KSI * (bw_od - bw_id) ** 2 * 0.5
    print(f"     washer OD {bw_od:.3f} / ID {bw_id:.3f} -> ~ {washer_force:.0f} lbf/washer;")
    print("     a short series stack provides ~200-300 lbf anti-recoil preload.")
    out["stage2_bladder_dV_in3"] = round(dV, 2)
    out["stage2_bladder_rating_psi"] = int(max(2500, p_dep * 2))

    section("6. TRIGGER / SEQUENCE / INTERLOCK")
    print("  T-   arm at surface: atmospheric reference chamber sealed, burst")
    print("       disks intact, EQ ports OPEN, Belleville preloaded+latched.")
    print("  T0   at depth: EQ pilot piston (SHEX-016A) shifts EQ sleeve CLOSED")
    print("       first (lowest cracking pressure), isolating below.")
    print("  T1   stage-1 burst disk opens at p1 -> bladder inflates -> 3.375.")
    print("  T2   metering orifice delays ~30 s, then stage-2 burst disk opens")
    print("       at p2 (>p1) -> drive piston advances swage cone -> 5.750.")
    print("  T3   body-lock ratchet rings hold both stages open; Belleville")
    print("       stack keeps preload as pressure later bleeds via EQ on retrieve.")
    print("  Then: setting tool applies the 10-in SECONDARY stroke (stage 3 +")
    print("       seals + slips), per SETTING_TOOL_MANUAL.")

    section("7. OPEN ITEMS (must close before any build)")
    for s in [
        "FEA of mesh plastic expansion (pressure, strain, fatigue) per stage.",
        "DCN-10: change stent material 17-4 PH H900 -> ductile (anneal 316L /",
        "        Ni alloy) so the mesh can plastically hinge ~2x without cracking.",
        "Full-scale deploy test of bladder + swage in a representative annulus.",
        "Burst-disk crack-pressure selection vs well hydrostatic window.",
        "Metering-orifice delay validation across temperature.",
        "Body-lock ratchet load rating + retrieval re-collapse kinematics.",
    ]:
        print(f"   - {s}")

    # write derived dims for the CAD module to consume
    p = Path(__file__).with_name("actuator_design.json")
    p.write_text(json.dumps(out, indent=2))
    print(f"\nDerived dimensions -> {p}")


if __name__ == "__main__":
    main()
