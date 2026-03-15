# Black-Box Optimisation Capstone Project

**Author:** Dibyajyoti Pradhan
**Programme:** Imperial College London — Professional Certificate in Machine Learning and Artificial Intelligence
**Modules:** 12–24 | **Cohort:** IMP-PCMLAI-25-08

---

## Project Overview

The BBO challenge tasks participants with maximising eight unknown functions over 13 weekly submission rounds. Each function is a black box — inputs go in, a scalar output comes back, and the internal mechanics are never revealed. The goal is to find the input combination that produces the highest possible output for each function within the query budget.

**Real-world analogues:**
- F1: Contamination source detection
- F2: Noisy log-likelihood model
- F3: Drug compound optimisation (minimise adverse reactions → maximise negated score)
- F4: Warehouse product placement (ML model hyperparameter tuning)
- F5: Chemical process yield optimisation
- F6: Recipe scoring (bring negative score as close to zero as possible)
- F7: ML model hyperparameter tuning (6 params)
- F8: 8-hyperparameter ML model tuning

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
│       └── week_01_queries.csv    ← actual submitted queries + outputs
│
├── notebooks/
│   └── bbo_function_{1-8}.ipynb  ← GP-UCB notebooks per function
│
├── src/
│   ├── bbo_utils.py               ← GP/UCB/LHS utilities
│   └── generate_notebooks.py     ← notebook generator
│
├── capstone_component_12_1_week_1.md   ← Week 1 queries + reflection
│
├── DATASHEET.md
├── MODEL_CARD.md
├── requirements.txt
└── README.md
```

---

## Function Catalogue

| Function | Dims | Initial Points | Output Range (initial) | Week 1 Query |
|----------|------|---------------|----------------------|--------------|
| F1 | 2D | 10 | Near-zero | 0.001000-0.999000 |
| F2 | 2D | 10 | Moderate | 0.001000-0.999000 |
| F3 | 3D | 15 | Moderate | 0.437056-0.996752-0.890886 |
| F4 | 4D | 30 | Moderate | 0.009153-0.333687-0.980781-0.997681 |
| F5 | 4D | 20 | High (~1088) | 0.999000-0.999000-0.999000-0.999000 |
| F6 | 5D | 20 | Moderate | 0.001000-0.001000-0.001000-0.001000-0.001000 |
| F7 | 6D | 30 | Low-moderate | 0.001000-0.001000-0.999000-0.001000-0.999000-0.001000 |
| F8 | 8D | 40 | High | 0.001000-0.001000-0.001000-0.001000-0.999000-0.001000-0.001000-0.001000 |

---

## Weekly Progress

| Week | Module | Strategy | Status |
|------|--------|----------|--------|
| 1 | 12 | Max-distance exploration (no outputs) | ✅ Submitted |
| 2 | 13 | Output-guided: exploit F5/F8, explore F1/F7, escape F3/F6 | ✅ Submitted |
| 3 | 14 | GP-UCB surrogates: trust region F5/F8, κ=5.0 F1/F7, balanced rest | ✅ Submitted |
| 4 | 15 | Hybrid GP + MLP gradient ascent: F7/F8 via backprop gradients | ✅ Submitted |
| 5 | 16 | Hierarchical strategy: tight exploit F5/F8, gradient ascent F7, explore F1 | ✅ Submitted |
| 6 | 17 | CNN-parallel: progressive feature extraction, trust-region F5/F8, gradient ascent F7 | ✅ Submitted |
| 7 | 18 | Adaptive κ scheduling, tighter trust regions, dimension reduction F8 | ✅ Submitted |
| 8 | 19 | LLM-assisted hypothesis generation; few-shot CoT prompting; trust regions F5/F8 | ✅ Submitted |
| 9 | 20 | Scaling-law framing; tiered exploit/explore; ensemble hedging F7/F8 | ✅ Submitted |
| 10 | 21 | Transparency lens: reproducibility, stationarity assumption, exploitation bias | ✅ Submitted |
| 11 | 22 | Clustering lens: converging/drifting/unresolved clusters; function-specific radii | ✅ Submitted |
| 12 | 23 | PCA-inspired dimension reduction; ultra-tight trust regions F5/F8 (21 pts) | ✅ Submitted |
| 13 | 24 | Final round: decisive exploitation F5/F8, reduced 4D subspace F8, RL lens | ✅ Submitted |

---

## Technical Approach

| Phase | Weeks | Technique |
|-------|-------|-----------|
| Exploration | 1–2 | Max-distance heuristic, LHS candidate generation |
| Pattern recognition | 3–6 | GP surrogates, UCB (κ=3.0), SVM region classification |
| Exploitation | 7–13 | Trust-region GP + MLP gradient ascent, κ=0.02–1.5 |

---

## Quick Start

```bash
pip install -r requirements.txt
python src/generate_notebooks.py
jupyter notebook notebooks/bbo_function_5.ipynb
```

---

## Documentation

- **[DATASHEET.md](DATASHEET.md)** — Gebru et al. (2021) dataset documentation
- **[MODEL_CARD.md](MODEL_CARD.md)** — Mitchell et al. (2019) model documentation
