"""Build an ICML-2026-style PDF from ../draft_conditions_short.md.

Pipeline: split the markdown into abstract / body / bibliography, convert each with pandoc,
turn pandoc's longtables into floats that fit a two-column layout, fill template.tex, run pdflatex.
Usage: python3 build.py            one column (default; not accepted by ICML for submission)
       python3 build.py --twocol   ICML's two-column submission layout
"""
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).parent
SOURCE = HERE.parent / "draft_conditions_short.md"
TITLE = "When Is Agent Safety a Reinforcement Learning Problem? Six Stated and Four Unstated Conditions"
RUNNING_TITLE = "When Is Agent Safety an RL Problem?"
WIDE_TABLE_MIN_COLS = 4  # tables with this many columns span both columns


def split_markdown(text):
    body = text.split("\n## Abstract\n", 1)[1]
    abstract, rest = body.split("\n## ", 1)
    main, bibliography = ("## " + rest).split("## Bibliography", 1)
    main = main.rstrip().removesuffix("---").rstrip()
    return abstract.strip(), main, bibliography.strip()


def pandoc(markdown):
    out = subprocess.run(["pandoc", "-f", "markdown-auto_identifiers", "-t", "latex", "--wrap=preserve",
                          "--shift-heading-level-by=-1"],
                         input=markdown, capture_output=True, text=True, check=True)
    return out.stdout


def blank_line_before_lists(markdown):
    """Pandoc needs a blank line before a list; the drafts often omit it."""
    return re.sub(r"(?m)^(?!\s*(?:[-*]|\d+\.)\s)(.+)\n(?=(?:[-*]|\d+\.) )", r"\1\n\n", markdown)


def unnumber_headings(latex):
    """Markdown headings carry their own numbers ('## 1. Claim'); let LaTeX number them instead."""
    return re.sub(r"\\(section|subsection)\{\d+(\.\d+)*\.?\s*", r"\\\1{", latex)


# pandoc's column spec spans several lines and always ends with '@{}}'
LONGTABLE = re.compile(r"\\begin\{longtable\}\[\]\{(.*?@\{\})\}\n(.*?)\\end\{longtable\}", re.S)


SHORT_CELL = 14  # a column whose cells are all at most this many visible characters gets a natural width


def visible_length(cell):
    text = re.sub(r"\\cite[pt](\[[^]]*\])?\{[^}]*\}", "(Author, 2026)", cell)
    text = re.sub(r"\\[a-zA-Z]+\*?|[{}]", "", text)
    return len(text.strip())


def column_spec(rows):
    """Short columns -> 'l'; long ones -> ragged-right X columns that share the remaining width."""
    lines = [r for r in re.split(r"\\\\", rows) if "&" in r]
    ncols = lines[0].count("&") + 1
    widest = [0] * ncols
    for line in lines:
        for i, cell in enumerate(line.split("&")[:ncols]):
            widest[i] = max(widest[i], visible_length(cell))
    cols = ["l" if w <= SHORT_CELL else r">{\raggedright\arraybackslash}X" for w in widest]
    if "l" not in cols or all(c == "l" for c in cols):
        cols = [r">{\raggedright\arraybackslash}X"] * ncols if "l" not in cols else cols
    return ncols, "@{}" + "".join(cols) + "@{}", all(c == "l" for c in cols)


def to_float(_pandoc_spec, rows):
    """One pandoc longtable -> a table (narrow) or table* (wide) float holding a tabularx/tabular."""
    rows = re.sub(r"\\endfirsthead.*?\\endhead", "", rows, flags=re.S)  # drop the repeated header
    rows = re.sub(r"\\(endhead|endfirsthead|endfoot|endlastfoot)\b|\\noalign\{\}", "", rows).strip()
    rows = re.sub(r"\\begin\{minipage\}\[[a-z]\]\{[^}]*\}\\raggedright\s*|\\end\{minipage\}", "", rows)
    ncols, spec, natural = column_spec(rows)
    wide = ncols >= WIDE_TABLE_MIN_COLS and not natural
    env, width = ("table*", r"\textwidth") if wide else ("table", r"\columnwidth")
    body = (f"\\begin{{tabular}}{{{spec}}}\n{rows}\n\\end{{tabular}}" if natural
            else f"\\begin{{tabularx}}{{{width}}}{{{spec}}}\n{rows}\n\\end{{tabularx}}")
    return (f"\\begin{{{env}}}[!htb]\n\\centering\\small\\setlength{{\\tabcolsep}}{{3pt}}\n"
            f"{body}\n\\end{{{env}}}\n")


CAPTIONS = (  # in order of appearance in the markdown; update when tables are added or moved
    "Conditions stated in the source papers of the tools named by McLean et al.",
    "Which tool's guarantee needs which stated condition.",
    "Conditions that none of the source papers states.",
    "Decision settings. Prefix T- training, D- deployment; CHAT has no tools, AGENT has tools.",
    r"Conditions by setting and phase. \checkmark{} holds, $\sim$ partly, $\times$ fails. n/a does not apply. Left four columns: training; right three: deployment.",
)


def float_tables(latex):
    tables = iter(CAPTIONS)

    def replace(match):
        caption = next(tables, None)
        if caption is None:
            raise SystemExit("more tables than CAPTIONS; add a caption in build.py")
        return to_float(match.group(1), match.group(2)).replace(
            r"\centering", f"\\centering\n\\caption{{{caption}}}", 1)
    out = LONGTABLE.sub(replace, latex)
    if next(tables, None) is not None:
        raise SystemExit("fewer tables than CAPTIONS; remove a caption in build.py")
    return out


ENTRY = re.compile(r"^\[(\d+)\]\s+(.*?)(?=^\[\d+\]\s|\Z)", re.M | re.S)
CITE = re.compile(r"\[(\d+(?:[–-]\d+)?(?:, ?\d+(?:[–-]\d+)?)*)(?:, ([^\]\d][^\]]*))?\]")


YEAR_OVERRIDES = {46: "2016"}  # entries whose year is not written as a four-digit number


def first_author_surname(name):
    """'J. X. Wang' -> 'Wang'; an organization without initials keeps its full name."""
    return name.split()[-1] if re.match(r"^([A-Z]\.[ -]?)+", name) else name


def parse_entries(markdown):
    """{number: (label for natbib, sort key, entry markdown)} from '[n] Authors, "Title," ... year. url'."""
    entries = {}
    for number, entry in ENTRY.findall(markdown):
        entry = re.sub(r"(?<![<(])(https?://[^\s)>]+?)([.,;]?)(?=\s|$)", r"<\1>\2", entry.strip())
        authors = re.split(r',\s*["“*]', entry, maxsplit=1)[0]
        names = [re.sub(r"\s*et al\.?$", "", a.strip()) for a in re.split(r",\s*", authors)]
        names = [n for n in names if n]
        surname = first_author_surname(names[0]) if names else "Anon"
        if len(names) == 2 and "et al" not in authors:
            short = f"{surname} and {names[1].split()[-1]}"
        elif len(names) > 2 or "et al" in authors:
            short = f"{surname} et~al."
        else:
            short = surname
        no_urls = re.sub(r"<https?://[^>]+>", "", entry)
        years = re.findall(r"\b(19\d\d|20\d\d)\b", no_urls)
        year = YEAR_OVERRIDES.get(int(number), years[-1] if years else "n.d.")
        entries[int(number)] = [short, year, (surname.lower(), year), entry]
    return disambiguate(entries)


def disambiguate(entries):
    """Same label and year -> 2024a, 2024b, in bibliography order."""
    groups = {}
    for n, (short, year, key, _) in sorted(entries.items(), key=lambda kv: (kv[1][2], kv[0])):
        groups.setdefault((short, year), []).append(n)
    out = {}
    for (short, year), ns in groups.items():
        for i, n in enumerate(ns):
            suffix = "abcdefgh"[i] if len(ns) > 1 else ""
            _, _, key, text = entries[n]
            out[n] = (f"{short}({year}{suffix})", key, text)
    return out


def numbers(spec):
    out = []
    for part in re.split(r",\s*", spec):
        if re.fullmatch(r"\d+[–-]\d+", part):
            a, b = map(int, re.split(r"[–-]", part))
            out.extend(range(a, b + 1))
        else:
            out.append(int(part))
    return out


TEXTUAL_LEAD = ("as", "of", "in", "So", "tools", "supports")  # words after which a citation is read as a name


def is_textual(before):
    """A citation is part of the sentence when it starts one or follows a word in TEXTUAL_LEAD."""
    before = before.rstrip("*").rstrip(" ")
    return (not before or before[-1] in ".;:\n|" or before.endswith(("-", "1.", "2.", "3."))
            or before.split()[-1] in TEXTUAL_LEAD)


def author_year_citations(markdown):
    """[n], [n, m], [a–b] and [n, §x] -> natbib.

    'Surname et al. [n]' -> \\citet (the name is already in the text). A citation that starts a
    sentence or follows a word such as 'as' or 'of' is read as a name -> \\citet. The rest -> \\citep.
    """
    markdown = re.sub(r"\b[A-Z][\w-]+ et al\. \[(\d+)\]", r"\\citet{r\1}", markdown)

    def replace(match):
        keys = ",".join(f"r{n}" for n in numbers(match.group(1)))
        note = match.group(2)
        command = "citet" if is_textual(markdown[max(0, match.start() - 40):match.start()]) else "citep"
        note_arg = f"[{note.strip().replace(' ', '~', 1)}]" if note else ""
        return f"\\{command}{note_arg}{{{keys}}}"
    return CITE.sub(replace, markdown)


def cited_numbers(latex):
    """Reference numbers that the text cites; the reference list prints only these."""
    keys = re.findall(r"\\cite[pt](?:\[[^\]]*\])?\{([^}]*)\}", latex)
    return {int(k[1:]) for group in keys for k in group.split(",")}


def bibliography_items(entries, cited):
    ordered = sorted(((n, e) for n, e in entries.items() if n in cited), key=lambda kv: kv[1][1])
    return "\n".join(f"\\bibitem[{label}]{{r{n}}} {pandoc(text).strip()}" for n, (label, _, text) in ordered)


def main():
    abstract, main_md, bib_md = split_markdown(SOURCE.read_text())
    entries = parse_entries(bib_md)
    body = float_tables(unnumber_headings(pandoc(author_year_citations(blank_line_before_lists(main_md)))))
    abstract_tex = pandoc(author_year_citations(abstract)).strip()
    cited = cited_numbers(abstract_tex + body)
    missing = cited - entries.keys()
    if missing:
        raise SystemExit(f"cited but not in the bibliography: {sorted(missing)}")
    tex = (HERE / "template.tex").read_text()
    # two columns: the title block is \twocolumn's full-width argument; one column: plain text
    head_start, head_end = (r"\twocolumn[", "]") if "--twocol" in sys.argv else (r"\onecolumn", "")
    tex = (tex.replace("%%HEADSTART%%", head_start).replace("%%HEADEND%%", head_end)
              .replace("%%TITLE%%", TITLE).replace("%%RUNNING%%", RUNNING_TITLE)
              .replace("%%ABSTRACT%%", abstract_tex)
              .replace("%%BODY%%", body)
              .replace("%%BIBITEMS%%", bibliography_items(entries, cited)))
    (HERE / "paper.tex").write_text(tex)
    for _ in range(2):
        run = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "paper.tex"],
                             cwd=HERE, capture_output=True, text=True, errors="replace")
        if run.returncode != 0:
            print(run.stdout[-3000:])
            raise SystemExit("pdflatex failed")
    print("wrote", HERE / "paper.pdf", "|", len(cited), "of", len(entries), "references cited")


if __name__ == "__main__":
    main()
