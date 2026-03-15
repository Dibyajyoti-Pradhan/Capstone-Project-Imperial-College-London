# Required Capstone Component 17.2 — Documenting the Technical Foundations of the BBO Challenge

**Module:** 17 — Convolutional Neural Networks
**Submitted:** 27/02/2026
**Cohort:** IMP-PCMLAI-25-08

---

## 1. Main Technical Justification

My BBO approach is grounded in surrogate-assisted Bayesian optimisation with adaptive strategy selection based on function dimensionality and observed landscape characteristics. The core justification is sample efficiency under severe query constraints — with only 2–3 queries per week across 8 functions, every evaluation must maximise information gain.

The approach evolves across three phases:

- **Early iterations:** Gaussian Process (GP) surrogates with Upper Confidence Bound (UCB) acquisition for principled exploration-exploitation balance
- **Mid iterations:** SVM classification to separate "good" versus "bad" regions, reducing wasted queries in unpromising areas
- **Late iterations:** Neural network surrogates with gradient-based exploitation for high-dimensional functions (F5, F8)

This progression is supported by established Bayesian optimisation theory, which demonstrates that surrogate-based sequential decision-making outperforms uninformed search when evaluations are expensive (Jones et al., 1998; Shahriari et al., 2016).

---

## 2. Academic Papers Guiding the Design

Several foundational papers shaped my strategy:

| Paper | Key Contribution | Application in My Project |
|:------|:-----------------|:--------------------------|
| Jones et al. (1998) — Efficient Global Optimization | Introduced GP surrogates + Expected Improvement | Foundation for surrogate-based query selection |
| Srinivas et al. (2010) — GP-UCB | Theoretical regret bounds for UCB acquisition | Justified exploration parameter κ selection |
| Lakshminarayanan et al. (2017) — Deep Ensembles | Ensemble variance as uncertainty proxy | MLP ensembles (5 networks) for high-D functions |
| Rasmussen & Williams (2006) — GP for ML | Kernel selection and length-scale interpretation | Matérn kernels for smooth functions |

The most influential technique is ensemble-based uncertainty quantification — training multiple neural networks and using prediction variance to guide exploration. This provides calibrated uncertainty estimates without requiring full Bayesian inference, crucial when data points number only 10–15.

---

## 3. Third-Party Libraries and Frameworks

Central tools:

- **scikit-learn:** Gaussian Process regression, SVM classification, and preprocessing. Chosen for stability, interpretability, and suitability for small datasets.
- **NumPy/SciPy:** Numerical computation, acquisition function optimisation via L-BFGS-B, and Latin Hypercube Sampling for initial exploration.
- **PyTorch:** Neural network surrogates for F5 (4D) and F8 (8D). Enables gradient computation through autograd for gradient-ascent exploitation.

**Why not TensorFlow/BoTorch?** With datasets of 10–15 points, scikit-learn's L-BFGS-based GP fitting converges faster and more reliably than stochastic gradient methods.

---

## 4. Documentation Strategy for GitHub

To ensure transparency and reproducibility:

- **README.md:** High-level methodology overview linking theoretical motivation to implementation choices
- **Weekly reflection files:** Documenting iteration-by-iteration decisions, failed experiments, and lessons learned
- **Annotated notebooks:** Inline comments explaining parameter choices
- **DATASHEET.md / MODEL_CARD.md:** Following Gebru et al. (2021) and Mitchell et al. (2019) frameworks for dataset and model transparency
- **References section:** Academic citations enabling reviewers to trace design decisions to literature

---

## 5. Future Sources for Refinement

Looking ahead, I plan to explore:

- **TuRBO (Eriksson et al., 2019):** Trust-region methods for high-dimensional BBO
- **BoTorch/GPyTorch:** Modern Bayesian optimisation frameworks for sophisticated acquisition strategies
- **COCO/BBOB benchmarks:** Standardised test functions to validate strategy generalisation
- **Multi-fidelity optimisation:** Leveraging cheaper approximations to guide expensive queries
- **Spectral mixture kernels:** Capturing periodic or multi-scale structure

---

## References

Eriksson, D. et al. (2019) 'Scalable global optimization via local Bayesian optimization', *Advances in Neural Information Processing Systems*, 32.

Jones, D.R., Schonlau, M. and Welch, W.J. (1998) 'Efficient global optimization of expensive black-box functions', *Journal of Global Optimization*, 13(4), pp. 455–492.

Lakshminarayanan, B., Pritzel, A. and Blundell, C. (2017) 'Simple and scalable predictive uncertainty estimation using deep ensembles', *Advances in Neural Information Processing Systems*, 30.

Rasmussen, C.E. and Williams, C.K.I. (2006) *Gaussian Processes for Machine Learning*. MIT Press.

Shahriari, B. et al. (2016) 'Taking the human out of the loop: a review of Bayesian optimization', *Proceedings of the IEEE*, 104(1), pp. 148–175.

Srinivas, N. et al. (2010) 'Gaussian process optimization in the bandit setting: no regret and experimental design', *Proceedings of ICML*, pp. 1015–1022.
