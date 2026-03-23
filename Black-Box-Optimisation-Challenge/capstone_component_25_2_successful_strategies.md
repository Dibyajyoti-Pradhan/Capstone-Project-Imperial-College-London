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

## 4. Peer Analysis

**Craig Dawson** — The most interesting finding in Craig's results is that Weeks 16–18 (Random Forest and SVM surrogates) produced the best outputs for five of his eight functions, while the more sophisticated GP-TuRBO pipeline in later weeks did not improve on those results for those functions. This is a clean empirical demonstration that surrogate complexity is not monotonically related to performance. The likely explanation is that RF and SVM surrogates with brute-force search, while theoretically less principled than GPs, are less susceptible to kernel misspecification — a GP with a fixed RBF kernel will underperform a simpler model when the true function has structure that the kernel doesn't capture. Craig's observation directly supports the principle that method-function matching matters more than method sophistication.

The overlap with my approach: both converged on function-specific strategies and both observed that complexity has diminishing returns. The difference: Craig's RF/SVM phase delivered better results than my LHS-only early phase did, suggesting that a non-parametric surrogate with high model flexibility can outperform LHS exploration in early rounds.

**Jack Dunning** — Jack's reframing of F1 as a logistic regression boundary-finding problem is the most creative methodological decision I encountered in this cohort. My approach kept F1 as a regression target throughout, which kept it anchored near zero because the GP assigned near-zero predicted values everywhere and generated near-random UCB queries. Jack's recognition that the correct objective is not "find the maximum of a nearly-zero function" but "find the boundary of the region where the function is not zero" is a fundamental problem-reformulation that I did not consider. This is the type of insight that separates strong practitioners from competent ones: the ability to see that the problem formulation itself might be wrong.

His F8 best of 9.90 versus my 9.68 confirms that his MLP + gradient ascent with multi-restart optimisation outperformed my LHS + GP posterior argmax for high-dimensional functions. This is expected: gradient-based candidate selection scales better with dimensionality because it does not require exponentially growing candidate budgets to maintain effective coverage density.

**Suggestion to strengthen peers' strategies:** The single addition that would most improve both Craig's and Leonardo's pipelines is a formalised convergence diagnostic — a decision rule that triggers strategy reclassification (from exploitation back to exploration, or from one surrogate to another) when the running best has not improved for a specified number of consecutive rounds. Without this, the natural human tendency is to persist with the current approach longer than the data justifies. Jack already built this in through his Week 8 validation table; Craig and Leonardo would benefit from an equivalent.

**What peers' reflections changed:** Stephen's observation that clustering emerged naturally from the EI acquisition function — without explicitly programming it — reinforced that acquisition function design implicitly encodes structural assumptions about where the optimum lies. A GP with EI will cluster in a different way than a GP with UCB even on the same function, because EI only rewards improvement over the current best while UCB rewards high predicted value regardless of improvement. Understanding this distinction would have led me to experiment with EI more explicitly for functions where the surrogate was well-calibrated but the optimum was narrow.

---

## References

Shahriari, B. et al. (2016) 'Taking the human out of the loop: a review of Bayesian optimization', *Proceedings of the IEEE*, 104(1), pp. 148–175.

Srinivas, N. et al. (2010) 'Gaussian process optimization in the bandit setting: no regret and experimental design', *Proceedings of ICML*, pp. 1015–1022.

Eriksson, D. et al. (2019) 'Scalable global optimization via local Bayesian optimization', *Advances in Neural Information Processing Systems*, 32.
