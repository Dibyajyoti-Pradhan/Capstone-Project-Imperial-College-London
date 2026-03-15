# Required Capstone Component 16.1 — Week 5
## Refining Strategies for the Black-Box Optimisation Challenge

**Module:** 16 — Deep Learning
**Submitted:** 26/02/2026
**Cohort:** IMP-PCMLAI-25-08

---

## Part 1: Queries Submitted

| Function | Dimensions | Strategy | Query Submitted | Output |
|----------|------------|----------|-----------------|--------|
| F1 | 2D | Heavy exploration (κ=5.0) | 0.246150-0.552918 | TBC |
| F2 | 2D | Balanced GP-UCB (κ=1.0) | 0.580740-0.999512 | TBC |
| F3 | 3D | Balanced GP-UCB (κ=1.2) | 0.329261-0.236790-0.348523 | TBC |
| F4 | 4D | Balanced GP-UCB (κ=1.0) | 0.590813-0.462616-0.394784-0.203792 | TBC |
| F5 | 4D | Tight trust-region exploit (κ=0.2, r=0.04) | 0.934694-0.988611-0.984445-0.959862 | TBC |
| F6 | 5D | Balanced-explore (κ=1.2) | 0.723133-0.115027-0.680658-0.690641-0.014391 | TBC |
| F7 | 6D | GP gradient ascent (κ=3.5) | 0.061529-0.489971-0.245297-0.240728-0.404250-0.720651 | TBC |
| F8 | 8D | MLP gradient ascent (κ=0.2, r=0.10) | 0.052437-0.067920-0.033845-0.027417-0.413885-0.783172-0.502821-0.894560 | TBC |

---

## Part 2: Reflection on Strategy

### 1. Hierarchical Feature Learning and Optimisation Strategy

The concept of hierarchical feature learning fundamentally reshaped how I view the BBO search process. Rather than treating each query as an isolated experiment, I now conceptualise the optimisation in layers:

- **Layer 1 (Early weeks):** Broad exploration establishing coarse "edges" — identifying which regions of the input space show any promise
- **Layer 2 (Mid weeks):** Pattern recognition — understanding which input dimensions exert the strongest influence on outputs
- **Layer 3 (Current iteration):** Fine-grained refinement — exploiting learned structure while maintaining exploration guards

This mirrors how CNNs progress from detecting edges to shapes to semantic concepts. My surrogate model's accumulated knowledge now allows targeted queries that would have been blind guesses in Week 1.

---

### 2. Parallels with AlexNet and ImageNet Breakthroughs

AlexNet's success wasn't a single innovation but a convergence of architectural choices (ReLU, dropout), computational scale (GPU training) and data utilisation. My capstone progress follows a similar pattern:

| AlexNet Component       | BBO Strategy Parallel                                         |
|:------------------------|:--------------------------------------------------------------|
| Deeper architecture     | Evolving from random sampling to GP + SVM hybrid              |
| Dropout regularisation  | Balancing exploration to prevent "overfitting" to local optima |
| Large-scale data        | Accumulating 14+ observations to inform surrogate confidence  |
| GPU acceleration        | Computational efficiency through acquisition function optimisation |

Individual weekly submissions rarely produce dramatic jumps, but the compounding effect of incremental refinements — better surrogates, smarter acquisition, dimension-aware search — mirrors how deep learning advances accumulate into step-changes.

---

### 3. Trade-offs: Depth/Complexity vs Exploration/Exploitation

The neural network trade-off between model capacity and training efficiency directly parallels the exploration-exploitation dilemma:

**Exploration (shallow/broad):**
- Covers more input space
- Avoids premature convergence
- Expensive in query budget

**Exploitation (deep/focused):**
- Refines known promising regions efficiently
- Risks missing global optima
- Can overfit to noisy observations

For high-performing functions (F5, F8), I shifted toward exploitation with small perturbations around best-known points. For functions with flat or inconsistent outputs, I maintained broader exploration — analogous to choosing a simpler model when data is insufficient to support complexity.

The SVM-based classification approach embodies this trade-off: it identifies "good" vs "bad" regions (broad structure) before Bayesian optimisation refines within promising zones (localised depth).

---

### 4. Neural Network Building Blocks and Learning Intuition

| Building Block  | BBO Interpretation                                                      |
|:----------------|:------------------------------------------------------------------------|
| Inputs          | Query coordinates                                                       |
| Activations     | Surrogate predictions and uncertainty estimates                         |
| Loss            | Gap between predicted and observed function values                      |
| Gradients       | Directional signals from acquisition function — where to query next     |
| Weight updates  | Surrogate retraining after each new observation                         |

The **gradient** concept proved most transformative. Although explicit gradients are unavailable in the black-box setting, the acquisition function's gradient guides query placement toward regions of maximum expected improvement. Each observation acts as a "weight update" that reshapes the surrogate's belief landscape — shifting the mindset from "searching for peaks" to "iteratively reducing prediction error".

---

### 5. Framework Mindset: Rapid Prototyping vs Production Design

My approach aligns firmly with **rapid prototyping (PyTorch-style)** rather than production-ready design:

- **Flexibility:** Strategy adapts weekly based on new observations and module concepts
- **Experimentation:** Testing GP, SVM classification, neural surrogates — no fixed pipeline
- **Interpretability:** Prioritising understanding of function behaviour over pure automation
- **Small-data regime:** 14 observations doesn't justify rigid infrastructure

A TensorFlow-style production approach would only become appropriate once function landscapes are well-understood and strategy stabilises. Currently, the value lies in learning speed, not deployment scalability.

---

### 6. Real-World Applications and Benchmarking Success

Giovanni Liotta's discussion of sports analytics highlighted that real-world success isn't measured by theoretical optimality but by consistent, decision-relevant improvement. This perspective transformed how I benchmark capstone progress:

**Beyond raw function values:**
- Is uncertainty decreasing in promising regions?
- Are surrogate predictions becoming more reliable?
- Does the strategy adapt appropriately to different function characteristics?

**Process metrics alongside outcomes:**
- **Query efficiency:** information gained per evaluation
- **Robustness:** avoiding catastrophic failures in unexplored regions
- **Adaptability:** learning from both successes and poor outcomes

Just as deployed ML systems are judged by reliability under real-world constraints, a BBO strategy should demonstrate systematic learning rather than lucky peaks. A lower maximum achieved through principled search may indicate better methodology than a high outlier from random chance.
