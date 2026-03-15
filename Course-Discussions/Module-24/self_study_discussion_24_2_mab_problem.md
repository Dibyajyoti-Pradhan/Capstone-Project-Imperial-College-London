# Self-study Discussion 24.2 — Applying RL to the MAB Problem

**Module:** 24 — Reinforcement Learning
**Type:** Self-study (not graded)
**Cohort:** IMP-PCMLAI-25-08

---

## 1. Agent, Actions, Rewards, Environment

| RL Component | Marketing Equivalent |
|:-------------|:--------------------|
| Agent | The ad-selection algorithm |
| Actions | Display ad A, B, or C to the current visitor |
| Reward | 1 (click) or 0 (no click) |
| Environment | The stream of visitors with unknown click propensities |
| State | Stateless — classic MAB assumes i.i.d. visitors |

The agent observes no state transitions; each visitor is treated as an independent trial. This is precisely why MAB — rather than full RL — is the appropriate framework here.

---

## 2. Exploration vs Exploitation in Ad Selection

After each round, the agent updates its estimated CTR per ad. Two strategies illustrate the trade-off:

- **Exploitation:** Always show the ad with the highest estimated CTR. Risk: if Ad B received only two clicks early, it may be over-exploited before a truer estimate forms.
- **Exploration:** Occasionally serve lower-ranked ads to refine estimates. Risk: wasted impressions on inferior ads, reducing conversions.

**ε-greedy** balances these directly: with probability ε show a random ad (explore), otherwise show the best-known ad (exploit). **UCB** provides a principled alternative — selecting the ad that maximises CTR estimate + confidence bonus, naturally reducing exploration as data accumulates.

---

## 3. Adapting to Non-Stationary CTR

If Ad B's CTR declines — due to audience fatigue or seasonal shifts — a static bandit algorithm will lag, continuing to exploit B based on stale estimates. Solutions:

- **Sliding window:** Weight only recent k impressions, discarding old data
- **Discounted UCB:** Multiply historical rewards by decay factor γ < 1
- **Restless bandits:** Model each arm as having a time-varying latent state

These approaches convert the stationary MAB into a non-stationary one, more representative of real marketing environments.

---

## 4. Feedback Signal for Policy Refinement

The binary click/no-click signal is a *sparse, immediate reward*. The agent refines its policy by updating each arm's estimated mean reward:

**Q(a) ← Q(a) + α[r − Q(a)]**

This incremental update is equivalent to a running average. Each impression provides an unbiased sample of the arm's true CTR, progressively reducing estimation variance.

---

## 5. Gittins Index

The Gittins index assigns each arm a single value representing the *opportunity cost of exploring that arm* — the maximum guaranteed reward rate achievable by focusing on it alone. Specifically, it answers: "What constant reward rate would make me indifferent between pulling this arm and accepting a fixed payment?"

**Balancing exploration and exploitation:** The agent always pulls the arm with the highest Gittins index. Poorly-sampled arms have inflated indices (high uncertainty bonus), naturally incentivising exploration. As evidence accumulates, the index converges toward the true CTR, shifting the agent toward exploitation — without any manual ε tuning.

---

## 6. Real-World MAB Analogy: Clinical Trial Dosing

In adaptive clinical trials, a physician chooses between dosage levels A, B, C for a new drug. Each administration yields a binary outcome (response / no response). A pure A/B/n test wastes patients on inferior doses; MAB with Thompson Sampling continuously shifts allocation toward the best-responding dose as evidence accumulates — improving patient outcomes *during* the trial, not just informing future practice. This directly mirrors the ad scenario: actions are doses, rewards are treatment responses, and the environment is the heterogeneous patient population.

---

*~470 words*
