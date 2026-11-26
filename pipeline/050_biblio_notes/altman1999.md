---
key: altman1999
read: partial
read_detail: Preface, Chapter 1, Chapter 2 §2.1–2.2; Parts II–III not read
read_on: 2026-11-24
---

# Altman 1999, Constrained Markov Decision Processes (CRC Press)

URL: https://www-sop.inria.fr/members/Eitan.Altman/TEMP/h.pdf
Cited by [1] for: constraining agent behaviour; CMDPs (§1, §3.6.2, §4, §5).
Read: Preface, Chapter 1 (§1.1–1.8) and Chapter 2 §2.1–2.2 in full. Parts II–III (Ch. 6–16) not read; only the table of contents and §1.4/§1.7 summaries of them.

Key findings
- Model (Ch. 2): finite state set X, finite action set A, transition probabilities P_xay, immediate costs c and d; the controller observes the state (and history).
- Problem: minimise C(u) subject to D_k(u) ≤ V_k, where V_k "are some given constants" and the cost functions are given.
- Solution: a linear program over occupation measures, whose coefficients are the transition probabilities. This is planning with a known model; there is no learner.
- Unknown parameters are a separate "adaptive problem" (§1.3), surveyed briefly, not the subject of the book.
- Part II allows countable states under uniform Lyapunov conditions, which make the problem "almost equivalent to one with a finite state space" (§1.7).
- Costs are expectations. §1.3 quotes Ross and Chen: expected-cost constraints bound "the average delay … and not … the actual delay"; sample-path constraints are a separate model.
- Several controllers are treated only as stochastic games (§1.3).

Conditions: S1 needed (given costs and bounds); S2 needed (P in the LP); S3 needed (finite, or countable with Lyapunov conditions); S4 needed (state observed); S5 not applicable (no learner); S6 in expectation only.

Verified quotes (checked against the source text, 2026-11-24)
- "given immediate cost functions"
- "a finite number of states"
- "a finite set of actions"
- "specified in terms of expectations"
