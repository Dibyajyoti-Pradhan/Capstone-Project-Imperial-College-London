# Required Capstone Component 21.2 — Reflecting on Transparency and Interpretability

**Module:** 21 — Transparency and Interpretability
**Submitted:** 02/03/2026
**Cohort:** IMP-PCMLAI-25-08

---

## Submission

Datasheet and Model Card have been created, updated to reflect 12 rounds of queries and 21 data points, and are publicly available in the GitHub repository:

- **DATASHEET.md:** [View on GitHub](https://github.com/Dibyajyoti-Pradhan/Capstone-Project-Imperial-College-London/blob/main/Black-Box-Optimisation-Challenge/DATASHEET.md)
- **MODEL_CARD.md:** [View on GitHub](https://github.com/Dibyajyoti-Pradhan/Capstone-Project-Imperial-College-London/blob/main/Black-Box-Optimisation-Challenge/MODEL_CARD.md)

Both are linked in the [README.md](https://github.com/Dibyajyoti-Pradhan/Capstone-Project-Imperial-College-London/blob/main/Black-Box-Optimisation-Challenge/README.md) under the Documentation section.

---

## Datasheet Summary (Gebru et al., 2021)

| Section | Key Content |
|:--------|:-----------|
| **Motivation** | Supports BBO maximisation of 8 unknown functions; full audit trail of strategy decisions |
| **Composition** | 8 functions × ~13 queries + initial data; input–output tuples in [0,1)^d; sparse by necessity |
| **Collection** | Three-phase: max-distance exploration → GP-UCB with SVM → hybrid GP + neural surrogates |
| **Preprocessing** | Coordinates standardised to 6 decimal places; raw outputs preserved |
| **Distribution** | Public GitHub repo, MIT Licence |
| **Maintenance** | Static on programme completion; corrections documented via Git commits |

**Key transparency insight:** The dataset is explicitly exploitation-biased — ~60% of F5 and F8 queries cluster in high-output corridors. This is documented as a gap rather than concealed, enabling future researchers to understand the limits of any conclusions drawn from it.

---

## Model Card Summary (Mitchell et al., 2019)

| Section | Key Content |
|:--------|:-----------|
| **Overview** | Hybrid GP–SVM–Neural BBO Optimiser, v1.0 (Round 12) |
| **Intended use** | Unknown scalar functions, d ∈ {2,…,8}, ≤15 evaluations; not for d > 20 or real-time use |
| **Strategy details** | Phase 1: max-distance; Phase 2: GP-UCB + SVM; Phase 3: MLP gradient ascent + trust regions |
| **Performance** | F5 best: ~1600+ near boundary (0.999)⁴; F8: X₁/X₃ dominant; F1/F7 still uncertain |
| **Assumptions** | Stationarity (violated for F5); local smoothness; bounded optimum in [0,1)^d |
| **Limitations** | Single-query constraint; curse of dimensionality for F8; no uncertainty in MLP phase |
| **Ethics** | Full reproducibility through documented hypotheses; mirrors model card best practice |

---

## Reflection: How Transparency Supports the Strategy

Creating these documents forced two important clarifications:

1. **The stationarity assumption:** Articulating it explicitly revealed that the GP is over-smoothing the F5 peak. A non-stationary kernel (deep kernel learning) would be theoretically superior, but data constraints prevent adoption. Documenting this in the model card turns a hidden weakness into an acknowledged limitation — enabling future researchers to address it.

2. **The exploitation bias:** The datasheet's composition section required honest accounting of query distribution. Acknowledging that F7 and the interior of F8's hypercube are almost entirely unsampled clarifies the scope of what the strategy has actually learned. This is not a failure to hide but a boundary condition to communicate.

Both insights emerged from the act of documentation itself — not retrospectively rationalising decisions but genuinely stress-testing them by writing them down.

---

## References

Gebru, T. et al. (2021) 'Datasheets for datasets', *Communications of the ACM*, 64(12), pp. 86–92.

Mitchell, M. et al. (2019) 'Model cards for model reporting', *Proceedings of FAccT*, pp. 220–229.
