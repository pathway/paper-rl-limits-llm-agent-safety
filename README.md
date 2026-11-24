# When Is Agent Safety a Reinforcement Learning Problem? Six Stated and Four Unstated Conditions

A reply to McLean et al. [1], who argue that LLM-agent safety is an RL problem because an agent is a POMDP. The paper accepts the formalisation. It asks which assumptions each safe-RL tool needs, reads six of them from the source papers of the tools [1] names, and adds four that those papers do not state. Deployed LLM agents violate all four. Main practical result: a shield on a property defined over actions keeps its guarantee around a deployed agent; a shield on a property of world state loses it. A pre-registered probe tests the first unstated condition.

**Status:** Draft. The paper says that a large language model assisted with the literature search, the drafting and the probe code. It has not been fully human-reviewed.

**Read the paper:** [`onepager.pdf`](onepager.pdf) (9 pages; identical to [`icml/paper.pdf`](icml/paper.pdf)). The file name `onepager.pdf` is kept so that older links still work. It is the full paper, not a one-page version.

## Contents

| Path | What it is |
|---|---|
| [`draft_conditions_short.md`](draft_conditions_short.md) | Paper source (Markdown) |
| [`icml/paper.pdf`](icml/paper.pdf) | Paper, built in the ICML 2026 style |
| `icml/build.py`, `template.tex`, `*.sty`, `*.bst` | Build: converts the Markdown to LaTeX and runs it |
| [`probe_c1/`](probe_c1/) | Supplement: a probe of condition C1 (can text inside a tool output change the objective of a deployed agent?) |
| [`probe_c1/PREREG.md`](probe_c1/PREREG.md) | Plan, written before the run |
| `probe_c1/items.py`, `run.py`, `analyze.py` | Items, runner and analysis |
| `probe_c1/results.jsonl`, `analysis_output.md` | Raw results (240 trials) and the analysis |

The earlier version (v0.2, "On the Limits of Reinforcement Learning for LLM-Agent Safety") is in the git history.

## Related repositories

- [paper-two-cultures-agent-safety](https://github.com/pathway/paper-two-cultures-agent-safety)

Part of a set of AI-safety research artefacts by [Robin Ranjit Singh Chauhan](mailto:robin@pathwayi.com), Pathway Intelligence Inc. No licence has been chosen.

## Reference

[1] R. McLean, T. E. Lee, M. Mohammedalamen, K. Roice, G. Berseth, P. Pilarski, M. C. Machado, A. Lefaivre Škopac, B. Rosman (2026). AI Agent Safety is a Reinforcement Learning Problem. Second Workshop on Agents in the Wild (AIWILD), ICML 2026. https://openreview.net/forum?id=wvga9chmb6
