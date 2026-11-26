---
key: muslimani2025
read: full
read_detail: main text §1–7; supplement not read
read_on: 2026-11-24
---

# Muslimani, Johnstonbaugh, Chandramouli, Booth, Knox, Taylor 2025, A Reward Alignment Metric for RL Practitioners (RLJ 2025)

URL: https://arxiv.org/abs/2503.05996
Cited by [1] for: "diagnosing reward misspecification" (§1, §3) and "reward function alignment" (§5).
Read: main text (§1–7) in full; supplementary material not read.

Key findings
- A diagnostic, not a safety method: the Trajectory Alignment Coefficient is Kendall's tau-b between a human stakeholder's ranking of trajectory distributions and the ranking induced by (r, γ).
- Reference is one "human stakeholder" whose ranking is "assumed to be transitive".
- Theory: invariance to potential-based shaping iff compared trajectory distributions share the start-state distribution (Theorem 4.4–4.5); invariance to positive linear transforms (Theorem 4.6). No safety guarantee.
- Needs a diverse set of trajectories to rank. In the paper they are generated "via RL agents partially trained with different reward functions"; the authors add that "human demonstrations" or behavioural cloning could be used. So repeated RL trials are not required.
- Evidence: an 11-person user study in the 4×4 Hungry-Thirsty grid world; 12 ranked trajectories; preferences were simulated from the task metric ("as a proxy for expert preferences").
- Broader impact: the metric "may be unreliable" "if the preferences provided by the human stakeholder do not accurately reflect their true beliefs" (part of our U2).
- LLM alignment is stated to be "beyond the scope of this work".

Conditions: S1 human preferences instead of a specification; S2–S5 not needed; S6 not needed (trajectories can come from demonstrations). U2 stated in part; U4 assumed (one stakeholder).

Verified quotes (checked against the source text, 2026-11-24)
- "finite subsets of trajectory distributions"
- "human demonstrations"
- "RL agents partially trained with different reward functions"
