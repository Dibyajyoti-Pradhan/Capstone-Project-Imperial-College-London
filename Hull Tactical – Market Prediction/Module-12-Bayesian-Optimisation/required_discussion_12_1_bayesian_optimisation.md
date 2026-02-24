# Required Discussion 12.1 – Analysing Real-World Applications of Bayesian Optimisation

## ML Problem: Hull Tactical – S&P 500 Market Return Prediction

My capstone project tackles the challenge of predicting S&P 500 returns using a rich set of financial indicators. The model selection and hyperparameter tuning process is particularly demanding because financial data exhibits non-stationary behaviour, and the performance surface is noisy. This analysis explores how Bayesian Optimisation could address these challenges.

---

## How could Bayesian optimisation help address the specific challenge you've identified?

### The Core Challenge: Expensive and Noisy Hyperparameter Search

Training machine learning models on financial time-series data presents a unique optimisation problem. Each model evaluation requires:

1. **Computationally expensive forward-chaining cross-validation** — To avoid data leakage, I use expanding window validation where each fold trains on all prior data. With 5-10 folds, a single hyperparameter configuration requires training multiple models sequentially.

2. **Noisy performance metrics** — Financial returns are inherently stochastic. A model's cross-validation score can vary significantly due to market regime changes captured in different folds, making it difficult to distinguish signal from noise.

3. **High-dimensional search spaces** — Models like XGBoost have 10+ hyperparameters (learning rate, max depth, subsample ratio, regularisation terms, etc.). Grid search becomes combinatorially explosive, and random search wastes evaluations.

### How Bayesian Optimisation Helps

**1. Sample Efficiency Through Surrogate Modelling**

Bayesian Optimisation builds a probabilistic surrogate model (typically a Gaussian Process) of the objective function. After just 20-30 evaluations, it develops an understanding of which regions of hyperparameter space yield good performance. This is invaluable when each evaluation takes 5-10 minutes with forward-chaining validation.

**2. Principled Exploration-Exploitation Trade-off**

The acquisition function (Expected Improvement, Upper Confidence Bound) balances:
- **Exploitation:** Sampling near known good configurations
- **Exploration:** Probing uncertain regions that might contain better solutions

This is particularly valuable in financial ML where the performance landscape has multiple local optima and flat regions.

**3. Handling Noise Gracefully**

Gaussian Processes naturally model observation noise. By specifying a noise term, Bayesian Optimisation can smooth over the inherent variability in cross-validation scores, focusing on the underlying trend rather than random fluctuations.

**4. Intelligent Early Stopping**

Advanced implementations can prune poorly performing configurations early. If after two folds a configuration is clearly underperforming, Bayesian Optimisation can terminate evaluation and move to more promising regions.

### Concrete Application in My Project

For my XGBoost model, I would define a search space:

```
learning_rate:    [0.01, 0.3]     (log-uniform)
max_depth:        [3, 12]         (integer)
n_estimators:     [50, 500]       (integer)
subsample:        [0.6, 1.0]      (uniform)
colsample_bytree: [0.6, 1.0]      (uniform)
reg_alpha:        [0.0, 10.0]     (uniform)
reg_lambda:       [0.0, 10.0]     (uniform)
```

Instead of testing thousands of combinations via grid search, Bayesian Optimisation would intelligently sample perhaps 50-100 configurations, each time updating its belief about the objective function and selecting the next most informative point to evaluate.

---

## Is Bayesian optimisation a good fit for this problem?

**Yes, Bayesian Optimisation is well-suited** for hyperparameter tuning in financial ML. Here's the analysis:

### Why It's a Good Fit

| Characteristic | Financial ML Context | BO Suitability |
|----------------|---------------------|----------------|
| **Expensive evaluations** | Forward-chaining CV takes minutes per evaluation | Excellent — BO minimises required evaluations |
| **Continuous hyperparameters** | Learning rates, regularisation, subsample ratios | Excellent — GPs model continuous spaces well |
| **Mixed parameter types** | Continuous + integers (max_depth, n_estimators) | Good — Modern BO handles mixed spaces |
| **Noisy objectives** | CV scores vary due to market regime differences | Good — GP noise modelling helps |
| **Black-box function** | No gradient information from CV scores | Excellent — BO is gradient-free |
| **Moderate dimensionality** | 7-12 hyperparameters typical | Good — BO works well up to ~20 dimensions |

### Potential Limitations

**1. Conditional Parameters**

Some hyperparameters only matter in certain configurations. For example, `min_child_weight` interacts with `max_depth` in non-obvious ways. Standard BO doesn't naturally handle conditional relationships, though tree-structured Parzen estimators (TPE) do better here.

**2. Categorical Choices**

Choosing between model families (Random Forest vs. XGBoost vs. Neural Network) creates a hierarchical search space. While BO can be extended to handle this, it's more complex than optimising within a single model.

**3. Non-Stationarity**

The optimal hyperparameters may drift over time as market regimes change. A configuration optimised on 2010-2020 data might not be optimal when 2021-2024 data is included. BO doesn't inherently address this temporal drift.

### Comparison with Alternatives

| Method | Evaluations Needed | Handles Noise | Handles Continuous | Parallel |
|--------|-------------------|---------------|-------------------|----------|
| Grid Search | 1000s | Poor | No | Yes |
| Random Search | 100s | Poor | Yes | Yes |
| **Bayesian Opt** | **50-100** | **Good** | **Yes** | Limited |
| Hyperband | 50-100 | Moderate | Yes | Yes |

For my project, where each evaluation involves expensive time-series CV, the sample efficiency of Bayesian Optimisation provides significant computational savings.

---

## What questions or uncertainties do you still have about applying Bayesian optimisation?

### 1. How to Handle Temporal Validation Properly?

In financial ML, I use forward-chaining (expanding window) cross-validation to respect temporal ordering. Does this affect how I should structure the objective function for Bayesian Optimisation? Should I weight more recent folds more heavily, or does this introduce bias into the optimisation process?

### 2. How Many Initial Random Points?

Bayesian Optimisation typically starts with random sampling before building the surrogate model. With expensive financial CV, how many initial points provide enough coverage without wasting evaluations? Is the common recommendation of "10 × dimensionality" appropriate, or should financial noise warrant more?

### 3. Dealing with Regime-Dependent Performance

A hyperparameter configuration might perform well in low-volatility periods but poorly during market crises. Should I optimise for average performance, worst-case performance, or some risk-adjusted metric like Sharpe ratio of out-of-sample predictions? How do I encode this multi-objective consideration into Bayesian Optimisation?

### 4. Transfer Learning Across Time Periods

If I've already optimised hyperparameters on 2010-2020 data, can I use that information as a warm start when re-optimising on 2010-2024 data? How much does prior optimisation knowledge transfer when the data distribution has shifted?

### 5. Choosing the Right Acquisition Function

Expected Improvement (EI) is standard, but alternatives like Knowledge Gradient or Entropy Search might be better for noisy objectives. Which acquisition function is most robust for the high-noise regime of financial prediction?

### 6. Computational Overhead

For models that train in seconds (e.g., logistic regression with small data), is Bayesian Optimisation's overhead justified? Should I use BO only for expensive models (XGBoost, neural networks) and simpler methods (random search) for lightweight models?

### 7. Reproducibility Across Runs

Given the stochastic nature of both the surrogate model initialisation and the financial objective, how do I ensure reproducibility? Should I run multiple BO optimisations with different seeds and ensemble the results?

---

## Conclusion

Bayesian Optimisation is a **strong fit** for hyperparameter tuning in my Hull Tactical market prediction project. The combination of expensive forward-chaining validation, noisy financial objectives, and multi-dimensional continuous search spaces aligns well with BO's strengths. While questions remain about handling temporal dependencies and regime-specific performance, the sample efficiency gains over grid or random search make BO the preferred approach for production-level model tuning.

The key insight is that financial ML involves optimising a fundamentally uncertain, expensive-to-evaluate function — exactly the scenario where Bayesian Optimisation's probabilistic approach provides the most value.
