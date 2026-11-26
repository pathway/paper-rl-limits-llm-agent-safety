QUESTION
Did the fixes of this review round introduce an error into the position paper? The answer decides which fixes are kept, repaired or reverted.

SCOPE
- The change log of the round is the attached file 096_review/changes/round_<n>.csv (the last attached file): one row per edit, with file, old text, new text and the source quote.
- The paper after the fixes (300_render/out/paper.tex) and the tables it is generated from are attached after it.

CONTRACTS
- New text must be true as worded against the attached tables and extracts.
- A fix must not contradict another part of the paper, move a count without the prose that uses it, or drop a qualification that was still true.
- Quotes must be verbatim.

ALREADY CHECKED
- The findings each fix addresses were verified by a separate reviewer. Do not re-open whether the finding was right; judge only the new text.
- 096_review/rejected.csv lists settled points.

NOT IN SCOPE
Style, length, findings unrelated to the changes.

ASK
All files are attached below; you cannot read the file system. For each change row, decide ok or broken.
Output ONLY JSON lines, one per change you judge broken, with keys: "change", "problem", "evidence" (verbatim quote from an attached file, naming the file), "repair" ("revert" or the exact corrected text). Output nothing for changes that are ok. If all are ok, output the single line {"all_ok": true}.
