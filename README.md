# Position: RL Safety Guarantees Do Not Yet Transfer to Deployed LLM Agents

A reply to McLean et al. [1], who argue that LLM-agent safety is an RL problem because an agent is a POMDP. The paper reads the twelve works behind the tools that [1] offers and asks which conditions each guarantee needs: six that the papers state and four that they do not. Of the eight works that state a guarantee, seven need in full a condition that fails in deployed LLM agents, and six do so even with the scaling gap that [1] concedes (finite spaces, a given model) granted. One guarantee survives deployment now: a shield over properties of typed tool calls, given a safe fallback such as halting. A certified safe set with a halting stop keeps its safety theorem only under assumptions that we found no method to meet. The paper closes with three open problems.

**Status:** Draft. The paper says that a large language model (Claude, Anthropic) drafted the text under the authors' direction, ran the literature search, proposed the conditions and table entries, and selected the quotations; a program checks that each quotation is verbatim in a stored copy of its source and that each cited work exists. The authors have not independently verified the citations, quotations or table entries. It reports no experiments.

**Read the paper:** [`onepager.pdf`](onepager.pdf) (21 pages, ICML 2026 style). The file name `onepager.pdf` is kept so that older links still work. It is the full paper, not a one-page version. [`draft.pdf`](draft.pdf) and [`icml/paper.pdf`](icml/paper.pdf) are the same file.

## The pipeline

The paper is generated. [`pipeline/`](pipeline/) holds numbered stage folders; each stage reads only from stages with lower numbers. Facts and judgements live in the stage tables, the draft imports them, and the build turns everything into the PDF. Each fact is stored once.

| Path | What it is |
|---|---|
| [`pipeline/000_README.md`](pipeline/000_README.md) | The stages of this paper, how to build, how to stamp claims |
| [`pipeline/000_METHOD.md`](pipeline/000_METHOD.md) | The method in general terms, for use on another paper, and how the review was made to converge |
| `pipeline/005_decisions/` | Each choice of scope or inclusion, with who decided it |
| `pipeline/010_target/` – `076_incidents/` | Target paper notes, search log, references, curated extracts, source notes, tools, conditions, incidents |
| `pipeline/065_tool_conditions/`, `085_setting_conditions/` | The judgement tables: each cell with its value, reason and evidence |
| `pipeline/095_claims/` | Fixed wording the paper prints (captions), with stamps |
| `pipeline/096_review/` | Review rounds: findings, gates, change logs, scores, cross-model checks |
| `pipeline/100_analysis/` | Pure, tested code that computes every count (`facts.json`, `sensitivity.md`) |
| [`pipeline/200_draft/draft.md`](pipeline/200_draft/draft.md) | Paper prose, with imports of facts and tables |
| `pipeline/300_render/` | Build, checks and template; [`out/paper.tex`](pipeline/300_render/out/paper.tex), [`out/backcheck.md`](pipeline/300_render/out/backcheck.md) (every quote with its source file and line) |

**Not included:** `045_fulltext/` (the stored full texts of the cited works, which are copyrighted), the extract candidates proposed by the scanner, review briefs that inline full texts, and the round snapshots. The build checks quotes against the full texts, so it does not run from this repository alone; the tests in `100_analysis/`, `300_render/`, `047_extracts/`, `040_biblio/` and `096_review/` do.

## Older material

- `draft.md`, `onepager.md` and `draft_conditions_short.md` are pointers kept so that old links still work.
- `icml/build.py`, `icml/template.tex` and the style files are the build of the earlier version; the current build is in `pipeline/300_render/`.
- [`probe_c1/`](probe_c1/): an earlier supplement, no longer part of the paper. A probe of whether text inside a tool output can change the objective of a deployed agent ([`PREREG.md`](probe_c1/PREREG.md), items, runner, 240 trials and their analysis).
- Earlier versions ("When Is Agent Safety a Reinforcement Learning Problem?", and v0.2 "On the Limits of Reinforcement Learning for LLM-Agent Safety") are in the git history.

## Related repositories

- [paper-two-cultures-agent-safety](https://github.com/pathway/paper-two-cultures-agent-safety)

Part of a set of AI-safety research artefacts by [Robin Ranjit Singh Chauhan](mailto:robin@pathwayi.com), Pathway Intelligence Inc. No licence has been chosen.

## Reference

[1] R. McLean, T. E. Lee, M. Mohammedalamen, K. Roice, G. Berseth, P. Pilarski, M. C. Machado, A. Lefaivre Škopac, B. Rosman (2026). AI Agent Safety is a Reinforcement Learning Problem. Second Workshop on Agents in the Wild (AIWILD), ICML 2026. https://openreview.net/forum?id=wvga9chmb6
