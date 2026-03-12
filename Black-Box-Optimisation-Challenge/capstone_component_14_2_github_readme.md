# Required Capstone Component 14.2 — GitHub README Documentation
## Creating Documentation for the Capstone Project on GitHub

**Module:** 14 — Support Vector Machines
**Cohort:** IMP-PCMLAI-25-08

---

## Reflection on GitHub README Documentation

This component documents the decisions behind the BBO capstone project's GitHub README, covering purpose, structure, technical approach and how the documentation consolidates ideas from regression, SVMs and iterative modelling.

---

### Purpose of the README

The README serves three audiences simultaneously:

1. **Self-documentation:** Forces clarity about what each modelling decision was and why — directly supporting reproducibility across the 13-week challenge
2. **External reviewers (assessors):** Demonstrates structured thinking, phased methodology and awareness of real-world ML constraints
3. **Future employers/collaborators:** Signals professionalism — a clean README shows the ability to communicate technical work clearly, which is increasingly valued in data science roles

---

### Core Elements Documented

**Project inputs and outputs:**
- Eight functions across 2D–8D input spaces, all bounded in [0,1]
- One scalar output per query, interpreted as a performance score to maximise
- Initial data: 10–40 observations per function (provided as `.npy` files)

**Objectives:**
- Maximise each function's output within 13 query rounds
- Demonstrate a principled, adaptive strategy — not just final values, but documented reasoning

**Technical approach documented:**

| Phase | Rounds | Technique |
|-------|--------|-----------|
| Exploration | 1–2 | Max-distance heuristic, Latin Hypercube Sampling |
| Pattern recognition | 3–6 | GP surrogates, UCB acquisition, SVM region classification |
| Exploitation | 7–13 | Trust-region GP, MLP gradient ascent, κ calibrated per function |

---

### How Recent Modules Shaped the Documentation

**Regression (Module 13):** The README explicitly notes why linear/logistic regression is unsuitable as a surrogate — violated assumptions (non-linearity, sparse data, multimodality). This framing demonstrates awareness of model limitations, not just blind application of the most complex tool.

**SVMs (Module 14):** The technical approach section references SVM-based region classification as a candidate pre-filter — thresholding outputs into good/bad regions before GP-based acquisition. This is documented in the approach table under "Pattern recognition" phase.

**Iterative modelling:** The weekly progress table in the README makes explicit that strategy evolves round by round. This mirrors the iterative feedback loop that characterises real-world ML deployment.

---

### Design Decisions

**Why function-specific κ values are documented:**
Different functions exhibit different signal-to-noise ratios and landscape geometries. Documenting per-function hyperparameter choices demonstrates that the approach is data-driven rather than algorithmic.

**Why DATASHEET.md and MODEL_CARD.md are included:**
Following Gebru et al. (2021) and Mitchell et al. (2019) frameworks signals awareness of responsible ML documentation practices — increasingly expected in professional and academic contexts.

**Why the repository includes executable notebooks:**
The `notebooks/bbo_function_{1-8}.ipynb` files allow any reviewer to reproduce the GP-UCB analysis against the initial data. Reproducibility is a core professional standard, and the README's quick-start section makes this accessible.

---

### Link to Repository

[https://github.com/Dibyajyoti-Pradhan/Capstone-Project-Imperial-College-London](https://github.com/Dibyajyoti-Pradhan/Capstone-Project-Imperial-College-London)

The `Black-Box-Optimisation-Challenge/` directory contains the full documented project including initial data, query logs, notebooks, utility source code, DATASHEET.md and MODEL_CARD.md.
