# Required Capstone Component 17.1 — Week 6
## Refining Strategies for the Black-Box Optimisation Challenge

**Module:** 17 — Convolutional Neural Networks
**Submitted:** 27/02/2026
**Cohort:** IMP-PCMLAI-25-08

---

## Part 1: Queries Submitted

| Function | Dimensions | Strategy | Query Submitted | Output |
|----------|------------|----------|-----------------|--------|
| F1 | 2D | Moderate exploration (κ=3.0) | 0.850891-0.775648 | TBC |
| F2 | 2D | Balanced GP-UCB (κ=1.0) | 0.772368-0.913563 | TBC |
| F3 | 3D | Balanced GP-UCB (κ=1.0) | 0.241048-0.271591-0.443703 | TBC |
| F4 | 4D | Balanced GP-UCB (κ=0.8) | 0.532765-0.420960-0.437436-0.247826 | TBC |
| F5 | 4D | Tight trust-region exploit (κ=0.2, r=0.03) | 0.987377-0.995102-0.979863-0.958435 | TBC |
| F6 | 5D | Balanced-explore (κ=1.2) | 0.689558-0.184451-0.747158-0.657878-0.026114 | TBC |
| F7 | 6D | GP gradient ascent (κ=3.0) | 0.080962-0.503343-0.326421-0.223510-0.415342-0.715003 | TBC |
| F8 | 8D | Trust-region exploit (κ=0.2, r=0.08) | 0.082656-0.155191-0.047568-0.087396-0.337200-0.762400-0.474602-0.919581 | TBC |

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
