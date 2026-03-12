# Required Capstone Component 12.1 — Week 1
## Applying Machine Learning Techniques to Black-Box Functions

**Module:** 12 — Bayesian Optimisation
**Submitted:** 02/03/2026
**Status:** PROCESSED
**Cohort:** IMP-PCMLAI-25-08

---

## Part 1: Queries Submitted

| Function | Dimensions | Query Submitted | Output |
|----------|------------|-----------------|--------|
| F1 | 2D | 0.001000-0.999000 | TBC |
| F2 | 2D | 0.001000-0.999000 | TBC |
| F3 | 3D | 0.437056-0.996752-0.890886 | TBC |
| F4 | 4D | 0.009153-0.333687-0.980781-0.997681 | TBC |
| F5 | 4D | 0.999000-0.999000-0.999000-0.999000 | TBC |
| F6 | 5D | 0.001000-0.001000-0.001000-0.001000-0.001000 | TBC |
| F7 | 6D | 0.001000-0.001000-0.999000-0.001000-0.999000-0.001000 | TBC |
| F8 | 8D | 0.001000-0.001000-0.001000-0.001000-0.999000-0.001000-0.001000-0.001000 | TBC |

*Strategy: Maximum spatial distance from all initial data points using Latin Hypercube Sampling candidate generation. No output data available at submission time — pure exploration phase.*

---

## Part 2: Reflection

### 1. What was the main principle or heuristic you used to decide on each query point?

My primary strategy was **structured exploration with dimensionality-aware sampling**, recognising that early-stage BBO with limited data demands broad coverage over premature exploitation.

**The Core Approach**

With only 10 initial data points per function and no prior output feedback, I treated this as a pure information-gathering phase. The guiding principle was:

> *Maximise spatial coverage while ensuring samples are informative across all dimensions.*

**Function-Specific Strategies**

| Dimension | Strategy | Rationale |
|-----------|----------|-----------|
| 2D–3D (Functions 1–3) | Centroid + boundary sampling | Low-dimensional spaces allow meaningful coverage |
| 4D–5D (Functions 4–5) | Latin Hypercube-inspired spacing | Each dimension sampled at distinct levels |
| 6D–8D (Functions 6–8) | Maximum distance from existing points | Sparse data requires aggressive exploration |

**Why Not Exploit Yet?**

- No output data available: Without knowing which regions produced high values, exploitation targets do not exist
- Unknown function structure: Functions could be unimodal, multimodal, smooth, or noisy
- Single query per function: With only one shot per round, exploration builds a foundation for future model fitting

---

### 2. Which function(s) were most challenging to query, and why?

**Most Challenging: Functions 7 (6D) and 8 (8D)**

The high-dimensional functions presented severe challenges rooted in the curse of dimensionality:

- **Exponential volume growth:** In 8D, the unit hypercube has a volume where 10 random points are statistically ~0.3 units apart on average. Neighbouring points provide almost no information about each other.
- **Surrogate model instability:** Gaussian Processes struggle when data density is low relative to dimensionality. The covariance matrix becomes poorly conditioned.
- **Visual intuition fails:** Beyond 3D, all reasoning must be mathematical rather than intuitive.

**Moderately Challenging: Function 4 (4D — Dynamic System)**

The description suggested "rapidly changing output" with potentially multiple local maxima. This created uncertainty about whether the function is stationary, whether noise dominates the signal, and whether historical observations remain relevant.

**What Would Have Helped**

| Information Needed | Why It Matters |
|-------------------|----------------|
| Output values from initial samples | Would enable surrogate model fitting |
| Noise level estimates | Determines whether small differences are meaningful |
| Smoothness/Lipschitz constant | Guides length-scale choices for GPs |
| Feature importance hints | Allows dimensionality reduction in 6D–8D problems |
| Bounds tighter than [0,1] | Reduces effective search space |

---

### 3. How do you plan to adjust your strategy in future rounds?

**Phased Transition from Exploration to Exploitation**

| Phase | Rounds | Approach |
|-------|--------|----------|
| Model Building | 2–4 | Fit GP surrogates; UCB with κ ≈ 3–5; identify smooth vs. noisy functions |
| Balanced Search | 5–8 | Reduce κ gradually to ~2; switch to EI for functions with clear optima |
| Refinement | 9–13 | Heavy exploitation near identified optima; small exploration reserve |

**Dimension-Specific Adaptations**

- **Low-dimensional (2D–4D):** Standard Bayesian Optimisation with Matérn or RBF kernel
- **High-dimensional (6D–8D):** ARD kernels to identify influential dimensions; TuRBO (Trust Region BO) to focus local search; Sobol quasi-random sequences for candidate generation

**Contingency Plans**

If a function shows no improvement over several rounds:
1. Increase exploration dramatically — possible local trap
2. Try alternative surrogate (Random Forest instead of GP)
3. Resample previously high-performing regions — possible noise masking signal
