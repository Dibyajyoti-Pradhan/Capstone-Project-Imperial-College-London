# Required Capstone Component 22.1: Refining BBO Strategies — Round 11

## Part 1: Queries Submitted

| Function | Dimension | Query |
|----------|-----------|-------|
| F1 | 2D | (0.152834, 0.341729) |
| F2 | 2D | (0.648213, 0.283047) |
| F3 | 3D | (0.728491, 0.467038, 0.608217) |
| F4 | 3D | (0.574812, 0.748391, 0.427963) |
| F5 | 4D | (0.961283, 0.058174, 0.851293, 0.972418) |
| F6 | 5D | (0.697234, 0.528471, 0.762841, 0.371893, 0.637524) |
| F7 | 6D | (0.213847, 0.492183, 0.678341, 0.147293, 0.831472, 0.392841) |
| F8 | 8D | (0.871492, 0.496738, 0.934821, 0.378413, 0.507829, 0.671384, 0.432817, 0.586941) |

---

## Part 2: Reflection

### 1. How have patterns in your past queries influenced your latest choices?

Eleven rounds of queries have produced a layered picture: each function now has a recorded trajectory rather than a scatter of isolated points. Functions F4, F5 and F8 show consistent directional improvement — the running best improves nearly every round — and their Round 11 queries continue the established vector with small, deliberate steps. F1 remains near-zero despite multiple probes in different quadrants; rather than persisting near explored territory, Round 11 tests a new region (0.15, 0.34) that no prior round has sampled, treating the previous cluster of near-zero outputs as a confirmed unproductive zone. F2 and F3 show moderate, gradual improvement; their queries extend the current trajectory by approximately 0.02–0.03 in each productive dimension.

---

### 2. Identified clusters or recurring regions in the search space

Applying a clustering lens to the accumulated query history reveals three natural groupings across all eight functions:

**Converging cluster (F4, F5, F8):** Queries have tightened into compact, high-density regions around consistently high outputs. For F5, the cluster centroid lies near (0.96, 0.06, 0.85, 0.97) — a boundary ridge that has produced the highest observed values (~1600+). For F8, X₁ and X₃ act as the dominant axes; the effective cluster is approximately a 2D slice of the full 8D space. These clusters are tight and credible — surrogate uncertainty is low within them.

**Drifting cluster (F2, F3, F6):** Queries show directional movement rather than convergence — a slowly translating centroid indicating a broad, gently sloping optimum rather than a sharp peak. The cluster is expanding along the improvement direction, resembling the elongated clusters that single linkage merges readily.

**Unresolved cluster (F1, F7):** Outputs are either near-zero or inconsistent across adjacent probes. These do not exhibit any spatial pattern suggesting a local optimum. Round 11 probes an undersampled region for both functions rather than refining a spurious peak.

---

### 3. Strategies that proved less effective and adjustments made

Aggressive gradient ascent without trust-region constraints failed for F6 in earlier rounds — the MLP surrogate identified a misleading ridge that collapsed when probed directly. I reverted to GP-guided UCB acquisition with κ=1.5 and ±0.04 perturbation bounds for F6. More broadly, applying uniform trust-region radii across all functions ignored the significant heterogeneity in function sensitivity: F5's output drops sharply outside its ridge, while F3's landscape is much flatter. Round 11 uses function-specific radii calibrated to the empirical output sensitivity observed in rounds 7–10.

---

### 4. Parallels to how clustering algorithms separate meaningful patterns from noise

The trust-region radius functions analogously to a clustering distance threshold: too large and meaningful sub-structure within the high-performance region is smoothed away; too small and the algorithm never consolidates a coherent centroid. The shift from GP exploration (κ=3.0) to GP exploitation (κ=1.5) mirrors the transition from initialising cluster centroids broadly to refining them toward the true cluster mean. Most directly, treating the unresolved functions (F1, F7) as confirmed low-output zones and redirecting query budget away from them mirrors k-means reassigning outlier points to a separate cluster rather than distorting the centroid of a productive cluster to accommodate them.

---

### 5. Trends and groupings if results were plotted

Plotting best-observed output against round number would reveal the three groupings identified above: a steeply rising series for F5 and F8, a gradually rising series for F2–F4 and F6, and a flat near-zero series for F1 and F7. In a 2D projection of query coordinates (first two input dimensions across all functions), the converging-cluster functions would show tightly concentrated late-round points, the drifting-cluster functions would show a visible directional sweep, and the unresolved functions would show scattered points with no spatial coherence. This plot would directly confirm the Round 12 strategy: lock in the converging functions, continue the drift trajectory for the moderate functions, and reassign the unresolved functions' budget to a final exploratory sweep.

---

### References

Shahriari, B., Swersky, K., Wang, Z., Adams, R.P. and de Freitas, N. (2016) 'Taking the human out of the loop: A review of Bayesian optimization', *Proceedings of the IEEE*, 104(1), pp. 148–175.

Frazier, P.I. (2018) *A tutorial on Bayesian optimization*. arXiv:1807.02811.
