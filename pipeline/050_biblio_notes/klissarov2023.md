---
key: klissarov2023
read: full
read_detail: full text: §1–8 and Appendices A–K
read_on: 2026-11-24
---

# Klissarov, Machado 2023, Deep Laplacian-based Options for Temporally-Extended Exploration (ICML 2023)

URL: https://arxiv.org/abs/2301.11181
Cited by [1] for: exploration (§3.5, with Tse 2025) and for options against the exploration problem (§4).
Read: Full text: §1–8 and Appendices A–K.

Key findings
- An exploration method, not a safety method: DCEO, "a fully online deep RL algorithm for discovering Laplacianbased options".
- The goal is to cover more of the state space: to ensure that parts of the environment "that are unlikely to be visited by chance can be visited more often".
- Earlier Laplacian methods needed the Laplacian "given or could be fully estimated" and tabular value functions; DCEO removes these needs.
- Experiments: "pixel-based tasks", navigation grids with "episodes being at most 100 steps long", Rubik's cube, Montezuma's Revenge, MiniWorld (3D, partially observed). Some tasks are non-stationary.
- Safety guarantee: none. More exploration raises the chance of reaching an irreversible state; the paper does not consider such states.

- Danger enters only as reward: in Rooms with obstacles, "If the agent collides with one of these obstacles it receives a −1 reward and the episode terminates."
- Every algorithm starts episodes with "Reset environment and observe state s"; "All environments are stochastic: the agent's action is overwritten by a random action with probability 0.15."
- The count baseline gets "perfectly accurate state counts". Non-stationary tasks change goal or topology mid-run; episodes still reset.
- Safety is not discussed anywhere in the paper.
Conditions: S1 reward only; S2, S3, S4 not needed; S5 exploration is a property of training; S6 episodes and revisits.

Verified quotes (checked against the source text, 2026-11-24)
- "a fully online deep RL algorithm for discovering Laplacianbased options"
- "that are unlikely to be visited by chance can be visited more often"
- "given or could be fully estimated"
- "pixel-based tasks"
- "episodes being at most 100 steps long"
- "If the agent collides with one of these obstacles it receives a −1 reward and the episode terminates."
- "Reset environment and observe state s"
- "perfectly accurate state counts"
