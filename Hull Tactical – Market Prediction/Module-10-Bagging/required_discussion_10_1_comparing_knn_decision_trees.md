# Required Discussion 10.1 – Comparing KNN and Decision Trees

## Challenge: Hull Tactical – S&P 500 Market Return Prediction

My capstone project focuses on predicting S&P 500 returns using financial time-series data. This involves forecasting return magnitude (regression) and can also be framed as predicting market direction (classification). The challenge requires handling noisy financial data, capturing non-linear relationships between market indicators, and producing predictions that can inform trading decisions.

---

## Question 1: Which method is more appropriate, and why?

**Decision Trees are significantly more appropriate** for predicting market returns than KNN.

Financial markets exhibit complex, non-linear relationships with threshold effects — for example, volatility above a certain level may signal regime change, or momentum indicators crossing specific values may trigger trend reversals. Decision trees naturally capture these threshold-based patterns through their split-based structure, whereas KNN relies on distance metrics that blur such boundaries.

Moreover, market prediction requires **interpretability**. Understanding *why* a model predicts a downturn is as valuable as the prediction itself — it allows traders to validate signals against market intuition and adjust positions accordingly. Decision trees provide explicit decision rules (e.g., "If VIX > 25 and momentum < 0, predict negative returns"), while KNN offers no such transparency.

---

## Question 2: What key factors influenced your choice?

### Interpretability
Decision trees produce human-readable rules that can be audited, explained to stakeholders, and validated against financial theory. KNN is essentially a black box — predictions are based on "similar historical periods" without explaining what makes them similar or why that similarity matters.

### Feature Types and Preprocessing
Financial datasets contain mixed features: continuous variables (returns, volatility, interest rates), categorical indicators (Fed policy stance, earnings season), and ordinal measures (sentiment scores). Decision trees handle this heterogeneity natively. KNN requires all features to be numeric and scaled, which adds preprocessing complexity and can distort meaningful relationships.

### Prediction Speed
Once trained, decision trees predict almost instantaneously by traversing a fixed set of splits. KNN must compute distances to every training observation at prediction time — computationally expensive for large historical datasets spanning decades of market data.

### Scalability
Market prediction often involves extensive feature engineering (lagged returns, rolling statistics, technical indicators), easily creating 50+ features. KNN suffers from the curse of dimensionality in such high-dimensional spaces, where distance metrics become less meaningful. Decision trees are more robust, selecting the most informative features through their splitting process.

### Handling Noise
Financial data is notoriously noisy. KNN can be misled by outliers and noise, treating them as legitimate patterns. Decision trees, especially with proper depth constraints, are more robust to noise because they aggregate observations within leaves rather than relying on individual point comparisons.

---

## Question 3: How did data characteristics affect your decision?

### Non-Linear Threshold Effects
Market dynamics often involve sharp regime changes — calm periods punctuated by sudden volatility spikes, or momentum strategies that work until they don't. Decision trees excel at capturing these discontinuities through their hierarchical splitting structure. KNN's smooth, distance-based predictions would blur these critical thresholds.

### Temporal Dependencies
Financial time-series data exhibits autocorrelation and regime persistence. While neither method explicitly models temporal structure, decision trees can incorporate lagged features and capture conditional relationships (e.g., "If last month's return was negative AND volatility is rising, predict continued decline"). KNN treats each observation as independent points in feature space, ignoring the sequential nature of market data.

### Class Imbalance in Direction Prediction
When framing the problem as classification (predicting up vs. down days), markets are not perfectly balanced — bull markets produce more up days than down. Decision trees can be tuned to handle this imbalance through class weighting or adjusting split criteria. KNN's majority voting among neighbours can be biased toward the dominant class.

### Mixed Feature Scales
My dataset includes percentage returns (small decimals), volatility indices (10-80 range), interest rates (0-5%), and volume (millions). KNN requires careful normalisation to prevent high-magnitude features from dominating. Decision trees are scale-invariant — they only care about feature ordering, not magnitude.

---

## Question 4: What trade-offs did you make?

### Stability vs. Interpretability
Single decision trees are unstable — small changes in data can produce dramatically different tree structures. KNN is more stable in this regard, as predictions change gradually with data. I accepted this instability trade-off because:
1. The interpretability benefits outweigh the stability costs
2. Ensemble methods (discussed below) can mitigate instability while preserving tree-based advantages

### Overfitting Risk
Decision trees can easily overfit by growing too deep, memorising historical patterns that won't repeat. KNN with appropriate k values tends to smooth predictions, reducing overfitting risk. I mitigate this through:
- Limiting tree depth (max_depth = 4-6)
- Requiring minimum samples per split and leaf
- Using time-aware cross-validation to detect overfitting

### Local Pattern Capture
KNN excels at capturing local similarities — finding historical periods that "look like" the current market environment. Decision trees impose a global structure that may miss nuanced local patterns. However, for market prediction, I prioritise robust generalisation over local fitting, as financial data is too noisy for reliable local pattern matching.

---

## Question 5: Would combining methods or ensembles offer advantages?

**Absolutely.** Ensemble techniques are not just advantageous — they're essential for serious market prediction.

### Random Forests
Training multiple decision trees on bootstrapped samples and averaging their predictions dramatically reduces variance while preserving the ability to capture non-linear threshold effects. Feature importance from Random Forests helps identify which market indicators genuinely drive returns versus which are noise.

### Gradient Boosting (XGBoost, LightGBM)
Sequential boosting builds trees that correct previous errors, capturing subtle patterns that single trees miss. These methods consistently rank among top performers in financial prediction competitions, including Kaggle's market forecasting challenges.

### Potential Hybrid Approaches
While I wouldn't use KNN as a primary model, it could serve complementary roles:
- **Regime detection:** KNN could identify which historical periods most resemble current conditions, informing which subset of data to emphasise in tree training
- **Anomaly detection:** Observations far from their k-nearest neighbours might signal unusual market conditions requiring special handling
- **Ensemble diversity:** Including KNN predictions as one input to a meta-model could add diversity, though tree-based ensembles alone typically provide sufficient performance

### My Chosen Approach
For Hull Tactical, I will use **Gradient Boosted Trees (XGBoost)** as my primary model, with **Random Forest** as a benchmark and diversity component. This combines:
- The interpretability advantages of tree-based methods
- The variance reduction of ensembles
- The pattern-capture capability of boosting
- Feature importance metrics to understand what drives predictions

---

## Conclusion

For predicting S&P 500 returns, decision trees are clearly superior to KNN. They handle the mixed, high-dimensional, noisy nature of financial data more effectively while providing the interpretability that trading applications demand. The instability of single trees is a manageable trade-off, readily addressed through ensemble techniques that amplify the strengths of tree-based methods while mitigating their weaknesses.

KNN's reliance on distance metrics, sensitivity to feature scaling, computational expense, and lack of transparency make it poorly suited for market prediction. While it could play a supporting role in regime identification or anomaly detection, the core prediction task belongs to tree-based ensembles.
