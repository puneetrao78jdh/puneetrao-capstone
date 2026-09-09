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