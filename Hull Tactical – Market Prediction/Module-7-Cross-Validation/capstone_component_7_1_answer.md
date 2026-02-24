# Capstone Component 7.1 – Applying Oversampling and Cross-Validation

For my capstone project, I chose the **Hull Tactical – Market Prediction** competition on Kaggle. The goal is to predict S&P 500 returns using financial time-series data. While this is fundamentally a regression problem, I can also frame parts of it as classification — for instance, predicting whether the market will move up or down, or flagging unusually large return days. That's where class imbalance comes into play.

## Will the Data Be Imbalanced?

Most likely, yes. In real markets, big moves — the kind that really matter for trading — are relatively rare. On most days, returns cluster around zero or small changes. If I try to classify "strong positive return" versus "everything else," the strong-return class will be a clear minority.

The risk here is that a model trained on imbalanced data might just learn to predict "no big move" most of the time. It would look accurate on paper, but it would miss the signals that actually matter for making money. That's why oversampling could help during hyperparameter tuning — it ensures the model gets enough exposure to these rare-but-important events so we're not just optimising for the boring majority.

## How Oversampling Helps

By boosting the representation of minority-class examples (like strong upward moves or market regime shifts), oversampling pushes the model to actually learn what distinguishes those cases. Instead of ignoring them, the model has to pay attention. For a trading-focused problem, this means better recall on the signals that drive investment decisions — which is ultimately what we care about.

## When to Apply Oversampling

This is where things can go wrong if you're not careful. Oversampling needs to happen **inside each cross-validation fold**, applied only to the training portion. If you oversample before splitting, you risk leaking information — duplicated or synthetic samples might end up in both training and validation sets, which inflates your metrics and gives you a false sense of how well the model is doing.

Since I'm working with time-series data, I'll use forward-chaining cross-validation (where training always comes before validation in time). Within each fold, I'll oversample the training data, train the model, and then evaluate on the untouched validation set. This keeps things realistic and avoids peeking into the future.

## What Can Go Wrong

If oversampling is applied incorrectly — say, before splitting — a few things happen:

- **Inflated metrics:** The model looks great during validation but fails on new data.
- **Overfitting:** The model memorises synthetic patterns instead of learning real ones.
- **Bad hyperparameters:** You end up tuning for a biased version of the data, not the real distribution.

All of this erodes trust in the results and can lead to poor decisions when the model is deployed.

## My Workflow Plan

Here's how I plan to combine oversampling, cross-validation, and hyperparameter tuning:

1. **Prepare the data:** Clean the features, handle missing values, and engineer lagged variables. Set aside a final test set from the most recent time period.

2. **Set up cross-validation:** Use time-aware forward-chaining splits so the model never trains on future data.

3. **For each fold:**
   - Split into training and validation (validation is always the later period)
   - Apply oversampling only to the training set
   - Train the model with a given set of hyperparameters
   - Evaluate on the validation set

4. **Tune hyperparameters:** Try different combinations and pick the one with the best average performance across folds.

5. **Train the final model:** Using the chosen hyperparameters, retrain on the full training set.

6. **Test on held-out data:** Evaluate on the final test set that was never touched during tuning.

## How I'll Know the Model Generalises

The real test is whether performance on the hold-out set matches what I saw during cross-validation. If the numbers are consistent, that's a good sign the model has learned something real. If there's a big drop, it's a red flag for overfitting.

I'll also look at how the model performs across different market conditions — bull markets, bear markets, sideways periods. If it only works in one regime, that's a problem. The goal is a model that's robust enough to handle whatever the market throws at it.
