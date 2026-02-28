# Self-study Discussion 19.2: Analysing the Implications of Model Sizes

---

## When model size increases, how do costs and energy requirements change?

Costs and energy scale **super-linearly** with model size. This manifests across two phases:

**Training costs:** Doubling parameters requires more than double the compute due to the quadratic attention complexity in transformers. GPT-3 (175B parameters) cost an estimated $4-12 million to train; GPT-4's training likely exceeded $100 million. Hardware requirements shift from consumer GPUs to clusters of thousands of specialised accelerators (H100s, TPUs).

**Inference costs:** Every user query activates all parameters. For a 175B model, this means ~700GB of weights must be loaded and processed per request. Energy consumption compounds with usage—millions of daily queries translate to substantial electricity demand and cooling requirements.

**Environmental impact:** Training a single large model can emit carbon equivalent to five cars' lifetime emissions. As AI becomes embedded in everyday products, inference energy at scale may dwarf training costs.

However, architectural innovations challenge this trajectory. **Mixture-of-Experts (MoE)** models like DeepSeek activate only a fraction of parameters per query, achieving frontier performance at dramatically lower cost—demonstrating that scale and efficiency need not be mutually exclusive.

---

## What does greater scale mean for who can access and use advanced AI?

Greater scale historically **concentrates power** among well-resourced organisations. Only hyperscalers (OpenAI, Google, Anthropic) can afford billion-dollar training runs, creating a two-tier system: producers who control frontier models and consumers who access them through rate-limited APIs.

This has **geopolitical implications**—AI capability becomes tied to capital access, potentially widening global inequality.

Yet efficient open-source models (DeepSeek, Llama, Mistral) are **democratising access**. By prioritising optimisation over raw scale, they enable:
- Local deployment on modest hardware
- Fine-tuning by startups and researchers
- Reduced dependence on proprietary APIs

The future may favour **efficiency over size**—making powerful AI a shared resource rather than a luxury.

---

*Word count: 298*
