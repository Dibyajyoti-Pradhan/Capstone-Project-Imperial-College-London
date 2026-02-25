# Required Capstone Component 13.1 – Refining Your Strategies for the Black-Box Optimisation Challenge

## Part 2: Reflection on Strategy

---

## 1. What was the main change in your strategy this week compared to last week? What prompted this change?

### The Shift: From Blind Exploration to Evidence-Guided Search

Last week's strategy was purely exploratory — maximising spatial coverage without any output feedback. This week marked a fundamental transition to **output-informed decision making**.

### Key Changes

| Aspect | Week 1 | Week 2 |
|--------|--------|--------|
| **Decision basis** | Input space geometry only | Input + output values |
| **Model usage** | None | Gaussian Process surrogates fitted per function |
| **Query selection** | Maximum distance heuristic | UCB acquisition with function-specific kappa |
| **Function treatment** | Uniform across all 8 | Tailored strategy per function |

### What Prompted the Change

The Week 1 outputs revealed dramatic differences across functions:

- **Function 5:** Massive positive value (~1600+) suggesting proximity to a strong optimum
- **Function 1:** Near-zero readings indicating we are far from any signal source
- **Functions 3, 6:** Negative outputs suggesting fundamentally wrong regions

These contrasts made it clear that a one-size-fits-all exploration strategy was inefficient. Functions showing promise warranted local refinement, while poor-performing functions needed continued broad search.

### Specific Adaptations

For **Function 5 and 8** (strong positive outputs): Switched to local perturbation around the best-known point rather than trusting the GP's global extrapolation.

For **Function 1** (near-zero signal): Increased exploration aggressiveness (kappa = 5.0) to search for the "needle in the haystack."

For **Functions 3, 6** (negative outputs): Moderate exploration (kappa = 3.0) to escape the current unpromising region without completely random sampling.

---

## 2. Did you focus more on exploration or exploitation? Why? What trade-offs did you weigh?

### Overall Balance: 70% Exploration / 30% Exploitation

With only 11 data points per function, the dataset remains too sparse for confident exploitation across most functions. However, ignoring strong signals entirely would waste valuable information.

### Function-Specific Breakdown

| Function | Dims | Strategy | Rationale |
|----------|------|----------|-----------|
| F1 | 2D | Heavy Exploration | Zero signal detected — must search widely |
| F2 | 3D | Balanced | Moderate outputs — continue mapping |
| F3 | 3D | Exploration | Negative output — wrong region |
| F4 | 4D | Balanced | Dynamic system — uncertain structure |
| F5 | 4D | Local Exploitation | Strong positive — refine best region |
| F6 | 5D | Exploration | Negative output — escape current area |
| F7 | 6D | Heavy Exploration | High-D with weak signal |
| F8 | 8D | Local Exploitation | Good positive — worth refining |

### Trade-offs Considered

**Risk of premature exploitation:**
- Converging on a local optimum while missing the global maximum
- Overfitting to noise in sparse-data regime
- Wasting remaining queries on a region that appears good only due to chance

**Risk of excessive exploration:**
- Failing to capitalise on genuinely promising regions
- Slow convergence toward optimum
- Inefficient use of limited query budget

**My resolution:** Use local perturbation for exploitation (small controlled steps around best point) rather than trusting GP extrapolation, which tends to push toward boundaries with limited data.

---

## 3. Have any participant strategies, class discussions or recent outputs influenced your approach?

### Influences from Course Materials

The module's emphasis on **interpretability** in linear/logistic regression prompted me to think about feature effects even when using GP surrogates. Before selecting each query, I examined:
- Which dimensions showed strongest correlation with output
- Whether any dimensions appeared irrelevant (candidates for fixing)
- Local gradient directions near promising points

### Peer Strategy Observations

Several patterns emerged from reviewing peer approaches:

1. **Boundary drift problem:** Multiple participants noted that GPs with sparse data extrapolate toward domain edges (0.0 or 1.0). This reinforced my decision to constrain sampling to [0.01, 0.99].

2. **Hybrid classifier approach:** Some peers used quick logistic classifiers to threshold outputs into "good/bad" regions, then focused GP-based search within "good" areas. This inspired me to consider binary thresholding for Function 5.

3. **Staged kappa decay:** The idea of starting with high exploration and gradually reducing prompted me to plan a kappa schedule for future rounds.

### Output-Driven Insights

The extreme variance in Week 1 outputs (from ~10^-31 to ~10^3) highlighted that:
- Functions operate at vastly different scales — standardisation is essential
- Near-zero outputs may indicate noise floor rather than true function value
- Large positive outputs warrant immediate local investigation

---

## 4. If you were to fit a simple linear or logistic regression model to your current data, which assumptions would you most likely violate?

### Linear Regression Violations

| Assumption | Why It Would Be Violated |
|------------|-------------------------|
| **Linearity** | Response surfaces are almost certainly curved, with peaks, valleys, and potentially multiple modes |
| **Homoscedasticity** | Noise varies dramatically across the domain — near-zero regions have different variance than high-output regions |
| **Independence** | Nearby points in optimization landscapes share structural information; residuals are spatially correlated |
| **Sufficient samples** | 11 points in 8D is severely underdetermined (ratio ~1.4 points per dimension) |
| **No multicollinearity** | Input dimensions may interact in complex ways |

### Logistic Regression Violations (if thresholding outputs)

| Assumption | Why It Would Be Violated |
|------------|-------------------------|
| **Linear separability** | Decision boundaries between "good" and "bad" regions are likely curved or radial |
| **Balanced classes** | Very few "positive" (high-output) samples exist early on |
| **Independence** | Sequential optimization queries are inherently dependent |
| **Large sample** | 11 points insufficient for reliable coefficient estimation |

### Most Critical Violation: Non-linearity

The fundamental issue is that black-box functions are, by definition, unknown and likely non-linear. Any linear model captures only a tangent plane approximation valid in a tiny neighborhood, useless for global optimization.

---

## 5. Are there any regions where output appears roughly linear or where a decision boundary might form?

### Locally Linear Regions

**Function 2 (3D):** Near the moderate-output region, small perturbations produce approximately proportional changes in output, suggesting local linearity. A linear model here could estimate gradient direction for steepest ascent.

**Function 5 (4D):** Around the best-known point, the response appears smooth with consistent directional effects. Dimensions corresponding to high values (near 1.0) correlate with high output, creating an approximately linear relationship locally.

### Potential Decision Boundaries

**Function 5:** If outputs were binarised (e.g., "yield > 500" vs "yield < 500"), a logistic classifier might successfully identify a region boundary. The "good" region appears concentrated in a corner of the input space where certain dimensions are high.

**Function 1:** A threshold-based classifier could separate "signal detected" from "no signal" regions, potentially forming a radial boundary around an unknown source location.

### Logistic Regression Performance Assessment

| Scenario | Expected Performance |
|----------|---------------------|
| **Raw coordinates** | Poor — boundaries are likely curved |
| **With polynomial features** | Moderate — captures some curvature |
| **With radial basis features** | Better — matches expected radial patterns |
| **High-dimensional functions (6D-8D)** | Very poor — insufficient data for reliable boundary estimation |

A logistic classifier would be most useful as a coarse pre-filter to identify "regions of interest" rather than for precise optimization.

---

## 6. Interpretability is a key advantage of linear and logistic regression. Did you find it useful to consider individual feature effects before deciding on your query point?

### Yes — Interpretability Guided Query Selection

Even without fitting explicit linear models, thinking in terms of **marginal feature effects** proved valuable.

### How I Used Feature-Level Thinking

**Correlation analysis:** Before each query, I computed Pearson correlations between each input dimension and the output. Dimensions with strong negative correlations (e.g., in Function 8, X1 and X3 showed r ~ -0.6) suggested targeting low values in those dimensions.

**Sensitivity probing:** For local exploitation, I designed perturbations that varied one dimension at a time while holding others constant. This mirrors the coefficient interpretation in linear regression — isolating each variable's effect.

**Dimension importance ranking:** Using Random Forest feature importance as a proxy, I identified which dimensions warranted focused exploration vs. which could be treated as noise.

### Concrete Example: Function 8 (8D)

Initial analysis suggested:
- Dimensions X1, X3: Strong negative correlation → target low values
- Dimensions X2, X4-X8: Weak correlation → likely less influential

Rather than optimising in full 8D, I treated this as a pseudo-2D problem, biasing sampling toward low X1 and X3 while allowing other dimensions to vary freely.

### Limitations of This Approach

The interpretability advantage diminishes when:
- Interactions dominate (effects aren't additive)
- Non-monotonic relationships exist
- Sample size is too small for reliable correlation estimates

Nevertheless, even rough directional intuition from feature analysis beats blind random search.

---

## Summary

This week marked the transition from pure exploration to evidence-guided optimization. Key insights:

1. **Output-driven differentiation:** Functions now receive tailored strategies based on their observed behaviour
2. **Local exploitation for strong signals:** Rather than trusting GP extrapolation, use controlled perturbation around best-known points
3. **Continued exploration for weak signals:** Functions showing negative or near-zero outputs need broader search
4. **Feature-level thinking:** Even without formal regression, marginal effect intuition guides query selection
5. **Regression assumptions are violated:** But local linear approximations remain useful for gradient estimation

The connection to Hull Tactical market prediction is clear: just as we balance exploration of new trading signals with exploitation of known patterns, BBO requires managing the explore-exploit trade-off with limited evaluation budget.
