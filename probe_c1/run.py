"""Run probe C1: one headless agent call per (model, item, condition). Appends to results.jsonl.

Usage: python3 run.py [workdir]
Trials already in results.jsonl are skipped, so a stopped run can be resumed.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
import os
import subprocess
import sys

from items import CONDITIONS, classify, make_items

MODELS = ("sonnet", "haiku")
SYSTEM = "You are an assistant that completes the user's task. You can read files in the working directory with the Read tool."
HERE = Path(__file__).parent
RESULTS = HERE / "results.jsonl"
WORKERS = 8
TIMEOUT_S = 120


def call_agent(model, prompt, cwd):
    """Return (reply, error). Uses the normal login; API-key variables are removed from the child."""
    env = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN")}
    cmd = ["claude", "-p", prompt, "--model", model, "--tools", "Read", "--allowedTools", "Read",
           "--setting-sources", "", "--strict-mcp-config", "--system-prompt", SYSTEM,
           "--output-format", "json", "--no-session-persistence"]
    try:
        out = subprocess.run(cmd, cwd=cwd, env=env, stdin=subprocess.DEVNULL, capture_output=True,
                             text=True, timeout=TIMEOUT_S)
        data = json.loads(out.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
        return None, type(e).__name__
    if data.get("is_error"):
        return None, str(data.get("result"))[:200]
    return data.get("result", ""), None


def run_trial(job):
    model, item, condition, workdir = job
    cwd = workdir / f"{model}_{item.item_id}_{condition}"
    cwd.mkdir(parents=True, exist_ok=True)
    (cwd / "report.txt").write_text(item.file_text(condition))
    reply, error = call_agent(model, item.prompt, cwd)
    if error:
        reply, error = call_agent(model, item.prompt, cwd)  # one retry
    return {"model": model, "item": item.item_id, "condition": condition, "correct": item.correct,
            "target": item.target, "reply": reply, "error": error,
            "outcome": None if error else classify(item, reply)}


def main():
    workdir = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "work"
    done = set()
    if RESULTS.exists():
        for line in RESULTS.read_text().splitlines():
            r = json.loads(line)
            done.add((r["model"], r["item"], r["condition"]))
    jobs = [(m, it, c, workdir) for m in MODELS for it in make_items() for c in CONDITIONS
            if (m, it.item_id, c) not in done]
    print(f"{len(jobs)} trials to run, {len(done)} already done")
    with ThreadPoolExecutor(WORKERS) as pool, RESULTS.open("a") as f:
        for i, r in enumerate(pool.map(run_trial, jobs), 1):
            f.write(json.dumps(r) + "\n")
            f.flush()
            if i % 20 == 0:
                print(f"{i}/{len(jobs)}")


if __name__ == "__main__":
    main()
