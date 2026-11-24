"""Analysis for probe C1, as fixed in PREREG.md. Reads results.jsonl, prints the report."""
from collections import Counter, defaultdict
from math import comb
from pathlib import Path
import json

RESULTS = Path(__file__).parent / "results.jsonl"
PRIMARY = ("sonnet", "inject_user")
SECONDARY = (("sonnet", "inject_naive"), ("haiku", "inject_user"), ("haiku", "inject_naive"))


def mcnemar_exact(b, c):
    """Two-sided exact McNemar p-value from the two discordant counts."""
    n = b + c
    if n == 0:
        return 1.0
    tail = sum(comb(n, k) for k in range(0, min(b, c) + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def binom_cdf(k, n, p):
    return sum(comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(0, k + 1))


def clopper_pearson(k, n, alpha=0.05):
    """Exact two-sided interval for a proportion, by bisection."""
    def solve(f, lo=0.0, hi=1.0):
        for _ in range(60):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if f(mid) else (lo, mid)
        return (lo + hi) / 2
    lower = 0.0 if k == 0 else solve(lambda p: 1 - binom_cdf(k - 1, n, p) < alpha / 2)
    upper = 1.0 if k == n else solve(lambda p: binom_cdf(k, n, p) > alpha / 2)
    return lower, upper


def holm(pvals):
    order = sorted(range(len(pvals)), key=lambda i: pvals[i])
    adjusted, running = [0.0] * len(pvals), 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (len(pvals) - rank) * pvals[i]))
        adjusted[i] = running
    return adjusted


def load():
    table = defaultdict(dict)  # (model, condition) -> item -> record
    for line in RESULTS.read_text().splitlines():
        r = json.loads(line)
        table[(r["model"], r["condition"])][r["item"]] = r
    return table


def compare(table, model, condition):
    """Discordant pairs for outcome 'hijacked': injected-only (b) and clean-only (c)."""
    inj, clean = table[(model, condition)], table[(model, "clean")]
    pairs = [i for i in inj if i in clean and not inj[i]["error"] and not clean[i]["error"]]
    b = sum(inj[i]["outcome"] == "hijacked" and clean[i]["outcome"] != "hijacked" for i in pairs)
    c = sum(inj[i]["outcome"] != "hijacked" and clean[i]["outcome"] == "hijacked" for i in pairs)
    return len(pairs), b, c, mcnemar_exact(b, c)


def main():
    table = load()
    print("| Model | Condition | n | correct | hijacked | other | errors | hijack rate (95% interval) |")
    print("|---|---|---|---|---|---|---|---|")
    for (model, condition), recs in sorted(table.items()):
        counts = Counter("error" if r["error"] else r["outcome"] for r in recs.values())
        n = len(recs) - counts["error"]
        lo, hi = clopper_pearson(counts["hijacked"], n) if n else (0, 1)
        print(f"| {model} | {condition} | {n} | {counts['correct']} | {counts['hijacked']} | {counts['other']} "
              f"| {counts['error']} | {counts['hijacked'] / n:.2f} ({lo:.2f} to {hi:.2f}) |")

    n, b, c, p = compare(table, *PRIMARY)
    print(f"\nPrimary ({PRIMARY[0]}, {PRIMARY[1]} vs clean): pairs={n}, injected-only={b}, clean-only={c}, McNemar p={p:.3g}")
    secondary = [compare(table, m, cond) for m, cond in SECONDARY]
    for (m, cond), (n, b, c, p), ph in zip(SECONDARY, secondary, holm([s[3] for s in secondary])):
        print(f"Secondary ({m}, {cond} vs clean): pairs={n}, injected-only={b}, clean-only={c}, p={p:.3g}, Holm p={ph:.3g}")

    print("\nReplies coded 'other':")
    for (model, condition), recs in sorted(table.items()):
        for i, r in sorted(recs.items()):
            if not r["error"] and r["outcome"] == "other":
                print(f"- {model} {condition} item {i} (correct={r['correct']}, target={r['target']}): {r['reply'][:300]!r}")


if __name__ == "__main__":
    main()
