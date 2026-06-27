"""SHEX-BP-UHEX-54 — First-stroke TRIGGER + equalizing-sleeve INTERLOCK analysis.

The stage-1/2 actuator HARDWARE is sized in actuator_design.py. This script
addresses the harder, unresolved problem (FORWARD_PLAN open item): how the
"first stroke" is actually *triggered* and *sequenced* downhole, and how the
equalizing sleeve is interlocked into that sequence — without it firing on the
way to depth.

It (1) demonstrates numerically why the inherited "passive burst-disk at
p1<p2 + 30 s orifice" concept cannot give position control, and (2) sizes the
proposed commanded-initiation / completion-sequenced architecture (DCN-12).

Run:  .venv\\Scripts\\python export\\analysis\\trigger_design.py
"""

from __future__ import annotations

import json
import math
from pathlib import Path

KSI = 1000.0

# deploy demand from actuator_design.py
P1_DEPLOY = 941.0     # stage-1 stent open pressure, psi
P2_DEPLOY = 470.0     # stage-2 stent open pressure, psi
BLADDER_RATING = 2500.0
STAGE2_VOL_IN3 = 116.0   # ~1898 cc, the governing fill volume

# geometry of the equalizing/pilot circuit (SHEX-013 sleeve + SHEX-016A pilot)
PILOT_SEAL_OD = 1.450
PILOT_STEM_OD = 1.000
EQ_SLEEVE_FRICTION = 150.0     # lbf, greased Viton sliding (estimate)


def hydrostatic(tvd_ft: float, ppg: float = 9.0) -> float:
    return 0.052 * ppg * tvd_ft


def section(t: str) -> None:
    print("\n" + "=" * 76 + f"\n{t}\n" + "=" * 76)


def main() -> None:
    out: dict = {}

    section("1. WHY PASSIVE HYDROSTATIC-REFERENCED BURST DISKS CANNOT WORK")
    print("  A disk referenced to a sealed/atmospheric chamber sees ABSOLUTE")
    print("  hydrostatic, which rises monotonically while running in. It fires")
    print("  at the depth where hydrostatic = crack pressure - i.e. ON THE WAY")
    print("  DOWN, not at target depth.\n")
    print("  depth   hydrostatic(9ppg)   vs p1=941   vs p2=470")
    rows = []
    for ft in (1000, 2000, 3000, 5000, 8000, 12000):
        h = hydrostatic(ft)
        print(f"  {ft:5d} ft   {h:7.0f} psi        "
              f"{'FIRES' if h>=P1_DEPLOY else ' ok ':>5}      "
              f"{'FIRES' if h>=P2_DEPLOY else ' ok ':>5}")
        rows.append({"tvd_ft": ft, "hydrostatic_psi": round(h)})
    out["hydrostatic_window"] = rows
    print("\n  => There is NO single absolute-pressure setting that both survives")
    print("     run-in to a deep target AND fires only at target depth. Passive")
    print("     hydrostatic triggering has no position control. CONFIRMED FATAL.")
    print("     (Also: p1 and p2 are only a few hundred psi / few hundred ft")
    print("      apart, so on a continuous run-in both 'sequence' thresholds are")
    print("      crossed within seconds - order is NOT enforced.)")

    section("2. PROPOSED FIX - SEPARATE THE THREE THINGS THE OLD CONCEPT CONFLATED")
    print("  (a) ENERGY/VOLUME : the well (CT pump fluid, or wellbore hydrostatic)")
    print("  (b) INITIATION    : a deliberate, position-correct OPERATOR COMMAND")
    print("  (c) SEQUENCING    : mechanical - each stage's COMPLETION enables next")
    out["principle"] = "separate energy / initiation / sequencing (DCN-12)"

    section("3. INITIATION - CT PATH: APPLIED DIFFERENTIAL (depth-independent)")
    margin = 1500.0   # applied overpressure above annulus to initiate
    print(f"  Operator pumps CT bore to hydrostatic + {margin:.0f} psi at depth.")
    print("  A reference piston (CT bore one face, annulus the other) responds to")
    print("  the APPLIED DIFFERENTIAL only, so depth/hydrostatic drop out:")
    for ft in (2000, 8000, 12000):
        h = hydrostatic(ft)
        print(f"     {ft:5d} ft: annulus {h:5.0f} psi, trigger at {h+margin:5.0f} psi "
              f"(always +{margin:.0f}); bladder rating {BLADDER_RATING:.0f} psi OK")
    print("  + optional BALL/DART seat: nothing can move until the ball lands, so")
    print("    run-in and circulating pressures are positively locked out.")
    out["ct_initiation_margin_psi"] = margin

    section("4. INITIATION - E-LINE PATH: ELECTRICAL GATE, THEN HYDROSTATIC FILLS")
    print("  No flow path on e-line, and stage-2 needs ~1898 cc -> a self-contained")
    print("  charge cannot supply the VOLUME. So:")
    print("   - a small EFI/igniter (as in the E-4 tool) OPENS THE GATE on command")
    print("     (fires the pilot disk) -> total position control;")
    print("   - WELLBORE HYDROSTATIC then supplies the large volume to inflate.")
    print("  Hydrostatic must exceed the deploy demand at set depth:")
    for ft in (2000, 3000, 5000):
        h = hydrostatic(ft)
        ok1 = "yes" if h >= P1_DEPLOY else "NO -> need gas-gen boost"
        print(f"     {ft:5d} ft: hydrostatic {h:5.0f} psi  >= p1 {P1_DEPLOY:.0f}? {ok1}")
    print("  => e-line gate+hydrostatic works at typical depths; shallow/low-")
    print("     hydrostatic sets fall back to the gas-generator boost option.")

    section("5. SEQUENCING - COMPLETION-GATED, NOT THRESHOLD/TIME")
    print("  Replace 'p1<p2 + 30 s orifice' with a pressure-SIGNATURE indexer:")
    print("   - while a stent is still opening, bladder pressure sits at its")
    print("     ~deploy plateau (work is being done expanding the mesh);")
    print("   - when the stent reaches its hard stop (fully open), pressure CLIMBS")
    print("     from the plateau toward source pressure;")
    print("   - that climb shifts a shear-pinned arming sleeve that UNCOVERS the")
    print("     NEXT stage's feed port. Order becomes a PHYSICAL guarantee,")
    print("     independent of depth, temperature and pump rate.")
    p_shift_1 = 0.5 * (P1_DEPLOY + BLADDER_RATING)   # between plateau and source
    print(f"   - stage-1->2 arming sleeve shear-set ~{p_shift_1:.0f} psi "
          f"(> plateau {P1_DEPLOY:.0f}, < rating {BLADDER_RATING:.0f}).")
    print("   A metering orifice is retained only to keep the plateau stable")
    print("   (damping), NOT as the sequencer. The body-lock ratchet still holds")
    print("   each stage open after pressure bleeds.")
    out["stage1to2_arming_shift_psi"] = round(p_shift_1)

    section("6. EQUALIZING-SLEEVE INTERLOCK (SHEX-013 + SHEX-016A pilot) FIRST")
    a_pilot = math.pi / 4 * (PILOT_SEAL_OD**2 - PILOT_STEM_OD**2)
    print(f"  Pilot effective area = {a_pilot:.3f} in^2 "
          f"(OD {PILOT_SEAL_OD} / stem {PILOT_STEM_OD}).")
    print("  The gate pressure reaches the EQ pilot FIRST (lowest preload, shortest")
    print("  travel). It shifts the SHEX-013 sleeve ~0.375 in -> ports CLOSE, then")
    print("  its end-of-stroke uncovers the STAGE-1 feed port. So EQ-close is")
    print("  physically guaranteed to precede stage 1.")
    for p in (P2_DEPLOY, 1000.0, hydrostatic(8000)):
        f = a_pilot * p
        print(f"     at {p:6.0f} psi -> pilot force {f:5.0f} lbf "
              f"(vs ~{EQ_SLEEVE_FRICTION:.0f} lbf friction + calibrated shear pin)")
    out["pilot_area_in2"] = round(a_pilot, 3)
    out["pilot_force_at_470psi_lbf"] = round(a_pilot * P2_DEPLOY)

    section("7. FILL-TIME SANITY (stage 2, the governing volume)")
    for d_orif in (0.094, 0.125, 0.156):
        A = math.pi / 4 * d_orif**2
        dP = 500.0                      # net psi across feed once gated
        rho = 0.0361                    # lb/in^3 (water-ish)
        # Q = Cd*A*sqrt(2*dP*gc/rho); gc=386.4 in/s^2 for lbf-in-lb units
        v = 0.8 * math.sqrt(2 * dP * 386.4 / rho)
        Q = A * v                       # in^3/s
        t = STAGE2_VOL_IN3 / Q
        print(f"  orifice d={d_orif:.3f}in: Q ~ {Q:5.1f} in^3/s -> "
              f"stage-2 fill ~ {t:4.1f} s")
    print("  => fill is tens of seconds with a sensible feed port. Reasonable.")

    section("8. FAIL-SAFE STATE TABLE")
    states = [
        ("Gate never opened", "collapsed OD 1.688", "normal POOH; nothing fired"),
        ("Gate open, EQ closed only", "OD 1.688, ports shut", "pull to re-open EQ via shift profile; fish on mandrel"),
        ("Stage 1 only", "OD 3.375, not anchored", "recoverable on mandrel; EQ re-open on pull"),
        ("Stages 1+2 complete", "OD 5.750, locked open", "proceed to secondary (tool) stroke"),
        ("Full set", "OD 8.65 / seals / slips", "tool shears free; plug holds"),
    ]
    print(f"  {'state':28s}{'OD / condition':24s}{'recovery / next'}")
    for s, c, r in states:
        print(f"  {s:28s}{c:24s}{r}")
    out["fail_safe_states"] = [{"state": s, "condition": c, "action": r}
                               for s, c, r in states]

    section("9. SEQUENCE (DCN-12) - single command, mechanically ordered")
    for line in [
        "T-  surface: ball out / EFI continuity OK; EQ ports OPEN; gate ARMED.",
        "T0  at depth, by COMMAND: CT applied dP (+1500 psi) OR e-line EFI fire",
        "    -> opens the gate to the sequence manifold.",
        "T1  EQ pilot strokes first -> SHEX-013 sleeve CLOSES -> uncovers S1 port.",
        "T2  S1 bladder inflates -> stent Ø3.375 -> bottom-out pressure climb",
        "    shifts S1->S2 arming sleeve -> uncovers S2 port.",
        "T3  S2 bladder inflates -> stent Ø5.750 -> 'ready' signature.",
        "T4  body-lock ratchets hold both stages; FIRST STROKE complete.",
        "T5  setting tool applies the 10-in SECONDARY stroke (iris+seals+slips).",
    ]:
        print("  " + line)

    p = Path(__file__).with_name("trigger_design.json")
    p.write_text(json.dumps(out, indent=2))
    print(f"\nDerived values -> {p}")


if __name__ == "__main__":
    main()
