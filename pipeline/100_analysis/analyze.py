"""Facts computed from the condition tables. Pure functions; I/O only in main().

Reads 063, 064, 065, 070, 075, 076, 085. Writes facts.json, which 200_draft imports as {{fact:<id>}},
and sensitivity.md. A count is always printed with the noun phrase of its set (063_tools/sets.csv).
"""
from collections import defaultdict
from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parent.parent
FAILS = "✗"
SCALING_GAP = ("S2", "S3")   # the gaps of representation and model that McLean et al. (§5) name as the first limit


def read_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def setting_grid(rows):
    """[{condition, setting, value}] -> {setting: {condition: value}}."""
    grid = defaultdict(dict)
    for r in rows:
        grid[r["setting"]][r["condition"]] = r["value"]
    return dict(grid)


def tool_needs(rows):
    """[{tool, condition, display}] -> {tool: [conditions whose cell is filled]}; a filled cell means 'needed'."""
    needs = defaultdict(list)
    for r in rows:
        if r["display"].strip():
            needs[r["tool"]].append(r["condition"])
    return dict(needs)


def with_guarantee_kind(tools, kind):
    """[{key, guarantee_kind}] -> keys whose guarantee is of this kind (safety | other | none)."""
    return [t["key"] for t in tools if t["guarantee_kind"] == kind]


def full_needs(rows):
    """[{tool, condition, display}] -> {tool: [conditions needed in full (a ✓ cell)]}; qualified cells are excluded."""
    needs = defaultdict(list)
    for r in rows:
        if r["display"].strip() == "✓":
            needs[r["tool"]].append(r["condition"])
    return dict(needs)


def differing(grid, a, b, order):
    return [c for c in order if grid[a][c] != grid[b][c]]


def failing_needs(needs, grid, setting):
    """{tool: [needed conditions that fail in setting]} for every tool with at least one."""
    out = {t: [c for c in cs if grid.get(setting, {}).get(c) == FAILS] for t, cs in needs.items()}
    return {t: cs for t, cs in out.items() if cs}


def guaranteed_failing(strict, guaranteed, grid, setting, granted=()):
    """Keys of guaranteed works that need in full (a ✓ cell) a condition that fails (a ✗ cell) in `setting`.

    Conditions in `granted` are treated as met, e.g. the scaling gap.
    """
    needs = {t: [c for c in strict.get(t, []) if c not in granted] for t in guaranteed}
    return list(failing_needs(needs, grid, setting))


def compress(ids, order):
    """['S1',...,'S6','U1',...,'U4'] -> 'S1–S6 and U1–U4'; ['S2','S4','U1'] -> 'S2, S4 and U1'."""
    groups, run = [], []
    for c in order:
        if c in ids:
            run.append(c)
        elif run:
            groups.append(run); run = []
    if run:
        groups.append(run)
    parts = []
    for g in groups:
        prefix_runs = defaultdict(list)
        for c in g:
            prefix_runs[c[0]].append(c)
        for cs in prefix_runs.values():
            parts.extend([f"{cs[0]}–{cs[-1]}"] if len(cs) > 2 else cs)
    if not parts:
        return "none"
    return parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1]


WORDS = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split()


def number_word(n):
    return WORDS[n] if n < len(WORDS) else str(n)


def count_phrase(k, n):
    if k == n == 2:
        return "both"
    return f"all {number_word(n)}" if k == n else f"{number_word(k)} of {number_word(n)}"


SHARED_STANCES = {"concedes", "states", "builds on"}


def conditions_with_stance(stance, wanted):
    """[{condition, stance}] -> ids whose stance is in `wanted`."""
    return [r["condition"] for r in stance if r["stance"] in wanted]


def failing(grid, setting):
    """Conditions that fail outright (a ✗ cell) in a setting."""
    return [c for c, v in grid[setting].items() if v == FAILS]


def holding(grid, setting):
    return [c for c, v in grid[setting].items() if v == "✓"]


def most_met_phrase(grid, setting, others):
    """How a setting ranks among `others` by the number of conditions that hold: the most, or as many as any."""
    mine = len(holding(grid, setting))
    best = max(len(holding(grid, s)) for s in others)
    if mine < best:
        return "fewer conditions than some other LLM column"
    tied = [s for s in others if s != setting and len(holding(grid, s)) == best]
    return "as many conditions as any LLM column" if tied else "the most conditions of any LLM column"


def needs_of(tool_cells, tool, order):
    """(full, part, none): the stated conditions that one tool needs in full, in part, or not at all, as compressed lists."""
    cell = {c["condition"]: c["display"].strip() for c in tool_cells if c["tool"] == tool}
    stated = [c for c in order if c in cell]
    full = [c for c in stated if cell[c] == "✓"]
    part = [c for c in stated if cell[c] and cell[c] != "✓"]
    none = [c for c in stated if not cell[c]]
    return tuple(compress(x, order) for x in (full, part, none))


def split_list(field):
    return [x.strip() for x in field.split(";") if x.strip()]


def members(tools, set_row):
    """Rows of the tool table that belong to a set; a set is defined by the roles it admits (063_tools/sets.csv)."""
    roles = split_list(set_row["roles"])
    return [t for t in tools if t["mclean_role"] in roles]


def counted(n, label):
    """A count with the noun phrase of its set, e.g. 'twelve works that McLean et al. offer as tools'."""
    return f"{number_word(n)} {label}"


def facts(tools, sets, stated, unstated, tool_cells, setting_cells, stance, incidents):
    order = [r["id"] for r in stated] + [r["id"] for r in unstated]
    grid = setting_grid(setting_cells)
    training = [s for s in grid if s.startswith("T-")]
    llm = [s for s in grid if not s.endswith("-RL")]            # the settings that involve an LLM
    llm_training = [s for s in llm if s.startswith("T-")]
    n_conditions = len(order)
    worked = [i for i in incidents if i["worked_at"].strip()]
    by_set = {s["id"]: members(tools, s) for s in sets}
    offered = by_set["offered"]
    guaranteed = [t["key"] for t in offered if t["guarantee_kind"] != "none"]
    strict = full_needs(tool_cells)
    fail = guaranteed_failing(strict, guaranteed, grid, "D-AGENT")
    safety = with_guarantee_kind(offered, "safety")
    stated_ids = [r["id"] for r in stated]
    dagent_failing = failing(grid, "D-AGENT")
    shield_full, shield_part, shield_none = needs_of(tool_cells, "alshiekh2018", order)
    out = {f"{s['id']}_n": number_word(len(by_set[s["id"]])) for s in sets}
    out.update({"shield_full": shield_full, "shield_part": shield_part, "shield_none": shield_none})
    passing = [t["tool"].lower() for t in offered if t["key"] in guaranteed and t["key"] not in fail]
    out["guaranteed_not_failing"] = " and ".join(passing) or "none"
    out["named_terms_n"] = number_word(len({t["mclean_term"] for t in by_set["named_tools"] if t["mclean_term"]}))
    out.update({f"{s['id']}_phrase": counted(len(by_set[s["id"]]), s["label"]) for s in sets})
    out.update({
        "offered_safety_n": number_word(len(with_guarantee_kind(offered, "safety"))),
        "offered_other_guarantee_n": number_word(len(with_guarantee_kind(offered, "other"))),
        "offered_none_n": number_word(len(with_guarantee_kind(offered, "none"))),
        "offered_guaranteed_n": number_word(len(guaranteed)),
        "guaranteed_failing_dagent": count_phrase(len(fail), len(guaranteed)),
        "guaranteed_failing_dagent_scale_granted": count_phrase(
            len(guaranteed_failing(strict, guaranteed, grid, "D-AGENT", SCALING_GAP)), len(guaranteed)),
        "guaranteed_failing_tagent": count_phrase(len(guaranteed_failing(strict, guaranteed, grid, "T-AGENT")), len(guaranteed)),
        "safety_failing_dagent": count_phrase(len([k for k in safety if k in fail]), len(safety)),
        "dagent_stated_fail": count_phrase(len([c for c in dagent_failing if c in stated_ids]), len(stated_ids)),
        "dagent_unstated_fail": count_phrase(len([c for c in dagent_failing if c not in stated_ids]), len(unstated)),
        "stated_n": number_word(len(stated)),
        "unstated_n": number_word(len(unstated)),
        "training_llm_max_fail": number_word(max(len(failing(grid, s)) for s in llm_training)),
        "dagent_fail": count_phrase(len(failing(grid, "D-AGENT")), n_conditions),
        "tchat_vs_tprm": compress(differing(grid, "T-CHAT", "T-PRM", order), order),
        "s3_fails_llm": count_phrase(sum("S3" in failing(grid, s) for s in llm), len(llm)),
        "tprm_met_phrase": most_met_phrase(grid, "T-PRM", llm),
        "drl_vs_dagent": compress(differing(grid, "D-RL", "D-AGENT", order), order),
        "dchat_vs_dagent": compress(differing(grid, "D-CHAT", "D-AGENT", order), order),
        "mclean_shared": compress(conditions_with_stance(stance, SHARED_STANCES), order),
        "mclean_partly": compress(conditions_with_stance(stance, {"partly"}), order),
        "mclean_absent": compress(conditions_with_stance(stance, {"not discussed"}), order),
        "incidents_listed": number_word(sum(i["listed_in_intro"] == "yes" for i in incidents)),
        "incidents_added": number_word(sum(i["in_mclean"] == "no" for i in incidents)),
        "incidents_worked": number_word(len(worked)),
        "incidents_worked_not_recovered_in_process": count_phrase(sum(i["recovered_in_process"] == "no" for i in worked), len(worked)),
        "incidents_worked_restored": count_phrase(sum(i["outcome"].startswith("restored") for i in worked), len(worked)),
        "s5_holds_in_training": count_phrase(sum(grid[s]["S5"] == "✓" for s in training), len(training)),
    })
    return out


def sensitivity(inputs):
    """{scenario: {fact: (baseline, value)}}: which facts change when a set of rows, or one row, is left out.

    A conclusion that changes when a contested row is removed rests on that row.
    """
    tools, sets = inputs["tools"], inputs["sets"]
    base = facts(**inputs)
    scenarios = {f"without the set '{s['id']}'": [t["key"] for t in members(tools, s)] for s in sets if s["id"] != "works"}
    scenarios.update({f"without {t['key']} ({t['mclean_role']})": [t["key"]] for t in tools})
    out = {}
    for name, dropped in scenarios.items():
        kept = [t for t in tools if t["key"] not in dropped]
        if not any(members(kept, s) for s in sets if s["id"] == "offered"):
            continue
        new = facts(**{**inputs, "tools": kept, "tool_cells": [c for c in inputs["tool_cells"] if c["tool"] not in dropped]})
        out[name] = {k: (base[k], v) for k, v in new.items() if v != base[k] and not k.endswith("_phrase")}
    return out


def sensitivity_report(changes):
    lines = ["# Sensitivity of the computed facts", "",
             "Generated by `100_analysis/analyze.py`. Each line leaves out a set of rows, or one row, of the tool table.",
             "A fact listed here changes without those rows, so the sentence that prints it rests on them.", ""]
    for name, diff in changes.items():
        shown = "; ".join(f"{k}: {a} -> {b}" for k, (a, b) in diff.items()) or "no fact changes"
        lines.append(f"- **{name}**: {shown}")
    return "\n".join(lines) + "\n"


def load():
    return {"tools": read_csv(ROOT / "063_tools/tools.csv"), "sets": read_csv(ROOT / "063_tools/sets.csv"),
            "stated": read_csv(ROOT / "064_conditions/stated.csv"),
            "unstated": read_csv(ROOT / "070_unstated_conditions/unstated.csv"),
            "tool_cells": read_csv(ROOT / "065_tool_conditions/cells.csv"),
            "setting_cells": read_csv(ROOT / "085_setting_conditions/cells.csv"),
            "stance": read_csv(ROOT / "075_mclean_conditions/stance.csv"),
            "incidents": read_csv(ROOT / "076_incidents/incidents.csv")}


def main():
    inputs = load()
    out = facts(**inputs)
    here = Path(__file__).parent
    (here / "facts.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    (here / "sensitivity.md").write_text(sensitivity_report(sensitivity(inputs)))
    return out


if __name__ == "__main__":
    print(json.dumps(main(), indent=1, ensure_ascii=False))
