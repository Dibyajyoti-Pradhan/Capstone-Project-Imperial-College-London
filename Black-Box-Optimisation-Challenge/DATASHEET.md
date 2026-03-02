# Datasheet: BBO Capstone Project Dataset

> Framework: Gebru et al. (2021), *Datasheets for Datasets*

---

## Motivation

**What task does this dataset support?**
This dataset supports black-box function optimisation (BBO) — specifically, the task of maximising eight unknown functions $f_1, \ldots, f_8$ with dimensionality ranging from 2D to 8D, given a severely limited query budget (~10 evaluations per function over 10 rounds).

**Who created it, and why?**
Created by Dibyajyoti Pradhan as part of the Imperial College London Professional Certificate in Machine Learning and Artificial Intelligence (Modules 12–21). The dataset documents every query submitted and the corresponding function evaluations returned by the BBO challenge portal, providing a complete audit trail of the optimisation strategy.

**Was it funded or supported by an organisation?**
The challenge infrastructure was provided by Imperial College London. The dataset itself was generated independently through coursework submissions.

---

## Composition

**What does it contain?**
The dataset consists of input–output pairs for eight unknown functions:

| Function | Input Dimension | Approx. Queries | Output Range |
|----------|----------------|-----------------|--------------|
| F1 | 2D | ~12 | Near-zero |
| F2 | 2D | ~12 | Moderate |
| F3 | 3D | ~12 | Moderate |
| F4 | 3D | ~12 | Moderate |
| F5 | 4D | ~12 | High (~1600+) |
| F6 | 5D | ~12 | Moderate |
| F7 | 6D | ~12 | Low-moderate |
| F8 | 8D | ~12 | High |

**Format:** Each record is a tuple `(x₁, x₂, ..., x_d, y)` where each `xᵢ ∈ [0, 1)` is specified to six decimal places and `y` is the scalar function output.

**Is it complete?**
No — this is an extremely sparse sample. Each function's search space is a unit hypercube in d dimensions; the observed queries cover a negligible fraction of the domain. The dataset is sufficient for surrogate model fitting but not for exhaustive coverage.

**Gaps and missing data:**
No missing values — every submitted query received a valid output. However, sampling is heavily biased toward high-performing regions in later rounds, leaving large areas (especially in F7 and F8) unexplored.

**Subpopulations or sensitive groups:**
None. The dataset contains only numerical coordinates and scalar values; it involves no personal data, demographic information or sensitive content.

---

## Collection Process

**How were queries generated?**
Queries were generated through a three-phase strategy:

1. **Weeks 1–2 (Exploration):** Maximum-distance heuristics to achieve spatial coverage across each function's domain.
2. **Weeks 3–5 (Pattern recognition):** Output-guided search using SVM region classification and Gaussian Process (GP) surrogates with UCB acquisition functions.
3. **Weeks 6–10 (Exploitation):** Hybrid GP + neural network (MLP) surrogates with gradient-informed query placement; trust-region exploitation for high-performing functions (F5, F8).

**Time frame:** Queries were submitted weekly over approximately 10 weeks (Modules 12–21 of the programme).

**Ethical review:** This is a structured academic exercise with no human subjects, personal data or ethical risk. No institutional review board approval was required.

**Consent and withdrawal:** Not applicable — no human participants.

---

## Preprocessing and Uses

**Transformations applied:**
- All input coordinates standardised to six decimal places before submission.
- No normalisation applied to outputs — raw values retained to preserve the natural scale of each function (outputs range from near-zero to ~1600+).
- Function outputs from early rounds were used to fit GP kernel hyperparameters via maximum likelihood estimation.

**Intended uses:**
- Training and validating surrogate models (GP, SVM, MLP) for BBO strategy development.
- Analysing the exploration–exploitation trade-off under query budget constraints.
- Benchmarking progressive strategy improvements across rounds.

**Inappropriate uses:**
- Should not be used to make inferences about real-world functions — the unknown functions are artificial and their structure is not generalisable.
- Should not be used as a training set for production ML systems without additional validation data.

---

## Distribution

**Availability:**
The dataset (embedded in weekly strategy markdown files) is publicly available at:
`https://github.com/Dibyajyoti-Pradhan/Capstone-Project-Imperial-College-London/tree/main/Black-Box-Optimisation-Challenge`

**Licensing:**
Available under the MIT Licence. Free to use, share and adapt with attribution.

**When was it made available?**
Progressively committed to the public GitHub repository across Modules 12–21 (January–March 2026).

---

## Maintenance

**Who maintains this dataset?**
Dibyajyoti Pradhan — contact via GitHub (`@Dibyajyoti-Pradhan`).

**Updates and corrections:**
The dataset is static upon programme completion. No future updates are planned. Any corrections to submitted queries or observed outputs would be documented through Git commit messages with version tagging.

**Archiving:**
The repository serves as the permanent archive. No separate long-term storage is planned beyond the public GitHub repository.

---

## References

Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J.W., Wallach, H., Daumé III, H. and Crawford, K. (2021) 'Datasheets for datasets', *Communications of the ACM*, 64(12), pp. 86–92.
