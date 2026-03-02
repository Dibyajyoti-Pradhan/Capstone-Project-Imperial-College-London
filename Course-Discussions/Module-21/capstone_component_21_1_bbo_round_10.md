# Required Capstone Component 21.1: Refining BBO Strategies — Round 10

## Part 1: Queries Submitted

| Function | Dimension | Query |
|----------|-----------|-------|
| F1 | 2D | (0.483291, 0.716842) |
| F2 | 2D | (0.621478, 0.304591) |
| F3 | 3D | (0.712046, 0.483712, 0.591834) |
| F4 | 3D | (0.568923, 0.731045, 0.412867) |
| F5 | 4D | (0.952841, 0.073621, 0.837492, 0.961074) |
| F6 | 5D | (0.683741, 0.512894, 0.749213, 0.384521, 0.621843) |
| F7 | 6D | (0.412847, 0.718934, 0.519283, 0.384712, 0.623891, 0.571234) |
| F8 | 8D | (0.847213, 0.492381, 0.913847, 0.381274, 0.512847, 0.673821, 0.428137, 0.591284) |

---

## Part 2: Reflection

### 1. Reasoning for Round 10

By round 10, the strategy has matured from broad spatial exploration (Weeks 1–2) through SVM region classification (Week 3) to a hybrid GP–neural surrogate framework (Weeks 4–5). This round operates in full exploitation mode for well-characterised functions and retains targeted exploration only where the surrogate remains uncertain.

**F5 (4D):** The ridge near (0.95, 0.08, 0.82, 0.95) was confirmed across multiple rounds. Round 10 probes a refined perturbation along the X₃–X₄ axis, guided by the elliptical high-performance region identified via backpropagation saliency in Week 4.

**F8 (8D):** MLP gradient ascent established X₁ and X₃ as dominant dimensions. Round 10 extends X₁ to 0.847 and X₃ to 0.914 while holding low-influence dimensions near current best values — effectively a pseudo-2D search within the full 8D space.

**F1, F7:** Outputs remain near zero or inconsistent. Rather than refining a spurious local peak, both receive probes in undersampled regions to test whether the plateau is genuine or a sampling artefact.

---

### 2. Transparency and Reproducibility

Module 21's emphasis on model cards maps directly onto the BBO strategy: a reproducible pipeline requires documenting *what* was chosen and *why*. My strategy can be fully reproduced from:

- The complete input–output log across all 10 rounds
- Surrogate specifications: GP (RBF kernel, noise=0.01) for F1–F4; MLP (8→16→8→1) for F7–F8
- Acquisition function: UCB with κ=1.5 for exploitation, κ=3.0 for exploration
- Trust region: ±0.05 perturbation around best-known point during exploitation

The documentation philosophy established in the software architecture reflection ensures each query traces back to an explicit hypothesis — answering the same questions a model card demands: *What was assumed? What was observed? What is the decision logic?*

---

### 3. Key Assumption

The central assumption is **stationarity**: the GP kernel treats the function's correlation structure as uniform across the domain. For F5, where the high-performance region is tightly concentrated near the boundary, a stationary RBF kernel underestimates how rapidly the function decays outside that ridge. The surrogate over-smooths the peak, placing the predicted optimum slightly offset from the true maximum. A non-stationary kernel (e.g., deep kernel learning) would address this, but requires more data than the current query budget permits.

---

### 4. Gaps and Biases

The dataset is heavily exploitation-biased: approximately 60% of all F5 and F8 queries cluster within high-performance corridors, leaving large fractions of both search spaces unsampled. For F8 (8D), even 18 observations cover an infinitesimal fraction of the unit hypercube — the curse of dimensionality renders the GP's uncertainty estimates unreliable in unseen regions. Functions with low observed outputs (F1, F2) received fewer exploratory attempts, creating a self-reinforcing cycle: we sample less where we expect less, so the surrogate's belief never updates in those regions.

---

### 5. Significant Limitation

The most fundamental limitation is the **single-query constraint**. Each round forces an irreversible commitment — there is no portfolio diversification across candidate points. This pushes the strategy increasingly toward conservative exploitation as the query budget depletes, even though significant unexplored regions remain. In a real hyperparameter tuning context, this mirrors the cost of expensive model evaluations: the inability to hedge across multiple candidates biases results toward local refinement and reduces the probability of discovering globally superior configurations. The constraint does not just affect results — it shapes the entire optimisation philosophy.

---

### References

Shahriari, B., Swersky, K., Wang, Z., Adams, R.P. and de Freitas, N. (2016) 'Taking the human out of the loop: A review of Bayesian optimization', *Proceedings of the IEEE*, 104(1), pp. 148–175.

Frazier, P.I. (2018) *A tutorial on Bayesian optimization*. arXiv:1807.02811.
