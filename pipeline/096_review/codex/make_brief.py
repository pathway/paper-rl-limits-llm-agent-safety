"""Write a self-contained Codex brief: the task text followed by the files inlined.
Codex's sandbox cannot read files on this machine, so the files travel in the brief.
Usage: python3 make_brief.py <task.md> <out.md> [--diff]"""
import sys, glob
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
FILES = ["300_render/out/paper.tex", "063_tools/tools.csv", "063_tools/roles.csv", "063_tools/sets.csv",
         "064_conditions/stated.csv", "065_tool_conditions/cells.csv", "070_unstated_conditions/unstated.csv",
         "075_mclean_conditions/stance.csv", "076_incidents/incidents.csv", "085_setting_conditions/cells.csv",
         "085_setting_conditions/reasons.csv", "100_analysis/facts.json", "096_review/key.csv", "096_review/rejected.csv"]
FILES += sorted(str(Path(p).relative_to(ROOT)) for p in glob.glob(str(ROOT / "047_extracts/*/extracts.csv")))

def main(task, out, extra):
    parts = [Path(task).read_text()]
    for rel in FILES + extra:
        parts.append(f"\n\n===== FILE {rel} =====\n{(ROOT / rel).read_text()}")
    Path(out).write_text("".join(parts))
    print(out, sum(len(p) for p in parts), "chars")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
