# DR #1 Summary: Matellio Employee Policy Assistant

## What I Am Building

I am building an Enterprise Knowledge Assistant for Matellio employees who need help understanding company policies.

The selected corpus contains 18 documents across three areas: Leave & HR, Workplace and Employee Lifecycle, and IT Security and Collaboration.

The planned assistant will answer questions using only these documents, provide citations, and clearly refuse when the corpus does not contain enough information. It will not approve requests, change policies, or make HR, IT, or management decisions.

The current application provides `/health`, streaming `/ask`, and structured `/ask_batched` endpoints. It uses `gpt-4o-mini` as the candidate model and stores answers and evaluation results in SQLite. All 31 existing tests pass.

The policy corpus has been selected, but retrieval has not yet been implemented. The current application sends only the user question to the model.

## What I Measured

I prepared a 20-question Golden Set containing:

- 14 happy-path questions
- 4 harder questions
- 2 edge questions

The final verified pre-RAG evaluation, `eval-run-003`, used `gpt-4o-mini` as the candidate and `gpt-4o` as the judge.

| Dimension | Average | Questions scoring 3 or 4 |
|---|---:|---:|
| Accuracy | 1.50 / 4 | 2 of 20 |
| Groundedness | 1.55 / 4 | 3 of 20 |
| Format | 3.40 / 4 | 18 of 20 |

The answers were generally clear but mostly incorrect or unsupported. The model used general knowledge because it did not receive the Matellio policies. This is my pre-RAG baseline.

I also compared two prompts. V2 added a rule telling the model not to guess when company information was unavailable. V2 won 9 questions, v1 won 1, 3 were ties, and 7 were ambiguous. The 35% order-dependence rate means I cannot claim that v2 is a clear winner.

The Critic-Creator exercise improved one difficult answer from 1.67 to 4.00 over three rounds. This worked because the critic had access to the ideal answer, so it is evidence of the improvement pattern rather than production readiness.

## Three Topics I Want to Discuss

1. What retrieval and chunking approach should I use for 18 Word policy documents containing overlapping rules?

2. How should the assistant identify whether a question concerns a regular employee, Professional, or Contractor?

3. How should I handle conflicting policy sections and produce citations that users can verify easily?

## What I Will Defend If Asked

**Why use `gpt-4o-mini`?**  
It is inexpensive enough for repeated candidate calls. A stronger `gpt-4o` model is used as the judge.

**Why use 20 Golden Set questions?**  
Twenty is a small but useful starting baseline. It covers normal, harder and refusal cases and can grow using real user questions.

**Why are the baseline scores low?**  
The model does not receive the private policy corpus. The low scores correctly show the need for retrieval. I will run the same Golden Set after RAG is implemented and compare the results.