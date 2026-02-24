# Self-Study Discussion 10.1 – Analysing Bagging Techniques

## Context: Predicting Customer Purchase Likelihood

This exercise demonstrates how bagging (Bootstrap Aggregating) works in practice using three decision trees that predict whether a customer is likely to purchase soon based on their behaviour.

### Customer Behaviour Data

| Customer | Last purchase >6 months ago? | Last purchase >£10? | Visited site >once in last 2 days? |
|----------|------------------------------|---------------------|-----------------------------------|
| 1 | No | No | Yes |
| 2 | Yes | Yes | No |

---

## Question 1: What is your final prediction for each customer based on the majority vote across the three trees?

| Customer | Final Prediction |
|----------|------------------|
| **Customer 1** | **Likely to purchase soon** |
| **Customer 2** | **Unlikely to purchase soon** |

**Customer 1** receives a "Likely" prediction because 2 out of 3 trees (Tree 2 and Tree 3) classify them as likely to purchase, while only Tree 1 classifies them as unlikely.

**Customer 2** receives an "Unlikely" prediction because 2 out of 3 trees (Tree 2 and Tree 3) classify them as unlikely to purchase, while only Tree 1 classifies them as likely.

---

## Question 2: How did each tree classify the customer?

### Customer 1 Classification

| Tree | Decision Path | Classification |
|------|---------------|----------------|
| **Tree 1** | Last purchase ≤6 months ago → Last purchase ≤£10 → **Unlikely** | Unlikely |
| **Tree 2** | Last purchase ≤6 months ago → Last purchase ≤£10 → Visited recently (Yes) → **Likely** | Likely |
| **Tree 3** | Last purchase ≤£10 → Last purchase ≤6 months ago → Visited recently (Yes) → **Likely** | Likely |

**Tree 1** stops at the low purchase value and immediately classifies as unlikely, ignoring the recent site visits.

**Tree 2** and **Tree 3** both consider the recent site activity and recognise that a customer actively browsing the site signals purchase intent.

### Customer 2 Classification

| Tree | Decision Path | Classification |
|------|---------------|----------------|
| **Tree 1** | Last purchase >6 months ago → Last purchase >£10 → **Likely** | Likely |
| **Tree 2** | Last purchase >6 months ago → No recent site visits → **Unlikely** | Unlikely |
| **Tree 3** | Last purchase >£10 → No recent site visits → **Unlikely** | Unlikely |

**Tree 1** sees a high-value past customer and optimistically predicts they'll return.

**Tree 2** and **Tree 3** both recognise that without recent site engagement, even a previously valuable customer is unlikely to convert soon.

---

## Question 3: How did you arrive at the majority decision?

I applied **majority voting**, which is the standard aggregation method in bagging for classification tasks:

### Step-by-Step Process

**Step 1:** Trace each customer through all three decision trees to obtain individual predictions.

**Step 2:** Count the votes for each class.

| Customer | Likely Votes | Unlikely Votes |
|----------|--------------|----------------|
| 1 | 2 (Tree 2, Tree 3) | 1 (Tree 1) |
| 2 | 1 (Tree 1) | 2 (Tree 2, Tree 3) |

**Step 3:** Assign the class with the most votes as the final prediction.

- **Customer 1:** 2 Likely vs 1 Unlikely → **Likely** wins
- **Customer 2:** 1 Likely vs 2 Unlikely → **Unlikely** wins

### Summary Table

| Customer | Tree 1 | Tree 2 | Tree 3 | Majority Vote | Final Prediction |
|----------|--------|--------|--------|---------------|------------------|
| 1 | Unlikely | Likely | Likely | 2-1 Likely | **Likely to purchase soon** |
| 2 | Likely | Unlikely | Unlikely | 2-1 Unlikely | **Unlikely to purchase soon** |

---

## Question 4: What does this process demonstrate about how bagging works in practice?

This exercise illustrates several key principles of bagging:

### 1. Diversity is Essential
Each tree uses the same three features but structures its decisions differently — Tree 1 starts with recency, Tree 2 also starts with recency but branches differently, and Tree 3 starts with purchase value. This structural diversity means trees make different errors, which is precisely what makes combining them valuable.

### 2. Individual Errors Get Corrected
Tree 1 made questionable predictions for both customers — it missed Customer 1's purchase intent (ignoring their active site engagement) and was overly optimistic about Customer 2 (ignoring their lack of recent engagement). The ensemble corrected both errors through majority voting.

### 3. Majority Voting Reduces Variance
A single tree can be sensitive to the specific patterns it learned. By requiring a majority to agree, bagging smooths out these idiosyncrasies and produces more stable, reliable predictions.

### 4. The "Wisdom of Crowds" Effect
For a bagged ensemble to make a wrong prediction, the *majority* of trees must be wrong simultaneously. If individual trees have independent errors, the probability of majority failure is mathematically much lower than individual tree failure. This is why ensembles consistently outperform single models.

### 5. Practical Trade-off
The ensemble sacrificed Tree 1's correct classification of Customer 2 (as Likely) in favour of the majority view. In practice, this trade-off is worthwhile because the ensemble's overall accuracy across many predictions will be higher than any single tree's accuracy.

---

## Connection to My Capstone Project

In my Hull Tactical market prediction project, bagging through Random Forests provides these same benefits:

- **Reduced overfitting:** A single tree might memorise historical patterns that don't repeat; an ensemble captures more robust signals.
- **Stable predictions:** Financial markets are noisy; bagged models produce smoother, more consistent forecasts.
- **Error correction:** When one tree makes a poor prediction due to noise in its training subset, other trees compensate.

The customer purchase example demonstrates exactly why ensemble methods have become the standard approach in machine learning — they harness diversity to achieve accuracy that individual models cannot match.
