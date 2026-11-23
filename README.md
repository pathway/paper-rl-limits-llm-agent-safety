# Rebuttal to "AI Agent Safety is an RL Problem"

McLean et al. [1] argue that LLM-agent safety failures "are not novel" because an agent is a POMDP and RL has studied POMDP safety for decades. This rebuttal accepts the formalisation and rejects the inference: every safe-RL tool they name rests on a precondition that LLM agents break (the policy learns, the designer sets the reward, the cost function can be written). A short paper plus a one-page version.

**Status:** Draft. Most text was written by Claude (Anthropic) under Robin Chauhan's direction and has not been human-reviewed.

Start with `onepager.md`; `draft.md` is the full draft (PDFs alongside).

## Contents

| File | Title |
|---|---|
| [`draft.md`](draft.md) | On the Limits of Reinforcement Learning for LLM-Agent Safety: Formal Equivalence Is Not Method Transfer |
| [`draft.pdf`](draft.pdf) |  |
| [`onepager.md`](onepager.md) | On the Limits of Reinforcement Learning for LLM-Agent Safety: Formal Equivalence Is Not Method Transfer |
| [`onepager.pdf`](onepager.pdf) |  |


## Related repositories

- [paper-two-cultures-agent-safety](https://github.com/pathway/paper-two-cultures-agent-safety)

Part of a set of AI-safety research artefacts by [Robin Ranjit Singh Chauhan](mailto:robin@pathwayi.com), Pathway Intelligence Inc. The website at pathway.github.io/research/ is built from these repositories.

## References

[1] R. McLean, T. E. Lee, M. Mohammedalamen, K. Roice, G. Berseth, P. Pilarski, M. C. Machado, A. Lefaivre Škopac, B. Rosman (2026). AI Agent Safety is a Reinforcement Learning Problem. Second Workshop on Agents in the Wild (AIWILD), ICML 2026. https://openreview.net/forum?id=wvga9chmb6
