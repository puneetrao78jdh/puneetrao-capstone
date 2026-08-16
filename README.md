# Capstone — Knowledge Assistant
A 30-week build of a Q&A assistant over a small document corpus, completed as part of
the *Agentic AI & RAG Engineering* programme.

## Corpus
My capstone corpus is a selected set of publicly available GitLab Handbook policies covering general people policies, India-specific employee policies and benefits, time off and leave, and travel and expense policies. The corpus will be used to build and evaluate a grounded HR policy Q&A assistant.
Source: GitLab Handbook

_1. Gitlab Handbook - People policies_
https://handbook.gitlab.com/handbook/people-policies/?utm_source=chatgpt.com

_2. People Policies — General employment practices, Workplace conduct, Confidentiality, etc._
https://handbook.gitlab.com/handbook/people-policies/?utm_source=chatgpt.com

_3. India Employee Policies & Benefits — Contains real India-specific rules such as earned leave, sick leave, casual leave, maternity and parental leave._⁠
https://handbook.gitlab.com/handbook/entity/india-pvt-ltd/?utm_source=chatgpt.com

_4. Time Off — Vacation/time-off rules and processes._
https://handbook.gitlab.com/handbook/people-policies/leave-of-absence/?utm_source=chatgpt.com

_5. Leave Types — Parental, emergency, military, sick and caregiving leave._
https://handbook.gitlab.com/handbook/people-group/time-off-and-absence/leave-types/?utm_source=chatgpt.com

_6. Travel & Expense Policy — Reimbursement rules, business travel, WFH equipment and expense restrictions._ 
https://handbook.gitlab.com/handbook/finance/expenses/?utm_source=chatgpt.com_

**Reason for Choice of this corpus: This will not be simple Q&A with open AI and these leave polices and Time off etc will give me enough opportunity to see if RAG is working or not.**

## Structure

- `src/` — application code
- `docs/adr/` — Architecture Decision Records (one per major design choice)
- `docs/runs/` — saved LLM outputs for evidence and reference

## Week 1

- [x] Set up repo + secrets discipline
- [ ] Build `hello_llm.py` (Lab Step 2)
- [ ] Write ADR v1 (Lab Step 3)