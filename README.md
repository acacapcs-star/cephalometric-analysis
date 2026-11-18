# Cephalometric Measurement & Error Analysis

Computes **18 cephalometric measurements** from 2D lateral-cephalogram
**landmark coordinates**, with **Monte Carlo error propagation** and a
**geometric self-check**. Part of a cross-institution orthodontics × CS
research collaboration; this repository contains **only my own code**,
demonstrated on **synthetic coordinates** — no patient data, images, or
clinical results are included.

## What this does

Given the (x, y) positions of anatomical landmarks (Sella, Nasion, A-point,
B-point, …), the code computes standard cephalometric angles and distances
(SNA, SNB, ANB, FMA/FMIA/IMPA, …) and, crucially, **how trustworthy each
number is**.

Three ideas:

1. **Three geometry primitives.** Every one of the 18 measurements is built
   from just: angle-at-a-point, angle-between-two-lines, and
   point-to-line distance. (`measure.py`)

2. **Monte Carlo error propagation.** Landmark placement is never pixel-exact.
   Each landmark is jittered by ±1.5 px and all measurements are recomputed
   2000 times, giving every measurement a standard deviation σ — a direct
   answer to *"how much could this number move if my hand slipped?"*
   ANB comes out most stable (subtraction cancels the shared baseline);
   the inter-incisal angle is most sensitive (short arms).

3. **Tweed geometric self-check.** FMA + FMIA + IMPA must equal 180°
   (interior angles of a triangle). The code checks this automatically, which
   catches sign/convention errors in the formulas. (`tweed_check`)

## Run the demo (synthetic data)

```bash
pip install numpy
python demo.py
```

Output: the 18 measurements on a made-up landmark set, each with its ±2σ
error bar, plus the Tweed self-check (= 180.0).

## Files

| File | What it is |
|---|---|
| `measure.py` | The 18 measurements + the three geometry primitives |
| `demo.py` | End-to-end demo on synthetic coordinates (Monte Carlo + Tweed) |
| `measurement_definitions.md` | Each measurement: landmarks used, formula, meaning |

## My role

I implemented the measurement and error-analysis code (the computation from
coordinates, Monte Carlo propagation, and the geometric self-check) and
validated it against hand calculations and the Tweed identity. Clinical
definitions and the landmark annotations are provided by the dental side of
the collaboration.

## Scope & data

The 18-measurement list is standard clinical cephalometric analysis. Patient
radiographs, coordinates, and any patient-derived results are **not** in this
repository and are handled only within the research team under the relevant
institutional data rules.
