---
key: elelimy2025
read: full
read_detail: full text: §1–6, Appendix (proof of Theorem 1) and Supplementary Materials (Theorem 2, PPO details)
read_on: 2026-11-24
---

# Elelimy, Szepesvari, White, Bowling 2025, Rethinking the Foundations for Continual Reinforcement Learning (RLJ 2025)

URL: https://arxiv.org/abs/2504.08161
Cited by [1] for: an explicit history-to-state map, offered against the finite context window (§4).
Read: Full text: §1–6, Appendix (proof of Theorem 1) and Supplementary Materials (Theorem 2, PPO details).

Key findings
- Not a safety method. It argues that four foundations of traditional RL (MDPs, atemporal artifacts, expected return, episodic benchmarks) are "antithetical to the goals of continual learning". It proposes the history process as formalism and deviation regret as evaluation measure.
- It rejects resets and ergodicity for the real world: "real-world settings do not allow one to reset the world into repeatable episodes or revisit states previously visited", and "This inability to revisit states renders ergodicity assumptions unrealistic for real-world settings." This is our S6, from a paper that [1] cite.
- The agent's state map is "some fixed partition of the histories", "the agent's own representation of the history". The paper does not learn it. [1] (§4, checked in 010_target) write that Elelimy et al. "propose that RL agents should learn an explicit mapping from trajectory history to state"; the formalism takes the map as fixed.
- The goal is given: "the agent's goal is a preference relation over histories" represented by a reward function. Spaces are finite: "we assume a finite action space" and "a finite observation space".
- Deviation regret is an evaluation measure. Its estimator is consistent only for "agents λ that take every action with probability at least c > 0 in every timestep" (Theorem 1). In a deployed agent, every action includes a destructive one.
- Safety guarantee: none.

- Episodic benchmarks "reinforce the idea that environments can always be thought of as ergodic and episodic and exhibit an optimal policy".
- The one experiment: PPO in a "Continuing Swimmer" (MuJoCo, no resets), 10 seeds; all agents stop learning after about 20M steps, and deviation regret detects it.
- The authors concede that deviation regret does not order agents ("This is a fair objection").
- The estimator bound grows as c^−H, so the requirement that every action has probability at least c is used in the proof, not only stated.
Conditions: S1 a given reward; S2 not needed; S3 finite actions and observations; S4 not needed; S5 the measure evaluates the learning rule; S6 explicitly not assumed.

Verified quotes (checked against the source text, 2026-11-24)
- "antithetical to the goals of continual learning"
- "real-world settings do not allow one to reset the world into repeatable episodes or revisit states previously visited"
- "This inability to revisit states renders ergodicity assumptions unrealistic for real-world settings."
- "some fixed partition of the histories"
- "the agent's own representation of the history"
- "the agent's goal is a preference relation over histories"
- "we assume a finite action space"
- "a finite observation space"
- "agents λ that take every action with probability at least c > 0 in every timestep"
- "reinforce the idea that environments can always be thought of as ergodic and episodic and exhibit an optimal policy"
- "Continuing Swimmer"
- "This is a fair objection"
