# Required Discussion 21.3: Considerations when dealing with ML models

## Trade-offs Between Interpretability, Fairness and Accuracy

---

### 1. Interpretability vs Accuracy: A Market Prediction Example

In the Hull Tactical capstone, I encountered this trade-off directly. XGBoost substantially outperforms logistic regression on directional accuracy by capturing nonlinear interactions — for example, high VIX coinciding with negative momentum behaves differently from either variable in isolation. A simpler model misses this. However, a compliance officer cannot explain to a regulator *why* the model issued a short signal at a particular moment. Under frameworks like MiFID II, firms must demonstrate model accountability; a high-accuracy black box may generate stronger returns but expose the firm to regulatory censure. The consequence for trust is asymmetric: stakeholders lose confidence in opaque models during drawdowns, precisely when accountability matters most.

---

### 2. Strategies to Improve Interpretability and Their Trade-offs

SHAP values provide both global feature attribution and local explanations for ensemble models. Applied to the Hull Tactical dataset, SHAP reveals that momentum and volatility measures dominate predictions — consistent with financial intuition, which validates the model. However, SHAP applied to temporally correlated time-series features can be misleading if lag structure is not respected: the attributed "importance" of a lagged feature may reflect autocorrelation rather than genuine predictive content. Post-hoc explanations thus add interpretability without altering the model, but they approximate rather than expose the true decision boundary — a useful but imperfect safeguard.

---

### 3. Why Interpretability and Fairness Can Be at Odds

In financial markets, "fairness" operates differently from healthcare or hiring — it concerns systemic risk and equal market access rather than demographic parity. A simple, transparent model visible to competitors can be reverse-engineered, enabling front-running. A complex opaque model protects alpha but creates systemic risk if many institutions deploy correlated strategies simultaneously (a recognised driver of flash crashes). Regulators seek interpretability for oversight, but full transparency may itself introduce unfairness by allowing exploitation of disclosed logic. This is a domain where the standard advice — "prefer interpretable models in high-stakes settings" — requires contextual qualification. A simple model can perpetuate historical biases encoded in financial data; a complex model may reduce those biases but resist audit.

---

### 4. Decision Complexity as a Practical Metric

Jo et al.'s (2022) decision complexity metric could function as a governance constraint analogous to how the BBO challenge imposed query budgets: practitioners optimise performance *within* a complexity ceiling rather than unconstrained. A financial regulator could mandate a maximum decision complexity as a condition of model approval, and firms would tune accordingly. The benefit is objectivity — decision complexity provides a quantifiable, auditable standard that reduces subjectivity in interpretability claims.

The key limitation is that structural simplicity does not guarantee semantic clarity. A depth-4 decision tree using PCA-derived features is structurally simple but cognitively opaque: a trader cannot intuitively understand a signal driven by "principal component 2." Decision complexity must therefore be paired with feature interpretability requirements to be practically meaningful.

---

### 5. Balancing Stakeholder Demands in Deployment

If deploying a live market prediction system, I would structure the decision as a constrained optimisation: maximise risk-adjusted returns subject to (a) a regulatory interpretability threshold, (b) documentation of model risk, and (c) human override capability for out-of-distribution market regimes.

The factors that matter most in this context are: (i) downside risk from model failure outweighs upside from marginal accuracy gains — the asymmetry of consequences forces conservatism; (ii) regulatory approval is a hard constraint, not a trade-off variable; (iii) interpretability enables human override, which is critical when models encounter regime changes entirely outside the training distribution — precisely the scenario where accuracy claims break down. Stakeholders demanding pure accuracy often underweight this last point: a 2% improvement in backtest accuracy is worthless if the model cannot be overridden during a crisis.

Ultimately, interpretability is not a concession to non-technical audiences — it is an operational risk management tool.

---

### References

Jo, N., Kim, B., Lee, S. and Shin, J. (2022) 'Learning optimal fair classification trees: trade-offs between interpretability, fairness, and accuracy', *Proceedings of the AAAI Conference on Artificial Intelligence*.

Caruana, R., Lou, Y., Gehrke, J., Koch, P., Sturm, M. and Elhadad, N. (2015) 'Intelligible models for healthcare: predicting pneumonia risk and hospital 30-day readmission', *Proceedings of the 21st ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, pp. 1721–1730.
