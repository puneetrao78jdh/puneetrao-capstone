# Prompt Pairwise Comparison 002

## Run Information

- Golden set: `data/golden_set.jsonl`
- Prompt v1: `data/prompt-v1.txt`
- Prompt v2: `data/prompt-v2.txt`
- Results: `data/pairwise-002-results.json`
- Judge model: `gpt-4o`
- Questions compared: 20

## What Changed

Prompt v1 asks the assistant to answer clearly and concisely.

Prompt v2 adds one specific rule: if the available information is insufficient for a company-specific question, the assistant must say that the answer cannot be determined and must not guess, invent a policy or provide typical industry ranges.

Only this refusal behaviour was intentionally changed.

## Aggregate Result

| Result | Count |
|---|---:|
| v1 wins | 3 |
| v2 wins | 9 |
| Ties | 0 |
| Ambiguous | 8 |

The recorded order-dependence rate was 40%.

## Findings

### V2 reduced invented information

V2 performed better when v1 invented specific figures.

For `g001`, v1 incorrectly stated that employees typically receive 12 Casual Leaves. V2 avoided inventing a number.

For `g011`, v1 invented a carry-forward limit of 30 Earned Leave days. V2 said that the answer required the company policy.

For `g020`, v1 invented a salary increase range of 3% to 10%. V2 correctly stated that the percentage could not be determined from the available information.

These cases show that the refusal instruction can reduce unsupported company-specific claims.

### V1 sometimes won by giving a closer answer

V1 won `g003`, `g005` and `g018`.

For `g005`, v1 correctly gave a three-month probation period, while v2 refused to provide the answer.

For `g018`, v1 mentioned the IT Department, remote wiping and possible cost recovery in case of negligence. This was closer to the ideal answer.

These wins do not prove that v1 is generally better. Some correct details came from the model’s general knowledge rather than from retrieved policy documents.

### The result was unstable

Eight of the 20 comparisons were ambiguous because the judge did not select the same underlying answer after the answer positions were reversed.

The ambiguous entries were `g006`, `g007`, `g008`, `g010`, `g013`, `g014`, `g017` and `g019`.

For example, in `g019`, one comparison preferred v1 while the reversed comparison called the answers a tie. Both answers refused to provide the budget, but each added assumptions that were not supported by the corpus.

The 40% order-dependence rate is too high to treat the aggregate result as a reliable v2 victory.

### Prompt changes cannot replace retrieval

V2 was safer when information was unavailable, but it also refused questions that had answers in the policy documents. The current API does not provide the Matellio corpus to the candidate model. Therefore, neither prompt can consistently produce accurate policy answers.

## Decision

Keep the refusal principle introduced in v2 because it reduces invented company-specific figures. Do not declare v2 as the final prompt based on this run because eight comparisons were order-dependent and both prompts lacked access to the policy corpus.

After retrieval is implemented, run the pairwise comparison again using retrieved policy context. Also review the pairwise judge instructions because some judge explanations incorrectly treated refusal as fully aligned with ideal answers that contained specific policy facts.

## Limitations

- The candidate model did not receive the Matellio policy corpus.
- Eight comparisons were order-dependent.
- Some answers were selected because they were less incorrect, even though neither answer matched the ideal answer.
- The result measures prompt behaviour before retrieval and does not measure the final RAG system.