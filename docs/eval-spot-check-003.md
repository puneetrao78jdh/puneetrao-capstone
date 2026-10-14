# Eval Run 002 Manual Spot Check

## Run Summary

- Run label: `eval-run-003`
- Entries checked: `g001`, `g007`, `g015`, `g019`, `g020`
- Candidate model: `gpt-4o-mini`
- Judge model: `gpt-4o`

## g001

The candidate stated that employees typically receive 10 to 15 Casual Leaves. The Matellio policy states 4 days. I agree with the accuracy and groundedness scores of 1. The format score of 4 is reasonable because the answer is clearly written.

## g007

The candidate said final project documents can remain permanently in OneDrive. The policy requires finalised project documents to be moved to SharePoint. I agree with the accuracy and groundedness scores of 1 and the format score of 4.

## g015

The candidate gave a six-month probation period and did not correctly identify the leave available during probation. The policy states three months for an employee with more than two years of experience, with 2 Casual Leaves and 2 Sick Leaves available. I agree with the scores of 1 for accuracy, 1 for groundedness and 3 for format.

## g019

The candidate correctly refused to provide budget figures. However, it described the information as proprietary and suggested that it may exist in financial reports. These claims are not established by the selected corpus. I agree with the practical conclusion, but a groundedness score of 2 or 3 would be more suitable than 4.

## g020

The candidate invented a salary-increase range of 5% to 15%. The corpus provides no salary-increase percentage after probation. I agree with the accuracy and groundedness scores of 1. The format score of 4 is reasonable because the answer is clearly written.

## Overall Finding

The manual check supports the low average accuracy and groundedness scores. The candidate answers are generally readable, but they rely on general knowledge because the current application does not provide the Matellio policy corpus. The main judge disagreement is `g019`, where the refusal was correct but its explanation included unsupported assumptions.