"""pipeline.py — Week 2 hands-on starter.

We'll fill in the TODOs together during the live session. The pieces:

    Step 2 — async def ask_llm                 (one call)
    Step 3 — ask_llm_with_retry                (exponential backoff)
    Step 4 — run_batch with asyncio.gather     (parallel fan-out)
    Step 5 — JSON-formatted structured logging

For the live demo we call ``fake_ask_llm`` from ``fake_llm.py`` —
no API quota, no network flakiness, and a ``fail_rate`` knob so retries
fire on demand. In the lab you'll swap to the real ``AsyncOpenAI`` client
(same ``Question``/``Answer`` shape — only one import changes).

Run it (after the TODOs are filled):
    python pipeline.py           # fail_rate = 0.0  (clean parallel run)
    python pipeline.py 0.4       # fail_rate = 0.4  (forces retries)
"""
from __future__ import annotations

import asyncio
import json
import logging
import time
from .fake_llm import Question, Answer, fake_ask_llm, FakeLLMError
from datetime import datetime, timezone
from openai import AsyncOpenAI
from .store import init_db, save_run

# Live-session stand-in. Same Pydantic shape as the real call.

from .settings import Settings, RunSummary

import csv
from pathlib import Path

settings = Settings()
client = AsyncOpenAI()


def load_questions(
    path: str | Path = "data/questions.csv"
) -> list[Question]:
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        
    return [
        Question(text=row["text"])
        for row in rows
        if row.get("text")
    ]

# ---------- Step 2: one async call ----------
async def ask_llm(q: Question, fail_rate: float = 0.0) -> Answer:

    if settings.use_fake:
        return await fake_ask_llm(q, fail_rate=fail_rate)

    t0 = time.perf_counter()

    resp = await client.chat.completions.create(
        model=settings.model,
        messages=[
            {"role": "user", "content": q.text}
        ],
        temperature=0.3,
    )

    latency = time.perf_counter() - t0

    usage = resp.usage

    cost = (
        usage.prompt_tokens * 0.15
        + usage.completion_tokens * 0.60
    ) / 1_000_000

    return Answer(
        question=q.text,
        text=resp.choices[0].message.content or "",
        latency_seconds=latency,
        retries=0,
        cost_usd=cost,
    )


# ---------- Step 3: retry with exponential backoff ----------
async def ask_llm_with_retry(
    q: Question, tries: int = 3, fail_rate: float = 0.0
) -> Answer:
    """Retry up to ``tries`` times. Wait 1 s, 2 s, 4 s between attempts."""
    # TODO (Step 3):
    for attempt in range(tries):
           try:
               ans = await ask_llm(q, fail_rate=fail_rate)
               ans.retries = attempt
               return ans
           except Exception:
               if attempt == tries - 1:
                   raise
               await asyncio.sleep(2 ** attempt)
    raise RuntimeError("unreachable")


# ---------- Step 4: gather it all together ----------
async def run_batch(
    questions: list[Question], fail_rate: float = 0.0
) -> list[Answer]:
    """Fire all questions in parallel via ``asyncio.gather``."""
    # TODO (Step 4):
    #   tasks = [ask_llm_with_retry(q, fail_rate=fail_rate) for q in questions]
    #   return await asyncio.gather(*tasks)
    tasks = [
        ask_llm_with_retry(q, fail_rate=fail_rate)
        for q in questions
    ]
    return await asyncio.gather(*tasks)

async def run_in_batches(
    questions: list[Question],
    batch_size: int = 5,
    fail_rate: float = 0.0,
) -> list[Answer]:

    out: list[Answer] = []

    for i in range(0, len(questions), batch_size):
        chunk = questions[i:i + batch_size]

        batch_answers = await asyncio.gather(
            *(
                ask_llm_with_retry(q, fail_rate=fail_rate)
                for q in chunk
            )
        )

        out.extend(batch_answers)

        await asyncio.sleep(0.1)

    return out

from datetime import datetime, timezone


def summarise_run(
    answers: list[Answer],
    *,
    started_at: float,
    elapsed: float,
    fail_rate: float,
    use_fake: bool,
) -> RunSummary:
    return RunSummary(
        started_at=started_at,
        elapsed_seconds=elapsed,
        n_questions=len(answers),
        n_succeeded=len(answers),
        n_retries_total=sum(a.retries for a in answers),
        total_cost_usd=sum(a.cost_usd for a in answers),
        fail_rate=fail_rate,
        use_fake=use_fake,
    )


# ---------- Step 5: structured (JSON) logging ----------
# TODO (Step 5):
#   * class JsonFormatter(logging.Formatter): ...
#       (emit one JSON record per call with ts / level / msg)
#   * log = logging.getLogger("pipeline"); log.setLevel(logging.INFO)
#   * handler = logging.StreamHandler(); handler.setFormatter(JsonFormatter())
#   * log.addHandler(handler)
#   * Then go back to ask_llm() and add: log.info(f"asked: {q.text[:40]}")
def save_results(
    summary: RunSummary,
    answers: list[Answer],
    path: str = "results.json",
) -> None:
    result = {
        "summary": summary.model_dump(),
        "answers": [a.model_dump() for a in answers],
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

# ---------- main ----------
# ---------- main ----------
if __name__ == "__main__":

    questions = load_questions(settings.questions_csv)

    started_at = time.time()
    t0 = time.perf_counter()

    answers = asyncio.run(
        run_in_batches(
            questions,
            batch_size=settings.batch_size,
            fail_rate=settings.fail_rate,
        )
    )

    elapsed = time.perf_counter() - t0

    summary = summarise_run(
        answers,
        started_at=started_at,
        elapsed=elapsed,
        fail_rate=settings.fail_rate,
        use_fake=settings.use_fake,
    )

    save_results(
        summary,
        answers,
        settings.results_json,
    )

    init_db(settings.results_db)

    save_run(
        summary,
        answers,
        settings.results_db,
    )

    print(summary)
