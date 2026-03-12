# Required Capstone Component 13.1 — Week 2
## Refining Strategies for the Black-Box Optimisation Challenge

**Module:** 13 — Logistic Regression
**Submitted:** 26/02/2026
**Cohort:** IMP-PCMLAI-25-08

---

## Part 1: Queries Submitted

| Function | Dimensions | Strategy | Query Submitted | Output |
|----------|------------|----------|-----------------|--------|
| F1 | 2D | Heavy exploration | 0.858703-0.783562 | TBC |
| F2 | 2D | Balanced | 0.788596-0.912389 | TBC |
| F3 | 3D | Moderate exploration (escape negative region) | 0.488361-0.663509-0.183247 | TBC |
| F4 | 4D | Balanced | 0.514874-0.428474-0.422867-0.202058 | TBC |
| F5 | 4D | Local exploitation | 0.989444-0.972030-0.987250-0.980016 | TBC |
| F6 | 5D | Moderate exploration (escape negative region) | 0.705815-0.131196-0.780837-0.738601-0.106925 | TBC |
| F7 | 6D | Heavy exploration | 0.125386-0.458533-0.244663-0.288875-0.416247-0.714687 | TBC |
| F8 | 8D | Local exploitation | 0.117631-0.033906-0.164674-0.039646-0.373290-0.749774-0.493738-0.936259 | TBC |

**Week 1 outputs that informed this strategy:**

| Function | Week 1 Output | Signal |
|----------|--------------|--------|
| F1 | ~0.000 | Near-zero — far from any signal |
| F2 | Moderate positive | Continue mapping |
| F3 | Negative | Wrong region |
| F4 | Moderate negative | Continue mapping |
| F5 | ~1600 | Strong optimum near corner (0.999,0.999,0.999,0.999) |
| F6 | Negative | Wrong region |
| F7 | Moderate | Continue mapping |
| F8 | Positive | Decent signal |

---

## Part 2: Reflection

### 1. What was the main change in your strategy this week?

The fundamental shift was moving from **blind exploration to output-informed decision making**. Last week, I sampled purely based on spatial coverage. This week, Week 1 outputs revealed critical information:

- **Function 5** returned a massive positive value (~1600), signalling proximity to a strong optimum
- **Function 1** showed near-zero readings, indicating we are far from any signal
- **Functions 3 and 6** produced negative outputs, suggesting wrong regions

This prompted a function-specific strategy: local exploitation for strong performers (F5, F8), aggressive exploration for weak signals (F1, F7), and moderate exploration to escape poor regions (F3, F6).

---

### 2. Did you focus more on exploration or exploitation?

I maintained a **70% exploration / 30% exploitation balance** overall, but this varied by function:

| Function | Strategy | Rationale |
|----------|----------|-----------|
| F1, F7 | Heavy exploration (κ=4.0) | Weak signal requires broad search |
| F3, F6 | Moderate exploration (κ=2.0) | Negative outputs — wrong region |
| F2, F4 | Balanced (κ=1.5) | Moderate signals, continue mapping |
| F5, F8 | Local exploitation (κ=0.5, trust region) | Strong positives worth refining |

**Trade-offs:** Premature exploitation risks local optima; excessive exploration wastes queries. For F5/F8, I used local perturbation within a trust region rather than trusting GP extrapolation, which tends to drift toward domain boundaries with sparse data.

---

### 3. Have any participant strategies or class discussions influenced your approach?

- **Boundary drift problem:** GPs extrapolate toward edges with sparse data — constrained sampling to [0.01, 0.99]
- **Staged exploration:** Early weeks should map function shape, not chase current best values
- **Output scale awareness:** Extreme variance (10⁻³¹ to 10³) requires target standardisation before fitting surrogates
- **Hybrid classifier approach:** Using logistic classifiers to threshold outputs into good/bad regions inspired me to think about binary decision boundaries for F5

---

### 4. Which regression assumptions would you most likely violate?

**Linear regression violations:**
- **Linearity:** Response surfaces are clearly curved and potentially multimodal
- **Homoscedasticity:** Noise varies dramatically across the domain (near-zero regions vs. high-output regions)
- **Sufficient samples:** 11 points in 8D is severely underdetermined (~1.4 points per dimension)
- **Independence:** Nearby points share structural information; residuals are spatially correlated

**Logistic regression violations (if thresholding outputs):**
- **Linear separability:** Decision boundaries are likely curved or radial
- **Balanced classes:** Very few "positive" (high-output) samples exist
- **Sufficient data:** Cannot reliably estimate coefficients with current sample size

---

### 5. Are there regions where the output appears roughly linear or where a decision boundary might form?

**Locally linear regions:** Functions 2 and 5 show neighbourhoods where small perturbations produce approximately proportional output changes — useful for gradient estimates and steepest-ascent steps.

**Potential decision boundaries:** Function 5 has high values concentrated near the corner where dimensions approach 1.0. A logistic classifier could identify this "good region" if outputs were binarised (e.g., yield > 500). Performance would likely be reasonable for F5's relatively clean structure but degrade severely for 6D–8D functions due to insufficient data.

---

### 6. Did you find it useful to consider individual feature effects?

Yes — interpretability proved valuable even without fitting explicit models:

- **Correlation analysis:** Computed Pearson correlations between each dimension and output. For F8, dimensions X1 and X3 showed notable correlation with output, suggesting targeting specific value ranges in those dimensions.
- **Sensitivity probing:** Designed perturbations varying one dimension at a time to isolate marginal effects and identify which directions showed promise.
- **Dimension importance:** Random Forest feature importance helped identify influential vs. potentially irrelevant dimensions, supporting pseudo-dimensionality reduction for F7 and F8.
