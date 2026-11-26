# When Is Agent Safety an RL Problem? — source pipeline

The paper is generated. Facts and judgements live in the stage folders; the draft imports them; `300_render/build.py` turns everything into the PDF. Each fact is stored once (single point of truth).

## Stages

A stage reads only from stages with lower numbers.

| Stage | Holds | Kind |
|---|---|---|
| `005_decisions/decisions.csv` | Each choice of scope or inclusion: who decided, the instruction in the author's words, and what the choice rested on | record |
| `010_target/` | McLean et al. 2026: tool-to-citation map and verified quotes (`mclean2026.md`); section-by-section parse (`mclean2026_sections.md`) | facts |
| `020_search/` | Novelty search record: every query, candidates, full-text reads | record (not printed) |
| `040_biblio/` | `refs.yaml`: one entry per work (`key`, natbib `short` and `year`, printed `text`). `existence.csv`: result of `verify.py`, which looks up each arXiv id, DOI, held text or URL and compares title and first author | facts |
| `045_fulltext/` | `pdf/<key>.pdf`: the source. `<key>.txt`: derived by `extract.py`, pages separated by form feeds. `tex/<key>/`: the authors' LaTeX from arXiv (`fetch_tex.py`), for formulae. `manifest.csv`: URL, hashes, pages. Copyrighted material: keep this folder out of any public copy | facts |
| `047_extracts/<key>/` | `candidates.csv`: passages proposed by `scan.py` (generated); `extracts.csv`: the curated key lines, formulae and tables that later stages cite by id (`tex` holds a formula in the authors' own LaTeX). `PROTOCOL.md` lists the topics to extract | facts |
| `050_biblio_notes/<key>.md` | Per source: read scope (front matter), key findings, verbatim quotes | facts |
| `063_tools/` | `tools.csv`: each work, its tool label (`label_origin`: source or ours), its role in McLean et al. (`mclean_role`, with `role_evidence`: McLean extract ids), guarantee and `guarantee_kind`, the `decision` that added it. `roles.csv`: the roles. `sets.csv`: the sets that counts and headers refer to, each defined by the roles it admits, with its noun phrase | judgement |
| `064_conditions/stated.csv` | S1–S6: label, definition, sources, `search_terms` (used to test absence claims) | judgement |
| `065_tool_conditions/cells.csv` | Tool × S1–S6: displayed cell, reason, `evidence_type` (quote, absence, judgement), `evidence` (extract ids), `hits_reviewed`, `by` | judgement |
| `070_unstated_conditions/unstated.csv` | U1–U4: label, definition (Table 3) | judgement |
| `075_mclean_conditions/stance.csv` | What McLean et al. say about each condition: stance (concedes, states, builds on, partly, not discussed), locator, evidence with quotes | judgement |
| `076_incidents/incidents.csv` | Incidents in McLean et al.: listed or worked through, irreversible, conditions that fail, our sources | judgement |
| `080_settings/settings.csv` | T-RL … D-AGENT: phase, how the problem is posed (Table 4) | judgement |
| `085_setting_conditions/` | `cells.csv`: setting × condition values, `by` (Table 5); `reasons.csv`: per-condition reasons | judgement |
| `090_related/related.md` | Related-work prose, citations by key | argument |
| `095_claims/claims.csv` | Fixed wording that the paper prints (captions) and the set definitions, each with the files it depends on and a stamp: hash, who verified it, when | judgement |
| `100_analysis/` | `analyze.py` (pure, tested) computes `facts.json` (each count comes with the noun phrase of its set) and `sensitivity.md` (which facts change when a set or a row is left out) | computed |
| `200_draft/draft.md` | Prose and imports only | argument |
| `300_render/` | `build.py` (shell), `render.py` (pure), `checks.py`, template, style; output in `out/` | presentation |
| `900_archive/` | Earlier drafts, the v0.2 draft, the removed probe | not used |

## Claims, sets and stamps

- A count in the prose is `{{fact:<set>_n}}` or `{{fact:<set>_phrase}}`; the noun phrase comes from `063_tools/sets.csv`. The build rejects a number typed next to a set noun (tools, works, papers, conditions, incidents).
- A table header over a set and every caption are generated from `sets.csv`, `roles.csv` and `095_claims`.
- A row joins the tool table only with a role, McLean extracts that name the work, and a decision id.
- A claim is stale when its wording or a file it depends on changes. Read it against those files, then run `python3 300_render/stamp.py <claim id> --by <name>`. The build never stamps.
- The role evidence proves that McLean et al. mention the work. It does not prove the role; that is a judgement, which the stamp records and a second reader should repeat.
- Independent review: a workflow of reader agents that see only a list of our claims and the stored full texts, and must answer with verbatim quotes and line numbers, finds errors the author misses. Check each of their quotes before acting, record the outcome in `005_decisions`, and only then stamp.

## Forward flow for a source

1. Put the full text in `045_fulltext/<key>.txt` and add a row to `manifest.csv`.
2. Scan it: `python3 047_extracts/scan.py structural <key>` (numbered assumptions and theorems, no model) and `python3 047_extracts/scan.py llm <key>` (topics of `PROTOCOL.md`, small model). Both write `candidates.csv`; a passage that is not verbatim in the full text is dropped.
   For several long sources, run the model pass as a workflow instead: one agent per chunk of about 45,000 characters reads `PROTOCOL.md` and its lines of the full text, and writes its passages to `047_extracts/<key>/llm_<n>.json`. Then `python3 047_extracts/scan.py merge <pass name> <key> ...` verifies them and writes the verbatim ones to `candidates.csv`. (First use, 2026-11-24: 9 Sonnet agents, 316 passages proposed, 316 verbatim.)
3. Curate: `python3 047_extracts/scan.py promote <key> c3 c7` copies candidates into `extracts.csv`. Add a readable `clean` form for a formula by hand; the build does not check `clean`.
4. Write the note, the table cells and the stance rows from the extracts, and cite the extract ids in the `evidence` column. For a cell that says a condition is not needed, set `evidence_type` to `absence`, read the search hits listed in `out/backcheck.md`, and record their number in `hits_reviewed`.
5. Build. `300_render/out/backcheck.md` then lists every extract and every quote used, with file and line.

## Imports in the draft

- `[@key]`, `@key`, `[@key, {§3.6}]`: citations (pandoc syntax; braces keep the § in locators).
- `{{table:stated|tool_conditions|unstated|mclean_stance|incidents|settings|setting_conditions}}`: a table from the CSVs.
- `{{fact:<id>}}`: a value from `100_analysis/facts.json`.
- `{{list:setting_reasons}}`, `{{include:related}}`, `{{appendix:tool_conditions}}`.
- `\ref{sec:…}`, `\ref{tab:…}`, `\ref{app:cells}`: cross-references.

## Build

```
cd 300_render && python3 build.py          # checks, facts, PDF in out/paper.pdf
cd 100_analysis && python3 -m pytest -q    # analysis tests
cd 300_render && python3 -m pytest -q      # render, check and back-check tests
cd 047_extracts && python3 -m pytest -q    # scanner tests
cd 040_biblio && python3 -m pytest -q      # reference-check tests
```

The build stops if any check fails:
- a citation key that is not in `040_biblio`;
- a tool without a McLean locator, a note, or a read scope;
- a missing tool cell or reason; a quoted phrase in a reason that is not in the source's note;
- a missing or invalid setting cell (allowed: ✓ ~ ✗ n/a);
- a missing or invalid McLean stance; an incident with unknown conditions, or one worked through by McLean without our sources;
- a cited reference whose existence is not confirmed (`040_biblio/existence.csv`);
- a stored PDF or text whose hash differs from the manifest;
- a formula in an extract that is not verbatim in the authors' LaTeX (or, without LaTeX source, has no page image);
- an absence cell whose search now finds a different number of hits than were reviewed;
- a quote in the draft or a table that is in no stored full text;
- a tool or the target without full text or extracts; an extract, a cell quote or a note's verified quote that is not in the full text;
- a cell or stance quote that is not in the extracts cited in its `evidence` column;
- a tool row without a role, role evidence that names the work, or a decision id;
- a stale or unverified claim (`095_claims`);
- a count typed in the draft next to a set noun;
- a typed table row in the draft;
- an unresolved import; undefined citations or overfull boxes in LaTeX.

## Rules

- Change a fact or judgement in its stage file, never in the draft.
- A quote enters a note only after it has been checked against the source text.
- Use quotation marks in the draft only for verbatim quotes. Set our own examples and objections in italics.
- A count or a list of conditions in the prose is a `{{fact:…}}`, never typed.
- `by` records who made a judgement (`LLM`, author, RL reader). All cells are `LLM` until a reader checks them.
