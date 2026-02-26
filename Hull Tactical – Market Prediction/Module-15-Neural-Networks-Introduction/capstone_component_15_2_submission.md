# Required Capstone Component 15.2: Evaluating the Impact of Hyperparameters on Neural Networks

---

## 1. Hyperparameter Effects

### Key Hyperparameters Observed

| Hyperparameter | Effect on Convergence | Effect on Stability | Effect on Performance |
|----------------|----------------------|--------------------|-----------------------|
| **Learning Rate** | Too high → oscillation/divergence; too low → slow convergence | High values cause loss spikes | Critical for reaching good minima |
| **Network Depth** | Deeper networks converge slower | More layers → gradient vanishing risk | Better capacity for complex patterns |
| **Hidden Units** | More neurons → faster initial learning | Overfitting risk with limited data | Improved expressiveness |
| **Dropout Rate** | Slows convergence slightly | Regularises, prevents co-adaptation | Better generalisation |
| **Batch Size** | Large batches → stable but slow; small → noisy but fast | Small batches introduce gradient noise | Affects generalisation gap |

### Observations from Experiments

**Learning rate** had the most dramatic effect. With $\alpha = 0.1$, training on my 8D surrogate diverged within 50 epochs. Reducing to $\alpha = 0.001$ stabilised training but required 500+ epochs to converge. The sweet spot was $\alpha = 0.01$ with Adam optimiser.

**Network architecture** mattered significantly for high-dimensional functions. For F8 (8D), a single hidden layer with 16 neurons captured only linear trends. Adding a second layer (8 → 16 → 8 → 1) allowed the model to learn interaction effects between dimensions — visible in the improved validation loss.

**Dropout** at 0.2 prevented the MLP from memorising the 30 training points for F8, improving out-of-sample predictions by ~15% on held-out queries.

---

## 2. Discrete vs Continuous Hyperparameters

### Classification

| Type | Hyperparameters | Characteristics |
|------|-----------------|-----------------|
| **Continuous** | Learning rate, weight decay, dropout probability, momentum | Smooth response surface; amenable to gradient-free optimisation |
| **Discrete** | Number of layers, neurons per layer, batch size, activation function, optimiser choice | Combinatorial; requires enumeration or structured search |

### Tuning Method Implications

**Continuous hyperparameters** are well-suited to **Bayesian optimisation**:

$$\alpha^* = \arg\min_{\alpha \in [10^{-5}, 10^{-1}]} \mathcal{L}_{val}(\alpha)$$

The smooth relationship between learning rate and validation loss allows GP surrogates to model the response surface efficiently.

**Discrete hyperparameters** require different strategies:

- **Grid search** for small discrete spaces (e.g., activation ∈ {ReLU, tanh, sigmoid})
- **Random search** when combinations are large
- **Conditional Bayesian optimisation** for hierarchical choices (e.g., optimiser-specific parameters)

In practice, I used a **hybrid approach**: fix discrete architecture choices based on problem dimensionality, then tune continuous parameters via Bayesian optimisation.

---

## 3. Application to the BBO Capstone

### How Hyperparameter Understanding Influences Decisions

My understanding of hyperparameter effects directly shapes how I deploy neural networks as surrogates:

**Architecture Scaling with Dimensionality:**

| Function Dimension | Recommended Architecture | Rationale |
|--------------------|-------------------------|-----------|
| 2D–3D (F1–F3) | Single layer, 8–16 neurons | Low complexity, avoid overfitting |
| 4D–5D (F4–F6) | Two layers, 16–32 neurons | Capture mild non-linearities |
| 6D–8D (F7–F8) | Two layers, 32–64 neurons + dropout | Handle interactions, regularise |

**Learning Rate Scheduling:**

For surrogates trained on sparse BBO data, I use **learning rate warmup** — starting at $\alpha_0 = 0.0001$ and increasing to $\alpha_{max} = 0.01$ over the first 100 epochs. This prevents early gradient explosions when the network weights are poorly initialised.

### Applying BBO to Improve Neural Network Performance

The BBO framework **recursively applies to hyperparameter tuning**:

1. **Define search space:**
   - $\alpha \in [10^{-4}, 10^{-1}]$ (log-uniform)
   - dropout $\in [0, 0.5]$
   - hidden_units $\in \{8, 16, 32, 64\}$

2. **Objective function:** Validation MSE on held-out BBO queries

3. **Acquisition:** Use UCB to balance exploring new configurations vs exploiting known good settings

4. **Update:** Train surrogate on hyperparameter-performance pairs, propose next configuration

This creates a **nested optimisation loop**:

```
Outer loop: BBO on unknown functions
  └─ Inner loop: BBO on neural network hyperparameters
       └─ Training: Gradient descent on network weights
```

### Practical Implementation

For the capstone, I allocate **~20% of compute budget** to hyperparameter tuning via this approach. Rather than exhaustive grid search (which would require $5^4 = 625$ configurations), BBO-guided tuning identifies good hyperparameters in ~15–20 evaluations.

**Key insight:** The same exploration-exploitation principles governing query selection for unknown functions also govern hyperparameter search. Early iterations explore diverse architectures; later iterations exploit configurations with demonstrated low validation error.

---

## Summary

Hyperparameters are not implementation details — they are **strategic design decisions** that interact with data availability, function complexity, and computational budget. For the BBO capstone:

- **Match architecture to dimensionality** to balance expressiveness and overfitting risk
- **Tune continuous parameters via Bayesian optimisation** to efficiently navigate smooth response surfaces
- **Apply the BBO mindset recursively** — hyperparameter selection is itself a black-box optimisation problem

This meta-level understanding transforms hyperparameter tuning from trial-and-error into principled, uncertainty-aware search.

