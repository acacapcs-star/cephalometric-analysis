# Cephalometric Measurement & Error Analysis

Computes **cephalometric measurements** from 2D lateral-cephalogram
**landmark coordinates**, with **Monte Carlo error propagation** and a
**geometric self-check**. Part of a cross-institution orthodontics × CS
research collaboration (started 2026/09, ongoing).

> This repository contains **only my own code**, demonstrated on
> **synthetic coordinates**. No patient radiographs, coordinates, or
> clinical results are included; patient data is handled only within the
> research team under its institutional data rules.

## My role

Measurement computation and error analysis on the CS side: turning
annotated landmark coordinates into standard cephalometric angles and
distances, and quantifying how much landmark-placement error moves each
measurement.

## What this does

Given the (x, y) positions of anatomical landmarks (Sella, Nasion, A-point,
B-point, …), compute standard cephalometric measurements (SNA, SNB, ANB,
FMA, Y-axis, Interincisal, FMIA, …) and **how trustworthy each number is**.

**1 · Three geometry primitives.** Every measurement is built from just
angle-at-a-point, angle-between-two-lines, and point-to-line distance
(`measure.py`).

**2 · Three traps that give wrong numbers without any error.** Documented
because each one fails silently:

| Trap | Why it goes wrong |
|---|---|
| ANB must be `SNA − SNB` | The raw A–N–B angle is unsigned, so a Class III reads as Class II |
| Angles are scale-invariant, distances are not | Angles compare across machines; mm distances need calibration — the ruler on the film is 20 mm, used to convert pixels → mm |
| Image y-axis points down | Every geometric derivation must follow, or it flips upside-down |

**3 · Monte Carlo error propagation.** Landmark placement is never
pixel-exact. Each landmark is jittered by its σ and all measurements are
recomputed 2000 times, giving every measurement a standard deviation and a
95% interval.

**4 · Tweed geometric self-check.** FMA + FMIA + IMPA must equal 180°
(interior angles of a triangle). Checked automatically to catch
sign/convention errors in the formulas.

## A methodological point

Landmark error propagates into angles **unevenly**: in simulation (±1.5 px
per point), the same point error is small on long-armed angles and
amplified on short-armed ones. So a single "average error in mm" cannot say
whether any one measurement is usable — clinicians read angles, so the error
bar belongs on the angles. (A claim from simulation; the next step is to
validate it on human-corrected landmark data.)

For the same reason the benchmark should be **inter-observer variability**,
not absolute error: "the model is closer to the clinician than two
clinicians are to each other" is a much stronger statement than "error of
1.3 mm".

## Run the demo (synthetic data)

```bash
pip install numpy
python demo.py
```

Output: the measurements on a made-up landmark set, each with its ±2σ error
bar, plus the Tweed self-check (= 180.0).

## Files

| File | What it is |
|---|---|
| `measure.py` | The measurements + the three geometry primitives |
| `demo.py` | End-to-end demo on synthetic coordinates (Monte Carlo + Tweed) |
| `measurement_definitions.md` | Each measurement: landmarks used, formula, meaning |
