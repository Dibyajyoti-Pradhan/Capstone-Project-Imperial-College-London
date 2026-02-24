# Required Capstone Component 12.1 – Applying Machine Learning Techniques to Black-Box Functions

## Part 2: Reflection on Query Strategy

---

## 1. What was the main principle or heuristic you used to decide on each query point?

My primary strategy was **structured exploration with dimensionality-aware sampling**, recognising that early-stage BBO with limited data demands broad coverage over premature exploitation.

### The Core Approach

With only 10 initial data points per function and no prior output feedback, I treated this as a pure information-gathering phase. The guiding principle was:

> *Maximise spatial coverage while ensuring samples are informative across all dimensions.*

### Function-Specific Strategies

| Dimension | Strategy | Rationale |
|-----------|----------|-----------|
| **2D-3D** (Functions 1-3) | Centroid + boundary sampling | Low-dimensional spaces allow meaningful coverage with few points |
| **4D-5D** (Functions 4-5) | Latin Hypercube-inspired spacing | Ensures each dimension is sampled at distinct levels |
| **6D-8D** (Functions 6-8) | Maximum distance from existing points | Sparse data in high dimensions requires aggressive exploration |

### Why Not Exploit Yet?

Several factors argued against exploitation in this first round:

1. **No output data available** — Without knowing which regions produced high values, exploitation targets do not exist
2. **Unknown function structure** — Functions could be unimodal, multimodal, smooth, or noisy
3. **Single query per function** — With only one shot per round, exploration builds a foundation for future model fitting

I calculated the point with maximum minimum distance from all existing observations and domain corners, ensuring the new sample filled the largest gap in the current coverage.

---

## 2. Which function(s) were most challenging to query, and why?

### Most Challenging: Functions 7 (6D) and 8 (8D)

The high-dimensional functions presented severe challenges rooted in the **curse of dimensionality**:

**Exponential Volume Growth**
- In 8D, the unit hypercube has a volume where 10 random points are statistically ~0.3 units apart on average
- This means neighbouring points provide almost no information about each other
- Local structure cannot be inferred from sparse observations

**Surrogate Model Instability**
- Gaussian Processes struggle when data density is low relative to dimensionality
- The covariance matrix becomes poorly conditioned
- Length-scale estimation is unreliable with insufficient samples

**Visual Intuition Fails**
- For Functions 1-3, I could plot the data and visually identify gaps
- Beyond 3D, all reasoning must be mathematical rather than intuitive

### Moderately Challenging: Function 4 (4D - Dynamic System)

The description suggested "rapidly changing output" with potentially multiple local maxima. This created uncertainty about whether:
- The function is stationary (same optima over time)
- Noise dominates the signal
- Historical observations remain relevant

### What Would Have Helped

| Information Needed | Why It Matters |
|-------------------|----------------|
| **Output values from initial samples** | Would enable surrogate model fitting |
| **Noise level estimates** | Determines whether small differences are meaningful |
| **Smoothness/Lipschitz constant** | Guides length-scale choices for GPs |
| **Feature importance hints** | Allows dimensionality reduction in 6D-8D problems |
| **Bounds tighter than [0,1]** | Reduces effective search space |

---

## 3. How do you plan to adjust your strategy in future rounds?

### Phased Transition from Exploration to Exploitation

My strategy will evolve as data accumulates across the 12 remaining submission rounds:

**Rounds 2-4: Model Building Phase**
- Fit Gaussian Process surrogates per function once outputs are available
- Use **Upper Confidence Bound (UCB)** acquisition with high exploration parameter (kappa ~ 3-5)
- Identify which functions are smooth vs. noisy vs. multimodal

**Rounds 5-8: Balanced Search Phase**
- Reduce exploration parameter gradually (kappa ~ 2)
- Switch to **Expected Improvement (EI)** for functions showing clear optima
- Implement separate strategies per function based on learned characteristics

**Rounds 9-12: Refinement Phase**
- Heavy exploitation near identified optima
- Reserve small exploration budget for functions that may have undiscovered peaks
- Local search around best-observed points

### Dimension-Specific Adaptations

**Low-Dimensional Functions (2D-4D):**
- Standard Bayesian Optimisation should work well
- May experiment with different kernels (Matern vs RBF) based on observed smoothness

**High-Dimensional Functions (6D-8D):**
- Apply **Automatic Relevance Determination (ARD)** to identify influential dimensions
- Consider dimensionality reduction if some inputs appear irrelevant
- Use **TuRBO (Trust Region Bayesian Optimisation)** to focus on local regions
- Generate candidates via quasi-random sequences (Sobol) rather than uniform random

### Performance Monitoring

After each round, I will:
1. Compare predicted vs. actual outputs to assess surrogate accuracy
2. Track cumulative regret (gap between best observed and true maximum if discoverable)
3. Adjust acquisition function parameters based on convergence speed

### Contingency Plans

If a function shows no improvement over several rounds:
- Increase exploration dramatically (possible local trap)
- Try alternative surrogate (Random Forest instead of GP)
- Resample previously high-performing regions (possible noise masking signal)

---

## Summary

This first submission prioritised **systematic exploration** to build a foundation for model-based optimisation. The high-dimensional functions (6D-8D) remain the primary challenge due to data sparsity. Future rounds will progressively shift toward exploitation as surrogate models stabilise, with function-specific adaptations based on observed characteristics.

The key insight from this exercise mirrors the Hull Tactical market prediction challenge: when facing an unknown system with expensive evaluations, initial broad exploration prevents premature convergence to local optima and builds the data foundation necessary for intelligent, model-guided decisions in later stages.
