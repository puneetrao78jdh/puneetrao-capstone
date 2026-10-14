"""Run a Critic-Creator loop on one Golden Set question."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv
from openai import OpenAI


sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent),
)

from src.eval.judge import judge_answer


load_dotenv()


def load_entry(path: Path, golden_id: str) -> dict:
    with path.open(encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            entry = json.loads(line)

            if entry["id"] == golden_id:
                return entry

    raise ValueError(
        f"Golden entry {golden_id!r} was not found"
    )


def get_first_draft(
    api_url: str,
    question: str,
    system_prompt: str,
) -> str:
    response = httpx.post(
        api_url,
        json={
            "question": question,
            "system_prompt": system_prompt,
        },
        timeout=90,
    )

    response.raise_for_status()
    return response.json()["content"]


def revise_answer(
    client: OpenAI,
    *,
    model: str,
    question: str,
    current_answer: str,
    critique: str,
) -> str:
    response = client.chat.completions.create(
        model=model,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": (
                    "You revise answers using the critic's "
                    "specific feedback. Correct every identified "
                    "problem. Keep the answer clear and concise. "
                    "Do not mention the critic or evaluation."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"QUESTION:\n{question}\n\n"
                    f"CURRENT ANSWER:\n{current_answer}\n\n"
                    f"CRITIC FEEDBACK:\n{critique}\n\n"
                    "Write the revised answer."
                ),
            },
        ],
    )

    return response.choices[0].message.content.strip()


def write_trace(
    output_path: Path,
    *,
    golden_id: str,
    question: str,
    creator_model: str,
    judge_model: str,
    rounds: list[dict],
    converged: bool,
) -> None:
    lines = [
        "# Critic-Creator Trace",
        "",
        f"- Golden ID: `{golden_id}`",
        f"- Creator model: `{creator_model}`",
        f"- Critic model: `{judge_model}`",
        f"- Converged: {'Yes' if converged else 'No'}",
        "",
        "## Question",
        "",
        question,
        "",
    ]

    for item in rounds:
        lines.extend(
            [
                f"## Round {item['round']}",
                "",
                "### Answer",
                "",
                item["answer"],
                "",
                "### Scores",
                "",
                (
                    f"- Accuracy: {item['accuracy']} / 4\n"
                    f"- Groundedness: "
                    f"{item['groundedness']} / 4\n"
                    f"- Format: {item['format']} / 4\n"
                    f"- Mean: {item['mean']:.2f} / 4"
                ),
                "",
                "### Critic Feedback",
                "",
                item["reasoning"],
                "",
            ]
        )

    lines.extend(
        [
            "## Reflection",
            "",
            "Replace this text with your reflection after "
            "reading the trace.",
            "",
        ]
    )

    output_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--golden-id",
        default="g015",
    )
    parser.add_argument(
        "--golden-set",
        default="data/golden_set.jsonl",
    )
    parser.add_argument(
        "--api-url",
        default="http://localhost:8000/ask_batched",
    )
    parser.add_argument(
        "--prompt",
        default="data/prompt-v1.txt",
    )
    parser.add_argument(
        "--creator-model",
        default="gpt-4o-mini",
    )
    parser.add_argument(
        "--judge-model",
        default="gpt-4o",
    )
    parser.add_argument(
        "--max-rounds",
        type=int,
        default=3,
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=3.5,
    )
    parser.add_argument(
        "--output",
        default="docs/critic-creator-trace.md",
    )

    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set")

    entry = load_entry(
        Path(args.golden_set),
        args.golden_id,
    )

    question = entry["question"]
    ideal_answer = entry["ideal_answer"]

    system_prompt = Path(
        args.prompt
    ).read_text(encoding="utf-8").strip()

    current_answer = get_first_draft(
        api_url=args.api_url,
        question=question,
        system_prompt=system_prompt,
    )

    creator_client = OpenAI(api_key=api_key)
    rounds = []
    converged = False

    for round_number in range(
        1,
        args.max_rounds + 1,
    ):
        score = judge_answer(
            question=question,
            ideal_answer=ideal_answer,
            candidate_answer=current_answer,
            judge_model=args.judge_model,
        )

        mean_score = (
            score.accuracy
            + score.groundedness
            + score.format
        ) / 3

        rounds.append(
            {
                "round": round_number,
                "answer": current_answer,
                "accuracy": score.accuracy,
                "groundedness": score.groundedness,
                "format": score.format,
                "mean": mean_score,
                "reasoning": score.reasoning,
            }
        )

        print(
            f"Round {round_number}: "
            f"a={score.accuracy} "
            f"g={score.groundedness} "
            f"f={score.format} "
            f"mean={mean_score:.2f}"
        )

        if mean_score >= args.threshold:
            converged = True
            break

        if round_number < args.max_rounds:
            current_answer = revise_answer(
                creator_client,
                model=args.creator_model,
                question=question,
                current_answer=current_answer,
                critique=score.reasoning,
            )

    write_trace(
        Path(args.output),
        golden_id=args.golden_id,
        question=question,
        creator_model=args.creator_model,
        judge_model=args.judge_model,
        rounds=rounds,
        converged=converged,
    )

    print(f"Trace saved to {args.output}")


if __name__ == "__main__":
    main()