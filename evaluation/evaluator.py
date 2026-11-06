import json
import time
from pathlib import Path
from datetime import datetime, timezone

from app.rag_pipeline import answer_question


BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "datasets" / "golden_dataset.json"
REPORT_DIR = BASE_DIR / "reports"


def run_benchmark():

    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        dataset = json.load(file)

    REPORT_DIR.mkdir(exist_ok=True)

    results = []

    for test in dataset:
        start_time = time.perf_counter()

        try:
            output = answer_question(test["question"])
            answer = output["answer"]
            sources = output["sources"]

            latency = round(
                time.perf_counter() - start_time, 2
            )

            answer_words = answer.lower()
            matched = [
                word for word in test["expected_keywords"]
                if word.lower() in answer_words
            ]

            keyword_score = round(
                len(matched) / len(test["expected_keywords"]), 2
            )

            results.append({
                "id": test["id"],
                "question": test["question"],
                "answer": answer,
                "sources": sources,
                "latency_seconds": latency,
                "keyword_score": keyword_score,
                "matched_keywords": matched
            })

            print(
                f"{test['id']}: latency={latency}s, "
                f"keyword_score={keyword_score}"
            )

        except Exception as error:
            results.append({
                "id": test["id"],
                "question": test["question"],
                "error": str(error)
            })

            print(f"{test['id']}: FAILED")

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_tests": len(dataset),
        "successful_tests": sum(
            1 for result in results if "error" not in result
        ),
        "results": results
    }

    filename = datetime.now().strftime(
        "benchmark_%Y%m%d_%H%M%S.json"
    )

    report_path = REPORT_DIR / filename

    with open(report_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print(f"\nReport saved: {report_path.name}")


if __name__ == "__main__":
    run_benchmark()