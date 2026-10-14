# Golden Set Notes

## Purpose

This document explains how the Golden Set for the Matellio Employee Policy & Support Enterprise Knowledge Assistant was prepared.

The Golden Set contains 20 questions based on the selected corpus of 18 policy documents across three areas:

- Leave & HR Policies
- Workplace Policies
- IT Security Policies

The Golden Set will be used to measure answer quality during Week 5 and later stages of the capstone.

---

## Coverage Mix

The Week 5 Golden Set uses the required 14/4/2 distribution.

| Category | Count | Purpose |
|---|---:|---|
| Happy-path | 14 | Test direct policy questions with answers available in one main document or policy section |
| Harder | 4 | Test questions that require combining rules from multiple documents or sections |
| Edge | 2 | Test whether the assistant refuses when the corpus does not contain the answer |
| **Total** | **20** | |

---

## Policy Coverage

The questions cover all three main policy areas.

### Leave & HR Policies

The questions cover:

- Casual Leave
- Sick Leave
- Earned Leave
- Leave during probation
- Leave rules for Professionals
- Leave rules for Contractors
- Maternity Leave
- Paternity Leave
- Compensatory Off
- Leave during the notice period

### Workplace Policies

The questions cover:

- Probation and confirmation
- Office working hours
- Hybrid working
- Permanent remote working
- Separation and notice-period rules
- Loss of a company-issued laptop

### IT Security Policies

The questions cover:

- Password changes
- OneDrive storage
- SharePoint storage
- Anonymous sharing links
- Personal devices
- Confidential information
- Company VPN usage
- Incident reporting and access revocation

---

## Question Sources

The first draft of the Golden Set was prepared in the earlier W5 capstone folder as an 8 easy, 8 medium and 4 hard question set.

For the current Week 5 lab, that draft was adapted to the required structure:

- 14 happy-path questions
- 4 harder questions
- 2 edge questions

Most questions were adapted from the earlier `data/golden_set_full.jsonl` and `docs/golden-set-coverage.md` files.

Some combined questions were separated into simpler questions. For example, the earlier comparison of Earned Leave rules for regular employees and Professionals was separated into two happy-path questions.

The second edge question about salary increase after probation was added to test whether the assistant avoids inventing compensation information that is not present in the selected corpus.

AI assistance was used to organise the questions, simplify wording, and convert the entries to the required JSONL structure. The policy documents remain the source of truth.

---

## Reference-Answer Verification

The reference answers must be verified against the original policy documents before the first evaluation run.

The verification process is:

1. Open the source document listed in the entry’s `notes`.
2. Find the relevant policy section.
3. Compare every fact, number, condition and exception with the ideal answer.
4. Correct the ideal answer if it includes unsupported information.
5. Confirm that the `must_mention` facts are supported by the source.
6. For harder questions, verify every source document listed.
7. For edge questions, confirm that the requested information is absent from the complete selected corpus.

The current JSON structure and category counts have been prepared, but a valid file structure does not prove that every reference answer is correct.

Final source verification status: **Complete. All 20 entries were checked against the full 18-document corpus. Entries g002 and g004 were reworded to remove wording not stated directly in the source policies. Entry g018 was expanded to include all required reporting contacts. The two edge questions were checked across the complete corpus, and the requested budget and post-probation salary-increase information was not found.**

---

## Hardest Questions to Prepare

The harder questions were the most difficult because their answers require information from several documents.

For example, the notice-period question combines separation rules, leave eligibility and Compensatory Off rules. The lost-laptop question combines remote-working responsibilities, confidential-data requirements and incident-response actions.

These answers must be checked carefully because one correct fact does not make the complete answer correct.

The edge questions also require care. It is difficult to prove that information is absent because the complete corpus must be checked. The correct answer should explain the limitation without inventing figures, benefits or company decisions.

---

## Known Limitations

The Golden Set currently has these limitations:

- The questions were not taken from actual production query logs.
- The questions were prepared from the policy corpus and earlier capstone work.
- The primary user and sponsor still need final confirmation.
- Some policies may contain overlapping or conflicting rules.
- The reference answers require final manual verification.
- The Golden Set has only 20 questions, which is enough for an initial baseline but not a complete production evaluation.
- The current application has not yet been connected to the 18-document corpus.

The Golden Set should grow when real user questions and evaluation failures become available.

---

## Final Files

The original question draft is retained in:

```text
data/golden_set_full.jsonl
```

The Week 5 evaluation set is maintained in:

```text
data/golden_set.jsonl
```

The required category mix is:

```text
14 happy-path + 4 harder + 2 edge = 20 questions
```
