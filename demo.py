"""
Self-contained demo on SYNTHETIC landmark coordinates (no patient data).

Shows the full pipeline:
  1. compute the 18 measurements
  2. Monte Carlo error propagation (jitter each landmark, re-measure)
  3. Tweed geometric self-check
"""
import numpy as np
from measure import measure, tweed_check

# --- synthetic landmark set (made-up coordinates, not a real patient) ---
SYN = {
    "S": (0, 0), "N": (470, -40), "A": (515, 420), "B": (475, 800),
    "Pog": (470, 840), "Gn": (455, 880), "Me": (430, 890), "Go": (-110, 650),
    "Ar": (-120, 255), "Por": (-180, 150), "Or": (320, 265),
    "L1a": (440, 760), "L1t": (515, 560), "U1a": (480, 410), "U1t": (560, 560),
}


def monte_carlo(base, sigma_px=1.5, n=2000, seed=0):
    rng = np.random.default_rng(seed)
    samples = {}
    for _ in range(n):
        p = {k: np.array(v, float) + rng.normal(0, sigma_px, 2) for k, v in base.items()}
        for k, val in measure(p).items():
            samples.setdefault(k, []).append(val)
    return {k: (float(np.mean(v)), float(np.std(v))) for k, v in samples.items()}


if __name__ == "__main__":
    r = measure(SYN)
    print(f"Tweed self-check (should be 180): {tweed_check(r):.1f}\n")

    stats = monte_carlo(SYN)
    print(f"{'measure':14}{'value':>9}{'±2σ':>9}")
    for k, (m, s) in stats.items():
        print(f"{k:14}{m:9.1f}{2*s:9.2f}")
