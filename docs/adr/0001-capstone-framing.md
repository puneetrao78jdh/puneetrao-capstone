# ADR-0001: Capstone Framing — puneetrao-capstone
- **Status:** Draft v1
- **Date:** 2026-08-17
- **Author:** Puneet Rao

## Context

Employees often need quick answers to HR policy questions related to leave, benefits, travel, expenses, and other people policies, but the relevant information is spread across multiple handbook pages. This capstone will build a grounded Q&A assistant over a selected set of public GitLab Handbook policies so that users can ask natural-language questions and receive concise answers based on the source documents rather than relying only on the LLM’s general knowledge.

## Decision — Solution Framing Canvas

| Box | Your answer |
|-----|-------------|
| **Inputs** | A natural-language HR policy question and, optionally, a user-uploaded policy document (such as PDF, DOCX, or TXT) to be used as an additional source for answering the question.|
| **Outputs** | A concise natural-language answer grounded in the available policy documents, with citations to the relevant source, or a clear response that the information could not be found when sufficient evidence is unavailable. |
| **Tools** | An OpenAI LLM for generating answers and a retrieval system for finding relevant information from the GitLab policy corpus and user-uploaded documents. |
| **Memory** | The system should maintain a short term conversational context within the current session so user can ask follow up question, for now we will avoid keep persistant memories between chats and treat this as out of scope |
| **Autonomy level** | Fro now this Q&A RAG assistant that proivde relevant answer based on feeded document, no action is plan for now |
| **Decision boundaries** | For now it will only provide answers to questions asked |

##Consequences

**Positive:**
-Users can get quick answers to HR policy questions without manually searching through multiple policy documents.
-Answers will be grounded in the available documents and supported by citations, improving reliability and transparency.

**Negative / risks:**
-The quality of the answer depends on the quality, completeness, and freshness of the source documents.
-Retrieval may find the wrong or incomplete policy section, which could result in an incorrect or misleading answer.
-In case the document does not have answer the model may halicunate

**Things we'll re-visit:**
-How retrieval quality and confidence should be measured before the assistant provides an answer.
-How to keep chat history