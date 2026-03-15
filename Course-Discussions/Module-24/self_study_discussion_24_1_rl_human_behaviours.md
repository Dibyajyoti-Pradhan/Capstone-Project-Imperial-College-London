# Self-study Discussion 24.1 — RL and Human Behaviours

**Module:** 24 — Reinforcement Learning
**Type:** Self-study (not graded)
**Cohort:** IMP-PCMLAI-25-08

---

## 1. A Toddler Learning to Walk as an RL Problem

A toddler learning to walk maps cleanly onto the RL framework: the child is the *agent*, gravity and the physical world are the *environment*, each attempted step is an *action*, and the sequence of attempts constitutes a *policy*. The objective — maximising stable upright movement over time — is the *cumulative reward*. Crucially, no explicit instruction is given; the child updates its motor policy solely from environmental feedback, exactly as an RL agent updates value estimates from observed transitions.

---

## 2. Rewards and Punishments

| Signal | Biological form | RL equivalent |
|:-------|:----------------|:--------------|
| Positive | Successful forward step, parental praise, proprioceptive stability | +reward |
| Negative | Pain from falling, muscle fatigue | −reward / penalty |
| Delayed | Reaching a toy after several attempts | delayed reward |

Speech acquisition follows the same structure: a sound approximating "mama" that triggers a parent's delighted response is a strong positive reward, reinforcing that phoneme pattern.

---

## 3. Factors Accelerating or Slowing Learning

- **Feedback frequency:** Immediate physical feedback (falling instantly) accelerates policy updates. Delayed or sparse feedback — analogous to sparse-reward RL environments — slows convergence dramatically.
- **Motivation:** A toddler reaching for a toy has a strong intrinsic reward signal; low motivation reduces effective reward magnitude.
- **Environment complexity:** A flat floor is a low-dimensional state space; stairs introduce combinatorial complexity, analogous to increasing the state-action space in RL.
- **Safety constraints:** Protective padding allows more exploration attempts per unit time — effectively increasing the sample efficiency of the policy search.

---

## 4. Trial-and-Error as Exploration–Exploitation

A toddler balances two competing imperatives: *exploit* known stable stances (standing still, crawling) versus *explore* new motor configurations (extending a leg further). Early learning is heavily exploratory — high-ε in ε-greedy terms — with many falls. As competence grows, the policy shifts toward exploitation of reliable gaits. This mirrors UCB or ε-decay schedules: broad early exploration collapsing into refined exploitation once the value landscape is better understood.

---

## 5. Dopamine and RL Reward Signals

Neuroscience research (Schultz et al., 1997) established that dopaminergic neurons encode *temporal difference (TD) prediction errors* — they fire when outcomes exceed expectations and are suppressed when outcomes fall short. This is structurally identical to the TD error δ = r + γV(s') − V(s) in Q-learning. Both systems:

- Signal *surprise*, not raw reward
- Drive learning proportional to prediction error magnitude
- Decay as predictions become accurate (reward becomes expected)

The dopamine system effectively implements biological TD-learning, suggesting RL is not merely a metaphor for human cognition but may reflect its underlying computational architecture.

---

## Reference

Schultz, W., Dayan, P. and Montague, P.R. (1997) 'A neural substrate of prediction and reward', *Science*, 275(5306), pp. 1593–1599.
