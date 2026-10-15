# Eval Run 001 Manual Spot Check

## Run Summary

- Run label: `eval-run-001`
- Candidate model: `gpt-4o-mini`
- Judge model: `gpt-4o`
- Entries reviewed manually: 5 of 20
- Entries reviewed: `g001`, `g007`, `g015`, `g019`, `g020`

## g001: Casual Leave entitlement

The ideal answer says a confirmed employee receives 4 days of Casual Leave in one financial year.

The candidate did not give the Matellio policy answer. It gave a general range of 5 to 12 days based on different companies.

- Accuracy score: 1
- I agree with the accuracy score: Yes
- Groundedness score: 1
- I agree with the groundedness score: Yes
- Format score: 4
- I agree with the format score: Mostly

The answer is readable, but it does not directly answer the Matellio policy question. A format score of 3 may be more suitable because it is clear but not useful for this question.

## g007: Permanent storage in OneDrive

The ideal answer says final project documents must not be stored permanently in OneDrive. They must be moved to the designated SharePoint Team Site.

The candidate gave the opposite answer and said permanent OneDrive storage is allowed.

- Accuracy score: 1
- I agree with the accuracy score: Yes
- Groundedness score: 1
- I agree with the groundedness score: Yes
- Format score: 4
- I agree with the format score: Yes

The answer is clearly written, but the policy information is incorrect. This shows that good format does not mean the answer is trustworthy.

## g015: Probation and leave eligibility

The ideal answer says the probation period is 3 months. During probation, the employee may use 2 Casual Leaves and 2 Sick Leaves. Earned Leave accumulates but cannot be used, and Occasional Leave is unavailable.

The candidate gave a probation range of three to six months. It did not give the correct Casual Leave and Sick Leave numbers and incorrectly suggested that Occasional Leave may be permitted.

- Accuracy score: 1
- I agree with the accuracy score: Yes
- Groundedness score: 1
- I agree with the groundedness score: Yes
- Format score: 2
- I agree with the format score: Yes

The answer is incomplete and uncertain. It does not give the clear policy conditions required by the question.

## g019: Annual budget

The ideal answer says the selected policy corpus does not contain information about the annual employee-benefits or IT-security budget.

The candidate correctly avoided inventing budget figures. However, it claimed that the information is proprietary and not publicly available. The selected corpus does not prove either claim.

- Accuracy score: 4
- I agree with the accuracy score: Partly
- Groundedness score: 4
- I agree with the groundedness score: No
- Format score: 4
- I agree with the format score: Yes

A more suitable accuracy score may be 3 because the candidate reached the correct practical conclusion but gave a different and unsupported reason.

A more suitable groundedness score may be 2 or 3 because “proprietary” and “not publicly available” are not supported by the ideal answer.

This is a judge disagreement. The judge treated “not available in the corpus” and “not publicly available” as the same claim, but they have different meanings.

## g020: Salary increase after probation

The ideal answer says the corpus does not specify any salary increase after probation and advises the employee to contact HR.

The candidate invented a possible range of 3% to 10%. That range is not supported by the selected documents.

- Accuracy score: 1
- I agree with the accuracy score: Yes
- Groundedness score: 1
- I agree with the groundedness score: Yes
- Format score: 4
- I agree with the format score: Yes

The response is readable, but it fails the safe-refusal test because it gives unsupported compensation figures.

## Overall Finding

The answers are generally readable, which explains the average format score of 3.45 out of 4. However, they are mostly incorrect or unsupported because the current application does not provide the Matellio policy corpus to the candidate model.

The candidate answered using general knowledge and common company practices. This caused direct policy errors, such as allowing permanent OneDrive storage, and unsupported claims, such as suggesting a salary increase of 3% to 10%.

The edge cases show mixed behaviour. The candidate avoided inventing a budget figure for `g019`, but added an unsupported explanation. For `g020`, it failed to refuse and invented a salary-increase range.

## Judge Disagreements

The main disagreement is `g019`. The judge gave accuracy and groundedness scores of 4, but the candidate’s claims that the information is proprietary and not publicly available are not supported by the ideal answer.

There is also a smaller concern about the format score for `g001`. The response is readable, but it does not directly answer the company-specific question.

The manual review shows why judge reasoning must be checked instead of accepting every score automatically.