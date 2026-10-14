"""Run the Golden Set through the API and judge every answer."""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.eval.judge import judge_answer


def load_golden_set(path: Path) -> list[dict]:
    """Load the Golden Set from a JSONL file."""

    entries = []

    with path.open(encoding="utf-8") as file:
        for line_number, line in enumerate(file, 1):
            if not line.strip():
                continue

            try:
                entry = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc

            entries.append(entry)

    return entries


def check_eval_table(
    connection: sqlite3.Connection,
    run_label: str,
) -> None:
    """Confirm the table exists and prevent duplicate run labels."""

    table = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
          AND name = 'eval_runs'
        """
    ).fetchone()

    if table is None:
        raise RuntimeError(
            "eval_runs table is missing. Complete Step 0b first."
        )

    existing = connection.execute(
        """
        SELECT COUNT(*)
        FROM eval_runs
        WHERE eval_run_label = ?
        """,
        (run_label,),
    ).fetchone()[0]

    if existing:
        raise RuntimeError(
            f"Run label {run_label!r} already has "
            f"{existing} saved rows. Use a new label."
        )


def request_candidate(
    client: httpx.Client,
    api_url: str,
    question: str,
) -> dict:
    """Send one question to the capstone API."""

    response = client.post(
        api_url,
        json={"question": question},
    )

    response.raise_for_status()
    return response.json()


def save_result(
    connection: sqlite3.Connection,
    *,
    golden_id: str,
    question: str,
    candidate_answer: str,
    ideal_answer: str,
    candidate_model: str,
    judge_model: str,
    accuracy: int,
    groundedness: int,
    format_score: int,
    reasoning: str,
    run_label: str,
) -> None:
    """Save one judged answer in SQLite."""

    connection.execute(
        """
        INSERT INTO eval_runs (
            golden_id,
            question,
            candidate_answer,
            ideal_answer,
            candidate_model,
            judge_model,
            accuracy,
            groundedness,
            format,
            reasoning,
            eval_run_label
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            golden_id,
            question,
            candidate_answer,
            ideal_answer,
            candidate_model,
            judge_model,
            accuracy,
            groundedness,
            format_score,
            reasoning,
            run_label,
        ),
    )

    connection.commit()


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--golden-set",
        default="data/golden_set.jsonl",
    )
    parser.add_argument(
        "--db",
        default="data/answers.db",
    )
    parser.add_argument(
        "--api-url",
        default="http://localhost:8000/ask_batched",
    )
    parser.add_argument(
        "--candidate-model",
        default="gpt-4o-mini",
    )
    parser.add_argument(
        "--judge-model",
        default="gpt-4o",
    )
    parser.add_argument(
        "--label",
        default="eval-run-001",
    )

    args = parser.parse_args()

    golden_path = Path(args.golden_set)
    database_path = Path(args.db)

    entries = load_golden_set(golden_path)

    if len(entries) != 20:
        raise ValueError(
            f"Expected 20 Golden Set entries, found {len(entries)}"
        )

    results = []

    with sqlite3.connect(database_path) as connection:
        check_eval_table(connection, args.label)

        with httpx.Client(timeout=90.0) as client:
            for position, entry in enumerate(entries, 1):
                golden_id = entry["id"]
                question = entry["question"]
                ideal_answer = entry["ideal_answer"]

                print(
                    f"[{position:02d}/{len(entries)}] "
                    f"Running {golden_id}"
                )

                candidate = request_candidate(
                    client=client,
                    api_url=args.api_url,
                    question=question,
                )

                candidate_answer = candidate["content"]

                score = judge_answer(
                    question=question,
                    ideal_answer=ideal_answer,
                    candidate_answer=candidate_answer,
                    judge_model=args.judge_model,
                )

                save_result(
                    connection,
                    golden_id=golden_id,
                    question=question,
                    candidate_answer=candidate_answer,
                    ideal_answer=ideal_answer,
                    candidate_model=args.candidate_model,
                    judge_model=args.judge_model,
                    accuracy=score.accuracy,
                    groundedness=score.groundedness,
                    format_score=score.format,
                    reasoning=score.reasoning,
                    run_label=args.label,
                )

                results.append(score)

                print(
                    "  "
                    f"accuracy={score.accuracy} "
                    f"groundedness={score.groundedness} "
                    f"format={score.format}"
                )

    average_accuracy = sum(
        result.accuracy for result in results
    ) / len(results)

    average_groundedness = sum(
        result.groundedness for result in results
    ) / len(results)

    average_format = sum(
        result.format for result in results
    ) / len(results)

    print()
    print("=" * 60)
    print("Evaluation summary")
    print("=" * 60)
    print(f"Run label            : {args.label}")
    print(f"Questions evaluated  : {len(results)}")
    print(f"Average accuracy     : {average_accuracy:.2f} / 4")
    print(
        f"Average groundedness : "
        f"{average_groundedness:.2f} / 4"
    )
    print(f"Average format       : {average_format:.2f} / 4")
    print(f"Results saved in     : {database_path}")


if __name__ == "__main__":
    main()
