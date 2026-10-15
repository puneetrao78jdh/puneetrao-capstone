# Prompt Pairwise Comparison 001

## Run Information

| Field | Value |
|---|---|
| Golden Set | `data/golden_set.jsonl` |
| Questions compared | 20 |
| Candidate model | `gpt-4o-mini` |
| Judge model | `gpt-4o` |
| Prompt v1 | `data/prompt-v1.txt` |
| Prompt v2 | `data/prompt-v2.txt` |
| Results | `data/pairwise-001-results.json` |

## What Changed

Prompt v1 gives the assistant a general instruction to answer clearly and concisely.

Prompt v2 adds one specific instruction:

> If the available information is not enough to answer a company-specific question, clearly say that the answer cannot be determined. Do not guess, invent a policy, or provide typical industry ranges.

No policy corpus was supplied to either prompt. This comparison tests whether an explicit refusal instruction reduces unsupported answers.

## Prompt v1

```text
You are an Enterprise Policy Assistant.

Answer the user's question clearly and concisely.
```

## Prompt v2

```text
You are an Enterprise Policy Assistant.

Answer the user's question clearly and concisely.

If the available information is not enough to answer a company-specific
question, clearly say that the answer cannot be determined. Do not guess,
invent a policy, or provide typical industry ranges.
```

## Aggregate Result

| Result | Count |
|---|---:|
| v1 wins | 4 |
| v2 wins | 6 |
| Ties | 3 |
| Ambiguous | 7 |
| Total | 20 |

The recorded order-dependence rate was 35%.

The pairwise judge evaluated every pair twice. In the second evaluation, the answer positions were reversed. Seven comparisons did not produce a consistent result.

## Findings

### V2 helped in some cases

V2 won six comparisons. The added refusal instruction made some answers more careful and reduced unsupported guessing.

For the salary-increase question, v1 suggested a typical percentage range. V2 avoided giving a percentage and advised checking the company policy or HR.

This is closer to the expected safe-refusal behaviour.

### V1 still won some comparisons

V1 won four comparisons. The refusal instruction did not provide the missing Matellio policy facts. For answerable questions, both prompts were still working without the corpus.

In some cases, v2 became cautious without becoming more accurate. A refusal prompt cannot replace retrieval.

### The result was not stable enough

Seven of the 20 comparisons were ambiguous. The judge did not choose the same underlying answer after the positions were reversed.

A 35% order-dependence rate is too high to treat the aggregate result as a clear v2 win.

This may reflect position sensitivity, close-quality answers, ties being handled differently, or normal judge instability. The result should therefore be interpreted carefully.

### Prompt quality is not the main problem

Both prompts lack the Matellio policy evidence. The main accuracy problem cannot be solved only by changing the wording of the system prompt.

The refusal instruction can reduce some hallucinations, but corpus retrieval is required to answer supported policy questions correctly.

## Decision

The result is inconclusive, so v2 will not be declared a clear overall winner.

The refusal instruction is useful for reducing unsupported salary and policy guesses, but it needs further testing. The next version should be tested after relevant policy context is supplied to the candidate model.

For the current milestone, the comparison is recorded as an iteration result:

- Keep the refusal principle.
- Do not claim that v2 improves overall policy-answer quality.
- Re-run the comparison after retrieval is implemented.
- Investigate the seven ambiguous cases before relying on the pairwise judge.

## Limitations

- The candidate did not receive the Matellio corpus.
- The two prompts were compared on answers generated in separate model calls.
- Seven comparisons were order-dependent.
- The pairwise judge used the ideal answer rather than the original policy text.
- A 20-question set provides an initial signal but is not enough for production conclusions.