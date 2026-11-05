#!/usr/bin/env python3
"""
Run criterion 4 (the appeal path) three times.  <- UNIT 8, MILESTONE 3

`run_eval.py`'s scenario shape (a list of texts or bodies sent to /submit)
has no place for a two-step flow: submit, get a content_id back, then appeal
against that specific id. So this criterion is tested here instead, with the
same shape as everything else — N trials, each one checked against the
target in criteria.md ("every call to /appeal with a valid content_id
changes status to under_review and writes exactly one new log line, in 5
out of 5 tries").

    python app.py                  # in one terminal
    python eval_appeal.py          # in another
"""

import datetime as dt
import json
import sys

import config

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass

DEFAULT_URL = f"http://{config.HOST}:{config.PORT}"
TRIALS = 3
APPEALS_PER_TRIAL = 5


def run_trial(trial_number, session, url):
    import requests

    results = []
    for i in range(1, APPEALS_PER_TRIAL + 1):
        submit_resp = session.post(
            f"{url}/submit",
            json={
                "text": f"A short genuine submission for appeal trial {trial_number}, case {i}.",
                "creator_id": f"eval_appeal_t{trial_number}_{i}",
            },
            timeout=90,
        )
        submit_body = submit_resp.json() if submit_resp.content else {}
        content_id = submit_body.get("content_id")

        before = requests.get(f"{url}/log?limit=1000", timeout=30).json()["count"]

        appeal_resp = session.post(
            f"{url}/appeal",
            json={"content_id": content_id, "reasoning": "I wrote this myself."},
            timeout=30,
        )
        appeal_body = appeal_resp.json() if appeal_resp.content else {}

        after = requests.get(f"{url}/log?limit=1000", timeout=30).json()["count"]

        status_check = requests.get(f"{url}/content/{content_id}", timeout=30).json()

        ok = (
            appeal_resp.status_code == 200
            and appeal_body.get("status") == "under_review"
            and status_check.get("status") == "under_review"
            and after == before + 1
        )

        results.append({
            "content_id": content_id,
            "appeal_status_code": appeal_resp.status_code,
            "appeal_response_status": appeal_body.get("status"),
            "content_status_after": status_check.get("status"),
            "log_entries_before": before,
            "log_entries_after": after,
            "ok": ok,
        })
    return results


def main():
    import requests

    url = DEFAULT_URL
    try:
        requests.get(f"{url}/health", timeout=5)
    except Exception:
        print(f"Nothing answering at {url}. Start it:  python app.py", file=sys.stderr)
        sys.exit(1)

    session = requests.Session()
    trials = []
    for t in range(1, TRIALS + 1):
        results = run_trial(t, session, url)
        passed = sum(1 for r in results if r["ok"])
        print(f"trial {t}: {passed}/{APPEALS_PER_TRIAL} appeals changed status and logged correctly")
        trials.append(results)

    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    path = config.RESULTS_DIR / f"eval_appeal_{stamp}.md"

    lines = [
        "# Criterion 4 — the appeal path",
        "",
        "- Produced by: `eval_appeal.py::main`",
        "- Service: `app.py::appeal`",
        f"- {TRIALS} trials of {APPEALS_PER_TRIAL} appeals each · "
        f"{dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
    ]
    for t, results in enumerate(trials, 1):
        passed = sum(1 for r in results if r["ok"])
        lines += [f"## Trial {t} — {passed}/{APPEALS_PER_TRIAL}", "", "```json",
                  json.dumps(results, indent=2), "```", ""]

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
