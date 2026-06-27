# First-Stroke Trigger & Equalizing-Sleeve Interlock — Design Memo

| | |
|---|---|
| Document | SHEX-EM-001 Rev A (engineering memo) |
| Subject | How the internal "first stroke" is **triggered** and **sequenced** downhole |
| Closes | FORWARD_PLAN open item: *"trigger / equalizing-sleeve interlock referenced but not designed — required for the first stroke to be real."* |
| Numbers | `export/analysis/trigger_design.py` (+ `.json`) |
| Proposes | **DCN-12** (initiation/sequencing re-architecture) + new sub **SHEX-017** |
| Companions | `ACTUATOR_MANUAL.md` (hardware), `SETTING_TOOL_MANUAL.md` (secondary stroke) |

---

## 0. The question, stated honestly

The stage-1/2 actuator **hardware** is designed and modelled (bladders, glands,
lock rings, Belleville hold, charge subs, pilot piston). What was **not** an
engineering design — only a narrative — is the part that actually makes the
first stroke happen at the right place, in the right order, without firing on
the way to depth:

> inherited concept: *"burst disk p1 fires the EQ pilot first, then stage-1
> disk at p1, then a 30 s metering orifice, then stage-2 disk at p2 > p1."*

If the first stroke isn't a **real, position-correct, ordered, fail-safe**
event, the whole two-stroke architecture is just a drawing. So this memo
pressure-tests that concept and replaces it.

---

## 1. Why the inherited concept cannot work (the fatal flaw)

A burst disk referenced to a sealed/atmospheric chamber responds to **absolute
hydrostatic**. Hydrostatic **rises continuously as you run in**, so the disk
fires at the depth where hydrostatic = its crack pressure — **on the way down,
not at target depth.**

`trigger_design.py` §1, 9.0 ppg:

| Depth | Hydrostatic | vs p1 = 941 psi | vs p2 = 470 psi |
|---|---|---|---|
| 1000 ft | 468 psi | ok | ok |
| 2000 ft | 936 psi | ok | **FIRES** |
| 3000 ft | 1404 psi | **FIRES** | **FIRES** |
| 8000 ft | 3744 psi | **FIRES** | **FIRES** |

**There is no single absolute-pressure setting that both survives run-in to a
deep target and fires only at target depth.** Set the disk high enough to
survive run-in and the hydrostatic at depth is too low to ever fire it; set it
low enough to fire and it trips during descent. Passive hydrostatic triggering
has **no position control** — this is fatal, not a tuning problem.

Three more problems fall out of the same root:

1. **Order isn't enforced.** p1 and p2 are only a few hundred psi (a few hundred
   feet) apart, so on a continuous run-in both "sequence" thresholds are crossed
   within seconds. A metering orifice delays *bladder fill*, not the *trigger* —
   with hydrostatic always present, both stages fire essentially together.
2. **Volume.** Stage 2 needs ~1898 cc. No self-contained downhole chamber that
   fits a 0.146-in annulus can store that volume of pressurised fluid; the
   **well** must supply it — which drags hydrostatic back into the trigger.
3. **No defined fail state.** If the sequence half-completes there's no stated
   safe/recoverable condition.

---

## 2. The fix — separate the three things the old concept conflated

| | What it is | Old concept (conflated) | New (DCN-12) |
|---|---|---|---|
| **Energy / volume** | what inflates the bladders | hydrostatic via disk | **the well** (CT pump fluid, or hydrostatic) — unchanged source, but *gated* |
| **Initiation** | what starts it, *when* | absolute pressure threshold | a **deliberate operator command** that is position-correct |
| **Sequencing** | EQ → S1 → S2 order | pressure thresholds + time orifice | **mechanical: each stage's completion enables the next** |

Once you stop asking one passive pressure threshold to do all three jobs, each
job has a clean, defensible solution.

---

## 3. Initiation — position-correct, run-in-safe, by conveyance

Both conveyances feed a **common sequence manifold** (new sub **SHEX-017**); the
*front end* differs, everything downstream of the gate is identical.

### 3.1 Coiled tubing — applied differential (depth-independent)

Operator pumps the CT bore to **hydrostatic + ~1500 psi** at depth. A reference
piston with **CT bore on one face and annulus on the other** responds only to
the *applied differential*, so depth/hydrostatic cancel:

| Depth | Annulus | Trigger pressure | vs bladder rating 2500 |
|---|---|---|---|
| 2000 ft | 936 psi | 2436 psi (always +1500) | ok |
| 8000 ft | 3744 psi | 5244 psi | ok (CT bore handles it) |
| 12000 ft | 5616 psi | 7116 psi | ok |

A **ball/dart seat** is added as a positive arm: nothing in the manifold can
move until the ball lands, so run-in and circulating pressures are mechanically
locked out. This is standard CT inflatable-packer / hydraulic-set practice.

### 3.2 Electric wireline — fire the gate, let hydrostatic fill

E-line has no flow path and a charge cannot supply 1898 cc. So split it:

- a **small EFI/igniter** (the same class of initiator the Baker E-4 already
  uses) **opens the gate on command** — total position control;
- **wellbore hydrostatic** then supplies the large volume to inflate.

Hydrostatic must exceed the deploy demand at set depth (p1 = 941 psi): true at
**≥ ~2000 ft / 9 ppg** and deeper. Shallow or under-balanced sets fall back to
the documented **gas-generator boost** option.

> This mirrors how the secondary-stroke tool already works on e-line (a
> command-fired power charge), so the conveyance crew uses one familiar
> initiation model for both strokes.

---

## 4. Sequencing — completion-gated, not threshold/time

This is the heart of the interlock. Instead of trusting pressure magnitude or a
timer, **each stage's completion physically arms the next**, using the
expansion's own **pressure signature**:

1. While a stent is still opening, bladder pressure sits at its **deploy
   plateau** (~941 psi stage 1) — work is being done hinging the mesh.
2. When the stent hits its **hard stop** (fully open), no more volume is
   accepted and pressure **climbs from the plateau toward source**.
3. That climb shifts a **shear-pinned arming sleeve** (set ~1720 psi — above the
   plateau, below the 2500 psi rating) that **uncovers the next stage's feed
   port.**

Order is now a **physical guarantee**, independent of depth, temperature and
pump rate. The metering orifice is kept only to keep the plateau stable
(damping), **not** as the sequencer. The body-lock ratchet rings still hold each
stage open after pressure bleeds (unchanged).

```
gate open ──► EQ pilot strokes ──► EQ ports CLOSE ──► uncovers S1 port
          ──► S1 bladder ──► stent Ø3.375 ──► bottom-out spike ──► uncovers S2 port
          ──► S2 bladder ──► stent Ø5.750 ──► "ready" signature ──► hand off to tool
```

---

## 5. Equalizing-sleeve interlock (this is what makes EQ close *first*)

The EQ sleeve (existing **SHEX-013**) must close before the stages expand
(so the plug can hold differential) but must **not** close during run-in (or you
swab/surge). DCN-12 makes that automatic:

- The gate pressure reaches the **EQ pilot (SHEX-016A) first** — lowest preload,
  shortest travel — and shifts the SHEX-013 sleeve ~0.375 in to **close the
  ports**.
- The pilot's **end-of-stroke uncovers the stage-1 feed port**, so S1 cannot
  start until EQ is shut.
- Pilot effective area 0.866 in² develops 407 lbf at just 470 psi and >3000 lbf
  at 8000-ft hydrostatic — ample over the ~150 lbf sleeve friction plus a
  calibrated shear pin.

EQ-close-before-stage-1 is therefore **mechanically enforced**, not a timing
hope.

---

## 6. Fail-safe states (defined, not left to chance)

| State reached | Plug condition | Recovery / next step |
|---|---|---|
| Gate never opened | collapsed Ø1.688 | normal POOH — nothing has fired |
| Gate open, EQ closed only | Ø1.688, ports shut | pull to re-open EQ via shift profile; fish on mandrel |
| Stage 1 only | Ø3.375, not anchored | recoverable on the mandrel; EQ re-opens on pull |
| Stages 1+2 complete | Ø5.750, locked open | proceed to the secondary (tool) stroke |
| Full set | Ø8.65 / seals / slips | tool shears free; plug holds |

The ratchets are one-way for hold-open, but a **shift-to-release profile** on the
mandrel (pulled by the fishing tool) collapses them for retrieval — which also
gives us a concrete answer to the separate open "retrieval kinematics" item.

---

## 7. What this adds to the tool (new/changed hardware)

| Item | Part | Role | Status |
|---|---|---|---|
| **Sequence / initiation sub** | **SHEX-017** (new) | houses the gate, ball seat (CT) / EFI port (e-line), reference piston, S1→S2 arming sleeve, metering orifice, manifold drillings | **to design** |
| EQ pilot | SHEX-016A (exists) | strokes first, closes SHEX-013, arms S1 | re-task per §5 |
| EQ sleeve | SHEX-013 (exists) | add the S1-arming port uncovered at end-of-stroke | minor rev |
| Charge subs | SHEX-014C / 015E (exist) | become **feed ports** off the manifold, not independent disks | re-task |
| Mandrel | SHEX-011 | add manifold drillings + arming-sleeve bore + ratchet bands | drawing update (already an open item) |

---

## 8. Proposed DCN-12

> **DCN-12 — First-stroke initiation & sequencing.** Replace the passive
> hydrostatic-referenced burst-disk trigger (p1<p2 + time orifice) with a
> **commanded-initiation, completion-sequenced** architecture: (a) energy from
> the well, (b) initiation by CT applied differential + ball seat *or* e-line
> EFI gate, (c) sequencing by completion/pressure-signature arming sleeves that
> physically enable each next stage, with the EQ pilot interlocked to close
> first. Adds sub **SHEX-017**; re-tasks SHEX-013/014C/015E/016A; defines
> fail-safe states. Rationale: a passive absolute-pressure trigger has no
> position control and fires during run-in (proven in `trigger_design.py` §1).

---

## 9. What I'd build next (on your go-ahead)

1. **CAD** `cad/actuator_solids.py`: add **SHEX-017** sequence sub (gate, ball
   seat, reference piston, arming sleeve, manifold) + the SHEX-013 arming-port
   rev; wire it into the run-in/deployed sub-assemblies.
2. **Drawing** ACT-DWG-017 (sequence sub) + SHEX-013 rev.
3. **Manual**: fold §1–6 into `ACTUATOR_MANUAL.md` Part 1.5/Part 4 and add
   DCN-12 to Part 5; index this memo.
4. **Figure**: a one-page sequence/interlock schematic (gate → EQ → S1 → S2).
5. **RELEASE_NOTES / logs**: record DCN-12.

Open items that still require **test/FEA** (cannot be closed on paper): EFI/gas-
generator selection and qualification, shear-pin/arming-sleeve calibration
across temperature, full-scale deploy of the completion-gating signature, and
the ball-seat/CT-pressure interface to the specific Model J tool.

---

*SHEX-EM-001 Rev A — conceptual engineering memo. Numbers are first-order
(`trigger_design.py`); not qualified for downhole use without test + FEA.*
