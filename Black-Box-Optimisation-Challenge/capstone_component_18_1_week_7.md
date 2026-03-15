# Required Capstone Component 18.1 — Week 7
## Refining Strategies for the Black-Box Optimisation Challenge

**Module:** 18 — Hyperparameter Tuning
**Submitted:** 27/02/2026
**Cohort:** IMP-PCMLAI-25-08

---

## Part 1: Queries Submitted

| Function | Dimensions | Strategy | Query Submitted | Output |
|----------|------------|----------|-----------------|--------|
| F1 | 2D | Balanced exploration (κ=2.0) | 0.837214-0.770672 | TBC |
| F2 | 2D | Balanced GP-UCB (κ=0.8) | 0.764017-0.915770 | TBC |
| F3 | 3D | Balanced GP-UCB (κ=0.8) | 0.238163-0.252402-0.430533 | TBC |
| F4 | 4D | Exploitation (κ=0.5) | 0.560545-0.414310-0.434061-0.217834 | TBC |
| F5 | 4D | Very tight trust-region (κ=0.1, r=0.02) | 0.987688-0.993934-0.985555-0.974125 | TBC |
| F6 | 5D | Balanced-explore (κ=1.5) | 0.702039-0.152715-0.785816-0.669538-0.014257 | TBC |
| F7 | 6D | GP gradient ascent (κ=2.5) | 0.019168-0.498371-0.228573-0.198239-0.453109-0.823038 | TBC |
| F8 | 8D | Very tight trust-region (κ=0.1, r=0.06) | 0.062743-0.157263-0.020914-0.073384-0.311819-0.727900-0.626634-0.893939 | TBC |

---

## Part 2: Reflection on Strategy — Seventh Iteration (16 Data Points)

---

### 1. Hyperparameters Chosen and Prioritisation

With 16 data points across 8 functions, I prioritised hyperparameters that most directly influence query quality under severe data constraints:

- **Surrogate model hyperparameters:** GP kernel length-scales (smoothness assumptions), noise level α (fitting vs uncertainty balance), and kernel type (Matérn vs RBF)
- **Acquisition function hyperparameters:** UCB κ parameter (reduced from κ=2.0 to κ=0.5 as data accumulated) and EI ξ parameter (minimum improvement threshold)
- **Neural surrogate hyperparameters:** Architecture depth (shallow networks to prevent overfitting) and dropout rate (increased for higher-dimensional functions)

I prioritised kernel parameters and acquisition settings because they have the most immediate impact on where the next query lands.

---

### 2. How Hyperparameter Tuning Changed Query Strategy

Early rounds relied on default settings and broad exploration. By iteration 7, tuning transformed my approach:

| Early Rounds | After Tuning |
|:-------------|:-------------|
| Fixed κ=2.0 for all functions | Function-specific κ based on observed variance |
| Global GP across entire space | Local trust regions for high-D functions |
| Uniform architecture for all surrogates | Dimension-adapted complexity |

The most significant shift: **adaptive κ scheduling**. Functions showing consistent improvement received lower κ for exploitation, while volatile functions retained higher κ for exploration coverage.

---

### 3. Tuning Methods Applied and Trade-offs

Methods used:

- **Manual adjustment:** Primary method for acquisition parameters — fast iteration, interpretable, but relies on intuition
- **Log-marginal likelihood (LML):** Automated kernel hyperparameter selection — principled but assumes GP model is appropriate
- **Cross-validation:** Limited use for neural surrogates due to small sample size — 3-fold CV on 16 points yields unstable estimates

I avoided Hyperband and full Bayesian HPO because evaluation budgets were too constrained — these methods assume abundant function evaluations.

---

### 4. Model Limitations Revealed at 16 Points

As data accumulated, several limitations became evident:

- **Diminishing returns:** Additional queries near known optima yielded marginal gains
- **Overfitting risk:** Neural surrogates with low regularisation produced overconfident predictions
- **Irrelevant dimensions:** Gradient analysis on F8 (8D) revealed dimensions X₄–X₈ contributed minimally
- **Non-stationarity:** F1 and F3 exhibited different behaviours in different regions

---

### 5. Applying Tuning Techniques to Larger Datasets

For future BBO rounds or complex ML projects, I would scale tuning approaches:

- Bayesian HPO for surrogate hyperparameters using HEBO or Optuna
- Multi-fidelity evaluation to prune poor configurations before expensive evaluations
- Automated feature selection via LASSO or gradient-based importance
- Ensemble HPO maintaining diverse configurations across ensemble members
- Transfer learning to warm-start hyperparameters from similar functions

---

### 6. Professional Preparation Through Black-Box Tuning

This black-box setup mirrors real-world ML practice where ground truth is inaccessible, evaluations are expensive, and decisions require justification.

Tuning in this constrained environment builds essential professional habits:

- Quantifying uncertainty rather than chasing point estimates
- Documenting rationale for hyperparameter choices to enable reproducibility
- Balancing exploration and exploitation under budget pressure
- Recognising diminishing returns and knowing when to stop tuning

Most importantly, it cultivates adaptive thinking — the recognition that optimal hyperparameters are context-dependent and must evolve as evidence accumulates.
