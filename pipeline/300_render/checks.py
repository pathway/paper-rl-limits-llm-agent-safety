"""Consistency checks over the stage folders. Each check returns a list of problems; the build stops on any."""
import re
from render import cite_keys

QUOTE = re.compile(r'"([^"]+)"')
CONDITION_VALUES = {"✓", "~", "✗", "n/a"}
STANCES = {"concedes", "states", "builds on", "partly", "not discussed"}
SHARED_STANCES = {"concedes", "states", "builds on"}
RECOVERED_VALUES = {"yes", "no", "disputed", "not assessed"}
EVIDENCE_TYPES = {"quote", "absence", "judgement"}


def normalise(text):
    return re.sub(r"\s+", " ", text.replace("“", '"').replace("”", '"').replace("’", "'"))


def missing_keys(texts, refs):
    keys = {r["key"] for r in refs}
    return [f"citation @{k} not in 040_biblio" for t in texts for k in sorted(cite_keys(t) - keys)]


def tool_problems(tools, notes):
    out = []
    for t in tools:
        if not t["mclean_locator"].strip():
            out.append(f"tool {t['key']}: no McLean locator")
        if t["key"] not in notes:
            out.append(f"tool {t['key']}: no note in 050_biblio_notes")
        elif not re.search(r"^read: (full|partial|quotes)$", notes[t["key"]], re.M):
            out.append(f"note {t['key']}: no read scope in front matter")
    return out


def tool_cell_problems(tools, cells, conditions):
    out = []
    have = {(c["tool"], c["condition"]) for c in cells}
    out += [f"cell {t['key']} {s}: missing" for t in tools for s in conditions if (t["key"], s) not in have]
    for c in cells:
        if not c["reason"].strip():
            out.append(f"cell {c['tool']} {c['condition']}: no reason")
    return out


def setting_cell_problems(cells, conditions, settings):
    have = {(c["condition"], c["setting"]): c["value"] for c in cells}
    out = [f"setting cell {s} {c}: missing" for c in conditions for s in settings if (c, s) not in have]
    out += [f"setting cell {s} {c}: bad value {v!r}" for (c, s), v in have.items() if v not in CONDITION_VALUES]
    return out


def draft_problems(draft):
    return [f"draft line {i}: typed table row; import tables with {{{{table:...}}}}"
            for i, line in enumerate(draft.splitlines(), 1) if line.lstrip().startswith("|")]


def stance_problems(stance, conditions):
    """075: one row per condition, a known stance, and evidence unless the condition is absent from the target."""
    have = {r["condition"]: r for r in stance}
    out = [f"stance {c}: missing" for c in conditions if c not in have]
    for c, r in have.items():
        if r["stance"] not in STANCES:
            out.append(f"stance {c}: bad value {r['stance']!r}")
        elif r["stance"] != "not discussed" and not (r["locator"].strip() and r["evidence"].strip()):
            out.append(f"stance {c}: needs a locator and evidence")
    return out


def incident_problems(incidents, conditions, refs):
    """076: valid flags and condition ids; an incident that the target works through needs our own sources."""
    keys = {r["key"] for r in refs}
    out = []
    for r in incidents:
        if r["recovered_in_process"] not in RECOVERED_VALUES:
            out.append(f"incident {r['id']}: bad recovered_in_process value {r['recovered_in_process']!r}")
        out += [f"incident {r['id']}: unknown condition {c}" for c in split_list(r["fails"]) if c not in conditions]
        sources = split_list(r["our_sources"])
        out += [f"incident {r['id']}: source @{k} not in 040_biblio" for k in sources if k not in keys]
        if r["in_mclean"] not in ("yes", "no"):
            out.append(f"incident {r['id']}: in_mclean must be yes or no")
        if (r["worked_at"].strip() or r["in_mclean"] == "no") and (not sources or r["recovered_in_process"] == "not assessed"):
            out.append(f"incident {r['id']}: worked through by the target, or added by us, so it needs our sources and an assessment")
    return out


def split_list(field):
    return [x.strip() for x in field.split(";") if x.strip()]


def verified_quotes(note):
    """Phrases listed under a note's "Verified quotes" heading (one per line, as - "phrase")."""
    _, found, tail = note.partition("Verified quotes")
    return re.findall(r'^- "(.+?)"', tail, re.M) if found else []


def existence_problems(cited, existence):
    """040: every cited reference must be confirmed to exist (status ok), or checked by hand (manual, with a note)."""
    status = {r["key"]: r for r in existence}
    out = []
    for k in sorted(cited):
        r = status.get(k)
        if r is None:
            out.append(f"reference @{k}: not checked; run 040_biblio/verify.py")
        elif r["status"] != "ok" and not (r["status"] == "manual" and r["note"].strip()):
            out.append(f"reference @{k}: existence {r['status']}; check by hand and record status manual with a note")
    return out


def evidence_type_problems(cells):
    """065: each cell declares its evidence. A quote cell cites extracts; an absence cell records the hits it reviewed."""
    out = []
    for c in cells:
        name = f"cell {c['tool']} {c['condition']}"
        if c["evidence_type"] not in EVIDENCE_TYPES:
            out.append(f"{name}: bad evidence_type {c['evidence_type']!r}")
        elif c["evidence_type"] == "quote" and not (c["evidence"].strip() and QUOTE.search(c["reason"])):
            out.append(f"{name}: a quote cell needs a quoted phrase and extract ids")
        elif c["evidence_type"] == "absence" and not c["hits_reviewed"].strip().isdigit():
            out.append(f"{name}: an absence cell needs hits_reviewed")
    return out


def role_problems(tools, roles, target_extracts, refs, decisions):
    """063: each row declares its role in the target paper, backed by a target extract that names the work."""
    role = {r["id"]: r for r in roles}
    extract = {e["id"]: e["text"] for e in target_extracts}
    short = {r["key"]: r["short"].replace("~", " ").replace(" et al.", "") for r in refs}
    decided = {d["id"] for d in decisions}
    out = []
    for t in tools:
        name = f"tool {t['key']}"
        if t["mclean_role"] not in role:
            out.append(f"{name}: unknown role {t['mclean_role']!r}")
            continue
        ids = split_list(t["role_evidence"])
        if not ids:
            out.append(f"{name}: no evidence for its role")
        out += [f"{name}: role evidence {i} is not an extract of the target" for i in ids if i not in extract]
        if role[t["mclean_role"]]["evidence_names_work"] == "yes" and not any(short[t["key"]] in extract.get(i, "") for i in ids):
            out.append(f"{name}: its role evidence does not name {short[t['key']]}")
        if t["label_origin"] not in ("source", "ours"):
            out.append(f"{name}: label_origin must be source or ours")
        if t["decision"] not in decided:
            out.append(f"{name}: decision {t['decision']!r} is not in 005_decisions")
    return out


NUMBER_WORDS = "two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen".split()


def typed_count_problems(text, nouns):
    """A count of a defined set must be a {{fact:...}}; flag a number typed next to one of the set nouns."""
    words = re.findall(r"[A-Za-z0-9{}:_]+", text)
    out = []
    for i, w in enumerate(words):
        if w.lower() in NUMBER_WORDS or w.isdigit():
            near = [x.lower() for x in words[i + 1:i + 3]]
            hit = next((n for n in nouns if n in near), None)
            if hit:
                out.append(f"draft: typed count \"{w} ... {hit}\"; use a {{{{fact:...}}}} so the count follows its set")
    return out
