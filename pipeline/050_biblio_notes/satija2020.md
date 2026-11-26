---
key: satija2020
read: full
read_detail: main text and Appendices A–C; D–J skimmed
read_on: 2026-11-24
---

# Satija, Amortila, Pineau 2020, Constrained MDPs via Backward Value Functions (ICML 2020)

URL: https://arxiv.org/abs/2008.11811
Cited by [1] with Altman for CMDPs (§4, "constrained MDPs address").
Read: main text and Appendices A–C in full; Appendices D–J (implementation details) skimmed.

Key findings
- CMDP with state cost d: X → [0, D_MAX], budget d0, finite horizon T.
- Assumption 3.1 (Stationarity): "The MDP is ergodic for any policy", i.e. every induced Markov chain is irreducible and aperiodic. This excludes irreversible states.
- Method: converts the trajectory constraint into state-wise constraints using backward value functions; "a reduction to any model-free on-policy bootstrap-based RL algorithm". No model needed.
- Guarantee (Theorem 3.1): consistent feasibility, only if "successive policies are updated sufficiently slowly" (total-variation bound). Theorem 3.2: monotone improvement.
- Proofs use transition matrices and vectors over the state set, and an LP with a constraint "∀x ∈ X": finite state set in the theory. Experiments: grid world and MuJoCo with neural networks.
- The authors admit a "gap between the stationary assumption … and in practice"; experiments start from a random policy and use a recovery update.
- Discussion: "It is impossible to be 100% safe without some knowledge"; early training exceeds the constraint.

Conditions: S1 needed; S2 not needed; S3 in proofs; S4 needed; S5 needed (slow updates); S6 needed (ergodicity, episodes).

Verified quotes (checked against the source text, 2026-11-24)
- "the maximum allowed cumulative cost"
