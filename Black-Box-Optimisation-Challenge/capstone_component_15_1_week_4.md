# Required Capstone Component 15.1 — Week 4
## Refining Strategies Using Neural Network-Based Methods

**Module:** 15 — Neural Networks
**Submitted:** 26/02/2026
**Cohort:** IMP-PCMLAI-25-08

---

## Part 1: Queries Submitted

| Function | Dimensions | Strategy | Query Submitted | Output |
|----------|------------|----------|-----------------|--------|
| F1 | 2D | Heavy exploration (κ=5.0) | 0.287557-0.328117 | TBC |
| F2 | 2D | Balanced GP-UCB (κ=1.2) | 0.633773-0.980766 | TBC |
| F3 | 3D | Balanced GP-UCB (κ=1.5) | 0.232745-0.174501-0.372346 | TBC |
| F4 | 4D | Balanced GP-UCB (κ=1.2) | 0.578712-0.482733-0.457525-0.220053 | TBC |
| F5 | 4D | Tight trust-region exploit (κ=0.3, r=0.05) | 0.982291-0.995943-0.990066-0.997766 | TBC |
| F6 | 5D | Balanced-explore (κ=1.5) | 0.776065-0.153169-0.757715-0.651481-0.001465 | TBC |
| F7 | 6D | GP gradient ascent (X2/X5 dominant) | 0.062029-0.489767-0.244567-0.248056-0.398445-0.717127 | TBC |
| F8 | 8D | MLP gradient ascent (X1/X3 dominant, α=0.03) | 0.062507-0.062925-0.015696-0.050786-0.392538-0.818350-0.473184-0.892827 | TBC |

---

## Part 2: Reflection

### 1. Which inputs acted like support vectors?

Certain inputs exhibited support-vector-like behaviour — points where small perturbations caused disproportionately large output changes. In **Function 5**, coordinates near **(0.999, 0.999, 0.999, 0.999)** produced outputs exceeding 1600, while nearby points dropped sharply. This confirms a steep ridge concentrated at the boundary of the search space.

**Function 8** showed similar patterns: dimensions X1 and X3 appeared to define a narrow high-performance corridor. Points straddling this boundary acted as natural support vectors, marking the transition between promising and unpromising regions.

**Guidance for next queries:** Rather than sampling randomly, I probe ±0.05 perturbations around these boundary points to map the curvature and confirm whether they represent local ridges or global optima.

---

### 2. Neural network surrogate and gradient exploration

I trained a shallow MLP (8→16→8→1) with ReLU activations as a surrogate for Function 8. Using backpropagation, I computed the gradient of the predicted output with respect to inputs.

The gradient vector revealed that **X1 and X3 had the steepest partial derivatives** — consistent with earlier correlation analysis. By performing gradient ascent from the current best point with step size α=0.03, I generated candidate queries that exploit the surrogate's learned surface while remaining within the trust region.

**Why neural networks over GPs here:** With 8 dimensions and 30+ observations, GP covariance matrices become computationally expensive O(n³). The MLP scales linearly and provides smooth, differentiable gradients for optimisation.

---

### 3. Framing BBO as classification

If outputs are thresholded into "good" (top 25%) vs "bad" (bottom 75%), classification models can learn decision boundaries:

| Model | Boundary Type | Strengths | Weaknesses |
|-------|--------------|-----------|------------|
| Logistic Regression | Linear hyperplane | Interpretable, fast | Cannot capture curved boundaries |
| SVM (RBF kernel) | Non-linear, margin-based | Works well with small data | No native probability estimates |
| Neural Network | Arbitrary non-linear | Highly flexible, provides gradients | Requires more data, prone to overfit |

**Trade-off:** Aggressive classification risks premature exploitation — labelling unexplored regions as "bad" before sufficient sampling. I mitigate this by using soft probabilities near the boundary (where P(good) ≈ 0.5) as exploration targets rather than hard class labels.

---

### 4. Model choice: interpretability vs flexibility

For **low-dimensional functions (F1–F3)**, Gaussian Processes remain optimal — they provide uncertainty estimates critical for acquisition functions and avoid overfitting with sparse data.

For **high-dimensional functions (F7–F8)**, neural networks became more appropriate. The MLP captured interaction effects between dimensions that additive GP kernels missed. I balanced interpretability by:
- Analysing gradient magnitudes to identify influential dimensions
- Using ensemble variance (5 MLPs with different initialisations) as a proxy for uncertainty
- Keeping architecture simple (2 hidden layers) to limit memorisation

---

### 5. Steepest gradients and variable influence

Backpropagation through the MLP surrogate revealed the following dimension importance rankings:

| Function | Most Influential Dimensions | Gradient Magnitude  |
|:---------|:---------------------------|:--------------------|
| F5 (4D)  | X3, X4                     | High (steep ridge)  |
| F7 (6D)  | X2, X5                     | Moderate            |
| F8 (8D)  | X1, X3                     | Very high           |

For F8, I effectively reduced the search from 8D to a **pseudo-2D problem** by fixing low-influence dimensions at their current best values and varying only X1 and X3.

---

### 6. Decision boundary approximation via backpropagation

When trained as a classifier, the neural network approximated non-linear boundaries between good/bad regions more effectively than logistic regression. Backpropagation enabled saliency analysis — computing the partial derivative of P(good) with respect to each input to visualise which inputs most strongly shifted classification.

For Function 5, this revealed a roughly **elliptical high-performance region in the (X3, X4) plane** — insight that linear models completely missed.

---

### 7. Neural networks vs simpler models

| Aspect | Linear/Logistic Regression | Neural Network |
|--------|---------------------------|----------------|
| Non-linear patterns | Poor | Excellent |
| Small data performance | Good | Risk of overfitting |
| Gradient access | Analytic, simple | Via backpropagation |
| Tuning complexity | Minimal | Architecture, lr, regularisation |

**Was added flexibility worth it?** For F1–F4, no — simpler models sufficed. For F7–F8, yes — the MLP captured curved response surfaces and enabled gradient-based query generation that GP-UCB could not provide efficiently at scale.

---

### Summary

This iteration marked a shift from pure Bayesian optimisation to **hybrid surrogate-gradient methods**. Neural networks served as differentiable approximators in high dimensions, while GPs remained preferable for low-dimensional, uncertainty-aware exploration. The key insight: match model complexity to data availability and dimensionality rather than applying one method uniformly.
