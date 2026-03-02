# Required Capstone Component 19.1: Refining Strategies for the Black-Box Optimisation Challenge

## Part 2: Reflection on Prompting and Decoding Strategies (Eighth Iteration)

---

### 1. Prompt Patterns Used

I employed a **few-shot chain-of-thought** approach, structuring prompts with the accumulated 17-point observation history sorted by performance, followed by explicit reasoning requirements before generating candidate coordinates.

**Zero-shot prompts** were occasionally useful for brainstorming alternative acquisition strategies, but produced unreliable coordinate suggestions—often ignoring bounds or dimensional constraints.

**Simplified vs. structured prompts:** When I simplified prompts ("suggest the next best point"), outputs varied unpredictably and sometimes violated the [0,1] constraint. Structured prompts—explicitly stating bounds, dimensionality, trust-region intent, and required output format—produced reproducible, validated suggestions. The trade-off: simplified prompts enabled broader exploration but required extensive post-filtering; structured prompts narrowed the search but ensured valid, actionable outputs.

---

### 2. Decoding Settings and Trade-offs

I selected conservative decoding parameters:

| Parameter | Setting | Rationale |
|-----------|---------|-----------|
| Temperature | 0.2 | Prioritise coherence over creativity |
| Top-p | 0.9 | Permit controlled diversity |
| Top-k | 50 | Limit extreme token choices |
| Max tokens | Sufficient to avoid truncation | Ensure complete coordinate vectors |

**Coherence vs. diversity trade-off:** Low temperature produced deterministic, exploitation-focused suggestions aligned with known high-value regions. Higher temperature (tested at 0.6-0.8) occasionally proposed novel exploration points but frequently hallucinated coordinates outside valid bounds.

**Effect on queries:** Conservative decoding meant suggestions clustered near proven optima—appropriate for late-stage refinement but requiring explicit exploration prompts to avoid premature convergence.

---

### 3. Token Boundaries and Truncation

Token boundaries affected floating-point precision—numbers like `0.123456` tokenise inconsistently (sometimes as `0.12`, `34`, `56`), causing occasional rounding errors or precision loss.

**Mitigation:** I standardised coordinate formatting to six decimal places with explicit precision requirements in prompts, and verified outputs maintained complete dimensionality.

**Truncation checks:** I monitored for incomplete coordinate vectors (missing dimensions) and cut-off reasoning. Keeping prompts compact—summarising history rather than including raw data—avoided context window pressure. No truncation issues occurred in practice.

---

### 4. Limitations at 17 Data Points

Several limitations emerged:

- **Recency bias:** The model over-weighted recent observations (Weeks 6-7), sometimes "forgetting" that global optima for certain functions were discovered earlier. I countered this by injecting "best historical point" summaries at prompt end.

- **Attention drift:** Longer prompts caused attention to spread across irrelevant context rather than focusing on high-performing regions.

- **Diminishing returns:** Adding more historical detail beyond key summaries did not improve suggestions—the model's reasoning capacity saturated before data complexity did.

- **Prompt overfitting:** Repeated similar prompt structures led to similar outputs, reducing exploratory diversity.

---

### 5. Hallucination Reduction Strategies

I employed multiple strategies:

- **Tight constraints:** Explicit bounds ("all values must be in [0,1]"), dimensionality requirements ("Function 8 requires exactly 8 coordinates"), and format specifications ("output as X1-X2-...-Xn with six decimal precision").

- **Grounding on prior data:** Referencing actual best-known observations rather than letting the model invent plausible-sounding coordinates.

- **Trust region constraints:** Forbidding suggestions outside a small radius of proven optima during exploitation phases.

- **Validation mindset:** Treating LLM suggestions as candidates requiring verification rather than authoritative answers—checking bounds, precision, and dimensionality before submission.

---

### 6. Scaling Strategies for Future Rounds

For larger datasets or more complex models:

- **Compressed context:** Replace full history with summaries—best points, regional statistics, trend indicators—to avoid attention dilution.

- **Retrieval-augmented prompting:** Index historical observations in a vector database, retrieving only the k-nearest relevant points for each query region.

- **Modular prompting:** Separate identification of promising regions from coordinate generation within those regions.

- **Dynamic decoding:** Lower temperature for exploitation phases; moderately higher for exploration.

- **Tool-augmented workflows:** Use LLMs for strategy selection and critique while delegating numerical optimisation to dedicated algorithms (GPs, neural surrogates).

---

### 7. Practitioner Mindset: Balancing Exploration, Risk, and Constraints

These design choices cultivated practical decision-making under uncertainty:

- **Every query is expensive:** Conservative decoding reduced operational risk—invalid coordinates waste irreplaceable budget.

- **Uncertainty is unavoidable:** Structured prompts and explicit constraints acknowledged that the model's "reasoning" is probabilistic, not mathematical.

- **Exploitation vs. exploration as explicit choice:** Rather than hoping randomness discovers useful regions, I encoded exploration intent explicitly in prompts when needed.

- **Reproducibility matters:** Structured prompts and low temperature ensured consistent suggestions, enabling systematic comparison across iterations.

This mirrors production ML practice: using AI as a co-pilot for hypothesis generation while maintaining human oversight for validation—combining LLM pattern recognition with principled numerical methods for robust black-box optimisation.

---

*Word count: 694*
