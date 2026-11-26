---
key: mohammedalamen2025b
read: full
read_detail: main text §1–6; appendices not read
read_on: 2026-11-24
---

# Mohammedalamen, Bowling 2025, Generalization in Monitored MDPs (arXiv 2505.08988)

URL: https://arxiv.org/abs/2505.08988
Cited by [1] for: "safe sequential decision-making under uncertainty" (§3).
Read: main text (§1–6) in full; appendices not read. Status: "Preprint. Under review."

Key findings
- Mon-MDP: the reward is sometimes unobservable; a monitor decides when it is seen. The environment state is observed; only the reward may be hidden.
- Earlier guarantees (Parisi et al. 2024, tabular) hold only if: (i) "a finite or countably infinite" number of states and actions; (ii) "each joint state pair … can be visited infinitely often"; (iii) every reward observable with nonzero probability; (iv) "the proxy reward is truthful".
- This paper uses function approximation (DQN + learned reward model) and gives no guarantee; results are empirical in a 10×10 plant-watering grid world.
- Finds "overgeneralization": rewards extrapolated wrongly to unmonitored states (agent waters cacti); mitigated with the k-of-N cautious method.
- Broader impact: automated safety measures "complement, not replace, human judgment".

Conditions: S1 reward only; S2 not needed; S3 needed for any guarantee; S4 needed; S5 needed; S6 needed (infinite visits). U2 stated in part ("truthful" proxy reward).
