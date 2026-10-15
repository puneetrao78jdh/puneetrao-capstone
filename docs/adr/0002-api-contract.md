# ADR 0002: API Contract

- **Status:** W4 contract retained; W5 scope updated
- **Updated:** 2026-10-10
- **Author:** Puneet Rao

## Context

The Matellio Employee Policy & Support Assistant will answer questions using
18 HR, workplace, and IT policy documents. We keep the working API contract
while adding corpus-based answering and evaluation behind it.

The prepared W5 folder described a single JSON `/ask` endpoint, but its API
returns a dummy answer. That contract does not replace the working application.

## Current endpoints

| Method and path | Current response |
|---|---|
| `GET /health` | HTTP 200 with `{"status": "ok"}` |
| `POST /ask` | Streaming `text/plain` answer |
| `POST /ask_batched` | JSON `Answer` with the six fields below |

`/health` confirms the endpoint is running. It does not check model access,
database readiness, or answer quality. `/ask_batched` accepts one question,
returns the complete answer, and saves it to the configured SQLite database.
The current `/ask` path streams text without saving an answer row.

## Request

Both question endpoints accept:

```json
{
  "question": "How many Casual Leaves is a confirmed employee entitled to?"
}
```

The `question` field is required and must be a string of at least one character.
Missing or invalid requests are rejected with HTTP 422. Whitespace-only text
is not explicitly rejected by the current model.

There is no implemented request field for a system-prompt override, uploaded
file, conversation history, or schema-version selection. Pairwise evaluation
must explicitly arrange for each prompt to reach the generation code.

## JSON response from `/ask_batched`

| Field | Type | Meaning |
|---|---|---|
| `content` | string | Generated answer |
| `cost_usd` | number | Calculated model-call cost in USD, based on token usage and configured rates |
| `retries` | integer | Retry count reported by the pipeline |
| `confidence` | number, 0 to 1 | Model-reported confidence; not a verified probability of correctness |
| `sources` | list of strings | Source identifiers returned by the pipeline |
| `schema_version` | string | Current response version, `v1` |

The streaming `/ask` response does not contain this JSON envelope.
Sources are not yet verified corpus citations: the generation code currently
receives the question without the Matellio policy documents. Grounding and
citation checks are planned work, not guarantees of the current API.

## Persistence and model settings

The API reads `Settings.results_db`, now defaulting to `data/answers.db`.
An environment setting can override this path. The model-comparison script
also defaults to `data/answers.db`. Keep these aligned with the W4 store schema;
the older `results.db` has a different table layout.

The default candidate model is `gpt-4o-mini`. Other supported models can be
selected through configuration. Automatic switching to `gpt-4o` based on
confidence is not implemented.

## Cost budget

Retain the W4 soft target: average `/ask_batched` cost of no more than $0.01
across a representative batch of 10 questions. This is a measurement target,
not an enforced per-request limit. W5 judge costs are separate from candidate
answer costs and should be reported separately.

## Schema versioning

Keep `v1` for compatible additions, including optional fields with defaults,
and internal model or retrieval changes that preserve the response contract.
Removing or renaming fields, changing their types or meaning, or requiring a
previously optional field requires a new version and a documented migration.

The earlier ADR proposed version negotiation through `X-Schema-Version` or a
query parameter and a minimum two-week overlap. Preserve this as a future
migration policy; negotiation and parallel versions are not implemented today.
Do not describe the plain-text `/ask` stream as a versioned JSON response.

## Validation and limitations

The user reported a successful `/ask_batched` request and 31 passing tests on
2026-10-10. These checks do not establish policy accuracy or full failure coverage.
Unexpected model or database errors may currently surface as HTTP 500.
The API has no documented custom error envelope in this implementation.

## Alternatives and consequences

Retain REST rather than introduce GraphQL: the current question-answer interface
is small. Keep model selection within configuration rather than add separate
cheap and quality endpoints. Preserve both streaming and complete-response
endpoints so existing clients keep working. Streaming requires separate error
handling, and future breaking changes will need explicit migration work.

## Change log

- 2026-09-09: Initial API ADR for the GitLab policy assistant.
- W4: Added confidence, sources, schema versioning, model choice, and cost budget.
- 2026-10-10: Updated scope to Matellio. Documented the actual three endpoints,
  six-field JSON response, database alignment, and unimplemented features.
