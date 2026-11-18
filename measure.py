"""
Cephalometric measurement from 2D landmark coordinates.

All 18 measurements are built from three geometry primitives:
  - angle_at(point)      : angle at a vertex formed by two other points
  - angle_between(lines) : angle between two lines
  - point_to_line(dist)  : perpendicular distance from a point to a line

Author: Olivia Lan
Note: runs on landmark coordinates only. No patient data is included
in this repository; see demo.py for a synthetic example.
"""
import numpy as np


def angle_at(p, a, vertex, b):
    """Angle A-vertex-B (degrees)."""
    V = np.asarray(p[vertex], float)
    va = np.asarray(p[a], float) - V
    vb = np.asarray(p[b], float) - V
    cos = np.dot(va, vb) / (np.linalg.norm(va) * np.linalg.norm(vb))
    return float(np.degrees(np.arccos(np.clip(cos, -1, 1))))


def angle_between(p, a1, a2, b1, b2):
    """Angle between line a1->a2 and line b1->b2 (degrees)."""
    v1 = np.asarray(p[a2], float) - np.asarray(p[a1], float)
    v2 = np.asarray(p[b2], float) - np.asarray(p[b1], float)
    cos = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    return float(np.degrees(np.arccos(np.clip(cos, -1, 1))))


def point_to_line(p, pt, a, b):
    """Perpendicular distance from pt to line a-b (pixels)."""
    A = np.asarray(p[a], float)
    ab = np.asarray(p[b], float) - A
    ap = np.asarray(p[pt], float) - A
    return float(abs(ab[0] * ap[1] - ab[1] * ap[0]) / np.linalg.norm(ab))


def measure(p, mm_per_px=1.0):
    """Return the 18 cephalometric measurements for one landmark set `p`.

    `p` maps landmark name -> (x, y). `mm_per_px` converts the two
    distance measures to millimetres (e.g. from a ruler of known length).
    """
    r = {}
    r["SNA"] = angle_at(p, "S", "N", "A")
    r["SNB"] = angle_at(p, "S", "N", "B")
    r["ANB"] = r["SNA"] - r["SNB"]           # signed: preserves Class III
    r["Convexity"] = angle_at(p, "N", "A", "Pog")
    r["Facial"] = angle_between(p, "Por", "Or", "N", "Pog")
    r["Y_axis"] = angle_between(p, "S", "Gn", "Por", "Or")
    r["FMA"] = angle_between(p, "Por", "Or", "Go", "Me")
    r["FMIA"] = angle_between(p, "Por", "Or", "L1a", "L1t")
    r["IMPA"] = 180 - angle_between(p, "Go", "Me", "L1a", "L1t")
    r["Interincisal"] = angle_between(p, "U1a", "U1t", "L1a", "L1t")
    r["U1_SN"] = 180 - angle_between(p, "S", "N", "U1a", "U1t")
    r["U1_FH"] = 180 - angle_between(p, "Por", "Or", "U1a", "U1t")
    r["Gonial"] = angle_at(p, "Ar", "Go", "Me")
    r["Ramus"] = angle_between(p, "Ar", "Go", "Por", "Or")
    r["AB_plane"] = angle_between(p, "N", "Pog", "A", "B")
    r["FH_SN"] = angle_between(p, "Por", "Or", "S", "N")
    r["U1_APog_mm"] = point_to_line(p, "U1t", "A", "Pog") * mm_per_px
    r["U1_NPog_mm"] = point_to_line(p, "U1t", "N", "Pog") * mm_per_px
    return r


def tweed_check(r):
    """Geometric self-check: FMA + FMIA + IMPA must equal 180 degrees."""
    return r["FMA"] + r["FMIA"] + r["IMPA"]
