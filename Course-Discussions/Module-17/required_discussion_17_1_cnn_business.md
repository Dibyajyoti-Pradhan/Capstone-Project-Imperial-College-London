# Required Discussion 17.1: When CNNs Make Sense in Business

## Industry Challenge: Market Regime Detection for Tactical Asset Allocation

My industry-specific challenge involves predicting market conditions for tactical investment decisions—specifically, determining whether to be risk-on (equities) or risk-off (bonds/cash) based on evolving market signals. This is the Hull Tactical challenge explored in my capstone work.

---

## 1. Relevant Data

### What types of data are available?

Traditional market prediction relies on tabular time-series data (prices, returns, volatility). However, several data types can be restructured into grid-like formats suitable for CNNs:

**Correlation matrices (2D grids):** Rolling correlations between asset classes (equities, bonds, commodities, currencies) form symmetric matrices where spatial patterns indicate market regime shifts—tight correlations during stress, decorrelation during calm periods.

**Price-volume heatmaps (2D: assets × time):** Daily returns or volumes across multiple tickers arranged as rows, with time windows as columns, creating "financial images" where CNNs can detect patterns like sector rotations or momentum cascades.

**Technical indicator matrices:** Multiple indicators (RSI, MACD, Bollinger Bands, moving averages) computed across various lookback windows create multi-channel grids analogous to RGB image channels.

**Order book snapshots:** Bid-ask depth visualized as 2D grids (price levels × time) capture microstructure patterns relevant to short-term prediction.

### Data quality and preprocessing considerations

- **Non-stationarity:** Financial data distributions shift over time; rolling normalization and careful train-test splits (temporal, not random) are essential
- **Class imbalance:** Market crashes are rare but critical; oversampling or focal loss functions may be needed
- **Noise:** Financial data has low signal-to-noise ratio; aggressive augmentation risks learning spurious patterns
- **Lookback window selection:** Grid dimensions depend on the prediction horizon—daily prediction may use 20-60 day lookbacks

---

## 2. Network Architecture Outline

### High-Level Design

For correlation matrix or heatmap inputs, a moderate-depth 2D CNN would be appropriate:

**Input layer:** Normalized correlation matrix (e.g., 50×50 for 50 assets) or price heatmap

**Convolutional blocks (3-4 layers):**
- Conv2D with small filters (3×3) to detect local correlation clusters
- Batch normalization for training stability
- ReLU activation
- MaxPooling (2×2) to capture broader market patterns

**Regularization:**
- Dropout (0.3-0.5) to prevent overfitting on noisy financial data
- L2 regularization on dense layers

**Special modules:**
- **Residual connections** to preserve gradient flow in deeper networks
- **Channel attention (SE blocks)** to weight importance of different indicator channels
- **Global Average Pooling** before classification to reduce parameters

**Output:** Binary classification (risk-on/risk-off) with sigmoid, or multi-class regime labels with softmax

### Transfer Learning

Transfer learning is less straightforward than in computer vision because financial "images" differ fundamentally from natural images. However:
- Pre-training on longer historical periods, then fine-tuning on recent data
- Pre-training on related tasks (volatility prediction) before transfer to regime classification
- Using CNN backbones pre-trained on generic pattern recognition, then fine-tuning final layers

---

## 3. Evaluation Strategies

### Accuracy Metrics

Given class imbalance (crashes are rare), accuracy alone is misleading. Appropriate metrics include:

- **Precision/Recall:** High recall for crash detection is critical—missing a drawdown is costly
- **F1-score:** Balances precision and recall
- **ROC-AUC / PR-AUC:** Evaluates discrimination across thresholds
- **Confusion matrix:** Understand false positive (unnecessary hedging) vs false negative (missed crash) tradeoffs

### Validation Techniques

- **Walk-forward validation:** Train on history, predict forward, roll window—mimics real deployment
- **Regime-stratified splits:** Ensure test sets contain both bull and bear periods
- **Out-of-sample stress testing:** Evaluate on specific historical crises (2008, 2020) excluded from training

### Visual Inspection and Expert Review

- **Grad-CAM heatmaps:** Visualize which regions of the correlation matrix or price grid influenced predictions
- **Portfolio manager review:** Domain experts assess whether highlighted patterns align with known market dynamics
- **Error analysis:** Investigate false negatives—did the model miss signals that were visible to human analysts?

### Business KPIs

The ultimate test is real-world value:

- **Risk-adjusted returns:** Sharpe ratio, Sortino ratio improvement over buy-and-hold
- **Maximum drawdown reduction:** Did the model help avoid significant losses?
- **Signal stability:** Excessive regime switching incurs transaction costs
- **Backtested P&L:** Simulated returns net of realistic trading costs
- **Comparison to baseline:** Does CNN outperform simpler models (logistic regression, random forest)?

---

## Conclusion

CNNs are not the default choice for financial prediction, but they become compelling when data is restructured into spatial representations where local patterns carry meaning. Correlation matrices and multi-indicator heatmaps fit this criterion. Success depends on rigorous temporal validation, domain expert review of learned patterns, and evaluation against business-relevant KPIs rather than pure accuracy.

---

*Word count: 698*
