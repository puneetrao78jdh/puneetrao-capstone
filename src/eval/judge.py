"""LLM judge for scoring candidate answers against the Golden Set."""

from __future__ import annotations

import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field


load_dotenv()

class JudgeScore(BaseModel):
    """Structured scores returned by the judge."""

    accuracy: int = Field(ge=1, le=4)
    groundedness: int = Field(ge=1, le=4)
    format: int = Field(ge=1, le=4)
    reasoning: str = Field(min_length=1)


RUBRIC_PROMPT = """
You are a strict and fair evaluator of answers produced by a
question-answering assistant.

Compare the CANDIDATE ANSWER with the IDEAL ANSWER.

Score the candidate on three dimensions. Each score must be an integer
from 1 to 4.

ACCURACY
1 = Incorrect or contradicts the ideal answer.
2 = Partly correct but misses an important fact or condition.
3 = Mostly correct with only a small omission.
4 = Correct and complete compared with the ideal answer.

GROUNDEDNESS
1 = Contains major unsupported or invented claims.
2 = Contains at least one important unsupported claim.
3 = Mostly supported, with only a minor unsupported detail.
4 = All important claims are supported by the ideal answer.

FORMAT
1 = Confusing, unusable, or does not answer the question.
2 = Understandable but poorly organised or unnecessarily difficult to read.
3 = Clear, with only a minor presentation issue.
4 = Clear, direct, and appropriately concise.

Important rules:

- Be strict about numbers, eligibility conditions, exceptions and time limits.
- An answer missing an important condition cannot receive accuracy 4.
- An answer that invents a company rule cannot receive groundedness above 2.
- A clear refusal is correct when the ideal answer says the information is
  unavailable.
- Do not reward an answer only because it is longer.
- In the reasoning, mention the specific facts that caused the scores.
"""


JUDGE_TOOL = {
    "type": "function",
    "function": {
        "name": "submit_scores",
        "description": "Submit evaluation scores for the candidate answer.",
        "parameters": {
            "type": "object",
            "properties": {
                "accuracy": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 4,
                },
                "groundedness": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 4,
                },
                "format": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 4,
                },
                "reasoning": {
                    "type": "string",
                },
            },
            "required": [
                "accuracy",
                "groundedness",
                "format",
                "reasoning",
            ],
        },
    },
}


def build_messages(
    question: str,
    ideal_answer: str,
    candidate_answer: str,
) -> list[dict[str, str]]:
    """Build the messages sent to the judge."""

    evaluation_input = f"""
QUESTION:
{question}

IDEAL ANSWER:
{ideal_answer}

CANDIDATE ANSWER:
{candidate_answer}
""".strip()

    return [
        {
            "role": "system",
            "content": RUBRIC_PROMPT,
        },
        {
            "role": "user",
            "content": evaluation_input,
        },
    ]


def judge_answer(
    question: str,
    ideal_answer: str,
    candidate_answer: str,
    judge_model: str = "gpt-4o",
) -> JudgeScore:
    """Score one candidate answer and return structured results."""

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set")

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=judge_model,
        temperature=0,
        messages=build_messages(
            question=question,
            ideal_answer=ideal_answer,
            candidate_answer=candidate_answer,
        ),
        tools=[JUDGE_TOOL],
        tool_choice={
            "type": "function",
            "function": {
                "name": "submit_scores",
            },
        },
    )

    tool_calls = response.choices[0].message.tool_calls

    if not tool_calls:
        raise ValueError("Judge did not return the submit_scores tool call")

    arguments = json.loads(
        tool_calls[0].function.arguments
    )

    return JudgeScore.model_validate(arguments)