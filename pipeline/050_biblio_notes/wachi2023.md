---
key: wachi2023
read: full
read_detail: main text §1–8 and Appendix D.1 (proof of Theorem 4.1); other appendices not read
read_on: 2026-11-24
---

# Wachi, Hashimoto, Shen, Hashimoto 2023, Safe Exploration in RL: A Generalized Formulation and Algorithms (NeurIPS 2023)

URL: https://arxiv.org/abs/2310.03225
Cited by [1] for: "ensuring safe exploration" (§1).
Read: main text (§1–8) in full; appendices not read.

Key findings
- Setting: episodic CMDP; "with a given (fully-observable) state s".
- Problem 4 (GSE): instantaneous constraint g(s_h, a_h) ≤ b_h with probability 1 at every step, during training. The threshold is "myopically known".
- Assumption 3.2: a safety margin (Slater-like).
- Assumption 3.3: "emergency stop action" with P(s1 | s, â) = 1 for all s; the agent may "reset the environment". The authors note that where human intervention is costly, the agent would need a learned reset policy, "which we will leave to future work".
- Assumption 3.4: a δ-uncertainty quantifier on the safety cost; realised by a GLM with a known feature map (Def. 5.1, Assumption 5.3) or by a GP with bounded RKHS norm (Theorem 6.1).
- Theorem 4.1: safety w.p. ≥ 1−δ, from executing only actions in the certified safe set and stopping when none exists. The reward is learned by "an arbitrary RL algorithm".
- The paper calls MASE "a variant of shielding methods (especially, preemptive shielding in [2])", where [2] is Alshiekh et al. 2018.
- Transitions are not assumed known; the paper criticises earlier work for "known state transition".
- Experiments: Safety Gym and a grid world.

Conditions: S1 needed (observed cost, known threshold, regular cost); S2 not needed; S3 not needed; S4 needed; S5 only as an action filter; S6 needed (emergency stop resets the environment).
Relevance to agents: stopping before an uncertified action is possible for a deployed agent (halt and ask); the reset to the initial state is not, and a valid uncertainty quantifier for the cost of a tool call does not exist yet.

Verified quotes (checked against the source text, 2026-11-24)
- "is known at time h"
- "an emergency stop action"
- "even with human interventions"

Appendix D.1 read on 2026-11-24: the proof of Theorem 4.1 uses the uncertainty quantifier for chosen actions and, when no action qualifies, the emergency stop, for which "safety is guaranteed with a probability of 1". It does not use the reset itself.
