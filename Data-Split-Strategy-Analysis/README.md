# Data Split Strategy Analysis

An analysis of how different train/validation/test split ratios affect machine learning model performance using Logistic Regression on the Wine dataset.

## Table of Contents
- [Overview](#overview)
- [Experiment Results](#experiment-results)
- [Observations](#observations)
- [Key Takeaways](#key-takeaways)
- [How to Run](#how-to-run)
- [File Structure](#file-structure)

## Overview

This experiment investigates the impact of different data split strategies on model generalization. Three split configurations were tested:

| Split | Training | Validation | Test |
|-------|----------|------------|------|
| 70:15:15 | 70% | 15% | 15% |
| 60:20:20 | 60% | 20% | 20% |
| 80:20 (No Val) | 80% | - | 20% |

**Dataset**: Wine dataset (178 samples, 13 features, 3 classes)
**Model**: Logistic Regression

## Experiment Results

### Summary Table

| Split Ratio | Training Samples | Validation Samples | Test Samples | Validation Acc | Test Acc |
|-------------|------------------|-------------------|--------------|----------------|----------|
| 70:15:15 | 124 | 27 | 27 | **100.00%** | 96.30% |
| 60:20:20 | 106 | 36 | 36 | 94.44% | **97.22%** |
| 80:20 | 142 | N/A | 36 | N/A | **97.22%** |

### Detailed Results

**70:15:15 Split:**
- Perfect validation accuracy (100%) but lower test accuracy (96.30%)
- Possible overfitting signal: validation set may be too small to reliably estimate generalization

**60:20:20 Split:**
- More realistic validation accuracy (94.44%)
- Higher test accuracy (97.22%)
- Larger validation/test sets provide more stable performance estimates

**80:20 Split (No Validation):**
- Highest training data available (142 samples)
- Same test accuracy as 60:20:20 split (97.22%)
- No intermediate validation for hyperparameter tuning

## Observations

### 1. Impact of 60:20:20 Split on Model Accuracy

The 60:20:20 split yielded a **test accuracy of 97.22%**, which is slightly higher than the 70:15:15 split (96.30%). Despite having fewer training samples (106 vs 124), the model performed comparably well. This suggests that for this dataset:

- The additional 18 training samples (70% vs 60%) did not significantly improve model learning
- Larger validation and test sets (36 samples each) provide more reliable performance estimates
- The slight improvement in test accuracy may be due to better sample representation in larger test sets

### 2. Performance Comparison: 70:15:15 vs 60:20:20

| Metric | 70:15:15 | 60:20:20 | Difference |
|--------|----------|----------|------------|
| Validation Accuracy | 100.00% | 94.44% | -5.56% |
| Test Accuracy | 96.30% | 97.22% | +0.92% |

**Key Finding**: The 70:15:15 split showed perfect validation accuracy but lower test accuracy. This discrepancy indicates that:

- **Small validation sets can be misleading**: With only 27 samples, the validation set may not capture enough variability
- **Larger evaluation sets are more stable**: The 60:20:20 split provides a more realistic gap between validation and test performance
- **Overfitting detection**: The 100% validation accuracy in 70:15:15 could mask potential overfitting issues

### 3. Consequences of Omitting the Validation Set

When using only training and testing data (80:20 split):

**Risks:**
- **No hyperparameter tuning safety net**: Without a validation set, you risk tuning hyperparameters directly on test data, leading to data leakage
- **Overfitting to test set**: Iterative model improvements based on test performance essentially "trains" on the test set
- **Unreliable generalization estimates**: The final test accuracy may be overly optimistic

**When it might be acceptable:**
- Very simple models with no hyperparameters to tune
- Extremely limited data where every sample is precious for training
- When using cross-validation as an alternative

**Recommendation**: Always maintain a separate validation set for hyperparameter tuning. Use the test set only for final, unbiased performance evaluation.

### 4. Application to Capstone Project

**Best Practices for Model Reliability:**

1. **Choose split ratios based on dataset size:**
   - Large datasets (>10,000 samples): 70:15:15 or even 80:10:10
   - Medium datasets (1,000-10,000): 60:20:20 is safer
   - Small datasets (<1,000): Consider cross-validation

2. **Use stratified splitting**: Ensures class distribution is preserved across all splits (as done in this experiment with `stratify=y`)

3. **Set random states**: Use `random_state=42` or similar for reproducibility

4. **Monitor the validation-test gap**: Large discrepancies may indicate:
   - Validation set is too small
   - Data distribution issues
   - Potential data leakage

5. **Consider cross-validation**: For small datasets, k-fold cross-validation provides more robust estimates than a single train/val/test split

## Key Takeaways

1. **Larger validation/test sets = more reliable estimates**: Even at the cost of some training data
2. **Perfect validation scores are suspicious**: Often indicate the validation set is too small
3. **Always keep test data separate**: Never tune based on test performance
4. **The "right" split depends on context**: Dataset size, model complexity, and project requirements all matter
5. **Stratification is essential**: Especially for imbalanced or multi-class problems

## How to Run

```bash
# Navigate to the project directory
cd Data-Split-Strategy-Analysis

# Run the solution script
python solution.py
```

**Requirements:**
```
scikit-learn>=0.24.0
```

## File Structure

```
Data-Split-Strategy-Analysis/
├── README.md          # This file - observations and analysis
├── problem.md         # Problem statement and objectives
└── solution.py        # Python implementation with all experiments
```

---

*This analysis is part of the Imperial College London Capstone Project on Machine Learning.*
