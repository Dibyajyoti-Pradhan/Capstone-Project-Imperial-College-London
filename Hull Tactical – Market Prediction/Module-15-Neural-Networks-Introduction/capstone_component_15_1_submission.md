# Required Capstone Component 15.1: Refining BBO Strategies with Neural Networks

## Part 2: Reflection on Strategy

---

### 1. Which inputs acted like support vectors?

Certain inputs exhibited **support-vector-like behaviour** — points where small perturbations caused disproportionately large output changes. In Function 5, coordinates near $(0.95, 0.08, 0.82, 0.95)$ produced outputs exceeding 1600, while nearby points dropped sharply. This suggests proximity to a steep ridge or decision boundary.

Function 8 showed similar patterns: dimensions $X_1$ and $X_3$ appeared to define a narrow high-performance corridor. Points straddling this boundary acted as natural support vectors, marking the transition between promising and unpromising regions.

**Guidance for next queries:** Rather than sampling randomly, I now probe $\pm 0.05$ perturbations around these boundary points to map the curvature and confirm whether they represent local ridges or global optima.

---

### 2. Neural network surrogate and gradient exploration

I trained a **shallow MLP (8 → 16 → 8 → 1)** with ReLU activations as a surrogate for Function 8. Using backpropagation, I computed:

$$\nabla_x f_{NN}(x) = \frac{\partial \hat{y}}{\partial x}$$

The gradient vector revealed that $X_1$ and $X_3$ had the **steepest partial derivatives** — consistent with my earlier correlation analysis. By performing gradient ascent from the current best point:

$$x_{new} = x_{best} + \alpha \cdot \nabla_x f_{NN}(x_{best})$$

with step size $\alpha = 0.03$, I generated candidate queries that exploit the surrogate's learned surface while remaining within the trust region.

**Why neural networks over GPs here:** With 8 dimensions and 30+ observations, GP covariance matrices become computationally expensive ($O(n^3)$). The MLP scales linearly and provides smooth, differentiable gradients for optimisation.

---

### 3. Framing BBO as classification

If outputs are thresholded into **"good" (top 25%)** versus **"bad" (bottom 75%)**, classification models can learn decision boundaries:

| Model | Boundary Type | Strengths | Weaknesses |
|-------|---------------|-----------|------------|
| Logistic Regression | Linear hyperplane | Interpretable, fast | Cannot capture curved boundaries |
| SVM (RBF kernel) | Non-linear, margin-based | Works well with small data | No native probability estimates |
| Neural Network | Arbitrary non-linear | Highly flexible, provides gradients | Requires more data, prone to overfit |

**Trade-off:** Aggressive classification risks **premature exploitation** — labelling unexplored regions as "bad" before sufficient sampling. I mitigate this by using soft probabilities near the boundary (where $P(\text{good}) \approx 0.5$) as exploration targets rather than hard class labels.

---

### 4. Model choice: interpretability vs flexibility

For **low-dimensional functions (F1–F3)**, Gaussian Processes remain optimal — they provide uncertainty estimates critical for acquisition functions and avoid overfitting with sparse data.

For **high-dimensional functions (F7–F8)**, neural networks became more appropriate. The MLP captured interaction effects between dimensions that additive GP kernels missed. I balanced interpretability by:

- Analysing gradient magnitudes to identify influential dimensions
- Using ensemble variance (5 MLPs with different initialisations) as a proxy for uncertainty
- Keeping architecture simple (2 hidden layers) to limit memorisation

---

### 5. Steepest gradients and variable influence

Backpropagation through the MLP surrogate revealed:

| Function | Most Influential Dimensions | Gradient Magnitude |
|----------|----------------------------|-------------------|
| F5 (4D) | $X_3$, $X_4$ | High (steep ridge) |
| F7 (6D) | $X_2$, $X_5$ | Moderate |
| F8 (8D) | $X_1$, $X_3$ | Very high |

For F8, I effectively reduced the search from 8D to a **pseudo-2D problem** by fixing low-influence dimensions at their current best values and varying only $X_1$ and $X_3$.

---

### 6. Decision boundary approximation via backpropagation

When trained as a classifier, the neural network approximated non-linear boundaries between good/bad regions more effectively than logistic regression. Backpropagation enabled **saliency analysis** — computing $|\partial P(\text{good}) / \partial x_i|$ to visualise which inputs most strongly shifted classification.

For Function 5, this revealed a roughly **elliptical** high-performance region in the $(X_3, X_4)$ plane — insight that linear models completely missed.

---

### 7. Neural networks vs simpler models

| Aspect | Linear/Logistic Regression | Neural Network |
|--------|---------------------------|----------------|
| Non-linear patterns | Poor | Excellent |
| Small data performance | Good | Risk of overfitting |
| Gradient access | Analytic, simple | Via backpropagation |
| Tuning complexity | Minimal | Learning rate, architecture, regularisation |

**Was added flexibility worth it?** For F1–F4, **no** — simpler models sufficed. For F7–F8, **yes** — the MLP captured curved response surfaces and enabled gradient-based query generation that GP-UCB could not provide efficiently at scale.

---

### Summary

This iteration marked a shift from **pure Bayesian optimisation** to **hybrid surrogate-gradient methods**. Neural networks served as differentiable approximators in high dimensions, while GPs remained preferable for low-dimensional, uncertainty-aware exploration. The key insight: match model complexity to data availability and dimensionality rather than applying one method uniformly.

