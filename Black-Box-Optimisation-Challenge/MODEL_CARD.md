# Model Card: BBO Optimisation Approach

> Framework: Mitchell et al. (2019), *Model Cards for Model Reporting*

---

## Overview

| Field | Detail |
|-------|--------|
| **Name** | Hybrid GP–SVM–Neural BBO Optimiser |
| **Type** | Black-box function optimiser |
| **Version** | Final (Round 10, Module 21) |
| **Developer** | Dibyajyoti Pradhan |
| **Repository** | https://github.com/Dibyajyoti-Pradhan/Capstone-Project-Imperial-College-London |
| **Licence** | MIT |

---

## Intended Use

**What tasks is this approach suitable for?**
- Maximising unknown scalar functions with input domains in $[0, 1)^d$ for $d \in \{2, \ldots, 8\}$
- Settings with severely limited query budgets (≤15 evaluations per function)
- Problems where gradient information is unavailable and function evaluations are expensive

**What use cases should be avoided?**
- Functions with known gradients — gradient-based methods (Adam, L-BFGS) are more efficient
- Very high-dimensional spaces ($d > 20$) — GP cubic complexity and sparse sampling make this approach unreliable at scale
- Problems requiring real-time decisions — the strategy involves offline surrogate fitting and is not latency-sensitive
- Production systems without additional validation against held-out data

---

## Strategy Details

### Phase 1: Exploration (Rounds 1–2)
**Technique:** Maximum-distance heuristics; spatial coverage across all dimensions.
**Rationale:** With no output data, informed exploitation is impossible. Queries were distributed to maximise minimum pairwise distance, sampling corners, centroids and boundary regions.

### Phase 2: Pattern Recognition (Rounds 3–5)
**Technique:** Output-guided search with SVM region classification (RBF kernel) and Gaussian Process (GP) surrogates using Upper Confidence Bound (UCB) acquisition ($\kappa = 3.0$).
**Rationale:** After receiving initial outputs, functions were classified by magnitude and sign. SVM classifiers identified "promising vs unpromising" regions; GPs provided posterior uncertainty estimates to balance exploration and exploitation.

### Phase 3: Exploitation (Rounds 6–10)
**Technique:** Hybrid GP (for F1–F4, lower-dimensional) + shallow MLP surrogate (8→16→8→1, ReLU, for F7–F8). Gradient ascent from MLP: $x_{\text{new}} = x_{\text{best}} + \alpha \cdot \nabla_x \hat{f}(x_{\text{best}})$ with $\alpha = 0.03$. Trust-region exploitation with ±0.05 perturbation bounds.
**Rationale:** Accumulated data made surrogates reliable enough for targeted queries. Neural gradients identified dominant input dimensions (F8: $X_1$, $X_3$), enabling pseudo-2D search within higher-dimensional spaces.

### Module-by-Module Evolution

| Module | Strategy Focus | Key Change |
|--------|---------------|------------|
| 12 | Blind exploration | Max-distance sampling, no feedback |
| 13 | Output-guided | Function-specific strategies, 70/30 explore/exploit |
| 14 | SVM classification | Threshold outputs → binary region classifier |
| 15–16 | Neural surrogates | MLP gradient ascent for high-D functions |
| 17–21 | Full exploitation | Trust regions, dimension-aware search |

---

## Performance Summary

| Function | Dim | Strategy Phase | Behaviour | Round 10 Action |
|----------|-----|---------------|-----------|-----------------|
| F1 | 2D | Exploration | Near-zero outputs throughout | Probe unexplored region |
| F2 | 2D | Balanced | Moderate, improving | Small directional step |
| F3 | 3D | Balanced | Gradual improvement | Continue trajectory |
| F4 | 3D | Exploitation | Consistent gains | Local refinement |
| F5 | 4D | Full exploitation | Strong ridge ~1600+ | Boundary exploitation |
| F6 | 5D | Balanced | Noisy, moderate | Conservative refinement |
| F7 | 6D | Exploration | Plateau, uncertain | Probe undersampled region |
| F8 | 8D | Full exploitation | High, X₁/X₃ dominant | Gradient ascent step |

**Primary metric:** Observed function output at best query (maximisation).
**Secondary metrics:** Surrogate prediction error, uncertainty reduction in promising regions, query efficiency (information gained per evaluation).

---

## Assumptions and Limitations

### Key Assumptions
1. **Stationarity:** GP RBF kernel assumes uniform correlation structure across the domain. Violated for F5 where the high-performance region is tightly concentrated near the boundary — causes over-smoothing of the peak.
2. **Local smoothness:** Small input perturbations produce gradual output changes. If functions are discontinuous, trust-region exploitation may miss distant optima.
3. **Bounded optimum:** The global maximum lies within $[0, 1)^d$. If true optima are at the boundary or outside, the approach cannot discover them.
4. **Gaussian noise:** GP likelihood assumes homoscedastic Gaussian noise. Noise level may vary across the domain.

### Limitations
- **Single-query constraint:** One query per function per round forces binary, irreversible commitments. Portfolio diversification is impossible.
- **Sparse high-dimensional coverage:** 12 observations in 8D leave the vast majority of the search space unsampled. GP uncertainty estimates become unreliable in unexplored regions.
- **Exploitation bias:** Late-phase clustering around high-output regions creates sampling bias; unexplored areas cannot be retrospectively assessed.
- **No uncertainty-aware acquisition in MLP phase:** MLP gradient ascent lacks uncertainty quantification; confidence intervals from GP are abandoned when switching to neural surrogates.

---

## Ethical Considerations

**Transparency and reproducibility:**
All queries, strategy reasoning and surrogate specifications are documented in the weekly markdown files and in the associated datasheet. A researcher with access to the query log and documented parameters can fully reproduce the strategy. This documentation philosophy mirrors model card best practices: every decision traces to an explicit hypothesis.

**Fairness and bias:**
This approach involves no personal data, demographic information or decisions affecting individuals. There are no fairness concerns in the conventional sense.

**Real-world adaptation:**
The exploration–exploitation framework documented here directly transfers to real-world hyperparameter tuning, drug discovery and engineering design optimisation. The key ethical obligation in those contexts — which this project models — is documenting assumptions and limitations clearly so that downstream users can assess suitability and avoid over-relying on sparse surrogate predictions.

---

## References

Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji, I.D. and Gebru, T. (2019) 'Model cards for model reporting', *Proceedings of the Conference on Fairness, Accountability, and Transparency*, pp. 220–229.

Shahriari, B., Swersky, K., Wang, Z., Adams, R.P. and de Freitas, N. (2016) 'Taking the human out of the loop: A review of Bayesian optimization', *Proceedings of the IEEE*, 104(1), pp. 148–175.

Frazier, P.I. (2018) *A tutorial on Bayesian optimization*. arXiv:1807.02811.
