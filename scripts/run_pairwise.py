"""Compare two prompt versions using both answer positions."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


PAIRWISE_TOOL = {
    "type": "function",
    "function": {
        "name": "submit_pairwise_result",
        "description": "Choose the better candidate answer.",
        "parameters": {
            "type": "object",
            "properties": {
                "winner": {
                    "type": "string",
                    "enum": ["first", "second", "tie"],
                },
                "reasoning": {
                    "type": "string",
                },
            },
            "required": ["winner", "reasoning"],
        },
    },
}


PAIRWISE_RUBRIC = """
You are a strict and fair evaluator.

Compare two candidate answers against the question and ideal answer.

Choose the answer that is more accurate, complete, grounded and clear.

Rules:

- Important facts and conditions must match the ideal answer.
- Penalise unsupported or invented company rules.
- A refusal is correct when the ideal answer says the information is absent.
- Do not prefer an answer only because it is longer.
- Choose tie when neither answer is meaningfully better.
- Return the result using the supplied tool.
"""


def load_golden_set(path: Path) -> list[dict]:
    entries = []

    with path.open(encoding="utf-8") as file:
        for line in file:
            if line.strip():
                entries.append(json.loads(line))

    return entries


def request_answer(
    client: httpx.Client,
    api_url: str,
    question: str,
    system_prompt: str,
) -> str:
    response = client.post(
        api_url,
        json={
            "question": question,
            "system_prompt": system_prompt,
        },
    )

    response.raise_for_status()
    return response.json()["content"]


def compare_answers(
    openai_client: OpenAI,
    *,
    judge_model: str,
    question: str,
    ideal_answer: str,
    first_answer: str,
    second_answer: str,
) -> dict:
    user_message = f"""
QUESTION:
{question}

IDEAL ANSWER:
{ideal_answer}

FIRST ANSWER:
{first_answer}

SECOND ANSWER:
{second_answer}
""".strip()

    response = openai_client.chat.completions.create(
        model=judge_model,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": PAIRWISE_RUBRIC,
            },
            {
                "role": "user",
                "content": user_message,
            },
        ],
        tools=[PAIRWISE_TOOL],
        tool_choice={
            "type": "function",
            "function": {
                "name": "submit_pairwise_result",
            },
        },
    )

    tool_calls = response.choices[0].message.tool_calls

    if not tool_calls:
        raise RuntimeError(
            "Pairwise judge did not return a tool call"
        )

    return json.loads(
        tool_calls[0].function.arguments
    )


def map_winner(
    positional_winner: str,
    *,
    first_label: str,
    second_label: str,
) -> str:
    if positional_winner == "first":
        return first_label

    if positional_winner == "second":
        return second_label

    return "tie"


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--prompt-v1",
        default="data/prompt-v1.txt",
    )
    parser.add_argument(
        "--prompt-v2",
        default="data/prompt-v2.txt",
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
        "--judge-model",
        default="gpt-4o",
    )
    parser.add_argument(
        "--output",
        default="data/pairwise-001-results.json",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
    )

    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set")

    output_path = Path(args.output)

    if output_path.exists():
        raise FileExistsError(
            f"{output_path} already exists. "
            "Choose a different output file or move the old file."
        )

    prompt_v1 = Path(
        args.prompt_v1
    ).read_text(encoding="utf-8").strip()

    prompt_v2 = Path(
        args.prompt_v2
    ).read_text(encoding="utf-8").strip()

    entries = load_golden_set(
        Path(args.golden_set)
    )[: args.limit]

    openai_client = OpenAI(api_key=api_key)
    results = []

    summary = {
        "v1": 0,
        "v2": 0,
        "tie": 0,
        "ambiguous": 0,
    }

    with httpx.Client(timeout=90.0) as api_client:
        for position, entry in enumerate(entries, 1):
            golden_id = entry["id"]
            question = entry["question"]
            ideal_answer = entry["ideal_answer"]

            print(
                f"[{position:02d}/{len(entries)}] "
                f"Comparing {golden_id}"
            )

            answer_v1 = request_answer(
                client=api_client,
                api_url=args.api_url,
                question=question,
                system_prompt=prompt_v1,
            )

            answer_v2 = request_answer(
                client=api_client,
                api_url=args.api_url,
                question=question,
                system_prompt=prompt_v2,
            )

            forward = compare_answers(
                openai_client,
                judge_model=args.judge_model,
                question=question,
                ideal_answer=ideal_answer,
                first_answer=answer_v1,
                second_answer=answer_v2,
            )

            reverse = compare_answers(
                openai_client,
                judge_model=args.judge_model,
                question=question,
                ideal_answer=ideal_answer,
                first_answer=answer_v2,
                second_answer=answer_v1,
            )

            forward_winner = map_winner(
                forward["winner"],
                first_label="v1",
                second_label="v2",
            )

            reverse_winner = map_winner(
                reverse["winner"],
                first_label="v2",
                second_label="v1",
            )

            if (
                forward_winner == reverse_winner
                and forward_winner in {"v1", "v2"}
            ):
                final_result = forward_winner
            elif (
                forward_winner == "tie"
                and reverse_winner == "tie"
            ):
                final_result = "tie"
            else:
                final_result = "ambiguous"

            summary[final_result] += 1

            results.append(
                {
                    "golden_id": golden_id,
                    "question": question,
                    "ideal_answer": ideal_answer,
                    "answer_v1": answer_v1,
                    "answer_v2": answer_v2,
                    "forward": {
                        "mapped_winner": forward_winner,
                        "reasoning": forward["reasoning"],
                    },
                    "reverse": {
                        "mapped_winner": reverse_winner,
                        "reasoning": reverse["reasoning"],
                    },
                    "result": final_result,
                }
            )

            print(
                f"  forward={forward_winner} "
                f"reverse={reverse_winner} "
                f"result={final_result}"
            )

    position_bias_rate = (
        summary["ambiguous"] / len(results)
        if results
        else 0
    )

    output = {
        "prompt_v1": args.prompt_v1,
        "prompt_v2": args.prompt_v2,
        "judge_model": args.judge_model,
        "questions_compared": len(results),
        "summary": summary,
        "position_bias_rate": position_bias_rate,
        "results": results,
    }

    output_path.write_text(
        json.dumps(output, indent=2),
        encoding="utf-8",
    )

    print()
    print("=" * 60)
    print("Pairwise summary")
    print("=" * 60)
    print(f"v1 wins       : {summary['v1']}")
    print(f"v2 wins       : {summary['v2']}")
    print(f"ties          : {summary['tie']}")
    print(f"ambiguous     : {summary['ambiguous']}")
    print(
        "position bias : "
        f"{position_bias_rate:.1%}"
    )
    print(f"saved to      : {output_path}")


if __name__ == "__main__":
    main()