# Stakeholder Map

## Purpose

This document identifies the users and stakeholders of the **Matellio Employee Policy & Support Enterprise Knowledge Assistant (EKA)**, the problems they face, and the expected value of the solution.

The EKA is intended to provide policy-based answers with citations from three policy areas:

- Leave & HR Policies
- Workplace Policies
- IT Security Policies

The selected corpus contains 18 policy documents across these three areas.

The features described in this document are the planned outcome of the project. The corpus-based answering and evaluation are still being developed.

---

## 1. Primary Users

All six roles below are intended users of the EKA. Employees checking policies for their daily work are the proposed priority users for the first version.

| Primary User | Current Challenge | How the EKA Will Help | Main Policy Areas |
|---|---|---|---|
| Employees | Employees need to search different documents to understand leave, workplace, and IT rules. | The EKA will find the relevant policy information and provide an answer with a citation. | Leave & HR, Workplace, IT Security |
| Professionals | Professionals need information about leave and employment rules that apply specifically to them. | The EKA will use the Professional policy and distinguish it from policies for regular employees. | Leave & HR, Workplace |
| Contractors | Contractors need to know which leave benefits and workplace rules apply to them. | The EKA will provide contractor-specific information and avoid applying regular employee benefits incorrectly. | Leave & HR, Workplace |
| Managers | Managers regularly answer questions about leave, probation, hybrid work, remote work, and separation. | The EKA will help managers find policy-backed information while managers continue to handle approvals and decisions. | Leave & HR, Workplace, IT Security |
| HR Support Staff | HR staff repeatedly answer questions about leave, probation, maternity, paternity, separation, and employee lifecycle policies. | The EKA will help HR staff find consistent answers and supporting policy references. | Leave & HR, Workplace |
| IT Support Staff | IT staff repeatedly answer questions about passwords, OneDrive, SharePoint, data security, backup, and company devices. | The EKA will help IT staff find the relevant IT rule and required process. | IT Security, Workplace |

If the employee category affects the answer and is not clear from the question, the EKA should ask the user whether they are a regular employee, Professional, or Contractor.

---

## 2. Secondary Stakeholders

### Human Resources Department

The HR Department owns and maintains many of the Leave, HR, and Workplace policies. It will help confirm whether the policy information and reference answers are correct.

### Information Technology Department

The IT Department owns and maintains the IT Security and Collaboration policies. It is also responsible for decisions related to access, security, storage, and company devices.

### Project Managers and Department Heads

Project Managers and Department Heads approve or review some employee requests. The EKA can provide policy information, but it will not make approval decisions for them.

### Information Security Owner

The Information Security owner is a gatekeeper for the use of internal company documents and confidential information. This stakeholder may need to review how the corpus is stored and accessed.

### Organisation Management

Organisation Management is a possible project sponsor because the EKA aims to reduce repeated support questions and improve access to company policies.

The specific sponsor and final approver have not yet been confirmed.

---

## 3. Current Workflow

Users currently search different policy documents or contact their manager, HR Support, or IT Support for help.

Some questions can be answered from one document. Other questions require information from more than one policy. For example, a question about leave during probation may require both the Leave Policy and the Probation Policy.

This process may take time and can lead to different interpretations of the same policy.

The current time required to find an answer and the number of repeated support questions have not yet been measured. These figures should be measured rather than assumed.

A small sample of policy searches can be timed to create an initial comparison.

---

## 4. Desired Improvement

The EKA should allow users to ask a policy question in normal language and receive a clear answer based on the selected 18 policy documents.

The answer should include the relevant document and section so the user can verify it.

The EKA should distinguish between regular employees, Professionals, and Contractors when different policies apply.

When the documents do not contain enough information, the EKA should clearly say that the answer is not available in the corpus. It should direct the user to the correct support team where appropriate.

The EKA will not:

- Approve or reject leave requests
- Change company policies
- Make HR, IT, or management decisions
- Invent an answer when the corpus does not contain enough evidence
- Take any action on behalf of the user

---

## 5. Expected Business Value

The EKA is expected to:

- Reduce the effort required to search multiple policy documents
- Improve consistency in policy interpretation
- Provide transparent answers with source citations
- Reduce repeated questions received by HR and IT Support
- Improve employee self-service
- Help users understand which policies apply to their employee category
- Allow HR, IT, and managers to spend more time on complex cases

These are expected benefits. They have not yet been measured.

---

## 6. Success Metrics

The targets below come from the capstone ADR. They are targets for evaluation and are not current results.

### Metric 1: Answer Quality

**Target:** At least 16 out of 20 golden-set questions should be answered correctly or refused correctly.

**How it will be measured:**

- Run all 20 golden-set questions through the EKA.
- Compare each answer with the verified ideal answer and source documents.
- Use the W5 AI judge to score the answers.
- Manually review selected judge results.
- Record incorrect, incomplete, unsupported, and hallucinated answers.

**Current result:** Not yet measured.

### Metric 2: Citation Coverage

**Target:** Every non-refusal answer should include at least one citation from the selected corpus.

**How it will be measured:**

- Count all answers that are not refusals.
- Count how many of those answers contain a citation.
- Calculate the citation coverage percentage.
- Manually check whether the cited document actually supports the answer.

A citation being present does not automatically mean the answer is correct.

**Current result:** Not yet measured.

### Metric 3: Response Time

**Target:** Every answer or refusal should be returned within 30 seconds during evaluation.

**How it will be measured:**

- Record the start and completion time for every evaluation request.
- Report how many requests completed within 30 seconds.
- Record failed and timed-out requests separately.

**Current result:** Not yet measured on the policy golden set.

---

## 7. Open Questions

The following points still need to be confirmed:

- Who is the official project sponsor?
- Who will approve the use of internal policy documents?
- Should employees be the priority users for the first version?
- How will outdated or conflicting policy documents be handled?
- How often should the corpus be reviewed and updated?
- Which document sections should be included in citations?
- When should the EKA ask the user to clarify their employee category?

---

## 8. Stakeholder Map Status

This stakeholder map is prepared for M1 and DR #1.

Before it is marked as locked, the primary-user priority, sponsor, success targets, and corpus-access approval should be reviewed and confirmed.