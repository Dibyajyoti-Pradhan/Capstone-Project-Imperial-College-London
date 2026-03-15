# BBO Capstone Project Presentation
## Capstone Component 23.2

**Author:** Dibyajyoti Pradhan
**Programme:** Imperial College London — Professional Certificate in ML/AI
**Cohort:** IMP-PCMLAI-25-08 | **Date:** 15/03/2026

---

## 1. An Overview of My BBO Approach

The Black-Box Optimisation (BBO) challenge tasks me with finding the input combinations that maximise eight unknown functions — F1 through F8 — across input spaces ranging from 2 to 8 dimensions. Each function behaves like a sealed vault: I submit a coordinate vector, receive a single number back, and the internal mechanics are never revealed. With only 13 query opportunities per function across the entire programme, every submission must be chosen deliberately. The goal is simple to state but hard to achieve: find the highest possible output for each function before the query budget runs out.

**Overall strategy — three phases:**

The approach unfolds in three phases that mirror how understanding builds progressively in any learning process.

*Phase 1 — Exploration (Weeks 1–3):* Cast a wide net. With no prior knowledge of any function's landscape, the first queries used maximum-distance heuristics and Latin Hypercube Sampling to spread points across the input space. The sole objective was coverage — ensuring the initial queries spanned the domain rather than clustering in one area.

*Phase 2 — Pattern recognition (Weeks 4–8):* Fit Gaussian Process (GP) surrogate models to the accumulated observations. A GP is a mathematical model that not only predicts function outputs at unsampled locations but also quantifies its own uncertainty. The Upper Confidence Bound (UCB) acquisition function then selects the next query by balancing high predicted value against high uncertainty — the core exploration-exploitation mechanism. SVM classification was used to pre-screen candidate regions into "promising" and "unpromising" zones.

*Phase 3 — Exploitation (Weeks 9–13):* Commit to the best-known regions. For functions with confirmed high-output basins, trust regions constrain the search to small neighbourhoods around the current best. For high-dimensional functions (F7, F8), gradient-guided search uses the neural network surrogate's backpropagation signal to navigate directionally rather than randomly.

The unifying principle: **treat uncertainty as information**. Regions the model doesn't understand are as valuable as regions it knows well — until the budget forces commitment.

---

## 2. How My Strategy Has Evolved

**Key changes since early rounds:**

Week 1 relied entirely on spatial heuristics — no function output data informed any decision. By Week 12, every query is the output of a fitted surrogate model, a calibrated acquisition function, and a function-specific parameter schedule. The transformation was not abrupt but incremental: each new observation shifted the surrogate's beliefs, and each shift unlocked a slightly more targeted query.

The most significant structural change was the introduction of **function-specific κ schedules** for the UCB acquisition parameter. Early rounds used a uniform κ=2.0 across all eight functions. By Week 7, observations revealed that F5 had a confirmed high-output peak (returning ~1600, far above any other function), while F1 and F7 remained flat and uncertain. Continuing to apply the same acquisition settings to both groups was clearly suboptimal. The solution: reduce κ dramatically for high-confidence functions (κ=0.05 by Week 12, forcing pure exploitation), while maintaining high κ for uncertain ones (κ≥1.5, preserving exploration).

**What influenced these changes:**

- *Data trends:* F5's Week 1 output of ~1600 immediately flagged it as an outlier. This single observation redirected the entire F5 strategy from Week 2 onward.
- *Model performance:* Gradient ascent on F6 (Week 5) failed because the MLP surrogate identified a misleading ridge that collapsed when probed directly. This failure triggered reversion to GP-UCB with tighter trust regions for F6.
- *Module concepts:* Each programme module introduced a new lens — SVM classification (Module 14), neural surrogates (Module 15), CNN-style hierarchical thinking (Module 17), PCA-inspired dimension reduction (Module 23) — and each was applied directly to the optimisation strategy.

**Principles now guiding query decisions:**

1. *κ follows confidence:* Low κ for functions with confirmed peaks; high κ for functions with unresolved landscapes
2. *Trust radius follows evidence:* Radius shrinks only when multiple consecutive queries confirm a stable peak, not optimistically
3. *Gradient sensitivity drives dimensionality:* Dimensions where |∂f/∂xᵢ| < 0.05 across all observations are treated as noise and fixed at best-known values
4. *Variance as a diagnostic:* Falling output variance across consecutive queries signals convergence — switch to pure exploitation

---

## 3. Patterns, Data and Insights

**Most meaningful trends:**

The clearest pattern across all twelve rounds is the **divergence of function trajectories**. Functions did not evolve uniformly — they separated into three distinct behavioural groups that directly determined the strategy applied to each:

- *Converging functions (F4, F5, F8):* Running best improves consistently across rounds. Surrogate uncertainty has collapsed in the high-output region. The search has effectively located the attractor basin and is now refining within it. F5 is the most extreme case: its best-observed output (~1600+) was discovered in Week 1 and confirmed by every subsequent query in the region near (0.999, 0.999, 0.999, 0.999).

- *Drifting functions (F2, F3, F6):* Outputs improve gradually but without a sharp peak — the landscape appears to have a broad, gently sloping optimum. Queries show a slowly translating centroid rather than tight convergence. These functions benefit from continued directional movement rather than aggressive trust-region tightening.

- *Unresolved functions (F1, F7):* Despite twelve rounds of queries across multiple regions, neither function has produced outputs significantly above their initial data range. The landscape may be intrinsically flat, or the optimum may lie in a region not yet adequately sampled.

**Variables that influence results most:**

Applying finite-difference gradient analysis (computing ∂f/∂xᵢ for each dimension using the surrogate model) revealed clear dimensionality structure:

| Function | Dominant dimensions | Effective search space |
|----------|--------------------|-----------------------|
| F5 | X₁, X₂, X₃, X₄ (uniform) | 4D — boundary optimum |
| F8 | X₁, X₃ (small), X₆, X₈ (large) | ~4D of 8D |
| F7 | X₂, X₆ | ~2D of 6D |
| F4 | X₁, X₃ | ~2D of 4D |

For F8, this analysis enabled genuine dimensionality reduction: fixing X₂/X₄/X₅/X₇ at best-known values and running UCB over the remaining 4D subspace — directly applying the PCA principle of discarding low-variance components while retaining the essential signal.

**How these observations shaped understanding:**

The most important insight was that BBO is not a uniform search problem — it is eight different problems, each with its own structure, and the biggest performance gains come from recognising which type of problem each function presents and matching the strategy accordingly. The functions that received individually tailored treatment from Week 5 onward consistently outperformed those managed with generic settings.

---

## 4. Decision-Making and Iteration

**Balancing exploration and exploitation:**

The exploration-exploitation balance was managed dynamically using function-specific UCB κ values, updated each round based on observed output variance. The heuristic: if the running best has not improved for three consecutive rounds, increase κ (explore more); if the running best has improved in the last round, decrease κ (exploit more). This created an adaptive schedule without requiring explicit regime detection.

By Week 12, the portfolio divides cleanly:
- F5 and F8: κ = 0.05 (≈ pure exploitation)
- F2, F4: κ = 0.3–0.5 (exploitation-dominant)
- F6: κ = 0.8 (balanced)
- F1, F7: κ ≥ 1.5 (exploration-dominant)

**Two examples of strategic decisions:**

*Decision 1 — F5 early commitment (Week 1, worked):*
The max-distance heuristic placed the Week 1 F5 query at (0.999, 0.999, 0.999, 0.999), which returned ~1600 — an output orders of magnitude above the initial data range (~20). The decision to immediately commit a trust region around this point from Week 5 onward was deliberate, not lucky. Risk: the true optimum might not be exactly at the boundary. Outcome: eleven consecutive rounds of queries in the neighbourhood confirmed the basin is stable. The commitment was correct.

*Decision 2 — F6 gradient ascent reversion (Week 6, failure corrected):*
After fitting an MLP surrogate to F6's 14 observations, the gradient ascent step predicted a high-output region near (0.72, 0.25, 0.83, 0.74, 0.19). When probed, the output was lower than expected — the surrogate had overfit to noise and identified a spurious ridge. The response was immediate: abandon gradient ascent for F6, revert to GP-UCB with κ=1.5, and widen the trust region. The failure was recognised because the new output was below the running best, triggering an automatic strategy downgrade. This is the correct professional response to surrogate failure — acknowledge the model error and revert to a more conservative baseline.

**Handling uncertainty:**

When results don't match expectations — either lower-than-predicted outputs or flat landscapes despite multiple diverse probes — the protocol is: widen κ, exit the current trust region, and probe the highest-uncertainty region identified by the GP. Persisting with exploitation when the surrogate is clearly wrong is the primary failure mode in BBO; the safeguard is maintaining surrogate uncertainty monitoring as a parallel diagnostic throughout all rounds.

---

## 5. Next Steps and Reflection

**Planned actions for the final round (Week 13):**

- *F5:* One final micro-perturbation within radius r=0.005 of the best-known point — small enough to avoid duplicating a previous query while remaining within the confirmed high-output basin. The goal is not to find something better but to confirm the basin boundary with maximum precision.
- *F8:* Apply GP acquisition over the reduced 4D subspace (X₁/X₃/X₆/X₈ only), with the remaining four dimensions fixed at best-known values.
- *F1/F7:* Final exploratory query in the highest-uncertainty region identified by the GP posterior. These functions have resisted twelve rounds of search; the final query is a deliberate last attempt to detect whether a peak exists in the unexplored interior.
- *F2–F4/F6:* Pure GP posterior maximum exploitation — no exploration value remains in the final round for converging functions.

**Connection to the broader ML landscape:**

This project operationalises the core challenge of modern ML deployment: learning from limited, expensive feedback in high-dimensional spaces under strict computational budgets. The GP-UCB framework used here is the theoretical foundation for Google Vizier and Meta's BoTorch — production systems that manage hyperparameter search across millions of model training runs daily. The exploration-exploitation trade-off that governed every BBO query decision is the same tension at the heart of reinforcement learning, clinical trial design, drug discovery, and automated experiment planning. Solving it well — not in theory but under real constraints — is the defining skill of a production ML practitioner.

**Communicating results to a non-technical audience:**

Imagine you are trying to find the highest point in a mountain range, but you are blindfolded and can only take 13 steps. After each step, someone tells you your current altitude — nothing more. The strategy is to start by spreading your steps widely to get a feel for the terrain, then gradually focus your remaining steps on the highest area you have discovered. By Round 12, for some mountains (F5, F8) we have found peaks much higher than where we started; for others (F1, F7), the ground has stayed frustratingly flat no matter where we step. The final round is one last committed step toward the best position found — not a guess, but the most informed choice the data allows.
