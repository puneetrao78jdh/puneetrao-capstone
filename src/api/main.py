"""FastAPI surface for the question-answering pipeline."""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from src.pipeline.pipeline import (
    Question as PipelineQuestion,
    ask_llm,
    stream_answer,
)
from src.pipeline.settings import Settings
from src.pipeline.store import connect, save_answer


class Question(BaseModel):
    question: str


class Answer(BaseModel):
    content: str
    cost_usd: float
    retries: int
    confidence: float = 1.0
    sources: list[str] = Field(default_factory=list)
    schema_version: str = "v1"


app = FastAPI(title="Capstone API — W4")
_settings = Settings()
_db_path = Path(_settings.results_db)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask_batched", response_model=Answer)
async def ask_batched(q: Question) -> Answer:
    pipeline_answer = await ask_llm(
        PipelineQuestion(text=q.question),
        _settings,
        fail_rate=_settings.fail_rate,
    )
    answer = Answer(
        content=pipeline_answer.text,
        cost_usd=pipeline_answer.cost_usd,
        retries=pipeline_answer.retries,
    )
    with connect(_db_path) as conn:
        save_answer(
            conn,
            question=q.question,
            content=answer.content,
            retries=answer.retries,
            cost_usd=answer.cost_usd,
            model=_settings.model,
            confidence=answer.confidence,
            sources=answer.sources,
            schema_version=answer.schema_version,
        )
    return answer


@app.post("/ask")
async def ask(q: Question) -> StreamingResponse:
    async def generate():
        async for chunk in stream_answer(q.question, _settings):
            yield chunk

    return StreamingResponse(generate(), media_type="text/plain")
