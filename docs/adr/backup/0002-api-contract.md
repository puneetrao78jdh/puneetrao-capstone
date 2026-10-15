# ADR-0002: API Contract

- **Status:** Draft
- **Date:** 2026-09-09
- **Author:** Puneet Rao

## Usecase
Enterprise knowlege assistant for GitLab Handbook. This capstone will build a grounded Q&A assistant over a selected set of public GitLab Handbook policies so that users can ask natural-language questions and receive concise answers based on the source documents rather than relying only on the LLM’s general knowledge.

## Context

Week 3 introduces a FastAPI layer in front of the existing pipeline so external clients can call the application over HTTP. We will be try to use this form 8000 port and also streamlit 8501 port

## Decision

The application will expose a small, stable API surface for asking questions and checking service health.

### Endpoints

- `GET /health` - to check server is working and is in good health
- `POST /ask` - return streaming answer
- `POST /ask_batched` - return entire answer in one batch without streaming

### Request contract

Question requests use this JSON shape:

```json
{
  "question": "What is RAG?"
}
```

- GET/health - will retrun {"status": "ok"}
- POST /ask_batched - complete answer + cost_usd + retries
- POST /ask - stream answer text peace by peace

## Validation

The API uses Pydantic to validate incoming requests. A valid request must contain a question field as a string. If required data is missing or invalid, FastAPI rejects the request with HTTP 422 before it reaches the LLM.

## Consequences
- Other applications can now use our AI pipeline through the API without knowing our internal Python code.
- We need to keep the API contract stable because changing endpoint names or request/response formats may break applications using it.
- Streaming gives users a better experience, but it also makes handling connections and errors more complex.

## Tests
- Test that /health returns 200 and {"status": "ok"}.
- Test that /ask rejects requests without a valid question.
- Test that ask_llm() calls the expected LLM function correctly.
- Test that retry logic makes 3 attempts before finally raising an error.

### Schema versioning rule (added W4)

Every `Answer` carries a `schema_version` field.

**Today's shape is `v1`.** It stays `v1` through any additive change:
new optional fields with defaults, new endpoints at different paths,
internal model swaps, prompt edits that don't change the output shape,
retry / logging / observability changes.

**Breaking changes ship as a new `schema_version`** (`v2`, `v3`, …):
removing a required field, renaming a public field, changing a field's
type, making an optional field required, semantic changes (e.g.,
`cost_usd` repurposed to mean something other than USD), changing the
error-response shape.

When `v2` ships:
- `/ask` and `/ask_batched` still return `v1` by default.
- A header `X-Schema-Version: v2` (or `?schema_version=v2`) opts the
  caller into the new shape.
- Both versions are supported in parallel for at least two weeks before
  `v1` is retired.
- The deprecation date is announced in the ADR before removal.

### Cost budget (added W4)

Capstone `/ask_batched` calls cost ≤ **$0.01 each** on average over a
representative batch of 10 questions. This is a soft budget — the
intent is to fail loud in observability if average cost suddenly
doubles, not to reject individual expensive calls.

The cohort confirms or refines this number against the actual results
of Lab Step 3 (`scripts/compare_models.py`).

### Chosen default model (added W4)

The default `Settings.model` is **`gpt-4o-mini`** for the lab. `gpt-4o`
is available via the same code path for harder questions or when the
mini model's confidence is low.

> Lab Step 4 — cohort fills in their own reasoning here, e.g.
> "I picked `gpt-4o-mini` because the comparison run showed it answers
> 8 of 10 questions correctly at $X total cost, which is well under


## Consequences

**Positive**
- Consumers can rely on `Answer.content`, `Answer.cost_usd`, and
  `Answer.retries` from W3 forwards.
- Internal refactors (W4 tool-calling, W6 retrieval, W13 tool-use,
  W19 agents) ship without consumer breakage.
- A clear bump policy means the cohort doesn't have to negotiate every
  schema change with downstream consumers.

**Negative**
- Supporting two `schema_version`s in parallel requires the API code
  to branch on the version header for at least two weeks per bump.
- The `cost_usd` budget assumes the cohort runs the comparison
  regularly enough to catch regressions.

## Notes

- JSON + Pydantic carries the cohort through the rest of the
  programme. Avro/Protobuf would enforce the same versioning
  discipline with more ceremony — not adopted for this cohort.
