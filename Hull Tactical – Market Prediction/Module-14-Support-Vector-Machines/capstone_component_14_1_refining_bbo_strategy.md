# Required Capstone Component 14.1 – Refining Your Strategies for the Black-Box Optimisation Challenge

## Part 2: Reflection on Strategy

---

## 1. How has your query strategy changed from earlier rounds?

### Evolution Across Three Weeks

My strategy has undergone a clear three-phase transformation:

| Phase | Week | Approach | Key Learning |
|-------|------|----------|--------------|
| **Blind Exploration** | Week 1 | Maximum spatial coverage | Build data foundation without bias |
| **Output-Guided Search** | Week 2 | Function-specific strategies based on observed values | Strong signals warrant local attention |
| **Model-Informed Decisions** | Week 3 | Surrogate models drive query selection | Trust the GP where data supports it |

### Concrete Changes

**From heuristics to models:** Early rounds used geometric heuristics (maximum distance from existing points). Now, Gaussian Process surrogates provide actual predictive capability, and acquisition functions give principled selection criteria.

**From uniform to differentiated:** Initially treated all eight functions identically. Now each function has a tailored strategy based on its observed behaviour, dimensionality, and model confidence.

**From global to local focus:** Functions 5 and 8 showed strong positive values early. Rather than continuing broad exploration, I shifted to local perturbation — small controlled steps around the best-known points to refine the optimum.

**From fixed to adaptive parameters:** Kappa values in UCB now vary by function and round. High-performing functions use lower kappa (exploit), while stagnant functions receive higher kappa (explore more aggressively).

---

## 2. How do you balance exploration against exploitation?

### Current Balance: 50/50 with Function-Specific Variation

As the competition progresses toward the midpoint, the overall balance has shifted from 70/30 exploration-heavy to approximately 50/50. However, this masks significant variation:

| Function | Current Balance | Rationale |
|----------|-----------------|-----------|
| F1 (2D) | 70% Exploration | Still searching for the main signal |
| F2 (3D) | 60% Exploration | Moderate progress, continue mapping |
| F3 (3D) | 60% Exploration | Escaped negative region, cautiously optimistic |
| F4 (4D) | 50% Balanced | Dynamic system showing structure |
| F5 (4D) | 30% Exploration | Strong optimum found, refining |
| F6 (5D) | 65% Exploration | High-D with weak signal |
| F7 (6D) | 70% Exploration | Curse of dimensionality persists |
| F8 (8D) | 40% Exploration | Good region identified, careful exploitation |

### Trade-off Management

**Exploration costs:** Each exploratory query could land in a low-value region, wasting one of the limited evaluation budget.

**Exploitation risks:** Premature focus on a local optimum might miss the global maximum entirely — particularly dangerous with only 20-30 data points per function.

**My resolution:** Use **trust region exploitation** for promising functions. Rather than letting the GP extrapolate freely (which drifts toward boundaries), I constrain exploitation queries to within a trust radius of the current best. This provides local refinement while limiting downside risk.

---

## 3. How would SVMs change your approach?

### SVMs as Region Classifiers

Support Vector Machines offer a fundamentally different perspective on the optimisation problem. Instead of modelling the continuous output surface, SVMs could classify input regions as **promising** or **unpromising**.

### Potential Applications

**1. Binary Region Classification**

Threshold the observed outputs (e.g., above/below the 75th percentile) and train an SVM to identify the decision boundary. New queries would focus on:
- Points predicted as "promising"
- Points near the decision boundary (high uncertainty)

**2. Kernel-Based Pattern Detection**

The kernel trick allows SVMs to find non-linear boundaries in the original input space. For Function 5, where high outputs concentrate in a corner of the 4D hypercube, an RBF kernel might identify this region more efficiently than a GP attempting to model the full response surface.

**3. Outlier Detection via One-Class SVM**

Train a one-class SVM on the high-output observations to define a "good region" boundary. Query points that fall just outside this boundary — exploring the frontier of promising space.

### Practical Integration

| GP Surrogate | SVM Classifier |
|--------------|----------------|
| Models continuous output values | Classifies regions as good/bad |
| Provides uncertainty estimates | Provides hard decision boundary |
| Struggles in high dimensions | Scales better with dimensionality |
| Sensitive to kernel length-scale | Controlled by C and gamma parameters |

**Hybrid approach:** Use SVM to pre-filter candidate queries (eliminate clearly unpromising regions), then apply GP-based acquisition function to select among the remaining candidates. This reduces computational cost and focuses GP modelling where it matters.

### Limitations of SVMs for BBO

- **No uncertainty quantification:** SVMs provide class predictions, not probabilities (without Platt scaling)
- **Binary thinking:** Loses the nuance of "how good" versus "good/bad"
- **Hyperparameter sensitivity:** C and gamma require tuning, adding another optimisation layer
- **Class imbalance:** Few "excellent" points early on makes training difficult

---

## 4. What limitations of your current model become apparent as data grows?

### GP Scalability Issues

**Computational complexity:** Gaussian Processes scale as O(n³) for training due to matrix inversion. With 30+ points per function now, fitting time is noticeable. By round 12 with 100+ points, this becomes a bottleneck.

**Memory requirements:** The covariance matrix grows as O(n²), limiting practical dataset sizes.

### Model Fidelity Concerns

**Length-scale estimation:** With more data, the GP might learn length-scales that are too short, overfitting to noise rather than capturing the underlying trend. This manifests as wiggly mean predictions that interpolate through every observation.

**Heteroscedastic noise:** The GP assumes constant noise variance across the domain. Financial and optimisation problems often have varying noise levels — quiet regions and volatile regions. As data grows, this assumption becomes increasingly problematic.

**Kernel choice matters more:** Early on, the difference between RBF and Matern kernels is negligible. With more data, the smoothness assumptions embedded in the kernel become significant. A misspecified kernel can systematically mis-model the function.

### High-Dimensional Challenges Persist

For Functions 7 (6D) and 8 (8D), even with 30 observations, data density remains desperately low. The curse of dimensionality means useful local structure cannot be learned — the GP effectively reverts to a global mean estimate with high uncertainty everywhere.

### Potential Mitigations

- **Sparse GPs:** Use inducing points to reduce complexity to O(nm²) where m << n
- **ARD kernels:** Automatic Relevance Determination to identify and potentially ignore irrelevant dimensions
- **Local models:** Fit separate GPs in different trust regions rather than one global model
- **Switch to Random Forest:** Tree-based surrogates scale better and handle noise naturally

---

## 5. How does this black-box setup prepare you to think like a data scientist?

### Core Data Science Competencies Developed

**1. Working Under Uncertainty**

Real-world ML problems rarely come with ground truth or clear feedback. This competition forces decisions with incomplete information — exactly what practitioners face when deploying models to production with delayed or noisy feedback signals.

**2. Resource-Constrained Optimisation**

The limited query budget mirrors real constraints: computational cost, API rate limits, experimental time, or financial budget for data acquisition. Learning to extract maximum value from each observation is a transferable skill.

**3. Model Selection and Criticism**

Choosing between GPs, Random Forests, and now SVMs requires understanding each model's assumptions, strengths, and failure modes. The BBO challenge makes these trade-offs concrete rather than theoretical.

**4. Adaptive Strategy**

Static approaches fail. The competition rewards practitioners who monitor results, identify what is working, and adjust accordingly — the core feedback loop of applied data science.

**5. Dimensionality Awareness**

The stark contrast between 2D functions (where visualisation guides intuition) and 8D functions (where only mathematics applies) teaches respect for the curse of dimensionality. This awareness prevents overconfidence when scaling models to production feature spaces.

### Connection to Hull Tactical

The BBO challenge directly parallels the capstone project:

| BBO Challenge | Hull Tactical Market Prediction |
|---------------|--------------------------------|
| Unknown function structure | Unknown market dynamics |
| Expensive evaluations (limited queries) | Expensive model training (forward-chaining CV) |
| Noisy outputs | Noisy financial returns |
| Multiple local optima | Regime-dependent optimal strategies |
| Model uncertainty | Prediction confidence intervals |

Both require balancing exploration (testing new hypotheses) against exploitation (trading on known patterns), managing limited resources, and adapting strategies as evidence accumulates.

---

## Summary

Week 3 marks the transition from data gathering to model-driven optimisation. SVMs offer a complementary perspective — classifying regions rather than modelling outputs — that could improve efficiency in high dimensions. However, the core challenges remain: scaling surrogates as data grows, managing the explore-exploit balance with limited budget, and recognising when model assumptions break down. These are precisely the skills that distinguish effective data scientists from those who simply apply algorithms without understanding their limitations.

