# Required Capstone Component 17.1 — Week 6
## Refining Strategies for the Black-Box Optimisation Challenge

**Module:** 17 — Convolutional Neural Networks
**Submitted:** 27/02/2026
**Cohort:** IMP-PCMLAI-25-08

---

## Part 1: Queries Submitted

| Function | Dimensions | Strategy | Query Submitted | Output |
|----------|------------|----------|-----------------|--------|
| F1 | 2D | GP-UCB exploration (κ=2.0) | 0.798792-0.949373 | TBC |
| F2 | 2D | Trust-region exploit (κ=0.5, r=0.08) | 0.668952-0.918290 | TBC |
| F3 | 3D | Trust-region exploit (κ=0.5, r=0.06) | 0.213857-0.300587-0.437974 | TBC |
| F4 | 4D | Trust-region exploit (κ=0.2, r=0.05) | 0.528154-0.438581-0.469133-0.231649 | TBC |
| F5 | 4D | Tight trust-region exploit (κ=0.02, r=0.04) | 0.987039-0.995007-0.996783-0.999459 | TBC |
| F6 | 5D | Trust-region exploit (κ=0.3, r=0.06) | 0.729225-0.157899-0.728413-0.755070-0.088009 | TBC |
| F7 | 6D | GP-UCB exploration (κ=2.5) | 0.056915-0.431224-0.147322-0.280081-0.405184-0.705437 | TBC |
| F8 | 8D | Trust-region exploit (κ=0.02, r=0.04) | 0.071236-0.002483-0.072505-0.072448-0.452562-0.733258-0.477203-0.838951 | TBC |

---

## Part 2: Reflection on Strategy — Sixth Iteration (15 Data Points)

---

### 1. Progressive Feature Extraction and BBO Strategy Refinement

CNNs construct understanding hierarchically: early layers detect edges, intermediate layers combine these into textures, and deep layers recognize semantic objects. This architecture directly shaped how I conceptualized my BBO strategy across iterations:

**Week 1–2 (Edge detection):** Broad exploration to identify coarse structure—which regions showed any signal, which dimensions seemed influential. Like a first convolutional layer, queries captured basic "gradients" in the function landscape.

**Week 3–4 (Texture building):** As observations accumulated, I began recognizing patterns—F5 and F8 exhibited steep ridges in specific dimensions, while F3 and F6 remained flat. My SVM classification approach emerged here, analogous to mid-layer feature combination: grouping observations into "good" versus "bad" regions before refining further.

**Week 5–6 (Object recognition):** With 15 data points, the surrogate model now captures global structure. For high-performing functions, I apply gradient ascent on neural network surrogates—exploiting the learned "object-level" understanding to navigate toward optima with precision rather than guesswork.

This layered progression prevented me from over-exploiting prematurely (before structure was understood) and ensured exploration served a purpose (building progressively richer representations).

---

### 2. Parallels Between CNN Breakthroughs and Incremental BBO Improvements

LeNet's success came not from a single innovation but from convergent improvements: better activations (ReLU), regularisation (dropout), and computational scale. My BBO progress mirrors this pattern:

| CNN Innovation | BBO Strategy Parallel |
|:---------------|:----------------------|
| Deeper architectures | Evolving from random sampling → GP-UCB → SVM classification → neural surrogates |
| Dropout regularisation | Maintaining exploration guards to prevent "overfitting" to local optima |
| Transfer learning | Carrying learned dimensional influences (e.g., F8's X₁, X₃ dominance) across iterations |
| Batch normalisation | Standardising observations before surrogate training |

No single weekly submission produced dramatic jumps. Instead, compounding refinements—smarter acquisition functions, dimension-aware search, gradient-guided exploitation—mirror how deep learning advances accumulate into capability step-changes.

---

### 3. Balancing Depth, Cost, and Overfitting vs. Explore/Exploit

Training deep CNNs requires trading model capacity against overfitting risk and computational cost. I faced an identical tension:

**Exploitation (deep, focused):**
- Refines known promising regions efficiently
- Risk: premature convergence to local optima
- Applied to: F5 (4D), F8 (8D) where surrogate confidence is high

**Exploration (shallow, broad):**
- Maintains coverage against unknown modes
- Cost: expensive in limited query budget
- Applied to: F1, F7 where signals remain weak or inconsistent

With only 15 observations per function, overfitting the surrogate model to noise is a real danger—analogous to training a deep CNN on insufficient data. My response: simpler GP kernels for low-dimensional functions, MLP ensembles (5 networks, variance as uncertainty proxy) for high-dimensional ones. The SVM classification layer acts as regularisation—preventing queries from chasing noisy outliers by requiring region-level consistency before exploitation.

---

### 4. CNN Building Blocks and Optimisation Learning

Several CNN concepts transformed how I interpret surrogate learning:

**Convolutions → Local Receptive Fields:** Just as convolution kernels detect local patterns, my surrogate's GP length-scales control how "local" the learned structure is. Short length-scales capture fine detail but risk noise sensitivity; longer scales smooth but may miss sharp optima.

**Gradients → Query Direction:** Although black-box, I now compute ∇ₓf_NN(x) through my neural surrogate via backpropagation. This provides directional guidance—where to step next—analogous to how CNN gradients guide weight updates during training.

**Loss Functions → Acquisition Objectives:** EI (Expected Improvement) and UCB serve as my "loss functions"—they encode what I value (improvement, uncertainty reduction) and guide optimisation just as cross-entropy guides CNN classification.

**Pooling → Dimension Reduction:** For F8 (8D), gradient magnitude analysis revealed only X₁ and X₃ matter significantly. I effectively "pooled" the other 6 dimensions, fixing them at best-known values—reducing computational complexity while preserving the essential signal.

---

### 5. Edge AI Deployment Constraints and Benchmarking Success

Andrea Dunbar's discussion of deploying CNNs on edge devices—where latency, power, and memory constraints matter as much as accuracy—reshaped how I benchmark BBO success.

**Query budget as resource constraint:** My 15-query limit mirrors edge compute limits. A strategy that finds the global optimum with 500 queries is useless here, just as a massive CNN is impractical on a low-power device.

**Beyond peak performance:**
- **Sample efficiency:** Information gained per query, not just final value
- **Robustness:** Avoiding catastrophic failures in unexplored regions
- **Consistency:** Steady improvement over iterations rather than lucky peaks

**New success metrics:**
- Rate of uncertainty reduction in promising regions
- Surrogate prediction reliability (cross-validation error)
- Strategy adaptability across function characteristics

This perspective means a lower maximum achieved through principled search may indicate better methodology than a high outlier from random chance—aligning with real-world deployment where reliability under constraints trumps theoretical optimality.
