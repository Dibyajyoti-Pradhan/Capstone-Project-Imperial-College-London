# Required Capstone Component 13.1 – Refining BBO Strategy

## Part 2: Reflection on Strategy

---

### 1. What was the main change in your strategy this week compared to last week?

The fundamental shift was moving from **blind exploration to output-informed decision making**. Last week, I sampled purely based on spatial coverage without any feedback. This week, the Week 1 outputs revealed critical information:

- **Function 5** returned a massive positive value (~1600), signalling proximity to a strong optimum
- **Function 1** showed near-zero readings, indicating we are far from any signal
- **Functions 3 and 6** produced negative outputs, suggesting fundamentally wrong regions

This prompted a **function-specific strategy**: local exploitation for strong performers (F5, F8), aggressive exploration for weak signals (F1, F7), and moderate exploration to escape poor regions (F3, F6). The change was driven primarily by observed outputs rather than acquisition function behaviour, though I implemented UCB with varying kappa values tailored to each function's characteristics.

---

### 2. Did you focus more on exploration or exploitation? Why?

I maintained a **70% exploration / 30% exploitation balance** overall, but this varied significantly by function:

| Function | Strategy | Rationale |
|----------|----------|-----------|
| F1, F7 | Heavy exploration (kappa=5.0) | Weak/zero signal requires broad search |
| F3, F6 | Moderate exploration (kappa=3.0) | Negative outputs mean wrong region |
| F2, F4 | Balanced (kappa=1.96) | Moderate signals, continue mapping |
| F5, F8 | Local exploitation | Strong positives worth refining |

**Trade-offs considered:**
- Premature exploitation risks converging on local optima
- Excessive exploration wastes limited queries
- With only 11 data points per function, surrogate models remain unreliable for confident exploitation

For F5 and F8, I used **local perturbation** around the best-known point rather than trusting GP extrapolation, which tends to drift toward domain boundaries with sparse data.

---

### 3. Have any participant strategies or discussions influenced your approach?

Yes, several insights shaped my approach:

1. **Boundary drift problem**: Class discussions highlighted that GPs with sparse data often extrapolate toward edges (0.0 or 1.0). This led me to constrain sampling to [0.01, 0.99].

2. **Staged exploration-exploitation**: Peers emphasized that early weeks should focus on mapping function shape rather than chasing current best values.

3. **Output scale awareness**: Seeing the extreme variance in outputs (from 10^-31 to 10^3) reinforced the need for target standardisation before fitting surrogates.

4. **Hybrid classifier approach**: Some participants used quick logistic classifiers to threshold outputs into "good/bad" regions, which inspired me to think about binary decision boundaries for F5.

---

### 4. Which linear/logistic regression assumptions would you most likely violate?

For **linear regression**, the most violated assumptions would be:
- **Linearity**: Response surfaces are clearly curved and potentially multimodal
- **Homoscedasticity**: Noise varies dramatically across the domain (near-zero regions vs. high-output regions)
- **Sufficient samples**: 11 points in 8D is severely underdetermined (~1.4 points per dimension)
- **Independence**: Nearby points share structural information; residuals are spatially correlated

For **logistic regression** (if thresholding outputs):
- **Linear separability**: Decision boundaries are likely curved or radial
- **Balanced classes**: Very few "positive" (high-output) samples exist
- **Sufficient data**: Cannot reliably estimate coefficients with current sample size

---

### 5. Are there regions where output appears roughly linear or where decision boundaries might form?

**Locally linear regions**: Function 2 and Function 5 show neighbourhoods where small perturbations produce approximately proportional output changes. These patches could provide useful gradient estimates for steepest ascent.

**Potential decision boundaries**: Function 5 appears to have high values concentrated in a corner where certain dimensions are near 1.0. A logistic classifier might successfully identify this "good region" if outputs were binarised (e.g., yield > 500).

**Logistic regression performance**: Would likely struggle globally due to curved boundaries, but could serve as a coarse pre-filter to identify regions of interest. Performance would degrade severely for 6D-8D functions due to insufficient data.

---

### 6. Did you find it useful to consider individual feature effects?

Yes, interpretability proved valuable even without fitting explicit linear models:

- **Correlation analysis**: Computed Pearson correlations between each dimension and output. For Function 8, dimensions X1 and X3 showed strong negative correlation (r ~ -0.6), suggesting targeting low values in those dimensions.

- **Sensitivity probing**: Designed perturbations varying one dimension at a time, isolating each variable's marginal effect.

- **Dimension importance**: Used Random Forest feature importance to identify influential vs. potentially irrelevant dimensions, allowing pseudo-dimensionality reduction for high-D functions.

This feature-level thinking guided query selection by highlighting which directions showed promise and where uncertainty remained highest.

