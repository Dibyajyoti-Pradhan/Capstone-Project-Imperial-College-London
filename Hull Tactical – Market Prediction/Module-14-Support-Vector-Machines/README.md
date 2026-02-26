# Black-Box Optimisation Capstone Project

## Section 1: Project Overview

This repository documents my approach to the Black-Box Optimisation (BBO) challenge, where the goal is to maximise eight unknown functions using severely limited evaluation budgets. Each function represents a hidden response surface that can only be queried — never inspected directly.

**Why BBO Matters in Real-World ML:**
BBO mirrors critical scenarios in applied machine learning where function evaluations are expensive, gradients are unavailable, and internal structure is unknown. Examples include hyperparameter tuning for complex models, drug compound optimisation, and financial strategy calibration.

**Connection to My Capstone:**
This project directly complements my Hull Tactical market prediction work. Both involve optimising under uncertainty — BBO with unknown functions, market prediction with unknown dynamics. The skills developed here (surrogate modelling, exploration-exploitation trade-offs, decision-making with sparse data) transfer directly to tuning prediction models on financial time-series where each backtest is computationally expensive.

**Career Relevance:**
Mastering BBO builds competencies essential for data science roles: experimental design under constraints, probabilistic reasoning, and iterative model refinement — all critical when deploying ML systems where real-world feedback is slow and costly.

---

## Section 2: Inputs and Outputs

### Input Format
Each function accepts a continuous vector bounded in [0, 1], with dimensionality varying by function:

| Function | Dimensions | Example Query |
|----------|------------|---------------|
| F1, F2 | 2D | `0.500000-0.750000` |
| F3 | 3D | `0.333333-0.666667-0.500000` |
| F4, F5 | 4D | `0.250000-0.500000-0.750000-0.250000` |
| F6 | 5D | `0.200000-0.400000-0.600000-0.800000-0.100000` |
| F7 | 6D | `0.166667-0.333333-0.500000-0.666667-0.833333-0.166667` |
| F8 | 8D | `0.125000-0.250000-0.375000-0.500000-0.625000-0.750000-0.875000-0.125000` |

**Constraints:**
- All values specified to 6 decimal places
- Values must begin with `0.` and remain strictly in [0, 1)
- One query per function per week

### Output Format
Each query returns a single scalar representing performance at that point. Outputs vary dramatically across functions (from ~10⁻³¹ to ~10³), with some exhibiting noise.

---

## Section 3: Challenge Objectives

**Primary Goal:** Maximise the output of each function within a strictly limited query budget (~13 queries per function total).

**Key Constraints:**
- **Unknown structure:** Functions may be smooth, noisy, unimodal, or multimodal
- **Sparse data:** Starting with only 10 observations per function
- **Delayed feedback:** Results returned weekly, requiring advance planning
- **Dimensional curse:** Higher-dimensional functions (6D-8D) suffer from exponentially sparse coverage

**Success Criteria:**
Demonstrate a principled, adaptive strategy that balances exploration (reducing uncertainty) with exploitation (refining promising regions) — not just final values achieved, but the reasoning behind each decision.

---

## Section 4: Technical Approach

### Evolution Across Three Rounds

**Week 1 — Pure Exploration:**
With no output feedback, I prioritised spatial coverage using maximum-distance heuristics. Queries were placed to fill gaps in the initial dataset, treating all functions uniformly.

**Week 2 — Output-Guided Differentiation:**
Week 1 results revealed dramatic differences: Function 5 returned ~1600 (strong signal), while Function 1 showed near-zero values. This prompted function-specific strategies:
- Strong performers (F5, F8): Local perturbation around best-known points
- Weak signals (F1, F7): Aggressive exploration with high UCB kappa
- Negative outputs (F3, F6): Moderate exploration to escape poor regions

**Week 3 — Model-Informed Decisions:**
Gaussian Process surrogates now drive query selection. I introduced SVM-inspired thinking to classify regions as promising/unpromising, pre-filtering candidates before GP-based acquisition.

### Methods Used

| Technique | Application |
|-----------|-------------|
| **Gaussian Processes** | Surrogate models providing mean predictions and uncertainty |
| **UCB Acquisition** | Balancing exploration (high kappa) and exploitation (low kappa) |
| **Trust Region Exploitation** | Constraining refinement to avoid boundary drift |
| **SVM Classification** | Identifying high-performing regions in high-dimensional spaces |
| **Feature Correlation Analysis** | Detecting influential dimensions for pseudo-dimensionality reduction |

### Exploration vs Exploitation Balance

Currently at ~50/50 overall, but varying significantly:
- **F5, F8:** 30% exploration — refining identified optima
- **F1, F7:** 70% exploration — searching for main signal
- **F2-F4, F6:** Balanced based on observed progress

### What Makes This Approach Thoughtful

Rather than applying one method blindly, I adapt strategy to each function's characteristics. Model complexity scales with data availability — simple heuristics early, surrogate models later. Decisions are documented with explicit rationale, treating this as a living record of iterative learning under uncertainty.

---

**Word count: ~680**

