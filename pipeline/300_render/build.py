"""Build the PDF from the stage folders. Imperative shell: reads files, calls pandoc and pdflatex.

Pipeline: checks (incl. quotes against 045_fulltext and 047_extracts) -> out/backcheck.md -> 100_analysis facts -> expand {{directives}} in 200_draft -> pandoc (--natbib) -> template -> pdflatex.
Usage: python3 build.py
"""
from pathlib import Path
import csv
import hashlib
import json
import os
import subprocess
import sys

import yaml

import backcheck
import checks
import claims
import render

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "100_analysis"))
import analyze  # noqa: E402

RUNNING_TITLE = "Position: RL Safety Guarantees and Deployed LLM Agents"
COUNTED_NOUNS = ["tools", "tool", "works", "papers", "conditions", "incidents"]   # nouns of the defined sets


def read_csv(rel):
    with open(ROOT / rel, newline="") as f:
        return list(csv.DictReader(f))


def pandoc(markdown):
    out = subprocess.run(["pandoc", "-f", "markdown", "-t", "latex", "--natbib", "--wrap=preserve",
                          "--shift-heading-level-by=-1"], input=markdown, capture_output=True, text=True, check=True)
    return out.stdout.strip()


def pandoc_many(cells):
    """Convert many short markdown strings in one pandoc call; empty strings stay empty."""
    sep = "\n\nZZCELLSEPZZ\n\n"
    filled = [c for c in cells if c.strip()]
    converted = iter(c.strip() for c in pandoc(sep.join(filled)).split("ZZCELLSEPZZ")) if filled else iter(())
    return [next(converted) if c.strip() else "" for c in cells]


def load():
    d = {
        "refs": yaml.safe_load((ROOT / "040_biblio/refs.yaml").read_text()),
        "notes": {p.stem: p.read_text() for p in (ROOT / "050_biblio_notes").glob("*.md")},
        "existence": read_csv("040_biblio/existence.csv"),
        "manifest": read_csv("045_fulltext/manifest.csv"),
        "decisions": read_csv("005_decisions/decisions.csv"),
        "claims": read_csv("095_claims/claims.csv"),
        "tools": read_csv("063_tools/tools.csv"),
        "roles": read_csv("063_tools/roles.csv"),
        "sets": read_csv("063_tools/sets.csv"),
        "stated": read_csv("064_conditions/stated.csv"),
        "tool_cells": read_csv("065_tool_conditions/cells.csv"),
        "unstated": read_csv("070_unstated_conditions/unstated.csv"),
        "stance": read_csv("075_mclean_conditions/stance.csv"),
        "incidents": read_csv("076_incidents/incidents.csv"),
        "settings": read_csv("080_settings/settings.csv"),
        "setting_cells": read_csv("085_setting_conditions/cells.csv"),
        "setting_reasons": read_csv("085_setting_conditions/reasons.csv"),
        "phase_note": (ROOT / "080_settings/phase_note.md").read_text().strip(),
        "related": (ROOT / "090_related/related.md").read_text().split("-->", 1)[-1].strip(),
        "draft": (ROOT / "200_draft/draft.md").read_text(),
    }
    d["fulltexts"] = {m["key"]: (ROOT / "045_fulltext" / m["file"]).read_text(errors="replace") for m in d["manifest"]}
    d["extracts"] = {p.parent.name: read_csv(p.relative_to(ROOT)) for p in sorted((ROOT / "047_extracts").glob("*/extracts.csv"))}
    d["tex_sources"] = {p.name: "\n".join(f.read_text(errors="replace") for f in sorted(p.glob("*.tex")))
                        for p in sorted((ROOT / "045_fulltext/tex").glob("*")) if p.is_dir()}
    d["formula_images"] = {(p.parent.name, p.stem) for p in (ROOT / "047_extracts").glob("*/*.png")}
    d["target_note"] = (ROOT / "010_target/mclean2026.md").read_text()
    d["notes"]["mclean2026"] = "\n".join(p.read_text() for p in sorted((ROOT / "010_target").glob("*.md")))
    return d


def quote_uses(d):
    """(evidence, prose): quotes whose source is known from where they stand, and quotes in running text."""
    Use, quotes = backcheck.Use, checks.QUOTE.findall
    evidence = [Use(c["tool"], f"cell {c['tool']} {c['condition']}", q) for c in d["tool_cells"] for q in quotes(c["reason"])]
    evidence += [Use("mclean2026", f"stance {r['condition']}", q) for r in d["stance"] for q in quotes(r["evidence"])]
    listed = [Use(k, f"note {k}", q) for k, note in {**d["notes"], "mclean2026": d["target_note"]}.items()
              for q in checks.verified_quotes(note)]
    indexes = {k: backcheck.build_index(t) for k, t in d["fulltexts"].items()}
    texts = {"draft": d["draft"], "related work": d["related"]}
    texts.update({f"{k} row {i}": " ".join(row.values()) for k in ("stated", "settings", "setting_reasons", "tools", "incidents")
                  for i, row in enumerate(d[k], 2)})
    prose = []
    for where, text in texts.items():
        cited_first = {k: indexes[k] for k in render.cite_keys(text) if k in indexes}   # prefer sources cited nearby
        prose += [Use(backcheck.attribute(q, {**cited_first, **indexes}), where, q) for q in quotes(checks.normalise(text))]
    return evidence, listed, prose


def cited_evidence(d):
    """{where: [extract ids]} from the evidence columns of the tool cells and the stance rows."""
    out = {f"cell {c['tool']} {c['condition']}": checks.split_list(c["evidence"]) for c in d["tool_cells"]}
    out.update({f"stance {r['condition']}": checks.split_list(r["evidence_ids"]) for r in d["stance"]})
    return out


def search_terms(d):
    return {r["id"]: checks.split_list(r["search_terms"]) for r in d["stated"]}


def run_checks(d):
    s_ids = [r["id"] for r in d["stated"]]
    all_ids = s_ids + [r["id"] for r in d["unstated"]]
    texts = [d["draft"], d["related"], d["phase_note"]] + [json.dumps(d[k], ensure_ascii=False) for k in
                                          ("tools", "stated", "tool_cells", "settings", "setting_reasons", "incidents")]
    cited = set().union(*(render.cite_keys(t) for t in texts))
    problems = (checks.missing_keys(texts, d["refs"]) + checks.tool_problems(d["tools"], d["notes"])
                + checks.existence_problems(cited, d["existence"])
                + checks.role_problems(d["tools"], d["roles"], d["extracts"].get("mclean2026", []), d["refs"], d["decisions"])
                + claims.stale(d["claims"], lambda path: (ROOT / path).read_text())
                + checks.typed_count_problems(d["draft"] + d["related"], COUNTED_NOUNS)
                + checks.tool_cell_problems(d["tools"], d["tool_cells"], s_ids)
                + checks.setting_cell_problems(d["setting_cells"], all_ids, [s["id"] for s in d["settings"]])
                + checks.stance_problems(d["stance"], all_ids)
                + checks.incident_problems(d["incidents"], all_ids, d["refs"])
                + checks.draft_problems(d["draft"]))
    evidence, listed, prose = quote_uses(d)
    problems += [f"{u.where}: quote not in any stored full text: \"{u.phrase}\"" for u in prose if not u.key]
    indexes = {k: backcheck.build_index(t) for k, t in d["fulltexts"].items()}
    paragraphs = {f"draft paragraph {i}": checks.normalise(p) for i, p in enumerate(d["draft"].split("\n\n"), 1)}
    paragraphs.update({"phase note": checks.normalise(d["phase_note"]), "related work": checks.normalise(d["related"])})
    problems += backcheck.misattributed_quotes(paragraphs, indexes, render.CITE_KEY)
    extract_uses = [backcheck.Use(k, f"extract {k} {e['id']}", e["text"]) for k, rows in d["extracts"].items() for e in rows]
    needed = [t["key"] for t in d["tools"]] + ["mclean2026"]
    files = {(m["key"], kind): ROOT / "045_fulltext" / (f"pdf/{m['key']}.pdf" if kind == "pdf" else m["file"])
             for m in d["manifest"] for kind in ("pdf", "txt")}
    hashes = {k: hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None for k, p in files.items()}
    problems += (backcheck.stale_files(d["manifest"], hashes)
                 + [f"{k}: no full text in 045_fulltext" for k in needed if k not in d["fulltexts"]]
                 + [f"{k}: no extracts in 047_extracts" for k in needed if not d["extracts"].get(k)]
                 + backcheck.missing_in_fulltext(extract_uses + evidence + listed, d["fulltexts"])
                 + backcheck.not_covered_by_extracts(evidence, d["extracts"], cited_evidence(d))
                 + backcheck.formula_problems(d["extracts"], d["tex_sources"], d["formula_images"])
                 + checks.evidence_type_problems(d["tool_cells"])
                 + backcheck.absence_problems(d["tool_cells"], search_terms(d), d["fulltexts"]))
    if problems:
        raise SystemExit("checks failed:\n  " + "\n  ".join(problems))


def tables(d):
    """{table id: (header, rows)} with markdown cells."""
    cell = {(c["tool"], c["condition"]): c["display"] for c in d["tool_cells"]}
    s_ids = [r["id"] for r in d["stated"]]
    grid = {(c["condition"], c["setting"]): c["value"] for c in d["setting_cells"]}
    settings = [s["id"] for s in d["settings"]]
    conds = d["stated"] + d["unstated"]
    code = {r["id"]: r["code"] for r in d["roles"]}
    return {
        "stated": (["\\#", "Condition", "Source"], [[r["id"], r["definition"], r["sources"]] for r in d["stated"]]),
        "tool_conditions": ([set_label(d, "works"), "Role", "Guarantee"] + s_ids,
                            [[f"{t['tool']} [@{t['key']}]", code[t["mclean_role"]], t["guarantee"]]
                             + [cell[(t["key"], s)] for s in s_ids] for t in d["tools"]]),
        "unstated": (["\\#", "Condition"], [[r["id"], r["definition"]] for r in d["unstated"]]),
        "mclean_stance": (["\\#", "Stance", "Where", "Evidence"],
                          [[r["condition"], r["stance"], r["locator"], r["evidence"]] for r in d["stance"]]),
        "incidents": (["Incident", "Where", "Recovered within the agent's process", "Outcome", "Fails", "Our sources"],
                      [[i["incident"], "; ".join(x for x in ("§1" if i["listed_in_intro"] == "yes" else "", i["worked_at"]) if x)
                        if i["in_mclean"] == "yes" else "not in McLean et al.",
                        i["recovered_in_process"], i["outcome"], i["fails"].replace(";", ","),
                        "[" + "; ".join("@" + k for k in checks.split_list(i["our_sources"])) + "]" if i["our_sources"] else ""]
                       for i in d["incidents"]]),
        "settings": (["Phase", "Setting", "Posed as"], [[s["phase"], s["id"], s["posed_as"]] for s in d["settings"]]),
        "setting_conditions": (["\\#"] + settings, [[f"{c['id']} {c['label']}"] + [grid[(c["id"], s)] for s in settings]
                                                  for c in conds]),
    }


def set_label(d, set_id):
    """Header text for a table over a defined set: the set's own label, capitalised."""
    label = next(s["label"] for s in d["sets"] if s["id"] == set_id)
    return label[0].upper() + label[1:]


def caption(d, name):
    """Caption of a table: its verified claim, plus the role legend generated from 063_tools/roles.csv."""
    text = next(c["text"] for c in d["claims"] if c["id"] == f"caption_{name}")
    if name == "tool_conditions":
        text += " Role: " + "; ".join(f"{r['code']}, {r['label']}" for r in d["roles"]) + "."
    return text


def table_block(d, name, header, rows):
    flat = pandoc_many(header + [c for r in rows for c in r])
    h, body = flat[:len(header)], flat[len(header):]
    n = len(header)
    latex = render.table_latex(caption(d, name), f"tab:{name}", h, [body[i:i + n] for i in range(0, len(body), n)])
    return "\n```{=latex}\n" + latex + "\n```\n"


def appendix(d):
    by_tool = {}
    for c in d["tool_cells"]:
        by_tool.setdefault(c["tool"], []).append(c)
    parts = []
    for t in d["tools"]:
        bullets = "\n".join(f"- {c['condition']}, {c['reason']}" for c in by_tool[t["key"]])
        parts.append(f"**{t['tool']} [@{t['key']}].** {t['appendix_intro']}\n\n{bullets}")
    return "\n\n".join(parts)


def bibitems(refs, cited):
    labels = render.natbib_labels(refs)
    used = sorted((r for r in refs if r["key"] in cited), key=lambda r: (r["short"].lower(), r["year"], r["key"]))
    texts = pandoc_many([render.wrap_bare_urls(r["text"]) for r in used])
    return "\n".join(f"\\bibitem[{labels[r['key']]}]{{{r['key']}}} {t}" for r, t in zip(used, texts))


def main():
    d = load()
    run_checks(d)
    evidence, _, prose = quote_uses(d)
    (HERE / "out").mkdir(exist_ok=True)
    by_type = {t: [f"{c['tool']} {c['condition']}" for c in d["tool_cells"] if c["evidence_type"] == t]
               for t in sorted(checks.EVIDENCE_TYPES)}
    summary = ("Evidence for the tool cells: " + "; ".join(f"{t} {len(v)}" for t, v in by_type.items())
               + f". Cells that rest on judgement alone: {', '.join(by_type['judgement']) or 'none'}.\n\n")
    (HERE / "out" / "backcheck.md").write_text(
        summary + backcheck.report(d["extracts"], evidence + prose, d["fulltexts"], d["manifest"])
        + backcheck.absence_report(d["tool_cells"], search_terms(d), d["fulltexts"], d["manifest"]))
    facts = analyze.main()
    (HERE / "out" / "sensitivity.md").write_text((ROOT / "100_analysis/sensitivity.md").read_text())
    tabs = tables(d)
    resolvers = {
        "fact": lambda k: facts[k],
        "table": lambda k: table_block(d, k, *tabs[k]),
        "list": lambda k: render.bullet_list((r["condition"], r["reason"]) for r in d[k]),
        "include": lambda k: d[k],
        "appendix": lambda k: appendix(d),
    }
    title, abstract, body, app = render.split_draft(d["draft"])
    abstract_tex, body_tex, app_tex = (pandoc(render.expand(x, resolvers)) for x in (abstract, body, app))
    cited = render.latex_cite_keys(abstract_tex + body_tex + app_tex)
    tex = (HERE / "template.tex").read_text()
    for k, v in {"%%HEADSTART%%": r"\onecolumn", "%%HEADEND%%": "", "%%TITLE%%": title,
                 "%%RUNNING%%": RUNNING_TITLE, "%%ABSTRACT%%": abstract_tex, "%%BODY%%": body_tex,
                 "%%APPENDIX%%": app_tex, "%%BIBITEMS%%": bibitems(d["refs"], cited)}.items():
        tex = tex.replace(k, v)
    out = HERE / "out"
    out.mkdir(exist_ok=True)
    (out / "paper.tex").write_text(tex)
    env = {**os.environ, "TEXINPUTS": f"{HERE}:"}  # style files live next to build.py
    for _ in range(2):
        run = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "paper.tex"], cwd=out,
                             capture_output=True, text=True, errors="replace", env=env)
        if run.returncode != 0:
            print(run.stdout[-3000:])
            raise SystemExit("pdflatex failed")
    log = (out / "paper.log").read_text(errors="replace")
    if "undefined" in log or "Overfull" in log:
        raise SystemExit("LaTeX reports undefined references or overfull boxes; see out/paper.log")
    print("wrote", out / "paper.pdf", "|", len(cited), "of", len(d["refs"]), "references cited")


if __name__ == "__main__":
    main()
