# Golden Set Coverage Matrix

## Purpose

This document is used to plan and validate the evaluation dataset (Golden Set) for the Enterprise Knowledge Assistant (EKA).

The objective is to ensure that:

- Every major policy cluster is represented.
- Every important policy document contributes to evaluation.
- The Golden Set contains a balanced distribution of Easy, Medium, and Hard questions.
- Questions remain deterministic and objectively verifiable.
- Hard questions evaluate multi-document reasoning and safe refusal.

---

## Target Distribution

| Difficulty | Count |
|------------|------:|
| Easy | 8 |
| Medium | 8 |
| Hard / Edge | 4 |
| **Total** | **20** |

---

## Cluster Distribution

| Cluster | Easy | Medium | Hard | Total |
|----------|------:|--------:|------:|------:|
| Leave & HR | 4 | 2 | 1 | 7 |
| Workplace | 2 | 3 | 1 | 6 |
| IT Security | 2 | 3 | 2 | 7 |
| **Total** | **8** | **8** | **4** | **20** |

---

## Question Matrix

| ID | Difficulty | Cluster | Question | Source Documents | Evaluation Type | Status |
|----|------------|----------|----------|------------------|-----------------|--------|
| Q01 | Easy | Leave & HR | How many Casual Leaves (CL) is a confirmed employee entitled to in one financial year? | HR 01 | Numeric | |
| Q02 | Easy | Leave & HR | How many working days of Paternity Leave is an eligible employee entitled to for the birth of their first or second child? | HR 05 | Numeric | |
| Q03 | Easy | Leave & HR | Are contractors eligible for paid leave according to the company Leave Policy for Contractors? | HR 03 | Yes / No | |
| Q04 | Easy | Leave & HR | How many weeks of paid maternity leave is an eligible employee entitled to for the birth of her first or second child? | HR 04 | Numeric | |
| Q05 | Easy | Workplace | What is the probation period for an employee who joins Matellio with more than two years of prior work experience? | WP 01 | Numeric | |
| Q06 | Easy | Workplace | What are the standard office working hours, including office start time, flexible reporting time, lunch break duration, and weekly off days? | WP 04 | Time | |
| Q07 | Easy | IT Security | Can final project documents be stored permanently in Microsoft OneDrive, and if not, where must they be stored? | IT 03 + IT 04 | Policy retrieval | |
| Q08 | Easy | IT Security | How often must passwords be changed for applications that are not integrated with Single Sign-On (SSO)? | IT 05 | Numeric | |
| Q09 | Medium | Leave & Workplace | An employee with three years of prior work experience joins Matellio. What will be the employee's probation period, and which of the following leave types can be used during probation: Casual Leave, Sick Leave, Earned Leave and Occasional Leave? | WP 01 + HR 01 | Cross-document reasoning | |
| Q10 | Medium | Leave & HR | What happens if an employee's Casual Leave extends beyond two consecutive days? | HR 01 | Rule interpretation | |
| Q11 | Medium | Leave & Workplace | An employee with three years of prior work experience joins Matellio on 5 June and successfully completes probation on 5 September. Can the employee now use the Earned Leave accumulated during probation, and how many Occasional Leaves are added to the employee's leave balance? | WP 01 + HR 01 | Cross-document reasoning | |
| Q12 | Medium | Workplace & IT Security | An employee approved for hybrid working wants to save confidential company documents on their personal laptop while working from home. Is this permitted? If not, where should those documents be stored according to company policy, and can the personal laptop be used to access confidential company documents? | WP 05 + IT 02 | Cross-document reasoning | |
| Q13 | Medium | Leave & HR | A Professional and a regular on-roll employee both have unused Earned Leave on 31 March. According to company policy, how many days of Earned Leave can each employee carry forward into the next leave year? | HR 01 + HR 02 | Cross-document comparison | |
| Q14 | Medium | Leave & Workplace | An employee serving the notice period wants to use the remaining Compensatory Off balance. According to company policy, can the employee use the Compensatory Off, what happens to any unused balance, and which leave types may be applied for in the event of a medical emergency during the notice period? | HR 06 + WP 02 | Cross-document reasoning | |
| Q15 | Medium | IT Security | An employee wants to share a confidential company report with a client by creating an anonymous Microsoft OneDrive sharing link. Is this permitted according to company policy, and what approvals or restrictions apply before sharing confidential information externally? | IT 02 + IT 03 | Cross-document reasoning | |
| Q16 | Medium | Workplace & IT Security | A permanent remote employee is issued a company laptop. According to company policy, can the employee store confidential company data on the laptop, and what security requirements apply to the device and network connection when working with confidential information remotely? | WP 06 + IT 02 | Cross-document reasoning | |
| Q17 | Hard | Leave & Workplace | An employee with three years of prior work experience joins Matellio on 5 June 2025, successfully completes probation, and submits a resignation on 20 December 2025 while serving the full notice period. According to company policy, which leave types can the employee use during the notice period, what happens to the employee's Compensatory Off balance, and is the employee eligible for leave encashment? | WP 01 + WP 02 + HR 01 + HR 06 | Multi-document lifecycle reasoning | |
| Q18 | Hard | IT Security & Workplace | A hybrid employee keeps the final version of a confidential client deliverable only in Microsoft OneDrive, shares it with the client through an anonymous OneDrive sharing link, and resigns without moving the files to Microsoft SharePoint. For each of these three actions, identify the company rule that has been violated according to company policy. | IT 02 + IT 03 + IT 04 + WP 02 | Policy violation analysis | |
| Q19 | Hard | Workplace & IT Security | A permanent remote employee loses a company-issued laptop containing confidential company information. According to company policy, whom must the employee report the incident to and how quickly, what actions will the IT Department take, and can the company recover the cost of the laptop from the employee? | WP 06 + IT 02 + IT 06 | Multi-document incident response reasoning | |
| Q20 | Hard | Edge Case | What is Matellio's annual budget allocated for employee benefits and IT security, and how is that budget distributed across different departments? | Not available in corpus | Safe refusal | |

---

## Notes

- All questions are designed to have one deterministic answer based solely on the selected policy corpus.
- Easy questions evaluate direct factual retrieval from a single policy or closely related policies.
- Medium questions require reasoning across two or more policy documents.
- Hard questions require multi-document reasoning, policy synthesis, or safe refusal when information is unavailable in the corpus.
- This matrix is a planning document. The final evaluation dataset will be maintained in `data/golden_set_full.jsonl`.