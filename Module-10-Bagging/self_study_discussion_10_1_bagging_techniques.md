# Self-Study Discussion 10.1 – Analysing Bagging Techniques

## Context: Predicting Customer Purchase Likelihood

This exercise demonstrates how bagging (Bootstrap Aggregating) works in practice using three decision trees that predict whether a customer is likely to purchase soon based on their behaviour.

## Analysis of Each Decision Tree

### Tree 1
Tree 1 starts by asking whether the customer's last purchase was more than six months ago.

- **If yes (inactive customer):** It then checks whether their last purchase was worth more than £10. High-value past purchasers are classified as "Likely to purchase soon." For lower-value past purchasers, it checks recent site visits — frequent visitors are likely, infrequent visitors are unlikely.
- **If no (recent customer):** It checks purchase value. High-value recent customers are likely; low-value recent customers are unlikely.

**Key insight:** Tree 1 prioritises recency and purchase value, with site visits as a tiebreaker for dormant, low-value customers.

### Tree 2
Tree 2 also begins with the six-month recency question but branches differently.

- **If yes (inactive customer):** It immediately checks site visits. Recent site activity indicates likely purchase intent; no recent visits means unlikely.
- **If no (recent customer):** It checks purchase value first. High-value recent customers are likely. For low-value recent customers, it falls back to site visit frequency.

**Key insight:** Tree 2 places greater emphasis on recent site engagement, especially for dormant customers.

### Tree 3
Tree 3 starts with purchase value as the root node — a fundamentally different structure.

- **If yes (high-value purchaser):** Recent site visits indicate likely purchase; no visits means unlikely.
- **If no (low-value purchaser):** It checks recency. Recent low-value customers who visited the site are likely; dormant low-value customers are unlikely.

**Key insight:** Tree 3 treats purchase value as the primary discriminator, with site visits and recency as secondary factors.

---

## How Each Tree Votes

### Customer 1
**Profile:** Last purchase was NOT more than 6 months ago | Last purchase was NOT worth more than £10 | Has visited the site more than once in the last 2 days

| Tree | Decision Path | Prediction |
|------|---------------|------------|
| Tree 1 | Last purchase ≤6 months → Purchase ≤£10 → **Unlikely** | Unlikely |
| Tree 2 | Last purchase ≤6 months → Purchase ≤£10 → Visited recently → **Likely** | Likely |
| Tree 3 | Purchase ≤£10 → Last purchase ≤6 months → Visited recently → **Likely** | Likely |

### Customer 2
**Profile:** Last purchase WAS more than 6 months ago | Last purchase WAS worth more than £10 | Has NOT visited the site more than once in the last 2 days

| Tree | Decision Path | Prediction |
|------|---------------|------------|
| Tree 1 | Last purchase >6 months → Purchase >£10 → **Likely** | Likely |
| Tree 2 | Last purchase >6 months → No recent visits → **Unlikely** | Unlikely |
| Tree 3 | Purchase >£10 → No recent visits → **Unlikely** | Unlikely |

---

## Arriving at the Majority Decision

Bagging uses **majority voting** to combine predictions from multiple trees:

| Customer | Tree 1 | Tree 2 | Tree 3 | Majority Vote | Final Prediction |
|----------|--------|--------|--------|---------------|------------------|
| 1 | Unlikely | Likely | Likely | 2 Likely, 1 Unlikely | **Likely to purchase soon** |
| 2 | Likely | Unlikely | Unlikely | 1 Likely, 2 Unlikely | **Unlikely to purchase soon** |

**Customer 1:** Despite Tree 1 predicting "unlikely," the ensemble overrules this because two trees agree that recent site visits from a recent customer signal purchase intent.

**Customer 2:** Despite Tree 1 seeing a high-value past purchaser as promising, the ensemble recognises that someone who hasn't visited recently — regardless of past spending — is unlikely to convert.

---

## What This Demonstrates About Bagging

### 1. Diversity Through Different Tree Structures
Each tree uses the same three features but structures them differently, leading to different decision boundaries. This diversity is the foundation of bagging's power — if all trees were identical, combining them would offer no benefit.

### 2. Robustness Through Aggregation
Individual trees can make errors. Tree 1 missed Customer 1's purchase intent; Tree 1 was overly optimistic about Customer 2. But by aggregating votes, these individual errors are corrected by the collective wisdom of the ensemble.

### 3. Majority Voting Reduces Variance
Any single tree might overfit to specific patterns in its training data. By taking a majority vote, bagging smooths out these idiosyncrasies and produces more stable, reliable predictions.

### 4. The "Wisdom of Crowds" Effect
For a bagged prediction to be wrong, the *majority* of trees must be wrong. If each tree has, say, a 30% error rate and their errors are independent, the probability that 2 out of 3 are wrong is much lower than 30%. This is the mathematical foundation of why ensembles outperform individual models.

---

## Practical Implications

In real-world applications like my Hull Tactical market prediction project, bagging (through Random Forests) offers similar benefits:

- **Reduced overfitting:** A single decision tree might memorise historical market patterns that don't repeat; an ensemble is more likely to capture genuine, persistent signals.
- **Stable predictions:** Markets are noisy. Individual models can produce erratic signals; bagged models provide smoother, more consistent predictions.
- **Feature robustness:** If one tree over-relies on a noisy feature, other trees using different structures will counterbalance this.

The customer purchase example illustrates exactly why ensemble methods have become the standard approach in machine learning — they harness diversity to achieve accuracy that individual models cannot match.
