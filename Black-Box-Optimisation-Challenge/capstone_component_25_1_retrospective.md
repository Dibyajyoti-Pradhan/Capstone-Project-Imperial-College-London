# Required Capstone Component 25.1 — Retrospective on the BBO Capstone Project

**Module:** 25 — Programme Retrospective
**Submitted:** 23/03/2026
**Cohort:** IMP-PCMLAI-25-08

---

## 1. Initial Codebase

The codebase was built from scratch using three core libraries: `scikit-learn` for the Gaussian Process surrogate, `scipy.stats.qmc` for Latin Hypercube Sampling candidate generation, and `numpy` for all numerical operations. No pre-existing BBO framework was used. The decision to build from scratch was deliberate: wrapping an existing library (such as BoTorch or GPyOpt) would have obscured the mechanics that the programme was asking me to understand and reflect on each week. Writing `fit_gp`, `ucb_acquisition`, and `suggest_next_query` myself meant that every parameter — length scale, noise level, κ — had a visible effect I could trace directly to the output.

The full codebase, notebooks, and weekly query logs are publicly available at:
**https://github.com/Dibyajyoti-Pradhan/Capstone-Project-Imperial-College-London/tree/main/Black-Box-Optimisation-Challenge**

The repository includes `bbo_utils.py` (shared utilities), per-function Jupyter notebooks, a `DATASHEET.md` and `MODEL_CARD.md` documenting the surrogate model, and all weekly query CSVs with inputs and confirmed outputs.

---

## 2. Code Modifications Week by Week

**Weeks 1–2 (Modules 12–13): No surrogate — pure heuristics.**
Week 1 used max-distance heuristics to spread queries across each input space. No function outputs informed any decision. Week 2 applied a simple output-guided rule: move toward higher-output regions for functions that showed a positive signal. This produced the most important observation of the entire project: F5 at (0.999, 0.999, 0.999, 0.999) returned 8585 in Week 1, an output orders of magnitude above every other function. This single result defined the F5 strategy for all 13 rounds.

**Weeks 3–4 (Modules 14–15): GP surrogates introduced.**
`suggest_next_query` was completed and the GP-UCB acquisition loop became the core decision engine. Week 3 introduced function-specific κ values: high κ for uncertain functions (F1, F7), low κ for F5 once its basin was confirmed. Week 4 added the trust-region mechanism: candidates restricted to a hypercube of radius r around the current best, preventing the GP from recommending distant low-confidence points.

**Weeks 5–6 (Modules 16–17): Gradient-guided search and dimension sensitivity.**
Finite-difference gradient analysis (`dimension_sensitivity` in `bbo_utils.py`) was applied to identify which dimensions drove most of the output variance in high-dimensional functions. For F8, X₆ and X₈ emerged as dominant; for F7, X₂ and X₆. This was later formalised as a PCA-style dimensionality reduction in Week 12.

**Weeks 7–8 (Modules 18–19): Adaptive κ scheduling.**
A heuristic was introduced: if the running best had not improved for two consecutive rounds, increase κ by 0.3; if it had improved, decrease κ by 0.2. This removed the need for manual κ updates each week. By Week 8, F5 was at κ=0.05 and F1/F7 were at κ≥1.5.

**Weeks 9–12 (Modules 20–23): Convergence diagnostics and dimension reduction.**
Output variance across consecutive queries was tracked as a convergence signal — a falling variance envelope was treated as equivalent to a PCA scree plot flattening. For F8, fixing X₂/X₄/X₅/X₇ at best-known values and running UCB over the remaining 4D subspace was the single most impactful change after the F5 trust region. It reduced a wandering 8D search to a structured 4D problem and produced consistent F8 improvement in the final three rounds.

**Most significant changes:**
1. Introducing the F5 trust region at Week 3 (converted the best observation into a persistent anchor)
2. Adaptive κ scheduling at Week 7 (removed manual intervention)
3. F8 dimensionality reduction at Week 12 (structural rather than parametric improvement)

---

## 3. Final Result

| Function | W1 Output | Best Observed | Trend |
|----------|-----------|--------------|-------|
| F5 | 8585.27 | **8585.27** (W1) | Confirmed peak at (0.999)⁴ |
| F8 | 9.50 | ~9.68 | Slow monotonic improvement |
| F2 | −0.103 | ~0.44 | Strong consistent improvement |
| F3 | −0.092 | ~−0.009 | Approaching zero |
| F7 | 0.002 | ~1.79 | Modest improvement |
| F6 | −2.316 | ~−0.570 | Slow improvement |
| F4 | −34.09 | ~−3.77 | Large early gain, then plateaued |
| F1 | 0 | ~0 | Flat throughout |

**What I would do differently with a fresh start:**

First, I would implement the dense-boundary sampling approach for F5 from Week 1 rather than Week 5. The realisation that (0.999, 0.999, 0.999, 0.999) is near-optimal came from the data, but the trust-region radius was miscalibrated in early weeks: a radius of r=0.005 in 4D with 300k LHS candidates produces statistically zero survivors due to the tiny volume fraction ((0.01)⁴ ≈ 10⁻⁸). Switching to a dense uniform grid within [0.989, 1.0]⁴ from Week 3 onward would have kept F5 in its optimal basin rather than drifting.

Second, I would allocate query budget asymmetrically from Week 6 onward — effectively treating F1 as an unresolvable function and redirecting its later-round query budget toward a second probe of F5 or F8's high-uncertainty subspace.

---

## 4. Trade-offs and Decisions

**Exploration vs exploitation:** The fundamental tension was managed via κ, but the right level was not obvious until multiple rounds of data had accumulated. Setting κ too low early (as happened for F4 in Week 4, which returned −6.22 — worse than Week 3's −3.77) collapsed the search into a region that turned out to be a local trough. Setting κ too high for converging functions (F5, F8) wastes queries on already-understood regions.

The resolution was the adaptive κ heuristic (Week 7): rather than setting κ once per function, it updates automatically based on recent improvement. This is not a theoretically optimal policy, but it is a practical and responsive one that mirrors how a rational investor increases risk tolerance when a portfolio is stagnant and reduces it when returns are strong.

**Short-term vs long-term strategy:** The starkest example was F5. Committing to the (0.999)⁴ trust region from Week 3 was a long-term bet: the first three queries in the neighbourhood returned 8585, 7374, and 7197 — a sequence that looked discouraging. Reverting to exploration would have been defensible. Holding the commitment was correct because the GP posterior consistently identified the boundary region as having the highest expected value, and the decreasing outputs reflected imprecision in the trust-region calibration, not evidence that the peak had moved.

---

## 5. Learning and Application

**Most important lesson:** BBO is not one problem — it is eight different problems, each with its own structure, and the largest performance gains come from recognising which type each function presents (converging, drifting, or unresolved) and matching the strategy accordingly. Applying uniform settings across all eight functions is the primary source of suboptimal performance. This lesson transfers directly to production ML: hyperparameter search for different model families requires different strategies; AutoML systems that apply a fixed acquisition policy regardless of the objective surface systematically underperform systems that adapt to the observed landscape.

**Practical application:** In portfolio optimisation at Hull Tactical, the same GP-UCB framework can be applied to sequential strategy parameter tuning — where each "query" is a live strategy deployment and the "function output" is realised Sharpe ratio. The budget constraint maps naturally to regulatory risk limits on strategy changes per period. The exploration-exploitation balance is the same tension between deploying a known-good strategy and testing a potentially better one.

**What surprised me most:** The F5 output at Week 1 (8585) was 5× higher than any other function's best output across all 13 rounds. The boundary-attractor structure — where the global maximum sits at the extreme corner of the input space — is not intuitive. In most real-world optimisation problems, extreme parameter values lead to instability or degraded performance; the fact that F5 rewarded pushing every dimension to its maximum was genuinely unexpected and reinforced the importance of early diverse coverage. Had the Week 1 query not been placed at (0.999, 0.999, 0.999, 0.999) by the max-distance heuristic, this basin would likely have remained undiscovered until much later.

**What surprised me about peers' strategies:** Participants who used simpler acquisition strategies — greedy best-observation exploitation without surrogates — sometimes performed comparably to GP-based approaches in low-dimensional functions. This suggests the surrogate's value is strongest in higher-dimensional spaces (F7, F8) where naive search fails, and diminishes when the function landscape is simple enough that random restarts from the best-observed point are competitive. The lesson: model complexity should be matched to problem complexity, not applied uniformly.

---

## GitHub Repository

Full codebase, notebooks, weekly query data, and documentation:
**https://github.com/Dibyajyoti-Pradhan/Capstone-Project-Imperial-College-London**

---

## References

Shahriari, B. et al. (2016) 'Taking the human out of the loop: a review of Bayesian optimization', *Proceedings of the IEEE*, 104(1), pp. 148–175.

Srinivas, N. et al. (2010) 'Gaussian process optimization in the bandit setting: no regret and experimental design', *Proceedings of ICML*, pp. 1015–1022.

Eriksson, D. et al. (2019) 'Scalable global optimization via local Bayesian optimization', *Advances in Neural Information Processing Systems*, 32.
