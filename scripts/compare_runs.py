import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = BASE_DIR / "reports"


def compare_runs():

    reports = sorted(
        REPORT_DIR.glob("benchmark_*.json"),
        key=lambda path: path.stat().st_mtime
    )

    if len(reports) < 2:
        print("Run the benchmark at least twice to compare reports.")
        return

    with open(reports[-2], encoding="utf-8") as file:
        previous = json.load(file)

    with open(reports[-1], encoding="utf-8") as file:
        current = json.load(file)

    old_results = {
        item["id"]: item
        for item in previous["results"]
        if "error" not in item
    }

    new_results = {
        item["id"]: item
        for item in current["results"]
        if "error" not in item
    }

    print("Comparing latest benchmark runs\n")

    for test_id, new in new_results.items():

        old = old_results.get(test_id)

        if old is None:
            print(f"{test_id}: New test or missing previous result")
            continue

        latency_change = round(
            new["latency_seconds"] - old["latency_seconds"], 2
        )

        answer_changed = (
            new["answer"].strip() != old["answer"].strip()
        )

        print(f"Test: {test_id}")
        print(f"Latency change: {latency_change:+.2f} seconds")
        print(f"Answer changed: {answer_changed}")
        print(
            f"Keyword score: "
            f"{old['keyword_score']} -> {new['keyword_score']}"
        )
        print("-" * 35)


if __name__ == "__main__":
    compare_runs()