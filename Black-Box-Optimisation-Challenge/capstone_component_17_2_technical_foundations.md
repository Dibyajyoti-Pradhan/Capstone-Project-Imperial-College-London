# Required Capstone Component 17.2: Documenting the Technical Foundations of Your Black-Box Optimisation Challenge

---

## 1. Main Technical Justification

My BBO approach is grounded in **surrogate-assisted Bayesian optimisation** with adaptive strategy selection based on function dimensionality and observed landscape characteristics. The core justification is sample efficiency under severe query constraints—with only 2-3 queries per week across 8 functions, every evaluation must maximise information gain.

The approach evolves across three phases:
- **Early iterations:** Gaussian Process (GP) surrogates with Upper Confidence Bound (UCB) acquisition for principled exploration-exploitation balance
- **Mid iterations:** SVM classification to separate "good" versus "bad" regions, reducing wasted queries in unpromising areas
- **Late iterations:** Neural network surrogates with gradient-based exploitation for high-dimensional functions (F5, F8)

This progression is supported by established Bayesian optimisation theory, which demonstrates that surrogate-based sequential decision-making outperforms uninformed search when evaluations are expensive (Jones et al., 1998; Shahriari et al., 2016).

---

## 2. Academic Papers Guiding the Design

Several foundational papers shaped my strategy:

| Paper | Key Contribution | Application in My Project |
|-------|------------------|---------------------------|
| **Jones et al. (1998)** – Efficient Global Optimization | Introduced GP surrogates + Expected Improvement | Foundation for surrogate-based query selection |
| **Srinivas et al. (2010)** – GP-UCB | Theoretical regret bounds for UCB acquisition | Justified exploration parameter κ selection |
| **Lakshminarayanan et al. (2017)** – Deep Ensembles | Ensemble variance as uncertainty proxy | MLP ensembles (5 networks) for high-D functions |
| **Rasmussen & Williams (2006)** – GP for ML | Kernel selection and length-scale interpretation | Matern kernels for smooth functions, shorter length-scales for rugged landscapes |

The most influential technique is **ensemble-based uncertainty quantification**—training multiple neural networks and using prediction variance to guide exploration. This provides calibrated uncertainty estimates without requiring full Bayesian inference, crucial when data points number only 10-15.

---

## 3. Third-Party Libraries and Frameworks

**Central tools:**

- **scikit-learn:** Gaussian Process regression (`GaussianProcessRegressor`), SVM classification, and preprocessing (scaling, normalisation). Chosen for stability, interpretability, and suitability for small datasets where deep learning frameworks add unnecessary complexity.

- **NumPy/SciPy:** Numerical computation, acquisition function optimisation via `scipy.optimize.minimize` (L-BFGS-B), and Latin Hypercube Sampling for initial exploration.

- **PyTorch:** Neural network surrogates for F5 (4D) and F8 (8D). Enables gradient computation through `autograd` for gradient-ascent exploitation—computing ∇ₓf_NN(x) to identify steepest improvement directions.

- **Matplotlib:** Visualisation of surrogate surfaces, acquisition landscapes, and query trajectories.

**Why not TensorFlow/BoTorch?** With datasets of 10-15 points, scikit-learn's L-BFGS-based GP fitting converges faster and more reliably than stochastic gradient methods. PyTorch is reserved for neural surrogates where backpropagation is essential.

---

## 4. Documentation Strategy for GitHub

To ensure transparency and reproducibility:

- **README.md:** High-level methodology overview linking theoretical motivation to implementation choices

- **`/docs/methodology.md`:** Detailed technical rationale covering surrogate selection, acquisition functions, and dimension-specific strategies

- **Weekly reflection files:** Documenting iteration-by-iteration decisions, failed experiments, and lessons learned (e.g., `week_4_strategy.md`, `week_5_adaptive_strategy.md`)

- **Annotated notebooks:** Inline comments explaining why specific parameters were chosen (e.g., κ=1.96 for 95% confidence exploration bounds)

- **References section:** Academic citations enabling reviewers to trace design decisions to established literature

This structure allows peers, facilitators, and employers to understand not just *what* was implemented, but *why*.

---

## 5. Future Sources for Refinement

Looking ahead, I plan to explore:

- **TuRBO (Eriksson et al., 2019):** Trust-region methods for high-dimensional BBO where global GPs fail—particularly relevant for F7 and F8

- **BoTorch/GPyTorch:** Modern Bayesian optimisation frameworks for more sophisticated acquisition strategies (q-Expected Improvement, knowledge gradient)

- **COCO/BBOB benchmarks:** Standardised test functions to validate strategy generalisation beyond capstone functions

- **Multi-fidelity optimisation:** Leveraging cheaper approximations to guide expensive queries

- **Spectral mixture kernels:** Capturing periodic or multi-scale structure that standard Matern/RBF kernels may miss

---

## References

- Jones, D.R., Schonlau, M., & Welch, W.J. (1998). Efficient Global Optimization of Expensive Black-Box Functions. *Journal of Global Optimization*.
- Srinivas, N., et al. (2010). Gaussian Process Optimization in the Bandit Setting. *ICML*.
- Lakshminarayanan, B., Pritzel, A., & Blundell, C. (2017). Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles. *NeurIPS*.
- Rasmussen, C.E. & Williams, C.K.I. (2006). *Gaussian Processes for Machine Learning*. MIT Press.
- Shahriari, B., et al. (2016). Taking the Human Out of the Loop: A Review of Bayesian Optimization. *Proceedings of the IEEE*.

---

*Word count: 698*
