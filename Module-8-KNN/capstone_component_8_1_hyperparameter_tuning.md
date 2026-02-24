# Capstone Component 8.1 – Identifying Applications of Hyperparameter Tuning

## Context: Financial Market Prediction

For my capstone project, I'm working on the Hull Tactical – Market Prediction competition, which involves forecasting S&P 500 returns using financial time-series data. Hyperparameter tuning is critical here because small adjustments can significantly impact whether the model captures genuine market patterns or simply overfits to historical noise.

## Examples of Hyperparameter Tuning in Real-World Settings

| Domain | Application | Tuning Example | Impact |
|--------|-------------|----------------|--------|
| Finance | Predicting S&P 500 returns using Gradient Boosting (XGBoost) | Tuned learning rate, max depth, number of estimators, and subsample ratio | Improved out-of-sample returns by reducing overfitting to historical market regimes; better generalisation across bull and bear markets |
| Finance | Algorithmic trading signal classification using KNN | Tuned k (number of neighbours) and distance metric (Euclidean vs Manhattan) | More stable trade signals with fewer false positives; reduced transaction costs from spurious trades |
| Finance | Portfolio risk forecasting using Random Forest | Tuned number of trees, max features, and minimum samples per leaf | Enhanced risk estimates during volatile periods; improved Sharpe ratio by balancing accuracy with model stability |
| Quantitative Research | Time-series return prediction using LSTM networks | Tuned sequence length, number of hidden units, dropout rate, and learning rate | Captured longer-term dependencies in price movements while avoiding overfitting to short-term noise |

## Key Hyperparameters to Tune

In financial prediction, the most critical hyperparameters depend on the model:

**For Gradient Boosting (XGBoost):**
- **Learning rate:** Controls how aggressively the model updates; too high leads to overfitting, too low slows convergence
- **Max depth:** Limits tree complexity; deeper trees capture more patterns but risk memorising noise
- **Number of estimators:** More trees improve accuracy up to a point, then add computational cost without benefit
- **Subsample ratio:** Introduces randomness to prevent overfitting to specific market conditions

**For KNN:**
- **k (number of neighbours):** Small k captures local patterns but is sensitive to noise; large k smooths predictions but may miss regime changes
- **Distance metric:** Euclidean works well for normalised features; Manhattan may be more robust to outliers in financial data

**For Neural Networks:**
- **Dropout rate:** Prevents overfitting by randomly deactivating neurons during training
- **Learning rate:** Critical for stable convergence in noisy financial data

## Trade-offs to Consider

**Accuracy vs Overfitting:**
In financial markets, overfitting is the primary risk. A model that performs brilliantly on historical data but fails on new data is worse than useless — it gives false confidence. I'd prioritise cross-validated performance over training accuracy, using time-aware validation splits to respect temporal ordering.

**Complexity vs Interpretability:**
More complex models (deep networks, large ensembles) may squeeze out marginal gains, but simpler models are easier to debug and explain. For a trading strategy, understanding *why* a model makes predictions can be as valuable as the predictions themselves.

**Performance vs Training Time:**
Bayesian optimisation or random search can find good hyperparameters faster than exhaustive grid search, which matters when iterating quickly during competition deadlines.

**Generalisation vs Regime Sensitivity:**
Markets shift between regimes (trending, mean-reverting, volatile). Hyperparameters tuned on one regime may fail in another. I'd use expanding-window or rolling-window validation to test robustness across different market conditions.

## Knowledge, Skills, and Data Required

**Technical skills:**
- Proficiency with scikit-learn, XGBoost, and hyperparameter optimisation libraries (Optuna, Hyperopt)
- Understanding of time-series cross-validation (forward-chaining, expanding window)
- Experience with evaluation metrics relevant to finance (Sharpe ratio, maximum drawdown, not just RMSE)

**Domain knowledge:**
- Understanding of market microstructure and what features might be predictive
- Awareness of look-ahead bias and how to avoid it in feature engineering
- Knowledge of transaction costs and how they affect practical trading strategies

**Data requirements:**
- Clean historical price and volume data with sufficient history (multiple market cycles)
- Properly lagged features to prevent data leakage
- Representative validation sets spanning different market regimes

## Application to My Capstone Project

For Hull Tactical, I will:

1. **Start with baseline models** using default hyperparameters to establish benchmarks
2. **Use Bayesian optimisation** (via Optuna) for efficient hyperparameter search rather than exhaustive grid search
3. **Implement time-aware cross-validation** to ensure the model generalises across different time periods
4. **Track all experiments systematically** — logging hyperparameter combinations, validation scores, and test performance
5. **Evaluate multiple metrics** — not just prediction accuracy, but also metrics relevant to trading (directional accuracy, risk-adjusted returns)
6. **Test robustness** by checking whether optimal hyperparameters remain stable across different validation windows

The goal isn't just to find hyperparameters that maximise backtest performance, but to find settings that produce a model robust enough to work on genuinely unseen future data.
