# Black-Box Optimisation Capstone Project

**Author:** Dibyajyoti Pradhan
**Programme:** Imperial College London — Professional Certificate in Machine Learning and Artificial Intelligence
**Modules:** 12–22

---

## Project Overview

This repository documents my approach to the Black-Box Optimisation (BBO) challenge, where the goal is to maximise eight unknown functions using severely limited evaluation budgets. Each function represents a hidden response surface that can only be queried — never inspected directly.

BBO mirrors critical real-world ML scenarios: hyperparameter tuning for complex models, drug compound optimisation, financial strategy calibration — wherever function evaluations are expensive, gradients are unavailable, and internal structure is unknown.

---

## Repository Structure

```
Black-Box-Optimisation-Challenge/
│
├── data/
│   ├── initial_data/
│   │   ├── function_1/   initial_inputs.npy, initial_outputs.npy  (10 pts, 2D)
│   │   ├── function_2/   initial_inputs.npy, initial_outputs.npy  (10 pts, 2D)
│   │   ├── function_3/   initial_inputs.npy, initial_outputs.npy  (15 pts, 3D)
│   │   ├── function_4/   initial_inputs.npy, initial_outputs.npy  (30 pts, 4D)
│   │   ├── function_5/   initial_inputs.npy, initial_outputs.npy  (20 pts, 4D)
│   │   ├── function_6/   initial_inputs.npy, initial_outputs.npy  (20 pts, 5D)
│   │   ├── function_7/   initial_inputs.npy, initial_outputs.npy  (30 pts, 6D)
│   │   └── function_8/   initial_inputs.npy, initial_outputs.npy  (40 pts, 8D)
│   └── queries_data/
│       ├── round_10_queries.csv
│       └── round_11_queries.csv
│
├── notebooks/
│   ├── bbo_function_1.ipynb   (2D, GP-UCB, exploration)
│   ├── bbo_function_2.ipynb   (2D, GP-UCB, trust region ±0.08)
│   ├── bbo_function_3.ipynb   (3D, GP-UCB, trust region ±0.06)
│   ├── bbo_function_4.ipynb   (4D, GP-UCB, trust region ±0.05)
│   ├── bbo_function_5.ipynb   (4D, GP-UCB, trust region ±0.04, β=0.02)
│   ├── bbo_function_6.ipynb   (5D, GP-UCB, trust region ±0.06)
│   ├── bbo_function_7.ipynb   (6D, GP-UCB, exploration, β=3.0)
│   └── bbo_function_8.ipynb   (8D, GP-UCB, trust region ±0.04, β=0.02)
│
├── src/
│   ├── bbo_utils.py            ← reusable GP/UCB/LHS utilities
│   └── generate_notebooks.py  ← programmatic notebook generator
│
├── DATASHEET.md               ← Gebru et al. (2021) dataset documentation
├── MODEL_CARD.md              ← Mitchell et al. (2019) model documentation
├── requirements.txt
│
├── week_1_exploration_strategy.md
├── week_2_output_guided_search.md
├── week_3_svm_strategy.md
├── week_4_neural_network_surrogates.md
├── week_5_neural_network_concepts.md
├── week_5_software_architecture.md
├── week_6_cnn_reflection.md
├── hyperparameter_tuning.md
│
├── capstone_component_17_1_bbo_reflection.md
├── capstone_component_17_2_technical_foundations.md
├── capstone_component_18_1_hpo_reflection.md
├── capstone_component_19_1_prompting_strategies.md
├── capstone_component_20_1_scaling_emergence.md
├── capstone_component_21_1_bbo_round_10.md
└── capstone_component_22_1_bbo_round_11.md
```

---

## Function Catalogue

| Function | Dims | Initial Points | Output Range | Status (R11) |
|----------|------|---------------|--------------|--------------|
| F1 | 2D | 10 | Near-zero | Unresolved — exploring new region |
| F2 | 2D | 10 | Moderate | Drifting — gradual improvement |
| F3 | 3D | 15 | Moderate | Drifting — trajectory continuation |
| F4 | 4D | 30 | Moderate | Converging — tight local refinement |
| F5 | 4D | 20 | High (~1600+) | Converging — boundary ridge exploitation |
| F6 | 5D | 20 | Moderate | Drifting — conservative GP refinement |
| F7 | 6D | 30 | Low-moderate | Unresolved — full region reassignment |
| F8 | 8D | 40 | High | Converging — X₁/X₃ gradient ascent |

---

## Technical Approach

### Three-Phase Strategy

| Phase | Rounds | Technique | Rationale |
|-------|--------|-----------|-----------|
| **Exploration** | 1–2 | Max-distance heuristics, spatial coverage | No output data — maximise information gain |
| **Pattern recognition** | 3–5 | GP surrogates, SVM region classification, UCB (κ=3.0) | Outputs available — identify structure |
| **Exploitation** | 6–11 | Trust-region GP + MLP gradient ascent, κ=0.02–1.5 | Surrogates reliable — refine converging clusters |

### Key Methods

| Method | Application |
|--------|-------------|
| Gaussian Processes (RBF kernel) | Surrogate modelling for F1–F6; uncertainty-aware acquisition |
| MLP neural surrogate (8→16→8→1) | Differentiable surrogate for F7–F8; gradient-based query generation |
| UCB acquisition | Balances exploration (high β) and exploitation (low β) per function |
| Latin Hypercube Sampling | Efficient candidate generation in high-dimensional spaces |
| Trust region exploitation | Prevents boundary drift; constrains search around best-known point |
| Finite-difference sensitivity | Identifies dominant dimensions for pseudo-dimensionality reduction (F8: X₁, X₃) |

---

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Regenerate all notebooks from source
python src/generate_notebooks.py

# Open a notebook
jupyter notebook notebooks/bbo_function_5.ipynb
```

---

## Documentation

- **[DATASHEET.md](DATASHEET.md)** — Dataset documentation following Gebru et al. (2021)
- **[MODEL_CARD.md](MODEL_CARD.md)** — Model documentation following Mitchell et al. (2019)

---

## References

Shahriari, B., Swersky, K., Wang, Z., Adams, R.P. and de Freitas, N. (2016) 'Taking the human out of the loop: A review of Bayesian optimization', *Proceedings of the IEEE*, 104(1), pp. 148–175.

Frazier, P.I. (2018) *A tutorial on Bayesian optimization*. arXiv:1807.02811.

Gebru, T. et al. (2021) 'Datasheets for datasets', *Communications of the ACM*, 64(12), pp. 86–92.

Mitchell, M. et al. (2019) 'Model cards for model reporting', *Proceedings of FAccT*, pp. 220–229.
