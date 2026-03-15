# Required Discussion 23.2 — ML Methods That Impact My Field

**Module:** 23 — Dimensionality Reduction
**Type:** Required (graded)
**Cohort:** IMP-PCMLAI-25-08

---

## 1. Path Similarities and Differences

Jacopo's and Shawn's trajectories both illustrate a pattern I recognise in myself: a transition from domain expertise toward ML fluency, driven by the recognition that quantitative methods increasingly define competitive advantage in their fields. Where their paths likely began from pure data science or engineering disciplines and expanded into industry applications, mine runs in roughly the reverse direction — I entered from a finance and investment background and am now building the technical ML infrastructure to make that domain expertise computationally rigorous.

The key similarity is the hybrid profile: neither Jacopo nor Shawn appears to have succeeded by becoming purely technical at the expense of domain knowledge, or vice versa. The differentiating value lies precisely in the combination — being able to ask the right questions of data and also understand the mechanisms that generate it. In quantitative finance, this is sometimes called the "quant-with-intuition" profile: knowing when the model is right for the wrong reason.

The key difference is timeline and context. Their careers likely unfolded as ML was becoming mainstream; I am building capability in an environment where ML in finance has already moved from competitive advantage to table stakes, and the frontier has shifted to foundation models, alternative data, and real-time inference at scale.

---

## 2. How ML Methods Support My Professional Goals

My goal is to build and manage systematic investment strategies that are explainable, robust under regime change, and scalable across asset classes. The methods from this programme map directly onto that objective:

| Programme Method | Application in Systematic Finance |
|:-----------------|:----------------------------------|
| Gaussian Processes / BBO | Signal discovery, hyperparameter optimisation for alpha models |
| SVMs | Regime classification, credit risk scoring |
| Neural Networks (MLP, LSTM) | Return prediction, volatility forecasting |
| CNNs | Pattern recognition in price chart representations, correlation matrix analysis |
| PCA | Factor model construction, risk decomposition, signal decorrelation |
| Clustering (K-means, hierarchical) | Asset grouping, sector rotation, strategy diversification |
| RL / MAB | Dynamic portfolio rebalancing, adaptive allocation |

The through-line across all of these: they convert high-dimensional, noisy, non-stationary market data into actionable signals with quantified uncertainty.

---

## 3. Methods Meriting Further Study

Three methods stand out as highest priority for deeper investment:

**1. Gaussian Processes and Bayesian Optimisation**
The BBO capstone project was the most directly transferable module in the programme. Every alpha research problem — finding the best signal parameterisation, optimising portfolio construction rules, tuning execution algorithms — is a black-box optimisation problem with expensive evaluations. GP-UCB provides sample-efficient search that outperforms grid search by orders of magnitude. This warrants formal study beyond the programme, including TuRBO for high-dimensional extensions and BoTorch for production deployment.

**2. Recurrent and Temporal Architectures (LSTMs, Temporal CNNs)**
Financial time series are fundamentally sequential; methods that ignore temporal structure leave substantial predictive power untapped. LSTMs and temporal convolutional networks are particularly relevant for macro regime modelling — identifying whether we are in a growth, inflation, or contraction regime determines which alpha signals should be active. Further study of attention mechanisms (Transformers for time series) is a natural extension.

**3. Reinforcement Learning**
Dynamic portfolio construction is a sequential decision problem under uncertainty — exactly the RL framework. Most current industry implementations use simplified heuristics; genuine RL-based rebalancing remains an open research area with material practical upside. The main obstacle is sample efficiency in non-stationary environments — a problem I now have specific vocabulary and tools to address.

---

## 4. Unique Alignment with Career Goals

What makes these methods uniquely aligned is not their novelty but their structural fit with the constraints of financial decision-making: expensive evaluations (you cannot A/B test a portfolio strategy 10,000 times), non-stationarity (market regimes shift), interpretability requirements (regulators and investors demand explanations), and tail risk sensitivity (catastrophic failure modes matter more than average performance).

The methods above are precisely those that balance predictive power with uncertainty quantification, sample efficiency, and robustness — the combination that separates deployable strategies from academic exercises.
