# Evaluation Run 001

## Run Information

| Field | Value |
|---|---|
| Run label | `eval-run-001` |
| Golden Set | `data/golden_set.jsonl` |
| Questions | 20 |
| Candidate model | `gpt-4o-mini` |
| Judge model | `gpt-4o` |
| Candidate endpoint | `/ask_batched` |
| Evaluation type | Pre-RAG baseline |
| Result storage | `data/answers.db`, `eval_runs` table |

## Purpose

This run establishes the first quality baseline for the Matellio Employee Policy & Support Enterprise Knowledge Assistant.

The current application does not retrieve or provide the 18 Matellio policy documents to the candidate model. The candidate receives only the user question. This run therefore measures the behaviour of the model before corpus retrieval is added.

The same Golden Set can be run again after retrieval is implemented so that the change in quality can be measured.

## Aggregate Results

| Dimension | Average score |
|---|---:|
| Accuracy | 1.45 / 4 |
| Groundedness | 1.50 / 4 |
| Format | 3.45 / 4 |

- Questions with accuracy 3 or 4: 2 out of 20
- Questions with groundedness 3 or 4: 2 out of 20
- Questions with format 3 or 4: 18 out of 20

## Interpretation

The average accuracy and groundedness scores are low because the candidate model does not receive the Matellio policy documents.

The model answers using general knowledge and common company practices. This leads to answers that sound reasonable but do not match the selected policy corpus.

The format score is much higher. This shows that the model can produce clear and readable answers even when the policy facts are incorrect or unsupported.

A clear answer should therefore not be treated as a trustworthy answer without checking its evidence.

## Per-Entry Results

|  ID  | Accuracy | Groundedness | Format |
|------|----------|--------------|--------|
| g001 |        1 |            1 |      4 |
| g002 |        1 |            1 |      3 |
| g003 |        2 |            2 |      4 |
| g004 |        1 |            1 |      2 |
| g005 |        2 |            2 |      4 |
| g006 |        1 |            1 |      3 |
| g007 |        1 |            1 |      4 |
| g008 |        2 |            2 |      4 |
| g009 |        1 |            1 |      4 |
| g010 |        1 |            1 |      3 |
| g011 |        1 |            1 |      4 |
| g012 |        1 |            1 |      4 |
| g013 |        1 |            1 |      4 |
| g014 |        1 |            2 |      3 |
| g015 |        1 |            1 |      2 |
| g016 |        2 |            2 |      3 |
| g017 |        1 |            1 |      3 |
| g018 |        3 |            3 |      3 |
| g019 |        4 |            4 |      4 |
| g020 |        1 |            1 |      4 |

## Manual Spot Check

Five results were manually reviewed:

- `g001`: Casual Leave entitlement
- `g007`: Permanent OneDrive storage
- `g015`: Probation and leave eligibility
- `g019`: Annual budget edge case
- `g020`: Salary increase after probation

The full manual review is recorded in:

```text
docs/eval-spot-check-001.md
```

## Main Findings

### 1. Direct policy questions failed

For `g001`, the candidate did not provide the Matellio entitlement of 4 Casual Leaves. It gave a general range based on common company policies.

For `g007`, the candidate gave the opposite of the policy. It said final documents could remain permanently in OneDrive, while the policy requires them to be moved to SharePoint.

These failures show that the candidate cannot answer company-specific questions without receiving the policy evidence.

### 2. Harder questions exposed more gaps

For `g015`, the candidate did not provide the exact probation and leave rules. It gave an uncertain probation range and incorrectly suggested that Occasional Leave may be available.

Questions requiring several policy conditions are especially difficult without retrieval.

### 3. Edge-case behaviour was inconsistent

For `g019`, the candidate avoided inventing budget figures, but it claimed that the information was proprietary and not publicly available. Those claims are not supported by the selected corpus.

For `g020`, the candidate failed to refuse and invented a possible salary increase of 3% to 10%.

The assistant therefore does not yet refuse reliably when company-specific information is unavailable.

### 4. Good format did not mean good quality

The average format score was 3.45 out of 4, while accuracy was only 1.45.

The answers were generally readable and confident. However, many were factually wrong or unsupported. This is a risk because users may trust an answer based on how professional it sounds.

## Judge Disagreement

The main disagreement was `g019`.

The judge awarded accuracy and groundedness scores of 4 because the candidate said the budget information was not publicly available.

The ideal answer only says that the information is not present in the selected corpus. It does not establish that the information is proprietary or unavailable publicly.

A more suitable result may be:

- Accuracy: 3
- Groundedness: 2 or 3
- Format: 4

This disagreement shows why LLM judge results require manual checking.

There was also a smaller concern about the format score for `g001`. The answer was readable but did not directly answer the company-specific question.

## Changes Before DR #1

### 1. Verify the Golden Set

Check all 20 ideal answers against the original policy documents. Correct unsupported facts, conditions, source names and required phrases before using the Golden Set as a long-term baseline.

### 2. Tighten the judge rubric

Clarify that “not present in the supplied corpus” is different from “proprietary” or “not publicly available.”

Also clarify whether format should measure presentation only or whether an answer that avoids the question must receive a lower format score.

### 3. Record the pre-RAG limitation clearly

Present this run as a pre-RAG baseline. Do not claim that the current assistant provides policy-grounded answers or verified citations.

Corpus retrieval and evidence-based answering remain future implementation work.

## Conclusion

Evaluation Run 001 successfully processed and saved all 20 Golden Set entries.

The baseline shows that `gpt-4o-mini` can produce readable answers, but it cannot reliably answer private Matellio policy questions without receiving the relevant documents.

This result provides a useful starting point for measuring improvements after retrieval is added.