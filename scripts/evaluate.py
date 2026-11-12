"""Run explicitly selected synthetic evaluation; no model calls or external services."""
import argparse
import hashlib
import json
from pathlib import Path
from statistics import median
from time import perf_counter_ns

from app.triage import classify

ROOT = Path(__file__).resolve().parents[1]


def evaluate(split: str) -> dict:
    raw = (ROOT / "data/tickets.json").read_bytes()
    rows = [row for row in json.loads(raw) if row["split"] == split]
    outcomes = []
    for row in rows:
        started = perf_counter_ns()
        result = classify(row["subject"], row["body"])
        elapsed = (perf_counter_ns() - started) / 1_000_000
        outcomes.append({"id": row["id"], "expected": row["label"], "predicted": result.category,
                         "correct": result.category == row["label"], "latency_ms": round(elapsed, 4)})
    labels = sorted({row["expected"] for row in outcomes} | {row["predicted"] for row in outcomes})
    metrics = {}
    for label in labels:
        tp = sum(row["expected"] == label and row["predicted"] == label for row in outcomes)
        predicted = sum(row["predicted"] == label for row in outcomes)
        actual = sum(row["expected"] == label for row in outcomes)
        precision, recall = tp / predicted if predicted else 0, tp / actual if actual else 0
        metrics[label] = {"support": actual, "precision": round(precision, 3), "recall": round(recall, 3),
                          "f1": round(2 * precision * recall / (precision + recall), 3) if precision + recall else 0}
    return {"method": "lexical-v1", "split": split, "dataset_sha256": hashlib.sha256(raw).hexdigest(),
            "rule_sha256": hashlib.sha256((ROOT / "app/triage.py").read_bytes()).hexdigest(),
            "samples": len(outcomes), "accuracy": round(sum(row["correct"] for row in outcomes) / len(outcomes), 3),
            "median_latency_ms": round(median(row["latency_ms"] for row in outcomes), 4),
            "per_class": metrics, "outcomes": outcomes,
            "limitations": ["Small hand-authored synthetic dataset; no real-world generalization claim.",
                            "Holdout is public and has not been independently labeled; it is not a blind benchmark.",
                            "Rules do not understand negation or semantics. No LLM has been evaluated.",
                            "Timing measures in-process classification, excluding HTTP and frontend."]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", choices=["dev", "holdout"], required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = json.dumps(evaluate(args.split), ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report)
    else:
        print(report)
