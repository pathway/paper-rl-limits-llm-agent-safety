---
key: vasan2024
read: full
read_detail: full text: §1–7 and Appendix A (hyper-parameters, network, guiding reward)
read_on: 2026-11-24
---

# Vasan, Wang, Shahriar, Bergstra, Jägersand, Mahmood 2024, Revisiting Sparse Rewards for Goal-Reaching Reinforcement Learning (RLJ 2024)

URL: https://arxiv.org/abs/2407.00324
Cited by [1] for: reward misspecification (§3.5, with Muslimani 2025 and Knox 2023).
Read: Full text: §1–7 and Appendix A (hyper-parameters, network, guiding reward).

Key findings
- A reward-specification paper, not a safety method. It argues for a minimum-time reward: −1 per step "with termination upon reaching the goal state".
- Claim: the minimum-time specification avoids the bias of hand-crafted dense rewards and can beat them on their own metrics.
- Diagnostic: the goal-hit rate of the initial policy predicts learning success.
- Setting: an MDP with "continuous state space S and action space A"; SAC; simulated Reacher and Ball-in-Cup; four real robots, "pixel-based policies from scratch within two to three hours".
- Resets are part of the method: "If the agent exceeds the time limit, we reset the environment". The time limit is tuned to raise target hits.
- Safety guarantee: none. Scope: goal-reaching tasks with a known, observable goal state.

- Real-robot cost: the experiments "took nearly 200 hours of usage on real robots", and the reported robot time excludes resets: "robot experience time does not include time required to reset the environment".
- Safety is not discussed anywhere in the paper.
Conditions: S1 a known goal state; S2, S3 not needed; S4 the task is posed as an MDP; S5 training; S6 resets after each time limit.

Verified quotes (checked against the source text, 2026-11-24)
- "with termination upon reaching the goal state"
- "continuous state space S and action space A"
- "If the agent exceeds the time limit, we reset the environment"
- "the agent receives the next state"
- "pixel-based policies from scratch within two to three hours"
- "took nearly 200 hours of usage on real robots"
- "robot experience time does not include time required to reset the environment"
