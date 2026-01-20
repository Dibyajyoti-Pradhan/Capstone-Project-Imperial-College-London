# Data Split Strategy Analysis

## Problem Statement

Understanding the balance between training, validation, and test sets is key to building ML models that generalise well beyond a single data set. This activity analyzes how different data split strategies affect the model's performance.

## Objective

Experiment with different data split ratios and observe their impact on model performance using a Logistic Regression classifier on the Wine dataset.

## Dataset

- **Dataset**: Scikit-learn's built-in Wine dataset
- **Features**: 13 chemical analysis features
- **Target**: 3 wine classes (class_0, class_1, class_2)
- **Total Samples**: 178

## Experiments

### Experiment 1: 70:15:15 Split
- **Training Set**: 70% of data
- **Validation Set**: 15% of data
- **Test Set**: 15% of data

### Experiment 2: 60:20:20 Split
- **Training Set**: 60% of data
- **Validation Set**: 20% of data
- **Test Set**: 20% of data

## Key Questions to Address

1. **What impact does the 60:20:20 split have on model accuracy?**

2. **How does the model's performance change if you use a 70:15:15 split?**

3. **What might happen if you omitted the validation set and only used training and testing data?**

4. **How can you apply what you've learned from experimenting with different data splits and model types to improve your capstone project's model performance and reliability?**

## Technical Notes

### Understanding the Split Calculations

**For 70:15:15 Split:**
- First split: 15% for test (test_size=0.15)
- Second split: 17.65% of remaining 85% for validation
- Calculation: 0.1765 * 0.85 = 0.15 (15% of total)

**For 60:20:20 Split:**
- First split: 20% for test (test_size=0.20)
- Second split: 25% of remaining 80% for validation
- Calculation: 0.25 * 0.80 = 0.20 (20% of total)

## Dependencies

```
scikit-learn
```

## References

- [Scikit-learn Wine Dataset](https://scikit-learn.org/stable/datasets/toy_dataset.html#wine-dataset)
- [Train/Test/Validation Split Best Practices](https://scikit-learn.org/stable/modules/cross_validation.html)
