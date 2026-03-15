# Required Capstone Component 24.1 — Week 13
## Refining Strategies for the Black-Box Optimisation Challenge (Final Round)

**Module:** 24 — Reinforcement Learning
**Submitted:** 15/03/2026
**Posted:** 15/03/2026
**Cohort:** IMP-PCMLAI-25-08

---

## Part 1: Queries Submitted

| Function | Dimensions | Strategy | Query Submitted | Output |
|----------|------------|----------|-----------------|--------|
| F1 | 2D | Final exploration — highest-uncertainty region (κ=1.5) | 0.797370-0.894348 | TBC |
| F2 | 2D | Pure exploitation (κ=0.3, r=0.04) | 0.791642-0.924731 | TBC |
| F3 | 3D | Pure exploitation (κ=0.3, r=0.04) | 0.456539-0.606895-0.348186 | TBC |
| F4 | 4D | Tight exploitation (κ=0.2, r=0.025) | 0.552947-0.431219-0.428023-0.252723 | TBC |
| F5 | 4D | Micro-perturbation trust region (κ=0.05, r=0.005) | 0.988600-0.947963-0.973440-0.983707 | TBC |
| F6 | 5D | Balanced exploitation (κ=0.8, r=0.06) | 0.780609-0.178148-0.717981-0.676850-0.081457 | TBC |
| F7 | 6D | Final exploration — highest-uncertainty region (κ=1.5) | 0.049736-0.466129-0.313738-0.261308-0.438685-0.752395 | TBC |
| F8 | 8D | Reduced 4D subspace (X1/X3/X6/X8), fixed dims (κ=0.05, r=0.04) | 0.076587-0.189558-0.116004-0.057006-0.401034-0.696607-0.555764-0.942344 | TBC |

---

## Part 2: Reflection on Strategy — Thirteenth and Final Iteration (22 Data Points)

---

### 1. How Understanding of the Exploration–Exploitation Trade-Off Evolved

Week 1 treated every function identically: spread queries widely, gather initial signal, make no commitments. By Week 13, each function has its own κ value derived from thirteen rounds of evidence. The trade-off is no longer abstract — it has become a function-specific parameter calibrated against real feedback.

The clearest evolution was the recognition that exploration and exploitation are not binary modes but points on a continuous spectrum controlled by κ. Early rounds used κ=5.0 uniformly; by Week 13, the range spans κ=0.05 (F5, near-pure exploitation of a confirmed peak) to κ=1.5 (F1, F7, where the landscape remains unresolved). The risk calculation also changed: in early rounds, exploring was low-cost because no promising region had been found. By Week 12, exploring away from F5's confirmed basin carried a real opportunity cost — one fewer confirmation of the highest-value region already discovered. The transition from symmetric to asymmetric risk management mirrors how a rational RL agent shifts from uniform exploration to policy-specific exploitation as the value function converges.

Balancing risks meant accepting that F1 and F7 might simply be flat functions. Committing another high-κ query to them in Round 13 is not optimism — it is the correct Bayesian response to genuine posterior uncertainty. The cost of one final exploratory step is bounded; the cost of missing a peak that existed is unbounded within the query budget.

---

### 2. How Feedback Influenced the Optimisation Process — The RL Parallel

Each query output functions as a reward signal. The GP surrogate is the analogue of a Q-table: it stores the current belief about expected return at every unsampled location, and it updates when a new observation arrives. This is functionally identical to Q-learning's update rule — the new observation shifts the posterior mean at nearby locations (via kernel smoothing), reducing or increasing the estimated value of those candidates.

The practical impact was visible in three patterns. First, F5's Week 1 output (~1600) acted as an unexpectedly large reward signal that reshaped the entire Q-surface for that function, immediately flagging a region far above the rest of the space. The GP's posterior updated to assign high mean predictions to the neighbourhood, directing all subsequent queries there — exactly how a Q-learning agent increases action-values after receiving a large reward. Second, F6's gradient ascent failure in Week 6 was a negative reward signal: the GP had assigned high predicted value to a ridge that the actual evaluation deflated. The response — reverting to conservative GP-UCB with κ=1.5 — mirrors temporal-difference correction, pulling the inflated Q-estimate back toward the true return. Third, the progressive narrowing of trust regions for F4/F5/F8 reflects the diminishing learning-rate schedule in Q-learning: as confidence accumulates, each update makes smaller adjustments rather than overwriting the policy with each observation.

---

### 3. AlphaGo Zero Parallels — Self-Play and Model-Based Planning

AlphaGo Zero improved by playing against its own previous version: each iteration generated training signal from the current best policy, refined the value and policy networks, and produced a stronger next policy. The BBO process follows the same loop: at each round, the current GP surrogate (analogous to the value network) generates a candidate query via UCB acquisition (the policy network), the actual function evaluation returns a ground-truth output, and the surrogate is retrained on the expanded data set. The next round's query is informed by a strictly better-calibrated belief — self-improvement from self-generated data.

The process was predominantly **model-based** rather than model-free. Rather than applying random perturbations and accepting whatever output arrived (trial and error), each query was chosen by maximising an explicit predictive model of the function landscape. The GP encodes beliefs about unmeasured locations and propagates uncertainty coherently — the defining feature of model-based planning. The exception was F1 and F7 in early rounds, where the surrogate had too little data to be informative and queries were essentially random probes: genuinely model-free trial and error. As data accumulated, even these functions transitioned toward model-guided search.

The key difference from AlphaGo Zero: there is no self-play because there is no adversary. The analogue is a single agent playing against the function itself — each query is a move that reveals one bit of the hidden game board.

---

### 4. How RL Strategies Could Enhance Real-World Optimisation Tasks

Four direct applications emerge from this project:

**Adaptive exploration budgets via MAB policies:** The BBO challenge allocated one query per function per round. A Thompson Sampling policy across all eight functions — sampling a query from the posterior distribution of each function's current best estimate and allocating the next query to the function with highest sampled value — would dynamically concentrate budget on high-promise functions rather than treating all eight equally. This would likely have increased total best-observed value by redirecting F1/F7's later-round queries toward F5/F8.

**Policy gradient for trust-region radius scheduling:** The trust-region radius was adjusted by hand based on qualitative observation. An actor-critic architecture could learn this radius schedule directly: the actor proposes a radius, the critic evaluates whether the resulting query improved the running best, and the policy updates toward radii that historically improve output. This removes the manual schedule and generalises across function types.

**Q-learning for strategy selection:** Rather than choosing a fixed strategy per function (GP-UCB, gradient ascent, trust region), a Q-learning agent could maintain action-values for each strategy and select adaptively. The reward signal is simply the improvement in running best. After sufficient rounds, the agent would learn which strategy performs best at each stage of the budget, conditioned on the function's behavioural cluster (converging, drifting, unresolved).

**Model-based RL for drug discovery and hyperparameter search:** The BBO framework is directly applicable to molecular optimisation (each query is a wet-lab experiment), clinical dose-response studies, and AutoML hyperparameter tuning. RL augments this by adding a policy for how to sequence experiments across multiple compounds or model architectures simultaneously — the multi-armed bandit problem operating over a portfolio of optimisation problems rather than a single function. This is precisely the setting of Google Vizier and Meta's BoTorch: RL-guided Bayesian optimisation at scale.

---

## References

Sutton, R. and Barto, A. (2018) *Reinforcement Learning: An Introduction*. 2nd edn. MIT Press.

Silver, D. et al. (2017) 'Mastering the game of Go without human knowledge', *Nature*, 550, pp. 354–359.

Srinivas, N. et al. (2010) 'Gaussian process optimization in the bandit setting: no regret and experimental design', *Proceedings of ICML*, pp. 1015–1022.
