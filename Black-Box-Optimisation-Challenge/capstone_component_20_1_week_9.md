# Required Capstone Component 20.1 — Week 9
## Refining Strategies for the Black-Box Optimisation Challenge

**Module:** 20 — Scaling Large Language Models
**Submitted:** 28/02/2026
**Cohort:** IMP-PCMLAI-25-08

---

## Part 1: Queries Submitted

| Function | Dimensions | Strategy | Query Submitted | Output |
|----------|------------|----------|-----------------|--------|
| F1 | 2D | Exploration (κ=1.6) | 0.830399-0.767887 | TBC |
| F2 | 2D | Balanced GP-UCB (κ=0.6) | 0.755635-0.920896 | TBC |
| F3 | 3D | Balanced GP-UCB (κ=0.6) | 0.219671-0.254999-0.424515 | TBC |
| F4 | 4D | Exploitation (κ=0.35) | 0.578500-0.416692-0.423202-0.276134 | TBC |
| F5 | 4D | Tight trust-region (κ=0.08, r=0.012) | 0.983402-0.986019-0.955749-0.987486 | TBC |
| F6 | 5D | Balanced (κ=1.0) | 0.701731-0.114762-0.739213-0.692731-0.044651 | TBC |
| F7 | 6D | GP gradient ascent (κ=2.0) | 0.084858-0.545780-0.248800-0.266367-0.376177-0.771856 | TBC |
| F8 | 8D | Tight trust-region (κ=0.08, r=0.045) | 0.130996-0.214270-0.023203-0.201722-0.278679-0.687286-0.559759-0.944046 | TBC |

---

## Part 2: Reflection on Strategy — Ninth Iteration (18 Data Points)

---

### 1. How Scaling Laws Influence Current Query Choices

Scaling laws predict that performance improves predictably with increased compute, data, and model capacity — but with diminishing marginal returns. With 18 data points now informing my search, I observe this pattern clearly across the eight functions.

**Evidence of diminishing returns:**

- Functions where I've identified strong optima (F5, F2) show plateauing improvements — small input perturbations yield minimal output changes
- The surrogate model's uncertainty has collapsed in well-explored regions, reducing the exploration bonus from UCB acquisition
- Each additional query near known optima provides less informational value than early-round queries

**Evidence of continued scaling potential:**

- High-dimensional functions (F7, F8) remain severely undersampled — 18 points in 7–8 dimensions provides negligible coverage
- Some functions exhibit sharp, localised peaks that only become detectable with sufficient data density
- Functions with noise or non-stationarity benefit from additional observations to distinguish signal from artefact

**Strategic implication:** I now differentiate between functions in "exploitation mode" (diminishing returns, focus on local refinement) versus "exploration mode" (still in early scaling phase, broader sampling justified).

---

### 2. Where Emergent Behaviours Might Alter Expectations

Emergent behaviours — sudden capability jumps that appear non-linearly — could manifest in several ways within the BBO context:

**Potential emergence scenarios:**

- **Structural discovery:** The surrogate may suddenly "recognise" underlying patterns once sufficient data accumulates. F5's dramatic spike suggests the function contains a narrow, high-value region that only became detectable after crossing a data threshold.
- **Dimensional interactions:** High-dimensional functions may exhibit non-linear interactions between variables that only emerge when exploration covers specific subspaces.
- **Phase transitions:** Some functions may behave fundamentally differently across regions — smooth in one area, discontinuous elsewhere.

**Preparation strategies:**

- Maintain deliberate exploration budget even in late rounds (20–30% of queries)
- Monitor for sudden variance changes or output sign reversals that signal regime transitions
- Use ensemble disagreement as an emergence indicator — high variance across surrogate models suggests unresolved structure
- Avoid fully committing to exploitation; preserve optionality for unexpected discoveries

---

### 3. Trade-offs Between Cost, Robustness, and Performance

With limited queries remaining, trade-off management dominates strategy:

- **Cost considerations:** Each query is irreplaceable — cannot afford speculative exploration without justification. Computational overhead for surrogate training scales with data.
- **Robustness concerns:** Overconfident surrogates may hallucinate optima in unexplored regions. Narrow exploitation risks missing global optima if current best is actually local.
- **Performance pressures:** Final rankings depend on best discovered values, not exploration breadth. Diminishing returns favour exploitation near proven high-value regions.

**Current balance:**

| Function group | Strategy |
|:--------------|:---------|
| Consistent improvement (F5, F4) | Aggressive exploitation |
| Volatile histories (F2, F7) | Cautious refinement with local probes |
| Minimal progress (F1, F3) | Targeted hypothesis-driven exploration |
| High-dimensional (F8) | Broader sampling given inherent sparsity |

---

### 4. Balancing Predictable Optimisation with Emergent Risk

The core tension: predictable optimisation assumes smooth, continuous improvement; emergence produces discontinuous jumps that violate those assumptions.

**Strategies for balance:**

- **Tiered allocation:** Most queries (70–80%) pursue predictable refinement near known optima; a minority (20–30%) explicitly probe for emergence via controlled exploration
- **Anomaly detection:** Track output variance, gradient magnitudes, and surrogate disagreement. Sudden changes trigger investigation rather than automatic exploitation
- **Trust regions with escape hatches:** Constrain most queries to small perturbations around current best, but periodically test points outside trust regions
- **Ensemble hedging:** Maintain surrogate diversity (GP + neural network) so that emergence signals appear as disagreement rather than false confidence
- **Endgame discipline:** As rounds conclude, shift toward submitting best-known values with maximum precision — accepting that late-stage emergence discoveries may not have time for proper exploitation

**Philosophical stance:** In black-box optimisation with incomplete information, the goal is not perfect prediction but robust decision-making under uncertainty. Emergence is a feature of complex systems; preparation means building adaptive strategies rather than assuming predictability.
