# ADR 0001: Matellio Employee Policy Assistant

- **Status:** v1 — Ready for DR #1
- **Updated:** 2026-10-14
- **Author:** Puneet Rao

## Context

Matellio maintains a growing collection of internal Human Resources (HR), Workplace Conduct, and IT Security policy documents that employees refer to throughout their employment lifecycle. The selected corpus for this Enterprise Knowledge Assistant (EKA) contains **18 internal policy documents**, organised into **three policy clusters**:

1. Leave & HR Policies
2. Workplace & Employee Lifecycle Policies
3. IT Security & Collaboration Policies

Employees, professionals, contractors, managers, HR support staff, and IT support staff frequently need answers to policy-related questions. Currently, answering these questions requires manually locating and interpreting information across multiple policy documents, which can be time-consuming and may lead to inconsistent interpretation.

This project proposes an Enterprise Knowledge Assistant (EKA) that enables users to ask natural-language questions and receive answers grounded only in the approved policy corpus, together with citations to the relevant source documents.

---

## Decision

The decision is to build a **Matellio Employee Policy & Support Enterprise Knowledge Assistant (EKA)**.

The EKA will answer questions using an internal corpus consisting of the following policy clusters:

### 1. Leave & HR Policies
- Leave Policy
- Leave Policy for Professionals
- Leave Policy for Contractors
- Maternity Policy
- Paternity Policy
- Compensatory Off Policy

### 2. Workplace & Employee Lifecycle Policies
- Probation & Confirmation Policy
- Separation Policy
- Diversity, Equity & Inclusion Policy
- Workforce Management – Office
- Workforce Management – Hybrid
- Workforce Management – Remote

### 3. IT Security & Collaboration Policies
- Data Retention Policy
- Data Security & Access Control Policy
- OneDrive Usage Policy
- SharePoint Usage Policy
- Password Management Policy
- Backup & Offsite Storage Policy

The EKA will:

- Answer questions only from the approved policy corpus.
- Provide citations to the source documents used to generate the answer.
- Clearly refuse to answer when sufficient evidence is not available in the corpus.
- Not generate or modify company policies.
- Not make HR, IT, or management decisions on behalf of the organisation.

---

## Stakeholders

The primary stakeholders are:

- Employees seeking clarification on company policies.
- Professionals and contractors requiring role-specific policy guidance.
- Managers interpreting HR and workplace policies for their teams.
- HR Support Team responding to employee policy-related queries.
- IT Support Team responding to IT policy and security-related questions.

The expected outcome is faster and more consistent access to policy information while reducing manual effort required by HR and IT support teams.

---

## KPI Targets

### KPI 1 – Answer Quality

**Target**

Correctly answer or safely refuse at least **16 out of 20** Golden Set questions.

**Reason**

The Golden Set contains answerable as well as intentionally unanswerable questions. The system should answer supported questions accurately while refusing questions that cannot be answered from the available corpus.

---

### KPI 2 – Citation Coverage

**Target**

**100%** of non-refusal answers must include at least one citation to a document within the selected corpus.

**Reason**

Employees should be able to verify every policy answer against its original source document, increasing transparency and trust.

---

### KPI 3 – Response Time

**Target**

Return an answer or safe refusal within **30 seconds** during demonstration and evaluation.

**Reason**

The objective is to reduce the effort required to locate information across multiple policy documents while maintaining trustworthy responses.

---

## Alternatives Considered

### Alternative 1 – HR Policy EKA Only

This alternative limited the EKA to HR policies such as leave, maternity, paternity, probation, separation, and employee benefits.

**Reason Rejected**

Although simpler to implement, many employee questions extend beyond HR and require IT policy guidance, such as password management, SharePoint usage, OneDrive usage, or data security. Restricting the scope to HR alone would reduce the usefulness of the assistant and limit opportunities to evaluate cross-domain retrieval.

---

### Alternative 2 – IT Security Policy EKA Only

This alternative focused only on IT security and collaboration policies such as password management, data security, SharePoint, OneDrive, backup, and data retention.

**Reason Rejected**

This scope would primarily benefit IT support users while excluding many common employee policy questions related to leave, workplace conduct, probation, separation, and employment lifecycle. The resulting assistant would therefore have a narrower organisational impact.

---

### Alternative 3 – Complete Enterprise Policy Repository

This alternative considered including every available HR and IT policy document within the organisation.

**Reason Rejected**

Although this approach would maximise coverage, it would significantly increase corpus size and evaluation complexity during the capstone. A carefully selected corpus of **18 documents** across three policy clusters provides sufficient coverage while remaining manageable for implementation, retrieval, evaluation, and demonstration.

## Current Implementation

The existing application provides:

- `GET /health`
- Streaming `POST /ask`
- JSON `POST /ask_batched`
- Structured answers with content, cost, retries, confidence, sources and schema version
- SQLite storage in `data/answers.db`
- An `eval_runs` table for evaluation results
- Optional system prompts for prompt comparison

The default candidate model is `gpt-4o-mini`. The W5 judge model is `gpt-4o`.

All 31 existing tests pass. One successful `/ask_batched` request cost approximately $0.0000612 and required no retries.

The 18 policy documents are stored in `data/corpus`. The current application does not yet retrieve or send these documents to the candidate model. Corpus-based answering and verified policy citations remain future work.

## Golden Set

The Week 5 Golden Set is stored in:

```text
data/golden_set.jsonl
```

It contains:

- 14 happy-path questions
- 4 harder questions
- 2 edge questions
- 20 questions in total

The questions cover Leave & HR, Workplace, and IT Security policies.

The original 8 easy, 8 medium and 4 hard draft is retained in `data/golden_set_full.jsonl`.

## Evaluation Baseline

Evaluation Run 003 used:

- Candidate model: `gpt-4o-mini`
- Judge model: `gpt-4o`
- Questions: 20
- Run label: `eval-run-003`

| Dimension | Average | Questions scoring 3 or 4 |
|---|---:|---:|
| Accuracy | 1.50 / 4 | 2 of 20 |
| Groundedness | 1.55 / 4 | 3 of 20 |
| Format | 3.40 / 4 | 18 of 20 |

The answers were generally readable but mostly incorrect or unsupported. This happened because the candidate model did not receive the Matellio policy documents.

The manual spot-check found one major judge disagreement. For `g019`, the judge treated the assistant’s lack of access to internal financial data as fully equivalent to the information being absent from the selected corpus. The practical refusal was correct, but some supporting claims were not established by the corpus.

This run is recorded as the final verified pre-RAG baseline for M1.

## KPI Status at M1

### KPI 1: Answer Quality

**Target:** Correctly answer or safely refuse at least 16 of 20 questions.

**Current measurement:** Only 2 of 20 answers received an accuracy score of 3 or 4 in the pre-RAG evaluation.

The target has not been achieved.

### KPI 2: Citation Coverage

**Target:** Every non-refusal answer includes a verified corpus citation.

**Current measurement:** No verified corpus citation coverage is available because the policy corpus is not connected to answer generation.

The target has not been achieved.

### KPI 3: Response Time

**Target:** Return every answer or refusal within 30 seconds.

**Current measurement:** The evaluation script did not record elapsed time for each request, so this KPI has not yet been measured.

## Prompt Comparison

Prompt v2 added one instruction asking the model not to guess or provide typical industry ranges when company information was unavailable.

Pairwise Comparison 003 produced:

| Result | Count |
|---|---:|
| v1 wins | 1 |
| v2 wins | 9 |
| Ties | 3 |
| Ambiguous | 7 |

The order-dependence rate was 35%.

The result is inconclusive because seven comparisons changed after the answer positions were reversed. V2 reduced some unsupported figures, especially for the salary-increase edge question. However, it also refused questions that could have been answered from the policy corpus, and it did not always follow its own refusal instruction.

The refusal principle will be retained, but v2 is not treated as the final production prompt. The comparison should be repeated after retrieval is implemented.

## Critic-Creator Result

The Critic-Creator loop was run on `g015`.

| Round | Mean score |
|---|---:|
| Round 1 | 1.67 / 4 |
| Round 2 | 3.33 / 4 |
| Round 3 | 4.00 / 4 |

The critic corrected the probation period, exact leave entitlements and Earned Leave accumulation rule.

This result demonstrates the improvement pattern, but it does not prove production readiness. The critic had access to the verified ideal answer, which would not normally be available for a live user question.

## Scope Boundaries

The assistant will use the selected 18-document Matellio corpus.

The current scope does not include:

- Arbitrary user-uploaded documents
- Persistent conversation memory
- Approval or rejection of employee requests
- Changes to HR or IT policies
- Actions on behalf of employees, managers, HR or IT
- Answers unsupported by the selected corpus

## Open Questions Before DR #1

- Who is the confirmed sponsor and final approver?
- How should the policy documents be chunked and retrieved?
- How should conflicting policy sections be handled?
- How should employee, Professional and Contractor categories be identified?
- What citation format should be returned to users?
- How should response time be captured in future evaluation runs?

## DR #1 Defence Notes

To be completed during or immediately after DR #1.

| Reviewer question | Decision or response |
|---|---|
| | |
| | |
| | |

## Change Log

- **2026-08-17:** Initial framing used public GitLab Handbook policies.
- **2026-10-10:** Changed the scope to 18 Matellio HR, Workplace and IT Security policy documents.
- **2026-10-13:** Added the 20-question Golden Set, pre-RAG evaluation baseline, prompt comparison and Critic-Creator result.
- **2026-10-14:** Verified all Golden Set answers against the 18-document corpus, recorded `eval-run-003`, and completed Pairwise Comparison 003.
- **DR #1:** Pending. Record review decisions and final lock here.