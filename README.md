# leo-channel-reproduction
# Reproducing Two LEO Ray-Tracing Channel Papers

Open-source reproduction of the channel-modeling pipeline described in:

1. Ning et al. — arXiv:2501.02798
2. Khawaja et al. — arXiv:2507.14622

## Project order

### Paper 1 — Geometry and Doppler

TLE
→ SGP4
→ satellite position/velocity
→ ground-relative geometry
→ elevation/azimuth/range
→ relative velocity
→ Doppler

### Paper 2 — Ray Tracing and Channel Statistics

Scene
→ ray tracing
→ multipath components
→ attenuation
→ Rician/shadowed-Rician fading
→ K-factor
→ RMS delay spread
→ angular spread
→ DBSCAN

### Validation

Results are compared against the reported trends/ranges in the papers
and against 3GPP NTN reference models.

## Reproducibility rule

No channel number is considered valid unless its relevant
hardware/carrier configuration, TLE, ground-station geometry,
and scene/environment are explicitly stated.

Absolute numerical agreement with the papers is not required when
their TLE, scene geometry, or proprietary ray-tracing implementation
cannot be reproduced. Trend, order-of-magnitude, and physical
consistency are the primary validation criteria.