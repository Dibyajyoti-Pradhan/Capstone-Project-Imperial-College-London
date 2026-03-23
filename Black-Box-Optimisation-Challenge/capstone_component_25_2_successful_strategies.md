# Required Capstone Component 25.2 — Successful Optimisation Strategies

**Module:** 25 — Programme Retrospective
**Submitted:** 23/03/2026
**Cohort:** IMP-PCMLAI-25-08

---

## 1. Strategies That Led to the Strongest Results

Three strategies produced the clearest performance improvements across the 13-round challenge.

**The early commitment to F5's boundary basin.** The most impactful single decision in the entire project was made in Week 1 before any surrogate model existed: a max-distance heuristic placed F5's first query at (0.999, 0.999, 0.999, 0.999), which returned 8585 — an output roughly 5× higher than any other function's best observed value across all 13 rounds. Recognising this as a boundary-attractor optimum and committing to a trust-region around it from Week 3 onward defined F5's entire trajectory. The strategy was effective because it converted a single lucky observation into a persistent structural constraint: every subsequent F5 query was constrained to a neighbourhood of the confirmed best, preventing the surrogate from recommending distant unrelated regions under UCB pressure. The practical lesson was that **certainty about one region is more valuable than vague beliefs about many regions**, and that the right response to an extremely high outlier observation is immediate, committed exploitation — not caution.

**Function-specific κ scheduling for the UCB acquisition.** Early rounds applied uniform κ=2.0 across all eight functions. By Week 7, the data made clear that this was suboptimal: F5 had a confirmed high-output basin (κ should be near zero — exploit ruthlessly), while F1 had returned near-zero outputs from every quadrant (κ should be high — explore aggressively, or accept the function is flat). The adaptive rule introduced at Week 7 — decrease κ by 0.2 when the running best improves, increase κ by 0.3 when it stalls for two consecutive rounds — removed the need for manual tuning and created a self-correcting mechanism. By Week 12, the portfolio spanned κ=0.05 (F5) to κ=1.5 (F1, F7). This strategy was effective because it treated the eight functions as eight different problems at different stages of resolution, rather than a uniform optimisation task.

**PCA-inspired dimensionality reduction for F8.** Applying finite-difference gradient analysis to F8's accumulated observations revealed that four of the eight dimensions (X₂, X₄, X₅, X₇) contributed near-zero sensitivity to the output. Fixing these at best-known values and running UCB acquisition over the remaining 4D subspace (X₁, X₃, X₆, X₈) converted an unwieldy 8D search into a structured 4D problem. This produced consistent F8 improvement in the final three rounds and is the type of structural intervention that matters most in high-dimensional black-box problems: not better hyperparameters, but a better problem formulation.

---

## 2. What Defines a Successful Strategy?

A successful strategy in BBO is not one that maximises output in a single round — it is one that **generates the most information per query while preserving optionality for future rounds**. Outcomes matter, but three other qualities determine whether a high outcome is reproducible:

**Adaptability:** A strategy that performs well under one function's structure must fail gracefully when that structure is absent. The κ scheduling mechanism worked because it adapted to each function's feedback history rather than imposing a fixed exploration-exploitation regime. A strategy that requires human judgement to override it each week is fragile; one that updates itself from the data is robust.

**Interpretability of failure:** The clearest sign of a strategy's quality is not what happens when it works, but what happens when it fails. When F6's MLP surrogate identified a spurious high-output ridge in Week 6, the failure was immediately visible because the new observation fell below the running best — triggering a reversion to GP-UCB with wider κ. A strategy with no built-in failure detection will persist on a wrong path indefinitely.

**Efficiency under budget constraints:** With 13 queries per function, every query that does not improve the running best is a permanent cost. Strategies that generate high posterior variance reduction per query — either through diverse candidate generation or targeted uncertainty reduction in high-value regions — are objectively more efficient than those that cluster observations in already-sampled regions. The 300k LHS candidate budget chosen for most functions, increased to 500k for F5's dense boundary sampling, reflects this: the candidate cost is negligible compared to the value of selecting the right next query.

---

## 3. Application to Professional ML/AI Projects

The GP-UCB framework used in this challenge maps directly onto three professional contexts.

**Sequential hyperparameter tuning:** Every training run of a deep learning model is a query against an unknown function (validation accuracy as a function of hyperparameters). The same exploration-exploitation balance applies: early runs should cover the space broadly (high κ); later runs should refine around the best-observed configuration (low κ). Systems like Google Vizier and Meta's BoTorch implement exactly this logic at scale.

**Financial strategy parameter optimisation:** In quantitative portfolio management, each parameter configuration of a trading strategy is a query against a noisy, expensive objective (realised Sharpe ratio over a live trading period). The trust-region mechanism — restricting the next query to a small neighbourhood of the current best — maps to risk management constraints on strategy modification: large parameter jumps carry higher model risk. A GP surrogate over the strategy parameter space provides a principled way to estimate expected performance in untested configurations without live deployment.

**Adaptive clinical trial design:** Response-surface optimisation in drug dose-response studies operates under the same query budget constraint (patient cohort size is fixed) and the same exploration-exploitation tension (explore dose ranges vs. confirm a candidate dose). The function-specific strategy differentiation in this project — tight exploitation for functions with confirmed peaks, continued exploration for flat functions — is directly analogous to adaptive enrichment trial designs that redirect recruitment toward subgroups where early signal is strongest.

---

## References

Shahriari, B. et al. (2016) 'Taking the human out of the loop: a review of Bayesian optimization', *Proceedings of the IEEE*, 104(1), pp. 148–175.

Srinivas, N. et al. (2010) 'Gaussian process optimization in the bandit setting: no regret and experimental design', *Proceedings of ICML*, pp. 1015–1022.

Eriksson, D. et al. (2019) 'Scalable global optimization via local Bayesian optimization', *Advances in Neural Information Processing Systems*, 32.
