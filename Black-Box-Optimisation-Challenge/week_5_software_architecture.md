# Required Capstone Component 16.2: Determining a Software Architecture

## Repository Structure

### Current Organisation

My repository has evolved alongside the BBO capstone project with a clear separation of concerns:

```
Black-Box-Optimisation-Challenge/
├── README.md                           # Project overview and methodology
├── week_1_exploration_strategy.md      # Initial exploration approach
├── week_2_output_guided_search.md      # Output-guided refinement
├── week_3_svm_strategy.md              # SVM-based region classification
├── week_4_neural_network_surrogates.md # Neural network surrogate models
├── week_5_neural_network_concepts.md   # NN concepts applied to BBO
├── week_5_software_architecture.md     # This document
└── hyperparameter_tuning.md            # Hyperparameter impact analysis
```

Each weekly markdown file documents the strategic evolution, capturing not just *what* was submitted but *why* those decisions were made. This chronological structure enables traceability — anyone reviewing the repository can follow the optimisation journey from broad exploration to targeted exploitation.

### Planned Improvements

| Improvement | Rationale |
|-------------|-----------|
| Add `data/` directory | Separate raw inputs/outputs from analysis |
| Create `notebooks/` folder | Isolate exploratory Jupyter notebooks from documentation |
| Include `src/` module | Reusable functions for surrogate fitting, acquisition optimisation |
| Add `requirements.txt` | Enable reproducibility with pinned dependencies |
| Introduce `results/` folder | Store visualisations, metrics, and submission logs |

These changes will transform the repository from a documentation archive into a fully reproducible optimisation pipeline.

---

## Coding Libraries and Packages

### Central Libraries

| Library | Purpose | Justification |
|---------|---------|---------------|
| **NumPy** | Array operations, candidate generation | Foundation for numerical computation; efficient vectorised operations |
| **scikit-learn** | Gaussian Process surrogates, SVM classification | Robust implementations with uncertainty quantification; ideal for small-data regimes |
| **SciPy** | Acquisition function optimisation (L-BFGS-B) | Reliable constrained optimisation; integrates seamlessly with NumPy |
| **Matplotlib** | Visualisation of response surfaces | Quick iteration on 2D projections and uncertainty plots |
| **Pandas** | Data management and logging | Structured tracking of queries and results across iterations |

### Framework Choice: Why Not PyTorch/TensorFlow?

While Module 16 introduced PyTorch and TensorFlow, I deliberately chose **not** to use deep learning frameworks as primary tools for this BBO challenge. The reasoning:

1. **Data scarcity:** With ~14 observations per function, neural networks risk severe overfitting
2. **Uncertainty quantification:** GPs provide natural uncertainty estimates; NNs require additional machinery (ensembles, dropout)
3. **Computational efficiency:** scikit-learn's GP fits in milliseconds; PyTorch training loops add unnecessary overhead
4. **Interpretability:** Kernel hyperparameters (lengthscales, noise) directly inform search strategy

**Trade-off acknowledged:** This choice sacrifices the expressiveness of deep surrogates for reliability and transparency. For higher-dimensional functions (F6-F8) with more data, PyTorch-based neural surrogates could become advantageous — a potential extension if the query budget expands.

### Rapid Prototyping vs Production Design

My approach aligns with **rapid prototyping** (PyTorch philosophy) rather than structured production (TensorFlow philosophy):

- Strategy adapts weekly based on new observations
- No rigid pipeline — experimentation drives decisions
- Interpretability prioritised over automation
- Small data regime doesn't justify infrastructure investment

---

## Documentation

### Current State

The README currently describes:
- Project goal: maximise 8 unknown functions with limited queries
- Input/output format: coordinate vectors → scalar function values
- Strategic evolution: exploration → pattern recognition → exploitation
- Weekly summaries linking observations to decisions

### Planned Updates

To align documentation with the latest strategy:

1. **Add "Quick Start" section:** Commands to reproduce query generation
2. **Expand methodology:** Document GP kernel choices, acquisition function parameters, SVM classification thresholds
3. **Include visualisations:** Response surface plots showing surrogate predictions vs actual observations
4. **Create "Lessons Learned" section:**
   - What worked: boundary exploitation for F5/F8, SVM region classification
   - What failed: aggressive gradient ascent without exploration guards
5. **Add reproducibility instructions:** Random seeds, dependency versions, exact notebook execution order

### Documentation Philosophy

The goal is to present the repository not as a code dump, but as a **narrative of iterative learning**. Each document answers:
- *What was the hypothesis?*
- *What was observed?*
- *How did this inform the next decision?*

This mirrors how employers evaluate technical work — clarity of reasoning matters as much as results.

---

## Reflection

This exercise highlighted that a well-structured repository is itself a form of documentation. The separation between raw data, analysis notebooks, and strategic reflections makes the optimisation process transparent and reproducible. Moving forward, I will commit these structural improvements directly to GitHub, ensuring the repository communicates both the *code* and the *thinking* behind the BBO capstone project.
