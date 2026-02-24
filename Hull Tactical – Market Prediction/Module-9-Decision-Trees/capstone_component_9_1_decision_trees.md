# Capstone Component 9.1 – How Could Decision Trees Be Used for Hyperparameter Tuning?

## Project Context: Hull Tactical – Market Prediction

My capstone project focuses on predicting S&P 500 returns using financial time-series data. This involves regression (predicting return magnitude) and can also be framed as classification (predicting market direction). Decision trees offer a transparent, interpretable approach that can serve multiple purposes in this project.

## How Decision Trees Help Identify Influential Features

Decision trees naturally reveal which features matter most by how they structure their splits. Features appearing near the root of the tree — those that produce the largest reduction in impurity — are the most influential predictors. In my market prediction project, this could help identify whether technical indicators (moving averages, momentum), fundamental data (earnings, valuations), or macro variables (interest rates, volatility) drive returns most strongly.

I would use a decision tree primarily as a **benchmark and exploratory tool** rather than the final model. Its interpretability makes it invaluable for:
- Understanding which features genuinely predict returns vs which are noise
- Validating that more complex models (gradient boosting, neural networks) are learning meaningful patterns
- Communicating insights to stakeholders who need to understand why a model makes certain predictions

However, financial data is notoriously noisy, and single decision trees tend to overfit. For final predictions, I'd likely move to ensemble methods that build on the same logic but offer better stability.

## Controlling Tree Depth and Avoiding Overfitting

Financial time-series data contains substantial noise — random fluctuations that don't represent true patterns. A deep tree will memorise this noise and fail on new data. To prevent this, I would:

**Set explicit constraints:**
- **max_depth:** Start with 4–6 levels and increase only if validation performance improves. Deep trees in financial data almost always overfit.
- **min_samples_split:** Ensure each split is based on enough observations (e.g., at least 50–100 data points) to be statistically meaningful.
- **min_samples_leaf:** Require each leaf to contain enough samples to represent a genuine market condition, not a one-off event.
- **min_impurity_decrease:** Only allow splits that meaningfully reduce variance or Gini impurity.

**Use cross-validation:** I would use time-aware forward-chaining validation (not random k-fold) to test whether depth constraints generalise across different market periods. The optimal depth is where validation performance plateaus — going deeper only adds complexity without improving out-of-sample results.

## Hyperparameter Tuning Approach

Given that decision trees train very quickly, I can afford to test many combinations systematically:

**My approach:**
1. **Random search first:** Broadly explore the parameter space (max_depth from 2–15, min_samples_split from 20–200, etc.) to identify promising regions
2. **Grid search to refine:** Once I've narrowed down good ranges, use a finer grid search around the best-performing combinations
3. **Time-series cross-validation throughout:** Every combination is evaluated using forward-chaining splits to ensure results reflect genuine out-of-sample performance

I'd avoid pure trial-and-error because it's prone to confirmation bias — you stop when results look good rather than when they're genuinely optimal.

## Evaluation Metrics

For market prediction, I would monitor:

**For regression (predicting return magnitude):**
- **RMSE / MAE:** Standard measures of prediction error
- **R²:** How much variance in returns the model explains (though this is typically low for financial data)
- **Directional accuracy:** What percentage of predictions got the sign right (up vs down)

**For classification (predicting direction):**
- **Precision and recall:** Especially for the "strong up" or "strong down" classes
- **F1-score:** Balance between precision and recall

**Generalisation check:** The model generalises well when:
- Training and validation performance are similar (no large gap indicating overfitting)
- Performance is stable across different time periods (not just one market regime)
- Results on the final hold-out test set match cross-validation estimates

## Leveraging Fast Training for Rapid Iteration

Decision trees train in seconds, which allows me to:
- **Test many feature combinations:** Quickly evaluate whether adding lagged returns, volatility measures, or sector indicators improves predictions
- **Experiment with preprocessing:** Try different scaling methods, outlier treatments, and feature transformations
- **Run extensive hyperparameter searches:** Grid search across dozens of combinations without waiting hours
- **Iterate on feature engineering:** Use feature importance scores to guide what to keep, drop, or engineer further

This speed makes decision trees ideal for the exploratory phase of my project — understanding the data before committing to computationally expensive models.

## Limitations and How I'd Address Them

**Key limitations for financial data:**

| Limitation | Impact on Market Prediction | Mitigation |
|------------|----------------------------|------------|
| **Overfitting** | Trees memorise historical patterns that don't repeat | Use aggressive pruning, cross-validation, and ensemble methods |
| **Instability** | Small data changes produce very different trees | Use Random Forest or Gradient Boosting for stability |
| **Axis-aligned splits** | Can't capture diagonal relationships between features | Feature engineering to create ratio-based or interaction features |
| **No temporal awareness** | Treats each observation independently | Include lagged features and use time-aware validation |
| **Sensitive to noise** | Financial data is extremely noisy | Require minimum samples per split/leaf; focus on robust features |

**My strategy:**
- Use decision trees for **exploration and benchmarking** — understanding feature importance and establishing baseline performance
- Move to **ensemble methods** (Random Forest, XGBoost) for final predictions — they combine many trees to reduce variance and improve stability
- Apply **strict time-based validation** — never let future data leak into training
- Keep the model **relatively simple** — in financial prediction, complex models often underperform because they overfit

Decision trees won't be my final model, but they're invaluable for understanding what drives market returns and setting a transparent, interpretable baseline against which more sophisticated approaches can be compared.
