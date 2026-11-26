import pytest
import checks
import render


def test_expand_resolves_and_rejects_unknown():
    assert render.expand("a {{fact:x}} b", {"fact": {"x": "1"}.__getitem__}) == "a 1 b"
    with pytest.raises(KeyError):
        render.expand("{{fact:y}}", {"fact": {"x": "1"}.__getitem__})


def test_split_draft():
    d = "# T\n\n## Abstract\n\nA.\n\n## Intro {#sec:intro}\n\nB.\n\n## Reasons {#app:cells}\n\nC.\n"
    title, abstract, body, app = render.split_draft(d)
    assert (title, abstract) == ("T", "A.")
    assert body.startswith("## Intro") and "C." not in body and app.startswith("## Reasons")


def test_cite_keys_markdown_and_latex():
    assert render.cite_keys("x [@wachi2023; @satija2020, {§3}] and @mclean2026 [{§5}]") == {"wachi2023", "satija2020", "mclean2026"}
    assert render.latex_cite_keys(r"\citep[§3]{a2020, b2021} \citet{c2022}") == {"a2020", "b2021", "c2022"}


def test_natbib_labels_disambiguate_same_label_and_year():
    refs = [{"key": "wen2024a", "short": "Wen et~al.", "year": "2024"},
            {"key": "wen2024b", "short": "Wen et~al.", "year": "2024"},
            {"key": "altman1999", "short": "Altman", "year": "1999"}]
    assert render.natbib_labels(refs) == {"wen2024a": "Wen et~al.(2024a)", "wen2024b": "Wen et~al.(2024b)",
                                          "altman1999": "Altman(1999)"}


def test_column_spec_short_and_long():
    spec = render.column_spec([["S1", "S2"], ["a long cell of text that wraps around"]])
    assert spec == r"@{}l>{\raggedright\arraybackslash}X@{}"


def test_checks_catch_missing_cell_and_empty_reason():
    tools = [{"key": "t2020", "mclean_locator": "§1"}]
    cells = [{"tool": "t2020", "condition": "S1", "reason": " "}]
    assert checks.tool_problems(tools, {"t2020": "---\nread: full\n---"}) == []
    assert checks.tool_cell_problems(tools, cells, ["S1", "S2"]) == ["cell t2020 S2: missing", "cell t2020 S1: no reason"]


def test_checks_setting_grid_and_draft_tables():
    assert checks.setting_cell_problems([{"condition": "S1", "setting": "A", "value": "?"}], ["S1"], ["A", "B"]) == \
        ["setting cell B S1: missing", "setting cell A S1: bad value '?'"]
    assert checks.draft_problems("text\n| a | b |\n") == ["draft line 2: typed table row; import tables with {{table:...}}"]


def test_missing_keys():
    assert checks.missing_keys(["see @nope2020"], [{"key": "yes2020"}]) == ["citation @nope2020 not in 040_biblio"]


def test_stance_needs_every_condition_and_evidence():
    stance = [{"condition": "S1", "stance": "concedes", "locator": "", "evidence": ""},
              {"condition": "U2", "stance": "not discussed", "locator": "", "evidence": ""}]
    assert checks.stance_problems(stance, ["S1", "S2", "U2"]) == ["stance S2: missing",
                                                                   "stance S1: needs a locator and evidence"]


def test_worked_incident_needs_sources_and_assessment():
    inc = [{"id": "x", "in_mclean": "yes", "worked_at": "§3", "our_sources": "", "recovered_in_process": "not assessed", "fails": "S9"}]
    problems = checks.incident_problems(inc, ["S1"], [{"key": "a"}])
    assert "incident x: unknown condition S9" in problems
    assert any("needs our sources" in p for p in problems)


FULL = "Assumption 3.1. The MDP is er-\ngodic for any pol-\nicy, i.e. the chain\nis irreducible. A ﬁnite set."


def test_locate_ignores_line_breaks_hyphens_and_ligatures():
    import backcheck
    assert backcheck.find(FULL, "ergodic for any policy").line == 1
    assert backcheck.find(FULL, "is irreducible").line == 4
    assert backcheck.find(FULL, "A finite set").line == 4
    assert backcheck.find(FULL, "ergodic for every policy") is None


def test_locate_ellipsis_parts_must_be_in_order():
    import backcheck
    index = backcheck.build_index(FULL)
    assert backcheck.locate(index, "The MDP … is irreducible") == 1
    assert backcheck.locate(index, "is irreducible … The MDP") is None


def test_quote_must_be_in_fulltext_and_in_an_extract():
    import backcheck
    uses = [backcheck.Use("k", "cell k S6", "ergodic for any policy"), backcheck.Use("k", "cell k S1", "always safe")]
    assert backcheck.missing_in_fulltext(uses, {"k": FULL}) == ['cell k S1: quote not in 045_fulltext/k.txt: "always safe"']
    extracts = {"k": [{"id": "e1", "text": "The MDP is ergodic for any policy"}]}
    cited = {"cell k S6": ["e1"], "cell k S1": ["e1", "e9"]}
    assert backcheck.not_covered_by_extracts(uses, extracts, cited) == [
        "cell k S1: evidence e9 is not in 047_extracts/k/extracts.csv",
        "cell k S1: quote not in its cited extracts ['e1', 'e9']: \"always safe\""]


def test_page_of_counts_form_feeds():
    import backcheck
    text = "page one\nstill one\n\fpage two\nmore two\n\fpage three"
    assert [backcheck.page_of(text, n) for n in (1, 2, 3, 4, 5)] == [1, 1, 2, 2, 3]
    assert backcheck.page_of("no breaks", 1) is None


def test_stale_files_reports_a_changed_pdf():
    import backcheck
    manifest = [{"key": "k", "pdf_sha256": "aa", "txt_sha256": "bb"}]
    assert backcheck.stale_files(manifest, {("k", "pdf"): "aa", ("k", "txt"): "bb"}) == []
    assert len(backcheck.stale_files(manifest, {("k", "pdf"): "zz", ("k", "txt"): "bb"})) == 1


def test_cited_reference_must_exist():
    existence = [{"key": "a", "status": "ok", "note": ""}, {"key": "b", "status": "unverified", "note": ""},
                 {"key": "c", "status": "manual", "note": "title page seen in the PDF"}]
    assert checks.existence_problems({"a", "c"}, existence) == []
    assert len(checks.existence_problems({"b", "z"}, existence)) == 2


def test_term_hits_match_word_starts_in_the_body_only():
    import backcheck
    text = "A finite set.\nPositive definite, Finite again.\nReferences\nFinite automata, 1999."
    assert backcheck.term_hits(text, ["finite"]) == [("finite", 1), ("finite", 2)]


def test_absence_cell_fails_when_hit_count_changes():
    import backcheck
    cell = {"tool": "k", "condition": "S3", "evidence_type": "absence", "hits_reviewed": "1", "reason": "not needed"}
    terms = {"S3": ["finite"]}
    assert backcheck.absence_problems([cell], terms, {"k": "A finite set."}) == []
    assert len(backcheck.absence_problems([cell], terms, {"k": "A finite set. Finite again."})) == 1


def test_formula_must_be_verbatim_in_source_or_have_an_image():
    import backcheck
    extracts = {"k": [{"id": "e1", "tex": r"$a \le b$"}, {"id": "e2", "tex": ""}], "j": [{"id": "e1", "tex": "$x$"}]}
    assert backcheck.formula_problems(extracts, {"k": r"so $a  \le b$ holds"}, {("j", "e1")}) == []
    assert len(backcheck.formula_problems(extracts, {"k": "so $a < b$ holds"}, set())) == 2


def test_claim_goes_stale_when_wording_or_a_file_changes():
    import claims
    files = {"a.csv": "row1"}
    stamp = claims.claim_hash("Caption.", ["row1"])
    claim = {"id": "c", "text": "Caption.", "depends_on": "a.csv", "verified_hash": stamp, "verified_by": "x"}
    assert claims.stale([claim], files.__getitem__) == []
    assert len(claims.stale([claim], {"a.csv": "row1\nrow2"}.__getitem__)) == 1
    assert len(claims.stale([{**claim, "text": "Other caption."}], files.__getitem__)) == 1
    assert "never verified" in claims.stale([{**claim, "verified_hash": ""}], files.__getitem__)[0]


def test_role_needs_evidence_that_names_the_work():
    roles = [{"id": "named", "evidence_names_work": "yes"}, {"id": "named_uncited", "evidence_names_work": "no"}]
    extracts = [{"id": "e1", "text": "constraining agent behavior (Altman, 1999)"}, {"id": "e2", "text": "lack a safety shield"}]
    refs = [{"key": "altman1999", "short": "Altman"}, {"key": "wachi2023", "short": "Wachi et~al."}, {"key": "alshiekh2018", "short": "Alshiekh et~al."}]
    row = {"mclean_role": "named", "label_origin": "source", "decision": "D1"}
    tools = [{**row, "key": "altman1999", "role_evidence": "e1"}, {**row, "key": "wachi2023", "role_evidence": "e1"},
             {**row, "key": "alshiekh2018", "mclean_role": "named_uncited", "role_evidence": "e2"}]
    assert checks.role_problems(tools, roles, extracts, refs, [{"id": "D1"}]) == ["tool wachi2023: its role evidence does not name Wachi"]


def test_typed_count_next_to_a_set_noun_is_flagged():
    assert checks.typed_count_problems("Of the {{fact:offered_phrase}}, four state none.", ["tools", "works"]) == []
    assert len(checks.typed_count_problems("All fourteen cited tools fail.", ["tools", "works"])) == 1


def test_incident_added_by_us_needs_sources():
    inc = [{"id": "y", "in_mclean": "no", "worked_at": "", "our_sources": "", "recovered_in_process": "no", "fails": ""}]
    assert any("added by us" in p for p in checks.incident_problems(inc, ["S1"], []))


def test_quote_must_be_in_a_source_cited_next_to_it():
    import re
    import backcheck
    idx = {"a2020": backcheck.build_index("The MDP is ergodic for any policy."), "b2021": backcheck.build_index("Costs are given.")}
    cite = re.compile(r"@([a-z]+\d{4})")
    good = {"p": 'It is "ergodic for any policy" [@a2020].'}
    bad = {"p": 'It is "ergodic for any policy" [@b2021].'}
    assert backcheck.misattributed_quotes(good, idx, cite) == []
    assert len(backcheck.misattributed_quotes(bad, idx, cite)) == 1
    assert backcheck.misattributed_quotes({"p": 'A so-called "ergodic" chain [@b2021].'}, idx, cite) == []
