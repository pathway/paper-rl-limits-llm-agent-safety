# Method: a paper as a generated pipeline, and how to make its review converge

For an agent who will apply this to another paper. `000_README.md` describes this paper's stages; this file states the method in general terms.

## Part 1. Structured folders and dependencies

### 1.1 Core rule

- The paper is a build output. The source of truth is the stage tables, not the draft.
- Each fact is stored once. The draft imports facts and tables; it never types them.
- To correct a fact, edit the stage file that holds it, then rebuild. Never correct only the draft text.

### 1.2 Numbered stages, one direction

- Each stage is a folder named `NNN_name/`. A stage reads only from stages with lower numbers. The dependencies form a DAG (Lakos levelization).
- Leave gaps in the numbering (045, 047, 063, 064 …) so you can insert a stage without renumbering.
- Each stage has a kind. The kind tells you how much to trust it and who must check it.

| Kind | Meaning | Example |
|---|---|---|
| record | what was done or decided, by whom | decisions log, search log |
| facts | stored or verbatim material | full texts, extracts, references |
| judgement | our reading of the facts | table cells with reasons |
| argument | prose | draft, related work |
| computed | pure functions of earlier stages | `facts.json` |
| presentation | rendering | build, template |

### 1.3 Generic stage template

| Stage | Holds | Rule |
|---|---|---|
| `005_decisions/decisions.csv` | each choice of scope or inclusion: id, who decided, the author's own words, the basis | Rows added by the agent say "author to confirm" |
| `010_target/` | the paper under discussion, parsed section by section, with verified quotes | Read it end to end before writing claims about it |
| `020_search/` | every search query and its candidates | not printed |
| `040_biblio/refs.yaml` | one entry per work with a stable key; `verify.py` checks each work exists (arXiv id, DOI, URL; title and first author) | The build rejects a cited key whose existence is not confirmed |
| `045_fulltext/` | PDFs (the source), derived text with page breaks, author LaTeX for formulae, `manifest.csv` with hashes | Copyrighted: keep out of public copies. Build checks hashes |
| `047_extracts/<key>/` | `candidates.csv` (proposed by a scanner, structural or LLM), `extracts.csv` (curated passages with ids) | A passage that is not verbatim in the full text is dropped |
| `050_biblio_notes/<key>.md` | per source: read scope in front matter (full, sections, extracts only), findings, quotes | Never claim "read in full" unless it was |
| `06x–08x` domain tables | the entities of the argument and entity × criterion cells | Each cell has: value, reason, `evidence_type` (quote, absence, judgement), `evidence` (extract ids), `by` (LLM, author, expert) |
| `095_claims/claims.csv` | fixed wording the paper prints (captions, set definitions), the files each depends on, a stamp (hash, verifier, date) | A claim goes stale when a file it depends on changes; a person or agent re-reads and re-stamps it. The build never stamps |
| `100_analysis/` | pure, tested code: tables → `facts.json` (counts with their noun phrase); `sensitivity.md` (which facts move if a row or set is dropped) | functional core, no I/O inside |
| `200_draft/draft.md` | prose plus imports only | `{{fact:id}}`, `{{table:name}}`, `[@key]` |
| `300_render/` | `build.py` (shell), `render.py` (pure), `checks.py`, template; output in `out/` | build stops on any failed check |
| `900_archive/` | old drafts, snapshots before each review round | not read by the build |

### 1.4 The evidence chain

Each quote in the paper can be traced in one step per link:

```
draft quote ──> table cell `evidence` ──> extract id ──> full-text file:line ──> PDF (hash in manifest)
```

- The build writes `out/backcheck.md`: every quote used, with file and line. This makes a back-check cheap.
- An absence claim ("the paper does not assume X") stores its search terms. The build reruns the search, and fails if the number of hits differs from the number reviewed.

### 1.5 Counts come from set definitions

- Define each set the prose counts (e.g. "works the target offers") in a `sets.csv` by an inclusion rule, with its noun phrase.
- The prose writes `{{fact:<set>_n}}` or `{{fact:<set>_phrase}}`. The build rejects a number typed next to a set noun.
- A row joins a set only with evidence that it meets the rule and a decision id. Test the rule on every row. (Error made here: a table header said "tool named by the target" and was false for 10 of 14 rows.)

### 1.6 Checks that pay for themselves

Make the build fail on each of these:
- unknown citation key; unconfirmed reference;
- a quote (two words or more) not found in a stored full text, or not in a source cited next to it;
- a cell quote not in the extracts it cites;
- a hash mismatch on a stored source;
- a formula not verbatim in the authors' LaTeX;
- a missing or invalid cell value;
- a stale or unstamped claim;
- a typed count; a typed table row in the draft;
- an unresolved import; LaTeX errors.

Test the pure parts (`analyze.py`, `render.py`, checks, scanner) with plain values. Write the failing test before each fix.

### 1.7 How to port to another paper

1. Create the folder skeleton (1.3). Copy `300_render/` and `100_analysis/` code; rename tables.
2. Store the target paper and every cited source as PDF + text + manifest. Do this before writing claims.
3. Read the target end to end; write `010_target/` with section locators.
4. Design the domain tables: which entities, which criteria, which cell values (keep a written grading rule).
5. Extract passages forward (scanner → candidates → curated extracts), then fill cells from extracts only.
6. Define the sets and facts; write the draft with imports only.
7. Build; fix every check failure in its stage file.
8. Log each scope choice in `005_decisions` with the author's words.
9. Before trusting your own stamps, run an independent blind reader (other agents that see only the claims and the full texts and must answer with verbatim quotes and line numbers). They find errors the author does not.

## Part 2. How the review started to converge

### 2.1 What did not converge (rounds 1–3)

- Each round: blind finders → fix everything found.
- About a third of the next round's findings were caused by the previous round's fixes.
- Finders re-reported points already decided. There was no stop rule and no stable measure.

### 2.2 What changed (round 4: measure only)

- **Frozen key.** `096_review/key.csv`: 21 core claims of the paper (id, claim, where). Each round scores every claim: supported, qualify or refuted. The key changes only with a recorded reason (`revised_in`).
- **Settled list.** `096_review/rejected.csv`: findings already judged (rejected or minor, with the reason). Every finder receives it and must not re-report it. Decisions in `005_decisions` are settled unless a source contradicts them.
- **Stop rule** (`converge.py`, tested): a round is clean when every key claim is supported, no fix changed a key claim, and no confirmed finding hit one.
- Round 4 only measured; it gave a baseline (20 of 21 supported, 21 raw findings).

### 2.3 The loop used in rounds 5–8

```
snapshot ─> MEASURE ─> COLLECT ─> GATE ─> FIX ─> FIX-CHECK ─> REPAIR ─> SETTLE ─> SCORE
            (2 model    (merge     (refute +  (tables   (2 model
             families)   to JSON)   material?) first)    families)
```

1. **Snapshot**: `900_archive/rounds/before_round_N.tgz` and the draft.
2. **Measure** (one workflow, Sonnet agents):
   - 4 scorer groups score the key claims against the built paper and sources;
   - 5 finder lenses (e.g. quotes, cells, counts, internal consistency, and a **diff-audit** lens that reads the previous round's change log, because fixes cause defects);
   - one finder from the other model family (Codex). Its sandbox could not read files here, so `096_review/codex/make_brief.py` inlines the paper, tables, facts, key, settled list and extracts into one brief.
   - Every finder brief has: QUESTION, SCOPE, CONTRACTS, ALREADY CHECKED (the settled list), NOT IN SCOPE (style, length), ASK (JSON lines with where, claim, problem, verbatim evidence, severity, key id, smallest fix; or `{"none": true}`).
   - Materiality bar: report only a wrong fact or quote, an unsupporting citation, a wrong count or cell, a contradiction, or a missing qualification that changes a key claim.
3. **Collect**: `collect.py` merges findings and every non-supported score into `findings/round_N.json`.
4. **Gate** (one workflow): per finding, a Sonnet refuter tries to refute it and judges materiality → confirmed, refuted or settled. Rule added after a miss: "A source described wrongly is a wrong fact and is material even when the claim it supports survives."
5. **Fix**: one fixer agent only (not one per finding, to avoid conflicts). It edits stage tables first, the draft only for prose, logs every edit in `changes/round_N.csv` (file, old, new, source quote), rebuilds and runs the tests.
6. **Fix-check**: a Sonnet check of sources and consistency, and the other model family judges each change row (ok or broken, with exact repair text). A repair agent applies the repairs.
7. **Settle**: `settle.py` adds refuted and minor findings to `rejected.csv`, so they are not raised again.
8. **Score**: `score_round.py` writes `scores/round_N.csv`; `converge.py` prints the trend.
9. Record each judgement the agent made as a decision with "author to confirm".

### 2.4 Results

| Round | Raw findings | Confirmed material defects | Key claims supported |
|---|---|---|---|
| 5 | 26 | 4 (2 by the gate, 2 the gate missed) | not measured |
| 6 | 13 | 4 | 17 / 21 |
| 7 | 7 | 1 | 17 / 21 |
| 8 | 3 (all from scores; all 6 finders found nothing) | 1 | 18 / 21 |

No round is clean yet: round 8's one fix must be re-measured.

### 2.5 Lessons

- **Measure before fixing**, and keep measure and fix in separate steps.
- **Freeze a key and a settled list from round 1.** Without them, finders re-litigate and the count does not fall.
- **Fixes are the main source of new defects.** Log every edit and audit the log next round (diff-audit lens and a cross-family fix-check).
- **Use two model families.** Each found defects the other missed.
- **Gate count is the signal; scorer verdicts are noisy.** Scorers flipped 3–5 claims per round on unchanged text.
- **Tighten the gate when it misses.** Write the miss into the gate rule.
- **One fixer, tables first.** Parallel fixers conflict; draft-only fixes break the single source of truth.
- **Snapshot each round** so any round can be reverted.
- **Stop rule up front**: e.g. one clean round, or a fixed budget.
