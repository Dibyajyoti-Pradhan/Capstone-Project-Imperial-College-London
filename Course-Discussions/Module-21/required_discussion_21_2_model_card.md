# Required Discussion 21.2: Analysing a Model Card

## Selected Model: Gemini 2.5 Pro

---

### Category 1: Understanding and Interpretation

Gemini 2.5 Pro is Google DeepMind's most capable model in the Gemini family, designed for advanced reasoning, coding, mathematics and long-context understanding across a 1M token context window. The card describes a Mixture-of-Experts Transformer architecture intended for complex scientific analysis, algorithmic development and long-document comprehension.

Stated limitations include hallucinations, a January 2025 knowledge cutoff, over-refusal of benign prompts and performance variability in multi-turn conversations. The primary audience is clearly developers and technical researchers: the card uses terms like "pass@1", "ELO scores" and benchmark names (MMLU, HumanEval, GPQA) without explanation, largely excluding non-technical readers. Key assumptions are that users have technical literacy, that deployment sits within broader responsible-use frameworks and that the model operates as a component in larger systems rather than autonomously.

---

### Category 2: Transparency and Trust

The card provides comparative benchmark tables against competing models, which helps technical decision-makers assess relative capability. However, critical gaps exist: training data composition is described only as "large-scale and diverse" with no sources, domains or licensing detail. Safety evaluations are reported as relative improvements over previous versions rather than absolute violation rates, making independent judgement difficult.

For a non-technical stakeholder — a compliance officer or end user — the card provides little actionable guidance. Real-world failure examples, plain-language summaries and explicit "do not use" scenarios are all absent. I would want to see absolute safety violation rates, concrete failure examples, disaggregated performance across languages and demographic groups, and clear documentation of training data provenance.

---

### Category 3: Ethical, Fairness and Social Impact

The card identifies frontier risk categories — CBRN, cybersecurity, persuasion — and describes red-teaming and safety evaluation processes. This is commendable. However, fairness across demographic groups, language communities and underrepresented dialects receives no quantitative treatment.

A model of this capability could cause serious harm in high-stakes autonomous contexts — medical triage, financial advice, legal analysis — yet the card does not address these scenarios explicitly. The acknowledgement that improved instruction-following increases willingness to engage with previously refused prompts is framed positively, but the corresponding risk increase warrants more careful treatment. The absence of subgroup performance metrics leaves it unclear which populations may be disadvantaged.

---

### Category 4: Practical Application and Decision-Making

Before adopting Gemini 2.5 Pro in production, I would request: disaggregated benchmark results by domain and demographic group; documentation of known failure modes with frequency estimates; data provenance and licensing details; latency and cost benchmarks under realistic workloads; and a versioning and update policy.

I would integrate the model card into internal risk assessments and share a plain-language summary with non-technical stakeholders. Deployment monitoring would track hallucination rates, refusal rates and domain-specific performance drift — but the card provides insufficient baseline metrics to anchor this rigorously. The absence of guidance on detecting model drift or communicating updates to downstream users is a notable operational gap.

---

### Category 5: Reflection and Improvement

The most valuable element is the honest acknowledgement of limitations — hallucination, over-refusal, knowledge cutoff — which discourages false confidence in deployment decisions. The structured benchmark table is a practical reference for technical comparison.

The primary weaknesses are absent demographic fairness data, opaque training data documentation and poor accessibility for non-technical audiences. If rewriting this card, I would add: a plain-language executive summary; absolute safety violation rates alongside relative improvements; disaggregated performance by language, demographic group and task domain; and concrete misuse scenarios with mitigation guidance.

Compared with datasheets for datasets, this card prioritises deployment performance over data provenance — reflecting a broader industry tendency to document model capability more thoroughly than model construction. Complementing model cards with datasheets and independent audits would provide a more complete and trustworthy transparency framework.

---

### References

Google DeepMind (2025) *Gemini 2.5 Pro Model Card*. Available at: https://ai.google.dev/gemini-api/docs/models

Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji, I.D. and Gebru, T. (2019) 'Model cards for model reporting', *Proceedings of the Conference on Fairness, Accountability, and Transparency*, pp. 220–229.

Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J.W., Wallach, H., Daumé III, H. and Crawford, K. (2021) 'Datasheets for datasets', *Communications of the ACM*, 64(12), pp. 86–92.
