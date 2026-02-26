# Required Discussion 16.1: Identifying a Human Benchmark

## Chosen Problem: Real-Time Fraud Detection in Digital Payments

### Problem Description and Significance

The task is detecting fraudulent transactions in real-time digital payment systems, where decisions must be made within milliseconds before authorisation. In 2024 alone, global payment fraud losses exceeded $40 billion. The challenge involves analysing transaction patterns, device fingerprints, behavioural biometrics, and merchant risk profiles to distinguish legitimate purchases from fraud.

**Why DL/NN methods are well-suited:**

Deep learning excels here because fraud manifests through complex, non-linear interactions across hundreds of features. A fraudster might use a legitimate device but exhibit anomalous velocity patterns — purchasing in London, then Dubai, within an hour. Recurrent architectures capture temporal dependencies in transaction sequences, while attention mechanisms identify which historical transactions are most relevant to the current decision. Traditional rule-based systems generate either excessive false positives (declining legitimate customers) or miss sophisticated fraud patterns.

---

### Justification for Human Benchmarking

Human benchmarking is critical because fraud analysts currently serve as the second line of defence, reviewing flagged transactions and making final disposition decisions. Comparing model performance against these experts establishes whether automation can reduce manual review queues without increasing losses.

**Reference points needed:**

| Benchmark | Purpose |
|-----------|---------|
| **Expert analysts** (5+ years experience) | Gold standard for complex, ambiguous cases |
| **Junior analysts** (6-18 months) | Operational baseline reflecting real throughput |

Both are necessary — experts validate that the model captures nuanced fraud patterns, while junior analyst comparison demonstrates operational value in high-volume settings.

---

### Collecting the Human Benchmark

**Participant selection:**
- 8-10 senior fraud investigators from major payment processors
- 15-20 junior analysts handling daily transaction queues

**Metrics to record:**

| Metric | Rationale |
|--------|-----------|
| Precision | False positives directly impact customer experience |
| Recall | Missed fraud = direct financial loss |
| Decision latency | Real-time systems demand sub-second responses |
| Confidence calibration | Understanding when humans are uncertain guides model deployment |

**Ensuring representativeness:**

The evaluation dataset must include:
- Class imbalance reflecting reality (~0.1% fraud rate)
- Geographic diversity (cross-border vs domestic)
- Temporal patterns (holiday spikes, unusual hours)
- Edge cases: first-time cardholders, high-value legitimate transactions, social engineering attacks

Ground truth would be established through confirmed chargebacks and verified fraud reports, not analyst labels alone.

---

### Comparing DL Performance to Human Benchmark

The model and analysts would evaluate identical transaction batches using matched metrics. Key analytical dimensions:

1. **Stratified performance:** Segment by transaction value, merchant category, and fraud type (card-not-present vs account takeover)
2. **Disagreement analysis:** Examine cases where model and humans diverge — is the model catching subtle patterns humans miss, or making implausible errors?
3. **Latency comparison:** Humans require 30-90 seconds per case; models decide in <50ms
4. **Inter-rater reliability:** Measure analyst agreement (Cohen's kappa) to contextualise model variance

Qualitative error analysis would examine false negatives specifically — are they random misses or systematic blind spots to particular fraud vectors?

---

### Implications if DL Model Surpasses Human Benchmark

**Identified risks:**

- **Automation bias:** Analysts may rubber-stamp model decisions without scrutiny
- **Adversarial adaptation:** Fraudsters will probe and exploit model weaknesses once patterns become predictable
- **Interpretability gaps:** Explaining to a declined customer *why* their legitimate purchase was blocked becomes difficult with opaque models
- **Rare event failures:** Models trained on common fraud may miss novel attack vectors entirely

**Bias and generalisation concerns:**

Historical fraud data may encode demographic biases — flagging transactions disproportionately in certain regions or merchant categories. A model that "beats" humans while perpetuating these biases creates legal and ethical exposure under regulations like the EU AI Act.

**Responsible integration strategy:**

1. **Human-in-the-loop for high-stakes decisions:** Transactions above threshold values require analyst confirmation
2. **Confidence-based routing:** Low-certainty predictions escalate to human review rather than auto-decline
3. **Continuous monitoring:** Track precision/recall drift as fraud patterns evolve; trigger retraining when performance degrades
4. **Explainability layer:** Provide analysts with top contributing features for each flagged transaction
5. **Adversarial testing:** Regularly red-team the model with synthetic fraud scenarios

The goal is augmentation rather than replacement — using DL to handle volume while preserving human judgement for ambiguous, high-impact, or novel cases.
