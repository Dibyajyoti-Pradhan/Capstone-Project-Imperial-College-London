# Self-study Discussion 16.2: Reflection on the Deep Learning Playground

## Data-Based Problem: S&P 500 Return Direction Prediction

The problem involves predicting whether the S&P 500 will deliver positive or negative monthly returns using financial indicators — volatility measures (VIX), interest rate signals, momentum indicators, and macroeconomic proxies. Deep learning is feasible because the relationships between these features and market returns are non-linear and regime-dependent.

---

## Trade-off Analysis

| Trade-off | Tension in This Problem |
|-----------|------------------------|
| **Model complexity vs computational cost** | Deeper architectures can capture subtle market regimes, but the small dataset (~3,000 observations) doesn't justify the overhead of training complex models |
| **Generalisability vs overfitting** | Markets are non-stationary; a model fitting 2008 crisis patterns may fail in 2024 low-volatility regimes. Expressiveness invites memorisation |
| **Usability vs accuracy** | Portfolio decisions require understanding *why* a prediction was made. Black-box neural networks complicate risk management and stakeholder communication |
| **Training time/data vs capacity** | High-capacity transformers or LSTMs need orders of magnitude more data than available. Simpler architectures are constrained but trainable |

The **dominant constraint** here is data scarcity combined with non-stationarity — the classic "small data, high noise" regime where deep learning struggles.

---

## Balancing Trade-offs in Design

**Recommended architecture:** Shallow MLP (2-3 hidden layers) with aggressive regularisation.

**Specific choices:**
- **Dropout (0.3-0.5):** Prevents co-adaptation of neurons on limited training samples
- **L2 weight decay:** Penalises large weights that signal overfitting
- **Early stopping:** Monitors validation loss with walk-forward splits to halt before memorisation
- **Batch normalisation:** Stabilises training on small batches

**Architectural simplification:**
Rather than end-to-end deep learning, a **hybrid approach** may work better — using a neural network for non-linear feature extraction, then feeding learned representations into an interpretable classifier (logistic regression or gradient boosting). This preserves some usability while leveraging neural pattern recognition.

---

## Hyperparameter Optimisation Strategy

**Key hyperparameters:**
- Learning rate (most sensitive)
- Hidden layer sizes and depth
- Dropout rate
- Batch size
- Weight decay coefficient

**Optimisation approach:**

| Stage | Method | Rationale |
|-------|--------|-----------|
| **Initial exploration** | Random search | More efficient than grid search in high-dimensional spaces; covers diverse configurations |
| **Refinement** | Bayesian optimisation (Optuna) | Exploits promising regions intelligently; suitable when each training run is costly |
| **Validation** | Walk-forward cross-validation | Essential for time-series; prevents lookahead bias that plagues random splits |

**Practical constraint:** With ~3,000 samples, even modest hyperparameter searches risk data leakage if validation sets overlap with training. Strict temporal separation is mandatory.

---

## Open Questions

1. **Minimum viable dataset size:** At what point do neural networks reliably outperform well-tuned logistic regression or XGBoost on financial time-series?

2. **Transfer learning potential:** Can pre-training on related markets (other indices, forex, commodities) provide useful initialisation for the target task?

3. **Regime adaptation:** How should hyperparameters be re-optimised when market regimes shift — continuous online learning or periodic retraining windows?

4. **Interpretability integration:** Can attention mechanisms or SHAP values provide actionable explanations without sacrificing predictive performance?

5. **Ensemble strategies:** Would combining neural predictions with traditional factor models improve robustness more than refining a single architecture?
