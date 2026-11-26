---
key: alshiekh2018
read: quotes
read_detail: targeted passages only
read_on: 2026-11-24
---

# Alshiekh, Bloem, Ehlers, Könighofer, Niekum, Topcu 2018, Safe RL via Shielding (AAAI 2018)

URL: https://arxiv.org/abs/1708.08611
Cited by [1]: NO. [1] names "safety shield" and "exact runtime shielding" without a citation. We use this paper because it introduced the term and because Wachi et al. 2023 (cited by [1]) names it as the model for its emergency stop.
Read: targeted passages only (preliminaries, abstraction definition, minimal interference, discussion of the learner); not read in full in this session.

Key findings (verified quotes)
- The shield is synthesised from a "given … temporal logic specification" (safety fragment of LTL).
- MDP preliminaries: "a finite set S of states", finite actions.
- The abstraction "has to be conservative with respect to the behavior of the real MDP"; it "may have finitely many states even if the MDP has infinitely many states and/or is only approximately known".
- The shield reads states through an "MDP observer function f : S → L".
- "The learning agent does not even need to know that it is shielded."
- Guarantee ends when "the abstraction turned out to be incorrect".
- A model of unsafe actions is "unavoidable if the allowed actions depend on the state of the environment".

Conditions: S1 needed; S2 needed (abstraction); S3 for the abstraction; S4 labels; S5 not needed; S6 not needed.

Verified quotes (located in 045_fulltext by the build)
- "We have constructed an abstraction"
- "satisfying a temporal logic safety specification"
- "has to be conservative with respect to the behavior of the real MDP"
- "The learner accepts elements from S × Q as state input"
