# Required Capstone Component 21.1 — Week 10
## Refining Strategies for the Black-Box Optimisation Challenge

**Module:** 21 — Transparency and Interpretability
**Submitted:** 02/03/2026
**Cohort:** IMP-PCMLAI-25-08

---

## Part 1: Queries Submitted

| Function | Dimensions | Strategy | Query Submitted | Output |
|----------|------------|----------|-----------------|--------|
| F1 | 2D | Exploration (κ=1.5) | 0.828550-0.767752 | TBC |
| F2 | 2D | Exploitation (κ=0.5) | 0.749964-0.922752 | TBC |
| F3 | 3D | Exploitation (κ=0.5) | 0.209727-0.258306-0.412798 | TBC |
| F4 | 4D | Tight exploitation (κ=0.3) | 0.557009-0.440657-0.423370-0.239493 | TBC |
| F5 | 4D | Tight trust-region (κ=0.07, r=0.01) | 0.971352-0.987369-0.993384-0.965409 | TBC |
| F6 | 5D | Balanced (κ=0.9) | 0.713093-0.197399-0.737187-0.715973-0.038437 | TBC |
| F7 | 6D | GP gradient ascent (κ=1.8) | 0.036222-0.449214-0.260365-0.227969-0.343345-0.714826 | TBC |
| F8 | 8D | Tight trust-region (κ=0.07, r=0.04) | 0.062359-0.053215-0.073123-0.075132-0.378150-0.900466-0.575775-0.883420 | TBC |

---

## Part 2: Reflection on Strategy — Tenth Iteration (19 Data Points)

---

### 1. Reasoning for Round 10

By round 10, the strategy has matured from broad spatial exploration (Weeks 1–2) through SVM region classification (Week 3) to a hybrid GP–neural surrogate framework (Weeks 4–5). This round operates in full exploitation mode for well-characterised functions and retains targeted exploration only where the surrogate remains uncertain.

**F5 (4D):** The ridge near (0.95, 0.08, 0.82, 0.95) was confirmed across multiple rounds. Round 10 probes a refined perturbation along the X₃–X₄ axis, guided by the elliptical high-performance region identified via backpropagation saliency in Week 4.

**F8 (8D):** MLP gradient ascent established X₁ and X₃ as dominant dimensions. Round 10 extends X₁ to 0.847 and X₃ to 0.914 while holding low-influence dimensions near current best values — effectively a pseudo-2D search within the full 8D space.

**F1, F7:** Outputs remain near zero or inconsistent. Rather than refining a spurious local peak, both receive probes in undersampled regions to test whether the plateau is genuine or a sampling artefact.

---

### 2. Transparency and Reproducibility

Module 21's emphasis on model cards maps directly onto the BBO strategy: a reproducible pipeline requires documenting what was chosen and why. My strategy can be fully reproduced from:

- The complete input–output log across all 10 rounds
- Surrogate specifications: GP (RBF kernel, noise=0.01) for F1–F4; MLP (8→16→8→1) for F7–F8
- Acquisition function: UCB with κ=1.5 for exploitation, κ=3.0 for exploration
- Trust region: ±0.05 perturbation around best-known point during exploitation

The documentation philosophy established in the software architecture reflection ensures each query traces back to an explicit hypothesis — answering the same questions a model card demands: What was assumed? What was observed? What is the decision logic?

---

### 3. Key Assumption

The central assumption is **stationarity**: the GP kernel treats the function's correlation structure as uniform across the domain. For F5, where the high-performance region is tightly concentrated near the boundary, a stationary RBF kernel underestimates how rapidly the function decays outside that ridge. The surrogate over-smooths the peak, placing the predicted optimum slightly offset from the true maximum. A non-stationary kernel (e.g., deep kernel learning) would address this, but requires more data than the current query budget permits.

---

### 4. Gaps and Potential Biases

The dataset is heavily **exploitation-biased**: approximately 60% of all F5 and F8 queries cluster within high-performance corridors, leaving large fractions of both search spaces unsampled. For F8 (8D), even 19 observations cover an infinitesimal fraction of the unit hypercube — the curse of dimensionality renders the GP's uncertainty estimates unreliable in unseen regions. Functions with low observed outputs (F1, F2) received fewer exploratory attempts, creating a self-reinforcing cycle: we sample less where we expect less, so the surrogate's belief never updates in those regions.

---

### 5. Significant Limitation

The most fundamental limitation is the **single-query constraint**. Each round forces an irreversible commitment — there is no portfolio diversification across candidate points. This pushes the strategy increasingly toward conservative exploitation as the query budget depletes, even though significant unexplored regions remain. In a real hyperparameter tuning context, this mirrors the cost of expensive model evaluations: the inability to hedge across multiple candidates biases results toward local refinement and reduces the probability of discovering globally superior configurations. The constraint does not just affect results — it shapes the entire optimisation philosophy.
