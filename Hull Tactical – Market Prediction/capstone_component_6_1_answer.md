# Capstone Component 6.1 – Execution Plan

In Required Capstone Component 4.1 I selected the **Hull Tactical – Market Prediction** competition on Kaggle, which focuses on predicting S&P 500 returns from financial time-series data. This execution plan outlines how I will approach the capstone project from here to the deadline.

## Time Management Strategy

I will structure my remaining time into four phases, aligned with the module schedule:

- **Weeks 1–2 (Data Exploration & Baseline):** Download and explore the Hull Tactical dataset. Profile the financial features, check for missing values, understand temporal ordering and establish a preprocessing pipeline. Build a simple baseline (e.g. linear regression on lagged returns) so I have a reference score from day one.

- **Weeks 3–6 (Model Development & Tuning):** Each week I will apply the technique introduced in the current module — progressing from regularised regression through decision trees, random forests and gradient-boosted trees. I will submit predictions weekly to benchmark against the leaderboard and log every result.

- **Weeks 7–8 (Evaluation & Refinement):** Freeze new model experiments and focus on hyperparameter tuning, cross-validation and error analysis. Compare all logged results and select the best-performing approach.

- **Weeks 9–10 (Documentation & Final Submission):** Finalise results, write up methodology, produce visualisations and polish the GitHub repository.

**Time allocation:** ~50% model building and tuning, ~30% data exploration and feature engineering, ~20% documentation and review.

## Model Improvement Approach

- **Results log:** I will maintain a Markdown table (or CSV) recording every experiment's date, model type, key hyperparameters, validation score and test score. This is informed by my earlier Data Split Strategy Analysis, where I saw how split ratios affect reported accuracy.

- **Version control:** All code will be committed to GitHub with descriptive messages, so every experiment is reproducible.

- **Decision rule:** I will continue improving the current model as long as incremental changes yield measurable gains. If validation performance plateaus for two consecutive iterations, I will switch to a different model family rather than over-tuning.

- **Validation strategy:** Because this is time-series data, I will use time-aware forward-chaining splits (expanding or sliding window) rather than random k-fold, to avoid look-ahead bias and respect temporal ordering.

## Collaboration and Feedback

- Post intermediate results and challenges on the discussion board to invite peer feedback.
- Review classmates' approaches, particularly around feature engineering and preprocessing choices for financial data, and incorporate useful ideas.
- Use office hours for targeted guidance on time-series pitfalls such as look-ahead bias, non-stationarity and regime changes.
- Request a peer review of my GitHub repository at the end of Week 8 to catch documentation gaps before final submission.

## Risk Management

**Key risks and mitigations:**

| Risk | Mitigation |
|------|------------|
| Overfitting to historical market patterns | Use forward-chaining validation, regularisation and monitor the validation-test gap closely |
| Look-ahead bias in time-series data | Use expanding-window splits; never shuffle temporal data; carefully lag all features |
| Running out of time | Baseline model is built in Weeks 1–2, so I always have a fallback submission |
| Unfamiliarity with financial time-series methods | Dedicate Week 0 to researching past winners' notebooks and time-series best practices before coding |

I will conduct a brief weekly review against milestones and adjust scope if I fall behind.

## Public GitHub Portfolio Strategy

All work will live in my public repository ([Capstone-Project-Imperial-College-London](https://github.com/dibyajyotipradhan/Capstone-Project-Imperial-College-London)). Planned structure:

```
├── Data-Split-Strategy-Analysis/          # Completed earlier
├── Hull-Tactical-Market-Prediction/
│   ├── notebooks/                         # EDA and experiment notebooks
│   ├── src/                               # Reusable preprocessing and model code
│   └── README.md                          # Problem description, approach and results
└── README.md                              # Project overview linking all components
```

To attract positive recruiter attention I will ensure: a clear top-level README summarising the problem, approach and key results; modular, well-commented code; reproducibility instructions; and visualisations of model performance progression across iterations.
