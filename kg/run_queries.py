"""
Run the Cypher query for every question in queries.txt and write results.csv
with the columns: Question, Cypher Query, Answer, Execution Time.

Execution Time = median wall-clock time (ms) of RUNS executions measured on the
client, from sending the query until all records are fetched, after one
untimed warm-up run (which lets the server cache the query plan).

    python -m kg.run_queries
"""
import csv
import json
import statistics
import time
from pathlib import Path

from kg.db import ROOT, database, get_driver

RUNS = 5
QUESTIONS_FILE = ROOT / "queries.txt"
CYPHER_DIR = ROOT / "cypher"
CSV_OUT = ROOT / "results.csv"
JSON_OUT = ROOT / "results.json"


def load_questions():
    text = QUESTIONS_FILE.read_text(encoding="utf-8")
    return [q.strip() for q in text.split("\n\n") if q.strip()]


def load_cypher():
    files = sorted(CYPHER_DIR.glob("q*.cypher"))
    out = []
    for f in files:
        lines = f.read_text(encoding="utf-8").splitlines()
        out.append("\n".join(l for l in lines if not l.lstrip().startswith("//")).strip())
    return out


def fmt_value(v):
    if v is None:
        return "n/a"
    if isinstance(v, list):
        return "[" + ", ".join(fmt_value(x) for x in v) + "]"
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    if isinstance(v, int) and not isinstance(v, bool) and abs(v) >= 10_000:
        return f"{v:,}"
    return str(v)


def fmt_answer(records):
    if not records:
        return "(no results)"
    return "\n".join(
        f"{i}. " + "; ".join(f"{k}: {fmt_value(v)}" for k, v in r.items())
        for i, r in enumerate(records, start=1)
    )


def run_once(session, query):
    t0 = time.perf_counter()
    result = session.run(query)
    records = [r.data() for r in result]
    result.consume()
    return records, (time.perf_counter() - t0) * 1000


def main():
    questions, queries = load_questions(), load_cypher()
    if len(questions) != len(queries):
        raise SystemExit(f"{len(questions)} questions but {len(queries)} cypher files")

    rows, raw = [], []
    with get_driver() as driver, driver.session(database=database()) as session:
        for n, (question, query) in enumerate(zip(questions, queries), start=1):
            run_once(session, query)  # warm-up
            timings = []
            for _ in range(RUNS):
                records, ms = run_once(session, query)
                timings.append(ms)
            median = statistics.median(timings)
            rows.append({
                "Question": question,
                "Cypher Query": query,
                "Answer": fmt_answer(records),
                "Execution Time": f"{median:.2f} ms",
            })
            raw.append({"question": question, "query": query, "records": records,
                        "timings_ms": [round(t, 2) for t in timings]})
            print(f"Q{n}: {len(records)} rows, median {median:.2f} ms")

    with CSV_OUT.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["Question", "Cypher Query", "Answer", "Execution Time"],
                           quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)
    JSON_OUT.write_text(json.dumps(raw, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {CSV_OUT.name} and {JSON_OUT.name}")


if __name__ == "__main__":
    main()
