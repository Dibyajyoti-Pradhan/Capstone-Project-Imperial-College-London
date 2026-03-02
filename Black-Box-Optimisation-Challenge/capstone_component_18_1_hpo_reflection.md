# Required Capstone Component 18.1: Refining Strategies for the BBO Challenge

## Part 2: Reflection on Hyperparameter Tuning Strategy — Seventh Iteration (16 Data Points)

---

### 1. Hyperparameters Chosen and Prioritisation

With 16 data points across 8 functions, I prioritised hyperparameters that most directly influence query quality under severe data constraints:

**Surrogate model hyperparameters:**
- **GP kernel length-scales:** Control smoothness assumptions—shorter scales capture local variation but risk overfitting; longer scales generalise but may miss sharp optima
- **Noise level (α):** Balances fitting observed points versus allowing interpolation uncertainty
- **Kernel type:** Matern vs RBF selection based on expected function roughness

**Acquisition function hyperparameters:**
- **UCB κ parameter:** Directly controls exploration-exploitation trade-off; reduced from κ=2.0 (exploratory) to κ=0.5 (exploitative) as data accumulated
- **EI ξ parameter:** Minimum improvement threshold preventing queries in already-saturated regions

**Neural surrogate hyperparameters (for F5, F8):**
- **Architecture depth:** Shallow networks (2 layers) to prevent overfitting with limited data
- **Dropout rate:** Regularisation to improve generalisation; increased for higher-dimensional functions

I prioritised kernel parameters and acquisition settings because they have the most immediate impact on *where* the next query lands—the fundamental decision in sample-efficient optimisation.

---

### 2. How Hyperparameter Tuning Changed Query Strategy

Early rounds relied on default settings and broad exploration. By iteration 7, tuning transformed my approach:

| Early Rounds | After Tuning |
|--------------|--------------|
| Fixed κ=2.0 for all functions | Function-specific κ based on observed variance |
| Global GP across entire space | Local trust regions for high-D functions |
| Uniform architecture for all surrogates | Dimension-adapted complexity |

The most significant shift: **adaptive κ scheduling**. Functions showing consistent improvement (F5, F8) received lower κ for exploitation, while volatile functions (F1, F4) retained higher κ to maintain exploration coverage. This replaced the "one-size-fits-all" strategy with evidence-driven adaptation.

---

### 3. Tuning Methods Applied and Trade-offs

**Methods used:**

- **Manual adjustment:** Primary method for acquisition parameters (κ, ξ)—fast iteration, interpretable, but relies on intuition
- **Log-marginal likelihood (LML):** Automated kernel hyperparameter selection via GP fitting—principled but assumes GP model is appropriate
- **Cross-validation:** Limited use for neural surrogates due to small sample size—3-fold CV on 16 points yields unstable estimates

**Trade-offs observed:**

| Method | Advantage | Disadvantage |
|--------|-----------|--------------|
| Manual tuning | Fast, interpretable | Inconsistent, misses interactions |
| LML optimisation | Principled, automated | Can overfit to training data |
| Grid search | Exhaustive | Computationally infeasible at scale |

I avoided Hyperband and full Bayesian HPO because evaluation budgets were too constrained—these methods assume abundant function evaluations, contradicting BBO's core constraint.

---

### 4. Model Limitations Revealed at 16 Points

As data accumulated, several limitations became evident:

**Diminishing returns:** For well-characterised functions (F2, F5), additional queries near known optima yielded marginal gains—the surrogate had already captured local structure.

**Overfitting risk:** Neural surrogates with low regularisation produced overconfident predictions, suggesting optima in unexplored regions that proved suboptimal when queried.

**Irrelevant dimensions:** Gradient magnitude analysis on F8 (8D) revealed that dimensions X₄–X₈ contributed minimally—yet the GP still allocated capacity to model them, diluting predictive power on relevant dimensions.

**Non-stationarity:** F1 and F3 exhibited different behaviours in different regions; a single global GP struggled to represent this heterogeneity, motivating partition-based approaches.

These observations directly informed my shift toward local trust regions and dimension-weighted surrogates.

---

### 5. Applying Tuning Techniques to Larger Datasets

For future BBO rounds or complex ML projects, I would scale tuning approaches:

- **Bayesian HPO for surrogate hyperparameters:** Treat kernel selection and architecture as a nested optimisation problem, using methods like HEBO or Optuna
- **Multi-fidelity evaluation:** Use cheaper approximations (smaller networks, subset data) to prune poor configurations before expensive full evaluations
- **Automated feature selection:** Apply LASSO or gradient-based importance to identify relevant dimensions before surrogate fitting
- **Ensemble HPO:** Maintain diverse hyperparameter configurations across ensemble members, hedging against any single poor choice
- **Transfer learning:** Warm-start hyperparameters from similar functions, reducing early-round inefficiency

---

### 6. Professional Preparation Through Black-Box Tuning

This black-box setup mirrors real-world ML practice where:

- **Ground truth is inaccessible:** Production models optimise noisy, delayed, or proxy metrics
- **Evaluations are expensive:** A/B tests, simulation runs, or training jobs cannot be repeated indefinitely
- **Decisions require justification:** Stakeholders demand rationale beyond "the model said so"

Tuning in this constrained environment builds essential professional habits:

- **Quantifying uncertainty** rather than chasing point estimates
- **Documenting rationale** for hyperparameter choices to enable reproducibility
- **Balancing exploration and exploitation** under budget pressure
- **Recognising diminishing returns** and knowing when to stop tuning

Most importantly, it cultivates **adaptive thinking**—the recognition that optimal hyperparameters are context-dependent and must evolve as evidence accumulates, not remain fixed from project start.

---

*Word count: 698*
