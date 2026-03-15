# Required Capstone Component 16.2 — Determining a Software Architecture

**Module:** 16 — Deep Learning
**Submitted:** 26/02/2026
**Cohort:** IMP-PCMLAI-25-08

---

## Repository Structure

### Current Organisation

The repository is structured with a clear separation of concerns:

```
Black-Box-Optimisation-Challenge/
├── data/
│   ├── initial_data/function_{1-8}/     # initial_inputs.npy, initial_outputs.npy
│   └── queries_data/                    # week_01 to week_05 query CSVs
├── notebooks/
│   └── bbo_function_{1-8}.ipynb        # GP-UCB analysis per function
├── src/
│   ├── bbo_utils.py                     # GP fitting, UCB acquisition, LHS sampling
│   └── generate_notebooks.py           # Programmatic notebook generator
├── capstone_component_12_1_week_1.md
├── capstone_component_13_1_week_2.md
├── capstone_component_14_1_week_3.md
├── capstone_component_14_2_github_readme.md
├── capstone_component_15_1_week_4.md
├── capstone_component_15_2_hyperparameters.md
├── capstone_component_16_1_week_5.md
├── capstone_component_16_2_software_architecture.md
├── DATASHEET.md                         # Gebru et al. (2021) dataset documentation
├── MODEL_CARD.md                        # Mitchell et al. (2019) model documentation
├── README.md
└── requirements.txt
```

Each weekly capstone component captures the strategic evolution — not just what was submitted but why. This chronological structure enables full traceability from broad exploration (Week 1) to targeted exploitation (Week 5+).

### Design Rationale

- **`data/initial_data/`** — version-controlled initial `.npy` files so the full pipeline is reproducible without portal access
- **`src/bbo_utils.py`** — reusable module isolating GP fitting, UCB acquisition and Latin Hypercube Sampling; notebooks import this rather than reimplementing each week
- **`notebooks/`** — one notebook per function, generated programmatically via `generate_notebooks.py`, so architecture changes propagate automatically
- **`data/queries_data/`** — structured CSV logs enabling audit trail and future re-analysis

---

## Coding Libraries and Packages

| Library | Purpose | Justification |
|:--------|:--------|:--------------|
| NumPy | Array operations, candidate generation | Foundation for vectorised computation; efficient LHS sampling |
| scikit-learn | Gaussian Process surrogates, SVM classification | Robust GP with uncertainty quantification; ideal for small-data regimes |
| SciPy | Latin Hypercube Sampling, acquisition optimisation | Reliable constrained search; integrates seamlessly with NumPy |
| Matplotlib | Response surface visualisation | Quick 2D projections and uncertainty plots |

### Framework Choice: Why Not PyTorch/TensorFlow?

While Module 16 introduced deep learning frameworks, I deliberately chose not to use them as primary tools. The reasoning:

- **Data scarcity:** ~14 observations per function — neural networks risk severe overfitting
- **Uncertainty quantification:** GPs provide natural uncertainty estimates; NNs require additional machinery (ensembles, MC dropout)
- **Computational efficiency:** scikit-learn GP fits in milliseconds; PyTorch training loops add unnecessary overhead at this scale
- **Interpretability:** Kernel hyperparameters (length-scales, noise) directly inform search strategy

**Trade-off acknowledged:** This sacrifices the expressiveness of deep surrogates for reliability and transparency. For F7–F8 with more data, PyTorch-based neural surrogates are used selectively via gradient ascent — a hybrid rather than wholesale switch.

### Rapid Prototyping vs Production Design

The approach aligns with **rapid prototyping (PyTorch philosophy)** — strategy adapts weekly, experimentation drives decisions, and interpretability is prioritised over automation. A TensorFlow-style production architecture would only be appropriate once function landscapes are well-understood and strategy stabilises.

---

## Documentation

### Current State

The README documents:
- **Project goal:** maximise 8 unknown functions within 13 query rounds
- **Input/output format:** coordinate vectors in [0,1]ⁿ → scalar function values
- **Function catalogue:** dimensionality, initial points, output range, weekly status
- **Strategic evolution:** three-phase approach (exploration → pattern recognition → exploitation)
- **Quick start:** `pip install -r requirements.txt && python src/generate_notebooks.py`

Supporting documentation includes `DATASHEET.md` (Gebru et al., 2021 framework) and `MODEL_CARD.md` (Mitchell et al., 2019 framework), ensuring transparency about both data and modelling decisions.

### Documentation Philosophy

The goal is to present the repository as a **narrative of iterative learning**, not a code dump. Each capstone component answers:
1. What was the hypothesis?
2. What was observed?
3. How did this inform the next decision?

This mirrors how employers evaluate technical work — clarity of reasoning matters as much as results. A well-structured repository is itself a form of documentation.

---

## References

Gebru, T. et al. (2021) 'Datasheets for datasets', *Communications of the ACM*, 64(12), pp. 86–92.

Mitchell, M. et al. (2019) 'Model cards for model reporting', *Proceedings of FAccT*, pp. 220–229.
