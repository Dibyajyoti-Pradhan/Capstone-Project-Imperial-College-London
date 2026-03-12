# Required Capstone Component 14.1 — Week 3
## Refining Strategies for the Black-Box Optimisation Challenge

**Module:** 14 — Support Vector Machines
**Submitted:** 26/02/2026
**Cohort:** IMP-PCMLAI-25-08

---

## Part 1: Queries Submitted

| Function | Dimensions | Strategy | Query Submitted | Output |
|----------|------------|----------|-----------------|--------|
| F1 | 2D | Heavy exploration (κ=5.0) | 0.379815-0.982348 | TBC |
| F2 | 2D | Balanced (κ=1.5) | 0.702361-0.999278 | TBC |
| F3 | 3D | Balanced-explore (κ=2.0) | 0.277230-0.271538-0.473161 | TBC |
| F4 | 4D | Balanced (κ=1.5) | 0.543145-0.483596-0.405342-0.279468 | TBC |
| F5 | 4D | Trust-region exploit (κ=0.5, r=0.10) | 0.971379-0.986894-0.963789-0.998582 | TBC |
| F6 | 5D | Balanced-explore (κ=2.0) | 0.782609-0.206420-0.672050-0.705469-0.046842 | TBC |
| F7 | 6D | Heavy exploration (κ=5.0) | 0.033347-0.504111-0.239718-0.275308-0.351609-0.695268 | TBC |
| F8 | 8D | Trust-region exploit (κ=0.5, r=0.15) | 0.130120-0.028182-0.070598-0.108879-0.318606-0.868987-0.404103-0.918808 | TBC |

---

## Part 2: Reflection

### 1. How has your query strategy changed from earlier rounds?

| Phase | Approach | Key Change |
|-------|----------|------------|
| Week 1 | Blind exploration | Maximum spatial coverage without output feedback |
| Week 2 | Output-guided search | Function-specific strategies based on observed values |
| Week 3 | Model-informed decisions | Gaussian Process surrogates drive query selection |

The most significant shift was moving from geometric heuristics (maximum distance from existing points) to model-based acquisition functions. Functions 5 and 8, showing strong positive outputs, now receive local perturbation — small controlled steps around the best-known points. Meanwhile, stagnant functions like F1 and F7 receive higher exploration parameters (κ=5.0) to escape potential local traps.

---

### 2. How do you balance exploration against exploitation?

The overall balance has shifted from 70/30 exploration-heavy to approximately 50/50, with significant function-specific variation:

- **F5, F8 (strong signals):** 30–40% exploration — refining identified optima, trust region ±0.10–0.15
- **F1, F7 (weak signals):** 70% exploration — still searching for main structure
- **F2, F3, F4, F6:** Balanced approach based on observed progress (κ=1.5–2.0)

**Trade-off management:** I use trust region exploitation for promising functions. Rather than letting the GP extrapolate freely (which tends to drift toward domain boundaries), I constrain exploitation queries within a trust radius of the current best. This provides local refinement while limiting downside risk from overconfident predictions.

---

### 3. How would SVMs change your approach?

SVMs offer a fundamentally different perspective: instead of modelling the continuous output surface, they classify regions as **promising** or **unpromising**.

**Potential applications:**

1. **Binary region classification:** Threshold outputs (e.g., above/below 75th percentile) and train an SVM to identify the decision boundary. Focus queries on predicted "good" regions or near the boundary.

2. **Kernel-based pattern detection:** The RBF kernel could identify non-linear regions where high outputs concentrate, potentially more efficiently than a GP attempting to model the full surface.

3. **Hybrid approach:** Use SVM to pre-filter candidates (eliminate clearly unpromising regions), then apply GP-based acquisition to select among the remaining points.

**Limitations:** SVMs provide no uncertainty quantification without Platt scaling, lose the nuance of "how good" versus binary classification, and suffer from class imbalance when few excellent points exist early on.

---

### 4. What limitations of your current model become apparent as data grows?

**GP scalability issues:**
- Computational complexity scales as O(n³) due to matrix inversion
- With 30+ points per function, fitting time is noticeable
- By round 12 with 100+ points, this becomes a bottleneck

**Model fidelity concerns:**
- Length-scale estimation may overfit to noise, creating wiggly predictions
- The constant noise assumption breaks down across different regions
- Kernel choice (RBF vs. Matérn) matters more with increasing data

**High-dimensional challenges persist:** For Functions 7 (6D) and 8 (8D), even 30 observations leave data density desperately low. The curse of dimensionality means the GP effectively reverts to a global mean estimate in unseen regions.

**Mitigations considered:** Sparse GPs with inducing points, ARD kernels to identify irrelevant dimensions, local trust region models, or switching to Random Forest surrogates that scale better with data volume.

---

### 5. How does this black-box setup prepare you to think like a data scientist?

**Working under uncertainty:** Real ML problems rarely come with ground truth. The BBO setup forces decisions with incomplete information — exactly what practitioners face deploying models to production.

**Resource-constrained optimisation:** The limited query budget mirrors real constraints: computational cost, API limits, experimental time. Learning to extract maximum value from each observation is essential.

**Model selection and criticism:** Choosing between GPs, Random Forests and SVMs requires understanding each model's assumptions and failure modes, making theoretical trade-offs concrete.

**Adaptive strategy:** Static approaches fail. The competition rewards monitoring results, identifying what works and adjusting — the core feedback loop of applied data science.

**Connection to Hull Tactical:** The BBO challenge parallels the market prediction capstone directly. Both involve unknown underlying dynamics, expensive evaluations (forward-chaining CV), noisy outputs (financial returns) and the need to balance exploration of new hypotheses against exploitation of known patterns.
