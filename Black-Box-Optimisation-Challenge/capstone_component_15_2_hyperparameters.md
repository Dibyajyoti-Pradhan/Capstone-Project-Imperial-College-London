# Required Capstone Component 15.2 — Evaluating the Impact of Hyperparameters on Neural Networks

**Module:** 15 — Neural Networks
**Submitted:** 26/02/2026
**Cohort:** IMP-PCMLAI-25-08

---

## 1. Hyperparameter Effects

### Key Hyperparameters Observed

| Hyperparameter  | Effect on Convergence            | Effect on Stability         | Effect on Performance       |
|:----------------|:---------------------------------|:----------------------------|:----------------------------|
| Learning Rate   | Too high → oscillation; too low → slow | High values cause loss spikes | Critical for good minima |
| Network Depth   | Deeper networks converge slower  | Gradient vanishing risk     | Better capacity             |
| Hidden Units    | More neurons → faster initial learning | Overfitting risk        | Improved expressiveness     |
| Dropout Rate    | Slows convergence slightly       | Regularises network         | Better generalisation       |
| Batch Size      | Large → stable but slow          | Small batches add noise     | Affects generalisation gap  |

### Observations from Experiments

**Learning rate** had the most dramatic effect. With α=0.1, training on the 8D surrogate diverged within 50 epochs. Reducing to α=0.001 stabilised training but required 500+ epochs. The sweet spot was α=0.01 with Adam optimiser.

**Network architecture** mattered significantly for high-dimensional functions. For F8 (8D), a single hidden layer with 16 neurons captured only linear trends. Adding a second layer (8→16→8→1) allowed the model to learn interaction effects between dimensions.

**Dropout at 0.2** prevented the MLP from memorising the 30 training points for F8, improving out-of-sample predictions by ~15%.

---

## 2. Discrete vs Continuous Hyperparameters

| Type       | Hyperparameters                                          | Tuning Method                               |
|:-----------|:---------------------------------------------------------|:--------------------------------------------|
| Continuous | Learning rate, weight decay, dropout rate, momentum      | Bayesian optimisation, gradient-free search |
| Discrete   | Number of layers, neurons per layer, batch size, activation function | Grid search, random search, enumeration |

**Continuous hyperparameters** are well-suited to Bayesian optimisation because the smooth relationship between parameter values and validation loss allows GP surrogates to model the response surface efficiently.

**Discrete hyperparameters** require structured search strategies. In practice, I used a hybrid approach: fix discrete architecture choices based on problem dimensionality, then tune continuous parameters via Bayesian optimisation.

---

## 3. Application to the BBO Capstone

### Architecture Scaling with Dimensionality

| Function Dimension  | Recommended Architecture              | Rationale                                |
|:--------------------|:--------------------------------------|:-----------------------------------------|
| 2D–3D (F1–F3)       | Single layer, 8–16 neurons            | Low complexity, avoid overfitting        |
| 4D–5D (F4–F6)       | Two layers, 16–32 neurons             | Capture mild non-linearities             |
| 6D–8D (F7–F8)       | Two layers, 32–64 neurons + dropout   | Handle interactions, regularise          |

### Applying BBO to Improve Neural Network Performance

The BBO framework applies recursively to hyperparameter tuning:

1. **Define search space:** learning rate (log-uniform [10⁻⁴, 10⁻¹]), dropout rate [0, 0.5], hidden units [8, 64]
2. **Objective function:** validation MSE on held-out BBO queries
3. **Acquisition:** UCB to balance exploration vs exploitation across the hyperparameter space
4. **Update:** train GP surrogate on hyperparameter–performance pairs

This creates a nested optimisation loop where the same exploration-exploitation principles governing query selection also govern hyperparameter search.

### Practical Implementation

For the capstone, I allocate ~20% of compute budget to hyperparameter tuning via BBO. Rather than exhaustive grid search (625+ configurations), BBO-guided tuning identifies good hyperparameters in ~15–20 evaluations — directly applying the principles from Module 12 to the model design problem.

---

## Summary

Hyperparameters are strategic design decisions that interact with data availability, function complexity and computational budget. For the BBO capstone:

- Match architecture to dimensionality to balance expressiveness and overfitting risk
- Tune continuous parameters via Bayesian optimisation
- Apply the BBO mindset recursively — hyperparameter selection is itself a black-box optimisation problem
