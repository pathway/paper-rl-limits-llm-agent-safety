from analyze import compress, differing, failing_needs, setting_grid, tool_needs, count_phrase, with_guarantee_kind, conditions_with_stance, full_needs, members, counted, facts, sensitivity, most_met_phrase, needs_of

ORDER = ["S1", "S2", "S3", "S4", "S5", "S6", "U1", "U2", "U3", "U4"]


def test_compress_full_groups():
    assert compress(ORDER, ORDER) == "S1–S6 and U1–U4"


def test_compress_scattered():
    assert compress(["S2", "S4", "S6", "U1", "U3"], ORDER) == "S2, S4, S6, U1 and U3"


def test_compress_of_nothing_is_none():
    assert compress([], ORDER) == "none"


def test_compress_short_run_is_listed():
    assert compress(["S1", "S2"], ORDER) == "S1 and S2"


def test_differing_and_failing():
    grid = setting_grid([{"condition": "S1", "setting": "A", "value": "✓"},
                         {"condition": "S1", "setting": "B", "value": "✗"},
                         {"condition": "S2", "setting": "A", "value": "~"},
                         {"condition": "S2", "setting": "B", "value": "~"}])
    assert differing(grid, "A", "B", ["S1", "S2"]) == ["S1"]
    needs = tool_needs([{"tool": "t", "condition": "S1", "display": "✓"},
                        {"tool": "t", "condition": "S2", "display": ""},
                        {"tool": "u", "condition": "S2", "display": "proofs"}])
    assert needs == {"t": ["S1"], "u": ["S2"]}
    assert failing_needs(needs, grid, "B") == {"t": ["S1"]}


def test_count_phrase():
    assert count_phrase(8, 8) == "all eight" and count_phrase(6, 8) == "six of eight"
    assert count_phrase(2, 2) == "both" and count_phrase(1, 2) == "one of two"


def test_with_guarantee_kind():
    tools = [{"key": "a", "guarantee_kind": "none"}, {"key": "b", "guarantee_kind": "safety"}]
    assert with_guarantee_kind(tools, "none") == ["a"] and with_guarantee_kind(tools, "safety") == ["b"]


def test_conditions_with_stance():
    stance = [{"condition": "S1", "stance": "concedes"}, {"condition": "U2", "stance": "not discussed"}]
    assert conditions_with_stance(stance, {"concedes", "states"}) == ["S1"]


def test_full_needs_excludes_qualified_cells():
    cells = [{"tool": "t", "condition": "S1", "display": "✓"}, {"tool": "t", "condition": "S2", "display": "proofs"},
             {"tool": "t", "condition": "S3", "display": ""}]
    assert full_needs(cells) == {"t": ["S1"]}


TOOLS = [{"key": "a", "mclean_role": "named", "guarantee_kind": "safety", "mclean_term": "x"},
         {"key": "b", "mclean_role": "topic", "guarantee_kind": "none"},
         {"key": "c", "mclean_role": "other", "guarantee_kind": "none"}]
SETS = [{"id": "works", "roles": "named; topic; other", "label": "works"},
        {"id": "offered", "roles": "named; topic", "label": "works offered as tools"},
        {"id": "other_works", "roles": "other", "label": "other works"},
        {"id": "named_tools", "roles": "named", "label": "named works"}]


def test_members_follow_the_set_definition():
    assert [t["key"] for t in members(TOOLS, SETS[1])] == ["a", "b"]
    assert counted(2, SETS[1]["label"]) == "two works offered as tools"


def test_counts_use_the_offered_set_and_sensitivity_names_what_changes():
    inputs = dict(tools=TOOLS, sets=SETS, stated=[{"id": "S1"}], unstated=[],
                  tool_cells=[{"tool": "a", "condition": "S1", "display": "✓"}, {"tool": "alshiekh2018", "condition": "S1", "display": "✓"}],
                  setting_cells=[{"condition": c, "setting": s, "value": "✗"} for c in ("S1", "S5")
                                 for s in ("D-AGENT", "D-RL", "D-CHAT", "T-RL", "T-CHAT", "T-PRM")],
                  stance=[], incidents=[])
    out = facts(**inputs)
    assert out["offered_n"] == "two" and out["offered_none_n"] == "one" and out["offered_phrase"] == "two works offered as tools"
    changes = sensitivity(inputs)
    assert changes["without the set 'other_works'"] == {"works_n": ("three", "two"), "other_works_n": ("one", "zero")}
    assert out["named_terms_n"] == "one" and out["guaranteed_not_failing"] == "none"
    assert "offered_none_n" in changes["without b (topic)"]


def test_most_met_phrase_reports_ties():
    grid = {"A": {"S1": "✓", "S2": "✓"}, "B": {"S1": "✓", "S2": "✓"}, "C": {"S1": "✓", "S2": "✗"}}
    assert most_met_phrase(grid, "A", ["A", "B", "C"]) == "as many conditions as any LLM column"
    assert most_met_phrase(grid, "A", ["A", "C"]) == "the most conditions of any LLM column"
    assert most_met_phrase(grid, "C", ["A", "C"]) == "fewer conditions than some other LLM column"


def test_needs_of_splits_full_part_and_none():
    cells = [{"tool": "t", "condition": c, "display": d} for c, d in (("S1", "✓"), ("S2", "label"), ("S3", ""))]
    assert needs_of(cells, "t", ORDER) == ("S1", "S2", "S3")


def test_deployment_failures_split_stated_from_unstated_and_safety_from_other_guarantees():
    inputs = dict(tools=TOOLS, sets=SETS, stated=[{"id": "S1"}], unstated=[{"id": "S5"}],
                  tool_cells=[{"tool": "a", "condition": "S1", "display": "✓"}],
                  setting_cells=[{"condition": c, "setting": s, "value": "✗" if c == "S1" else "~"} for c in ("S1", "S5")
                                 for s in ("D-AGENT", "D-RL", "D-CHAT", "T-RL", "T-CHAT", "T-PRM")],
                  stance=[], incidents=[])
    out = facts(**inputs)
    assert (out["dagent_stated_fail"], out["dagent_unstated_fail"]) == ("all one", "zero of one")
    assert out["safety_failing_dagent"] == "all one"


def test_training_agent_failures_count_guaranteed_works_by_full_cells_only():
    tools = [{**t, "tool": t["key"]} for t in TOOLS] + [{"key": "d", "tool": "d", "mclean_role": "topic", "guarantee_kind": "other"}]
    cells = [{"tool": "a", "condition": "S1", "display": "✓"}, {"tool": "d", "condition": "S1", "display": "proofs"},
             {"tool": "b", "condition": "S1", "display": "✓"}]
    grid = [{"condition": c, "setting": s, "value": "✗" if (c, s) == ("S1", "T-AGENT") else "✓"} for c in ("S1", "S5")
            for s in ("T-AGENT", "D-AGENT", "D-RL", "D-CHAT", "T-RL", "T-CHAT", "T-PRM")]
    out = facts(tools=tools, sets=SETS, stated=[{"id": "S1"}], unstated=[], tool_cells=cells,
                setting_cells=grid, stance=[], incidents=[])
    assert out["guaranteed_failing_tagent"] == "one of two"


def test_count_with_the_scaling_gap_granted_ignores_s2_and_s3():
    tools = [{"key": k, "tool": k, "mclean_role": "topic", "guarantee_kind": "other"} for k in ("p", "q")]
    cells = [{"tool": "p", "condition": "S2", "display": "✓"}, {"tool": "p", "condition": "S3", "display": "✓"},
             {"tool": "q", "condition": "S3", "display": "✓"}, {"tool": "q", "condition": "S4", "display": "✓"}]
    grid = [{"condition": c, "setting": s, "value": "✗"} for c in ("S2", "S3", "S4", "S5")
            for s in ("T-AGENT", "D-AGENT", "D-RL", "D-CHAT", "T-RL", "T-CHAT", "T-PRM")]
    out = facts(tools=tools, sets=SETS, stated=[{"id": c} for c in ("S2", "S3", "S4")], unstated=[], tool_cells=cells,
                setting_cells=grid, stance=[], incidents=[])
    assert out["guaranteed_failing_dagent"] == "both"
    assert out["guaranteed_failing_dagent_scale_granted"] == "one of two"
