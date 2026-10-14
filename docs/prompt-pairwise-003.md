# Prompt Pairwise Comparison 003

## Run Information

- Golden set: `data/golden_set.jsonl`
- Prompt v1: `data/prompt-v1.txt`
- Prompt v2: `data/prompt-v2.txt`
- Results: `data/pairwise-003-results.json`
- Judge model: `gpt-4o`
- Questions compared: 20

## What Changed

Prompt v1 asks the assistant to answer clearly and concisely.

Prompt v2 adds one rule: if the available information is insufficient for a company-specific question, the assistant must say that the answer cannot be determined and must not guess, invent a policy or provide typical industry ranges.

## Aggregate Result

| Result | Count |
|---|---:|
| v1 wins | 1 |
| v2 wins | 9 |
| Ties | 3 |
| Ambiguous | 7 |

The order-dependence rate was 35%.

## Findings

### V2 reduced some invented information

V2 performed better when v1 invented specific company figures.

For `g001`, v1 invented a Casual Leave range of 7 to 15 days. V2 avoided giving a number.

For `g011`, v1 invented an Earned Leave carry-forward limit of 30 days. V2 said that the number depended on the company policy.

For `g020`, v1 invented a salary increase range of 0% to 10%. V2 correctly said that the percentage could not be determined from the available information.

### V2 did not always follow its refusal rule

For `g002`, v2 still mentioned a typical entitlement of two weeks or 10 working days even though the prompt instructed it not to provide typical industry ranges. The pairwise judge still selected v2 because v1 gave an incorrect fixed answer.

This shows that a prompt instruction can reduce guessing but cannot guarantee safe behaviour.

### V2 also refused answerable questions

For questions such as `g005`, the correct answer exists in the Matellio policy corpus. V2 refused because the API did not provide that corpus to the model.

For `g015`, v2 correctly gave a three-month probation period but still incorrectly said that Casual Leave might not be available. It won because it was closer to the ideal answer than v1, not because it was fully correct.

### V1 win

V1 won only `g017`. However, its answer was still incorrect because it suggested that Compensatory Off might be encashed or carried forward. The judge selected it because it was closer to the ideal answer than v2.

Therefore, a pairwise win does not mean that an answer is correct. It only means that the judge considered it better than the other answer.

### Order dependence

Seven comparisons were ambiguous because the judge changed its decision after the answer positions were reversed.

The ambiguous entries were:

- `g003`
- `g007`
- `g008`
- `g012`
- `g014`
- `g016`
- `g018`

A 35% order-dependence rate is too high to treat the result as a reliable v2 victory.

## Decision

Keep the refusal principle from v2 because it reduced several unsupported figures. Do not treat v2 as the final production prompt because it still invented information, refused answerable questions and produced an inconclusive pairwise result.

Run the comparison again after retrieval is implemented and the candidate model receives trusted policy context. The pairwise judge rubric should also be improved so that it does not treat a less incorrect answer as fully correct.

## Limitations

- The candidate model did not receive the Matellio policy corpus.
- Seven comparisons were order-dependent.
- Some winning answers were still factually incorrect.
- Prompt instructions alone could not guarantee refusal behaviour.
- The result represents a pre-RAG system and not the final assistant.