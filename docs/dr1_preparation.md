# DR#1 Preparation Notes

## 1. What am I building?

I am building an **Enterprise Knowledge Assistant (EKA)** for Matellio. The objective is to help employees ask company policy questions in natural language and receive accurate, policy-backed answers with citations.

For this capstone, I selected **18 internal policy documents** organised into three policy clusters:

- **Leave & HR Policies** (6 documents)
- **Workplace Policies** (6 documents), covering probation, separation, diversity, office, hybrid, and remote working.
- **IT Security Policies** (6 documents), covering password management, data security, OneDrive, SharePoint, data retention, and backup.

The final objective is to build a **Retrieval-Augmented Generation (RAG)** based Enterprise Knowledge Assistant that retrieves relevant policy documents before generating responses, ensuring that answers are grounded in company policies rather than the language model's memory.

---

## 2. Why did I choose this corpus?

I selected this corpus for four reasons:

- It directly supports the business problem I am trying to solve by helping employees understand company policies.
- It covers three important organisational domains: Leave & HR, Workplace, and IT Security, providing a balanced evaluation corpus.
- The documents are reasonably structured and suitable for creating a meaningful Golden Set for evaluation.
- Most importantly, I received permission from my organisation to use these documents for this academic project.

---

## 3. Why this architecture?

My target architecture is a **Retrieval-Augmented Generation (RAG)** based Enterprise Knowledge Assistant.

A user asks a question in natural language, the system retrieves the most relevant policy documents, and the LLM generates an answer grounded in those retrieved documents together with supporting citations.

For **Milestone 1**, I have implemented only the foundation because that is how the course is structured. I have completed:

- API Contract (ADR 0002)
- Evaluation Framework
- Golden Set
- FastAPI Skeleton
- Stakeholder Map

These components will remain stable while retrieval, embeddings, vector database, and the LLM are added during the upcoming milestones.

---

## 4. How will I measure success?

The system will be evaluated using the **20-question Golden Set** created during Milestone 1.

The primary KPIs are:

- Correctly answer or safely refuse at least **16 out of 20** Golden Set questions.
- Provide citations for **100%** of non-refusal answers.
- Return responses within the response-time target defined in ADR 0001.

The evaluation framework created during Milestone 1 will remain the same throughout the project, allowing every future improvement to be measured objectively.

---

## 5. What am I uncertain about?

My biggest uncertainty is how different retrieval strategies, chunking methods, embedding models, and language models will affect answer quality.

I also want to better understand how confidence should be interpreted in probabilistic AI systems and how best to evaluate answers that may be phrased differently but are still factually correct.

I expect the evaluation framework and Golden Set to help me measure these improvements objectively during the remaining milestones.

---

## Closing Statement

My objective for DR#1 is not to demonstrate a completed AI system. My objective is to validate that I have built a strong architectural and evaluation foundation before implementing the complete RAG pipeline in the upcoming milestones.