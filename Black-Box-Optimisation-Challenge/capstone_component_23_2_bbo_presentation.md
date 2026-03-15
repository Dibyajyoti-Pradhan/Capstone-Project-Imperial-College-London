# Capstone Component 23.2 — Your Approach to the BBO Capstone Project
## A Structured Presentation of Methodology, Evolution and Insights

**Author:** Dibyajyoti Pradhan
**Programme:** Imperial College London — Professional Certificate in ML/AI
**Submitted:** 15/03/2026 | **Cohort:** IMP-PCMLAI-25-08

---

## Section 1: Overview of the BBO Approach

### What Am I Trying to Achieve?

The Black-Box Optimisation challenge tasks me with maximising eight unknown functions — F1 through F8 — across input spaces ranging from 2 to 8 dimensions. Each function behaves like a sealed vault: coordinates go in, a single scalar comes back, and the internal mechanics are never revealed. With only 13 query opportunities per function across the entire programme, every submission must be chosen deliberately.

The core objective is to find the input combination that yields the highest possible output for each function within this strict query budget. Unlike supervised learning — where data is plentiful and model improvement is gradual — BBO forces hard choices: a wasted query on a poor region is unrecoverable.

### Strategy at a Glance

The approach unfolds in three phases that mirror how understanding builds in any learning process:

1. **Exploration (Weeks 1–3):** Cast a wide net. Identify which regions of the input space produce any signal, which dimensions appear to matter, and which functions have obvious structure.
2. **Pattern recognition (Weeks 4–8):** Fit Gaussian Process surrogates to the accumulated data. Use Upper Confidence Bound (UCB) acquisition to balance information gain against exploitation of known peaks.
3. **Exploitation (Weeks 9–13):** Commit. Narrow trust regions around best-known coordinates. Apply gradient-guided search for high-dimensional functions. Reduce effective dimensionality where analysis reveals irrelevant dimensions.

The unifying principle across all phases: **treat uncertainty as information**, not an obstacle. Regions the model doesn't understand are as valuable as regions it knows well — until budget constraints force commitment.

---

## Section 2: How Strategy Has Evolved

### Early Rounds: Searching Blind

Weeks 1–2 used maximum-distance heuristics and Latin Hypercube Sampling with no surrogate model. The sole objective was coverage — ensuring queries spanned the input space rather than clustering. This was intentionally uninformed: forcing diversity before committing to any region.

### Key Inflection Points

| Round | Change | Driver |
|:------|:-------|:-------|
| Week 3 | Introduced GP surrogates + UCB acquisition | Enough data to fit a meaningful surrogate |
| Week 4 | Added MLP gradient ascent for F7/F8 | High-dimensional functions needed directional guidance beyond GP |
| Week 5 | Function-specific κ scheduling | Observed F5 consistently returning ~1600; F1/F7 still flat |
| Week 7 | Trust regions for F5 and F8 | Confirmed high-output basins; global search wasteful |
| Week 8 | LLM-assisted hypothesis generation | Used structured prompting to critique surrogate suggestions |
| Week 12 | PCA-inspired dimension reduction for F8 | Gradient analysis revealed X₁/X₃/X₆/X₈ dominant; fixed remainder |

### Guiding Principles (Current)

- **κ follows confidence:** Low κ (0.05–0.2) for functions with confirmed peaks; high κ (1.5–2.5) for functions still showing uncertainty
- **Trust regions follow evidence:** Radius shrinks only when multiple consecutive queries confirm a stable peak, not optimistically
- **Gradient sensitivity drives dimensionality:** Dimensions with |∂f/∂xᵢ| < 0.05 across all observations are treated as noise and fixed

---

## Section 3: Patterns, Data and Insights

### Most Meaningful Trends

**F5 — The clearest signal:** From Week 1, the corner (0.999, 0.999, 0.999, 0.999) returned ~1600, far above the initial data range. All subsequent F5 queries have refined within a shrinking neighbourhood of this point. The output surface appears to be a sharp ridge at the boundary — a pattern invisible from the initial data alone.

**F8 — Two-factor structure:** Gradient analysis across 21 observations consistently shows that X₁ and X₃ (small values) combined with X₆ and X₈ (large values) drive output. The remaining four dimensions contribute minimally. This is the BBO equivalent of a PCA scree plot with two dominant eigenvalues.

**F1 and F7 — Persistent uncertainty:** Despite 12 queries each, neither function has converged. F1 output remains near zero across diverse regions; F7 shows mild positive gradients but no clear peak. These may be intrinsically noisy or have optima in regions not yet sampled.

**F3 and F6 — Negative basins:** Both functions returned negative outputs in early explorations. Mid-programme queries shifted toward regions that minimised negativity. Current understanding: small X₁ values with moderate X₂/X₃ appear preferable for F3.

### Variables That Influence Results Most

Applying a PCA framing to the 21-point dataset:

| Function | Dominant dimensions | Effective dimensionality |
|:---------|:-------------------|:------------------------|
| F5 | All four, uniformly | 4D (boundary optimum) |
| F8 | X₁, X₃, X₆, X₈ | ~4D of 8D |
| F7 | X₂, X₆ | ~2D of 6D |
| F4 | X₁, X₃ | ~2D of 4D |

---

## Section 4: Decision-Making and Iteration

### Balancing Exploration and Exploitation

The exploration-exploitation trade-off was managed differently per function based on observed variance:

- **High confidence (F5, F8):** UCB κ ≤ 0.1 with trust regions. Exploitation dominates.
- **Moderate confidence (F2, F4, F6):** κ = 0.4–0.8. Balanced search near GP posterior maximum.
- **Low confidence (F1, F7):** κ ≥ 1.5. Exploration maintained to avoid prematurely abandoning the search.

### Two Strategic Decisions

**Decision 1 — F5 early commitment (Week 1):**
The max-distance heuristic happened to place the Week 1 F5 query at (0.999, 0.999, 0.999, 0.999), returning ~1600 — orders of magnitude above the initial data. This was partly luck, but the decision to *commit* a trust region around this point from Week 5 onward was deliberate. Risk: the true optimum might not be at the exact boundary. Result: consistent high-output queries in every subsequent round confirmed the commitment was sound.

**Decision 2 — F8 dimensionality reduction (Week 12):**
Rather than continuing to search all 8 dimensions with a GP that struggled in high dimensions, finite-difference gradient analysis identified four irrelevant dimensions. Fixing these and running UCB over the reduced 4D subspace immediately improved candidate quality. What didn't work earlier: treating F8 identically to lower-dimensional functions — the GP's curse of dimensionality caused it to produce flat, uninformative uncertainty estimates.

### Handling Uncertainty

When results didn't match expectations — particularly for F3 and F6, where outputs remained stubbornly low — the response was to broaden search (increase κ) rather than persist with exploitation. The key diagnostic: if the GP posterior maximum stops improving across three consecutive iterations, treat the current best as a local optimum and explore.

---

## Section 5: Next Steps and Reflection

### Final Round (Week 13) Plan

- **F5:** One micro-perturbation within r=0.005 of best known — final attempt to find whether the true optimum is exactly at the boundary or marginally inside
- **F8:** Fixed-subspace GP acquisition over X₁/X₃/X₆/X₈ only
- **F1/F7:** Single high-exploration query in the region of highest posterior uncertainty — last opportunity before budget exhaustion
- **F2–F4/F6:** Pure GP posterior maximum exploitation

### Connection to the Broader ML Landscape

This project operationalises the core challenge of modern ML deployment: learning from limited, expensive feedback in high-dimensional spaces. The same tension between exploration and exploitation that governs BBO query selection governs hyperparameter tuning, neural architecture search, drug discovery, and automated experiment design. The GP-UCB framework used here is the theoretical foundation for tools like Google's Vizier and Meta's BoTorch — production systems managing billions of model training runs.

BBO also illustrates *why* uncertainty quantification matters beyond accuracy metrics. In constrained settings, knowing *what you don't know* is as valuable as knowing what you do — a lesson that applies equally to deploying ML models in regulated industries such as finance and healthcare.

### Communicating Results to a Non-Technical Audience

Think of each function as a landscape with hills and valleys, but you're blindfolded and can only take 13 steps. Each step tells you your current height but not the terrain ahead. The strategy is: start by spreading out to get a feel for the landscape, build a mental map as you go, then head toward the highest ground with increasing confidence. By Round 12, for some functions we've found peaks much higher than where we started — for others, the landscape remains frustratingly flat. The final round is one last committed step toward the best position we've found.

---

## References

Eriksson, D. et al. (2019) 'Scalable global optimization via local Bayesian optimization', *NeurIPS*, 32.

Jones, D.R., Schonlau, M. and Welch, W.J. (1998) 'Efficient global optimization of expensive black-box functions', *Journal of Global Optimization*, 13(4), pp. 455–492.

Srinivas, N. et al. (2010) 'Gaussian process optimization in the bandit setting: no regret and experimental design', *Proceedings of ICML*, pp. 1015–1022.
