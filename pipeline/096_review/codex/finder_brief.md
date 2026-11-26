QUESTION
Which statements in this position paper are factually wrong, overclaimed, or contradicted by its own tables or its cited sources? The answer decides what the next review round fixes.

SCOPE
- Rendered paper with numbers expanded: 300_render/out/paper.tex
- Source tables the paper is generated from: 063_tools/*.csv, 064_conditions/stated.csv, 065_tool_conditions/cells.csv, 070_unstated_conditions/unstated.csv, 075_mclean_conditions/stance.csv, 076_incidents/incidents.csv, 080_settings/, 085_setting_conditions/cells.csv and reasons.csv; computed counts 100_analysis/facts.json
- Verbatim extracts from the cited works, with file and line: 047_extracts/<key>/extracts.csv (the full texts are not attached)
- Frozen key of core claims: 096_review/key.csv

CONTRACTS
- Every quote must appear verbatim in the cited full text.
- Every sentence citing a work must be supported by that work as worded.
- Counts in the prose must equal those the tables produce (100_analysis/facts.json).
- A table cell's value must be supported by its reason and evidence.
- Grading rule (paper appendix "settings"): a cell is x when the condition fails in the setting as usually run, ~ when it holds in usual runs but fails in reported cases or holds only in part.

ALREADY CHECKED
- 096_review/rejected.csv lists findings already judged and settled. Do not report them or rephrasings of them.
- Design choices recorded in 005_decisions/decisions.csv are settled unless a source contradicts them.

NOT IN SCOPE
Style, length, page limit, minor wording, LaTeX layout.

ASK
All files are attached below this brief; you cannot read the file system. Read the paper in full, then check the quotes, cells, counts and internal consistency against the attached files. Where a claim needs a full text that is not attached, report it only if the attached extracts contradict it. Report only material defects: a wrong fact or quote, a citation that does not support its sentence, a count or cell the sources do not support, a contradiction between two parts of the paper, or a missing qualification that changes a key claim.
Output ONLY JSON lines, one object per finding, with keys:
"where" (section or table), "claim" (the paper's words), "problem", "evidence" (verbatim quote from an attached file, naming the file), "severity" (wrong|overclaim|unsupported|unclear), "key" (K01..K21 or none), "fix" (smallest correct change).
If you find no material defect, output the single line {"none": true}. Do not run shell commands; everything you need is attached.
