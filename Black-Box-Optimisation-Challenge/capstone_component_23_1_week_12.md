# Required Capstone Component 23.1 — Week 12
## Refining Strategies for the Black-Box Optimisation Challenge

**Module:** 23 — Dimensionality Reduction
**Submitted:** 15/03/2026
**Cohort:** IMP-PCMLAI-25-08

---

## Part 1: Queries Submitted

| Function | Dimensions | Strategy | Query Submitted | Output |
|----------|------------|----------|-----------------|--------|
| F1 | 2D | Moderate exploration (κ=1.5) | 0.829693-0.767563 | TBC |
| F2 | 2D | Exploitation (κ=0.5) | 0.751849-0.922897 | TBC |
| F3 | 3D | Exploitation (κ=0.5) | 0.206105-0.261386-0.419116 | TBC |
| F4 | 4D | Tight exploitation (κ=0.3) | 0.593846-0.430421-0.420627-0.224232 | TBC |
| F5 | 4D | Ultra-tight trust-region (κ=0.05, r=0.01) | 0.992141-0.971422-0.991386-0.980369 | TBC |
| F6 | 5D | Balanced (κ=0.8) | 0.699188-0.126146-0.709437-0.669891-0.061930 | TBC |
| F7 | 6D | GP gradient ascent (κ=2.0) | 0.010536-0.496781-0.291065-0.231724-0.379195-0.721570 | TBC |
| F8 | 8D | Ultra-tight trust-region (κ=0.05, r=0.04) | 0.063553-0.189558-0.084752-0.057006-0.401034-0.705107-0.555764-0.950381 | TBC |

---

## Part 2: Reflection on Strategy — Twelfth Iteration (21 Data Points)

---

### 1. How Strategy Has Evolved

Week 1 was pure exploration — max-distance queries with no surrogate model, relying on Latin Hypercube Sampling to cover the input space without prior beliefs. By Week 12, the approach has become fully systematic:

- **Surrogate models** (GPs, MLPs) now underpin every query, replacing intuition with uncertainty quantification
- **Function-specific κ schedules**: high-confidence functions (F5, F8) operate at κ=0.05 whilst uncertain ones (F1, F7) retain κ≥1.5
- **Trust regions** anchor high-performing functions within ±0.01–0.04 of best-known coordinates, preventing wasteful exploration of regions the GP has already rejected
- **Gradient-guided search** on F7 uses finite-difference sensitivity to navigate the 6D space directionally rather than stochastically

The shift from week to week has been one of progressive commitment — trading broad coverage for precision as evidence accumulates.

---

### 2. Principal Directions of Variation — A PCA Lens

With 21 data points per function, the data set is rich enough to identify which dimensions drive the largest variation in outputs. Applying the PCA framing directly:

| Function | Dominant "PC1" dimension | Pattern identified |
|:---------|:------------------------|:-------------------|
| F5 | All four dimensions equally | High-output ridge near (0.999)⁴; near-uniform loading across X₁–X₄ |
| F8 | X₁, X₃ (small) and X₆, X₈ (large) | Two-factor structure; X₂/X₄/X₅/X₇ contribute minimally |
| F7 | X₂, X₆ | Moderate positive gradient; X₁ and X₄ near-zero sensitivity |
| F4 | X₁, X₃ | Mid-range values optimal; boundary regions underperform |

For F8, this analysis led to effective dimensionality reduction: fixing X₂/X₄/X₅/X₇ at their best-known values and optimising only over X₁/X₃/X₆/X₈ — exactly the "keep the principal components, discard the noise" logic of PCA applied to black-box optimisation.

---

### 3. What to Explore vs What to Reduce

PCA's core insight is to retain dimensions that explain variance and discard those that do not. I applied this heuristic explicitly:

- **Retain and refine:** Dimensions where gradient sensitivity exceeds a threshold (|∂f/∂xᵢ| > 0.05). For F8, this is X₁/X₃/X₆/X₈.
- **Fix and ignore:** Dimensions where sensitivity is near zero across all 21 observations — treated as irrelevant (analogous to low-variance PCs).
- **Maintain exploration:** F1 and F7 still show high uncertainty across their spaces; reducing search here risks missing undiscovered peaks.

The decision rule is adaptive: as each new observation arrives, the sensitivity estimates are updated and the effective search dimensionality can shift.

---

### 4. Implications for the Final Round (Week 13)

With one query remaining per function, the final round must be decisive. The strategy:

- **F5:** One final micro-perturbation around (0.992, 0.971, 0.991, 0.980) — small random offset within r=0.005 to avoid duplicating Week 12 exactly while staying in the confirmed high-output basin
- **F8:** Fix X₂/X₄/X₅/X₇ at best-known values; optimise X₁/X₃/X₆/X₈ via GP acquisition over the reduced 4D subspace
- **F1/F7:** Final exploratory query in the highest-uncertainty region — the last opportunity to discover a better mode before the budget expires
- **F2–F4/F6:** Pure exploitation of the GP posterior maximum; no exploration value in the final round for converging functions

---

### 5. PCA Insights Applied to BBO Results

PCA focuses on explaining variance, not raw values. This reframing changed how I interpret BBO progress:

- **High variance in outputs** signals that the surrogate is genuinely uncertain — worthwhile to explore
- **Low variance across recent queries** for a function signals convergence — time to switch to pure exploitation
- **Redundant dimensions** (high inter-dimension correlation in query coordinates) indicate the search has collapsed into a subspace — the same information PCA would compress into fewer components

The practical lesson: tracking the variance of predicted outputs across candidates, not just the maximum, provides a richer diagnostic for when to switch strategies. A falling variance envelope indicates diminishing information value of further exploration — the GP equivalent of a PCA scree plot flattening.

---

## References

Srinivas, N. et al. (2010) 'Gaussian process optimization in the bandit setting: no regret and experimental design', *Proceedings of ICML*, pp. 1015–1022.

Eriksson, D. et al. (2019) 'Scalable global optimization via local Bayesian optimization', *Advances in Neural Information Processing Systems*, 32.
