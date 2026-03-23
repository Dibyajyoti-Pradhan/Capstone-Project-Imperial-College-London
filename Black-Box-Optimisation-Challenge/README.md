# Black-Box Optimisation Capstone Project

**Author:** Dibyajyoti Pradhan
**Programme:** Imperial College London — Professional Certificate in Machine Learning and Artificial Intelligence
**Modules:** 12–24 | **Cohort:** IMP-PCMLAI-25-08

---

## What This Project Is (Non-Technical Summary)

Imagine trying to find the highest point in a mountain range while blindfolded, allowed only 13 steps, and told only your current altitude after each step. That is the Black-Box Optimisation (BBO) challenge. Over 13 weeks, I submitted one set of coordinates per function to a portal that returned a single number — the function's output — with no other information. Using statistical models that learn from each result, I progressively narrowed the search toward the highest-output regions. For one function (F5), the peak — returning over 8,500 — was found in the very first week. The project demonstrates how machine learning techniques can guide intelligent search through unknown spaces using minimal, expensive information.

---

## Project Overview

The BBO challenge tasks participants with maximising eight unknown functions over 13 weekly submission rounds. Each function is a black box — inputs go in, a scalar output comes back, and the internal mechanics are never revealed. The goal is to find the input combination that produces the highest possible output for each function within the query budget.

**Real-world analogues:**
| Function | Analogue |
|----------|----------|
| F1 | Contamination source detection |
| F2 | Noisy log-likelihood model |
| F3 | Drug compound optimisation |
| F4 | Warehouse product placement / hyperparameter tuning |
| F5 | Chemical process yield optimisation |
| F6 | Recipe scoring |
| F7 | ML model hyperparameter tuning (6 params) |
| F8 | 8-hyperparameter ML model tuning |

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
│       ├── week_01_queries.csv  ←  submitted inputs + confirmed outputs
│       ├── week_02_queries.csv
│       ├── ...
│       └── week_13_queries.csv
│
├── notebooks/
│   └── bbo_function_{1-8}.ipynb  ←  GP-UCB strategy notebooks per function
│
├── src/
│   ├── bbo_utils.py               ←  GP / UCB / LHS utilities (fully documented)
│   └── generate_notebooks.py      ←  notebook scaffolding generator
│
├── capstone_component_12_1_week_1.md   ←  Week 1: queries + reflection
├── capstone_component_13_1_week_2.md   ←  Week 2
├── capstone_component_14_1_week_3.md   ←  Week 3
├── capstone_component_14_2_github_readme.md
├── capstone_component_15_1_week_4.md   ←  Week 4
├── capstone_component_15_2_hyperparameters.md
├── capstone_component_16_1_week_5.md   ←  Week 5
├── capstone_component_16_2_software_architecture.md
├── capstone_component_17_1_week_6.md   ←  Week 6
├── capstone_component_17_2_technical_foundations.md
├── capstone_component_18_1_week_7.md   ←  Week 7
├── capstone_component_19_1_week_8.md   ←  Week 8
├── capstone_component_20_1_week_9.md   ←  Week 9
├── capstone_component_21_1_week_10.md  ←  Week 10
├── capstone_component_21_2_transparency.md
├── capstone_component_22_1_week_11.md  ←  Week 11
├── capstone_component_23_1_week_12.md  ←  Week 12
├── capstone_component_23_2_bbo_presentation.md  ←  Final presentation (25.2)
├── capstone_component_24_1_week_13.md  ←  Week 13 (final round)
├── capstone_component_25_1_retrospective.md  ←  Programme retrospective
├── capstone_component_25_2_successful_strategies.md
│
├── DATASHEET.md     ←  Gebru et al. (2021) dataset documentation
├── MODEL_CARD.md    ←  Mitchell et al. (2019) model documentation
├── LICENSE          ←  MIT Licence
├── requirements.txt
└── README.md
```

---

## Results Summary

| Function | Dims | Best Output Observed | Week of Best | Status |
|----------|------|---------------------|--------------|--------|
| F1 | 2D | ~0 | Throughout | Unresolved — flat landscape |
| F2 | 2D | 0.435 | Week 4 | Drifting — gradual improvement |
| F3 | 3D | −0.009 | Week 4 | Drifting — approaching zero |
| F4 | 4D | −3.770 | Week 3 | Drifting — large early gain |
| **F5** | **4D** | **8585.27** | **Week 1** | **Converged — boundary peak confirmed** |
| F6 | 5D | −0.570 | Week 3 | Drifting — slow improvement |
| F7 | 6D | 1.785 | Week 3 | Unresolved — modest signal |
| F8 | 8D | 9.683 | Week 3 | Converging — slow steady improvement |

---

## Weekly Progress

| Week | Module | Strategy | Status |
|------|--------|----------|--------|
| 1 | 12 | Max-distance exploration — no surrogate | ✅ Submitted |
| 2 | 13 | Output-guided: exploit F5/F8, explore F1/F7 | ✅ Submitted |
| 3 | 14 | GP-UCB surrogates; trust region F5; κ=3.0 F1/F7 | ✅ Submitted |
| 4 | 15 | Hybrid GP + MLP gradient ascent: F7/F8 via backprop | ✅ Submitted |
| 5 | 16 | Hierarchical strategy; tight exploit F5; dense boundary sampling | ✅ Submitted |
| 6 | 17 | Progressive trust-region tightening; gradient ascent F7 | ✅ Submitted |
| 7 | 18 | Adaptive κ scheduling; function-specific trust-region radii | ✅ Submitted |
| 8 | 19 | LLM-assisted hypothesis generation; few-shot CoT prompting | ✅ Submitted |
| 9 | 20 | Scaling-law framing; tiered exploit/explore; ensemble hedging F7/F8 | ✅ Submitted |
| 10 | 21 | Transparency lens: reproducibility, stationarity, exploitation bias | ✅ Submitted |
| 11 | 22 | Clustering lens: converging/drifting/unresolved clusters | ✅ Submitted |
| 12 | 23 | PCA-inspired dimension reduction; 4D subspace for F8 | ✅ Submitted |
| 13 | 24 | Final round: RL lens; decisive exploitation F5/F8 | ✅ Submitted |

---

## Technical Approach

| Phase | Weeks | Technique |
|-------|-------|-----------|
| Exploration | 1–2 | Max-distance heuristic, Latin Hypercube Sampling |
| Pattern recognition | 3–6 | GP surrogates, UCB (κ=3.0), SVM region classification |
| Exploitation | 7–13 | Trust-region GP + MLP gradient ascent, κ=0.02–1.5 |

**Core acquisition function:** Upper Confidence Bound — `UCB(x) = μ(x) + κ·σ(x)`

Low κ → exploit high-confidence regions (F5, F8)
High κ → explore uncertain regions (F1, F7)

---

## Quick Start

```bash
pip install -r requirements.txt
python src/generate_notebooks.py
jupyter notebook notebooks/bbo_function_5.ipynb
```

---

## Documentation

- **[DATASHEET.md](DATASHEET.md)** — Dataset documentation (Gebru et al., 2021)
- **[MODEL_CARD.md](MODEL_CARD.md)** — Model documentation (Mitchell et al., 2019)
- **[LICENSE](LICENSE)** — MIT Licence

---

## Licence

This project is released under the [MIT Licence](LICENSE).
