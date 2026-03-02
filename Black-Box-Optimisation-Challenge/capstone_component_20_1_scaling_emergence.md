# Required Capstone Component 20.1: Refining Strategies for the Black-Box Optimisation Challenge

## Part 2: Reflection on Scaling, Emergence, and Optimisation Strategy (Ninth Iteration)

---

### How Scaling Laws Influence Current Query Choices

Scaling laws predict that performance improves predictably with increased compute, data, and model capacity—but with diminishing marginal returns. With 18 data points now informing my search, I observe this pattern clearly across the eight functions.

**Evidence of diminishing returns:**
- Functions where I've identified strong optima (F5, F2) show plateauing improvements—small input perturbations yield minimal output changes
- The surrogate model's uncertainty has collapsed in well-explored regions, reducing the exploration bonus from UCB acquisition
- Each additional query near known optima provides less informational value than early-round queries

**Evidence of continued scaling potential:**
- High-dimensional functions (F7, F8) remain severely undersampled—18 points in 7-8 dimensions provides negligible coverage
- Some functions exhibit sharp, localised peaks that only become detectable with sufficient data density
- Functions with noise or non-stationarity benefit from additional observations to distinguish signal from artefact

**Strategic implication:** I now differentiate between functions in "exploitation mode" (diminishing returns, focus on local refinement) versus "exploration mode" (still in early scaling phase, broader sampling justified).

---

### Where Emergent Behaviours Might Alter Expectations

Emergent behaviours—sudden capability jumps that appear non-linearly—could manifest in several ways within the BBO context:

**Potential emergence scenarios:**

1. **Structural discovery:** The surrogate may suddenly "recognise" underlying patterns once sufficient data accumulates. F5's dramatic spike (2374.27 in Week 8) suggests the function contains a narrow, high-value region that only became detectable after crossing a data threshold.

2. **Dimensional interactions:** High-dimensional functions may exhibit non-linear interactions between variables that only emerge when exploration covers specific subspaces. Functions appearing flat may contain hidden structure accessible only through particular combinations.

3. **Phase transitions:** Some functions may behave fundamentally differently across regions—smooth in one area, discontinuous elsewhere. Crossing these boundaries could produce abrupt, unexpected output changes.

**Preparation strategies:**
- Maintain deliberate exploration budget even in late rounds (20-30% of queries)
- Monitor for sudden variance changes or output sign reversals that signal regime transitions
- Use ensemble disagreement as an emergence indicator—high variance across surrogate models suggests unresolved structure
- Avoid fully committing to exploitation; preserve optionality for unexpected discoveries

---

### Trade-offs Between Cost, Robustness, and Performance

With limited queries remaining, trade-off management dominates strategy:

**Cost considerations:**
- Each query is irreplaceable—cannot afford speculative exploration without justification
- Computational overhead for surrogate training scales with data; simplified models may be necessary
- Time constraints favour incremental refinements over architectural overhauls

**Robustness concerns:**
- Overconfident surrogates may hallucinate optima in unexplored regions
- Narrow exploitation risks missing global optima if current best is actually local
- Noise in observations can mislead refinement toward artefacts rather than true signal

**Performance pressures:**
- Final rankings depend on best discovered values, not exploration breadth
- Diminishing returns favour exploitation near proven high-value regions
- However, premature convergence forfeits potential breakthrough discoveries

**Current balance:**
- Functions with consistent improvement trajectories (F5, F4): aggressive exploitation
- Functions with volatile histories (F2, F7): cautious refinement with local probes
- Functions with minimal progress (F1, F3): targeted hypothesis-driven exploration
- High-dimensional functions (F8): maintain broader sampling given inherent sparsity

---

### Balancing Predictable Optimisation with Emergent Risk

The core tension: **predictable optimisation assumes smooth, continuous improvement; emergence produces discontinuous jumps that violate those assumptions.**

**Strategies for balance:**

1. **Tiered allocation:** Most queries (70-80%) pursue predictable refinement near known optima; a minority (20-30%) explicitly probe for emergence via controlled exploration.

2. **Anomaly detection:** Track output variance, gradient magnitudes, and surrogate disagreement. Sudden changes trigger investigation rather than automatic exploitation.

3. **Trust regions with escape hatches:** Constrain most queries to small perturbations around current best, but periodically test points outside trust regions to detect missed structure.

4. **Ensemble hedging:** Maintain surrogate diversity (GP + neural network + random forest) so that emergence signals appear as disagreement rather than false confidence.

5. **Endgame discipline:** As rounds conclude, shift toward submitting best-known values with maximum precision—accepting that late-stage emergence discoveries may not have time for proper exploitation.

**Philosophical stance:** In black-box optimisation with incomplete information, the goal is not perfect prediction but robust decision-making under uncertainty. Emergence is a feature of complex systems; preparation means building adaptive strategies rather than assuming predictability.

---

*Word count: 694*
