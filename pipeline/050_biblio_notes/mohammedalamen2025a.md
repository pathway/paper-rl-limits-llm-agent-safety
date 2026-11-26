---
key: mohammedalamen2025a
read: full
read_detail: main text §1–7; appendices not read
read_on: 2026-11-24
---

# Mohammedalamen, Morrill, Sieusahai, Satsangi, Bowling 2025, Learning to Be Cautious (TMLR 10/2025)

URL: https://arxiv.org/abs/2110.15907
Cited by [1] for: "safe sequential decision-making under uncertainty" (§3, with Mon-MDPs).
Read: main text (§1–7) in full; appendices not read.

Key findings
- Setting: train-and-deploy; the agent "does not perform any adaptation after seeing novel states"; zero-shot behaviour in novel situations.
- Uses no "task-specific safety information"; caution is risk aversion to epistemic reward uncertainty.
- Model: "A finite, discounted MDP"; implementation "is tabular" and "requires exact policy evaluation".
- Theory (§5) assumes "reward uncertainty and transition certainty"; the authors call transition certainty "a strong assumption".
- Method: ensemble of reward networks (posterior-like belief) + k-of-N CFR; regret and approximation bounds for the robust policy (Theorems 1–3). No safety-constraint guarantee.
- Experiments: MNIST/fashion/letters contextual bandits and a driving grid world; environments are "fully observable".
- Broader impact: "human oversight remains essential".

Conditions: S1 not needed; S2 needed; S3 needed; S4 needed; S5 not needed at deployment; S6 not needed at deployment.
Relevance: closest cited tool to a frozen deployed agent (no specification, no adaptation), but needs a finite, fully observed MDP with known transitions.

Verified quotes (checked against the source text, 2026-11-24)
- "are fully observable"
