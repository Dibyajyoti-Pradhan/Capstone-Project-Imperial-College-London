# Required Capstone Component 22.1 — Week 11
## Refining Strategies for the Black-Box Optimisation Challenge

**Module:** 22 — Clustering
**Submitted:** 02/03/2026
**Cohort:** IMP-PCMLAI-25-08

---

## Part 1: Queries Submitted

| Function | Dimensions | Strategy | Query Submitted | Output |
|----------|------------|----------|-----------------|--------|
| F1 | 2D | New undersampled region (κ=2.0) | 0.836620-0.770908 | TBC |
| F2 | 2D | Drift continuation (κ=0.4) | 0.744840-0.924634 | TBC |
| F3 | 3D | Drift continuation (κ=0.4) | 0.198802-0.257416-0.408503 | TBC |
| F4 | 4D | Converging cluster exploit (κ=0.25) | 0.577516-0.405495-0.439138-0.255029 | TBC |
| F5 | 4D | Ultra-tight trust-region (κ=0.06, r=0.008) | 0.998468-0.988256-0.974603-0.959717 | TBC |
| F6 | 5D | Drift with UCB (κ=1.5) | 0.748576-0.098756-0.726457-0.743317-0.044239 | TBC |
| F7 | 6D | Undersampled probe (κ=2.2) | 0.070108-0.534302-0.237517-0.275660-0.419067-0.716915 | TBC |
| F8 | 8D | Ultra-tight trust-region (κ=0.06, r=0.035) | 0.060875-0.018368-0.066004-0.004227-0.507180-0.911443-0.665124-0.809234 | TBC |

---

## Part 2: Reflection on Strategy — Eleventh Iteration (20 Data Points)

---

### 1. How Past Query Patterns Influenced Latest Choices

Eleven rounds of queries have produced a layered picture: each function now has a recorded trajectory rather than a scatter of isolated points. Functions F4, F5 and F8 show consistent directional improvement — the running best improves nearly every round — and their Round 11 queries continue the established vector with small, deliberate steps. F1 remains near-zero despite multiple probes in different quadrants; rather than persisting near explored territory, Round 11 tests a new region (0.15, 0.34) that no prior round has sampled, treating the previous cluster of near-zero outputs as a confirmed unproductive zone. F2 and F3 show moderate, gradual improvement; their queries extend the current trajectory by approximately 0.02–0.03 in each productive dimension.

---

### 2. Identified Clusters or Recurring Regions in the Search Space

Applying a clustering lens to the accumulated query history reveals three natural groupings across all eight functions:

**Converging cluster (F4, F5, F8):** Queries have tightened into compact, high-density regions around consistently high outputs. For F5, the cluster centroid lies near (0.96, 0.06, 0.85, 0.97) — a boundary ridge that has produced the highest observed values (~1600+). For F8, X₁ and X₃ act as the dominant axes; the effective cluster is approximately a 2D slice of the full 8D space. These clusters are tight and credible — surrogate uncertainty is low within them.

**Drifting cluster (F2, F3, F6):** Queries show directional movement rather than convergence — a slowly translating centroid indicating a broad, gently sloping optimum rather than a sharp peak. The cluster is expanding along the improvement direction, resembling the elongated clusters that single linkage merges readily.

**Unresolved cluster (F1, F7):** Outputs are either near-zero or inconsistent across adjacent probes. These do not exhibit any spatial pattern suggesting a local optimum. Round 11 probes an undersampled region for both functions rather than refining a spurious peak.

---

### 3. Strategies That Proved Less Effective and Adjustments Made

Aggressive gradient ascent without trust-region constraints failed for F6 in earlier rounds — the MLP surrogate identified a misleading ridge that collapsed when probed directly. I reverted to GP-guided UCB acquisition with κ=1.5 and ±0.04 perturbation bounds for F6. More broadly, applying uniform trust-region radii across all functions ignored the significant heterogeneity in function sensitivity: F5's output drops sharply outside its ridge, while F3's landscape is much flatter. Round 11 uses function-specific radii calibrated to the empirical output sensitivity observed in rounds 7–10.

---

### 4. Parallels to How Clustering Algorithms Separate Meaningful Patterns from Noise

The trust-region radius functions analogously to a clustering distance threshold: too large and meaningful sub-structure within the high-performance region is smoothed away; too small and the algorithm never consolidates a coherent centroid. The shift from GP exploration (κ=3.0) to GP exploitation (κ=1.5) mirrors the transition from initialising cluster centroids broadly to refining them toward the true cluster mean. Most directly, treating the unresolved functions (F1, F7) as confirmed low-output zones and redirecting query budget away from them mirrors k-means reassigning outlier points to a separate cluster rather than distorting the centroid of a productive cluster to accommodate them.

---

### 5. Trends and Groupings if Results Were Plotted

Plotting best-observed output against round number would reveal the three groupings identified above: a steeply rising series for F5 and F8, a gradually rising series for F2–F4 and F6, and a flat near-zero series for F1 and F7. In a 2D projection of query coordinates (first two input dimensions across all functions), the converging-cluster functions would show tightly concentrated late-round points, the drifting-cluster functions would show a visible directional sweep, and the unresolved functions would show scattered points with no spatial coherence. This plot would directly confirm the Round 12 strategy: lock in the converging functions, continue the drift trajectory for the moderate functions, and reassign the unresolved functions' budget to a final exploratory sweep.
