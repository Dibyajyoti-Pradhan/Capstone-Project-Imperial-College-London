# Self-study Discussion 24.3 — Applications of RL in My Industry

**Module:** 24 — Reinforcement Learning
**Type:** Self-study (not graded)
**Cohort:** IMP-PCMLAI-25-08

---

**Industry:** Quantitative Finance / Systematic Trading (Hull Tactical Asset Allocation)

**Challenge:** Dynamic portfolio rebalancing — deciding when and how much to shift allocations across asset classes (equities, bonds, commodities) to maximise risk-adjusted returns over rolling horizons.

---

## 1. Approach Selection: Model-Based

A **model-based** approach is most appropriate here. Financial markets have well-studied structural properties — mean reversion, momentum, volatility clustering — that enable partial environment modelling without full observability. Key considerations:

- **Simulation availability:** Historical market data enables realistic backtesting environments (e.g. OpenAI Gym-compatible market simulators)
- **Safety:** Model-free exploration in live markets is financially catastrophic; a learned world model allows safe policy optimisation offline before deployment
- **Interpretability:** Regulators and risk committees require explainable allocation rationale — model-based agents expose their transition assumptions explicitly
- **Sample efficiency:** Market regimes shift infrequently; model-free methods require millions of transitions to converge, whereas model-based agents generalise from hundreds of episodes

---

## 2. Data Requirements

| Data type | Role |
|:----------|:-----|
| Price/return time series | Primary state representation |
| Macro indicators (VIX, yield spreads) | Regime context features |
| Portfolio positions + P&L | Reward computation |
| Execution logs (slippage, fill rates) | Cost-aware reward shaping |

Ensuring relevance: stratified sampling across bull, bear, and sideways regimes prevents the agent from learning policies that only generalise to one market condition.

---

## 3. Limitations and Trade-offs

**Model-free limitations:**
- Extreme sample inefficiency — financial episodes are non-i.i.d. and serially correlated
- Unstable training under regime shifts; reward variance is high
- No safety guarantees during exploration phases

**Model-based limitations:**
- Model misspecification risk: a world model trained on 2010–2020 data will underestimate tail risks during COVID-style dislocations
- Engineering overhead: maintaining a calibrated market simulator is non-trivial
- Compounding errors in multi-step rollouts reduce planning reliability at long horizons

---

## 4. Optimisation Strategies

- **Reward shaping:** Penalise turnover and drawdown alongside raw returns; prevents the agent from chasing volatile signals
- **Experience replay with prioritised sampling:** Oversample rare high-volatility episodes to improve tail-risk policies
- **Discount factor γ:** Set near 0.99 to capture long-horizon compound returns; too low collapses the agent to myopic day-trading
- **Hyperparameter tuning:** Use Bayesian optimisation (directly applying BBO capstone principles) over learning rate, entropy coefficient, and reward scaling — treating validation Sharpe ratio as the black-box objective

---

## 5. Deployment and Monitoring

- **Drift detection:** Monitor KL-divergence between live state distributions and training distributions; flag when feature correlations shift beyond thresholds
- **Shadow deployment:** Run the RL agent in paper-trading mode alongside the production strategy before capital allocation
- **Periodic retraining:** Rolling 12-month fine-tuning windows to absorb new regime data without catastrophic forgetting (using EWC regularisation)
- **Circuit breakers:** Hard position limits and drawdown thresholds override RL decisions — a safety layer that model-free agents cannot self-enforce

---

*~480 words*
