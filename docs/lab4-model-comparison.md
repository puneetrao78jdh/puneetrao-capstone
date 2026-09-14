# Lab 4 — Model comparison: gpt-4o-mini vs gpt-4o

**Cohort member:** _<your name>_
**Date:** _<dd/mm/yyyy>_

## Numbers (filled in by `scripts/compare_models.py`)

```
Model            n    Total $     Avg $/q     Time
---------------------------------------------------
gpt-4o-mini     10    < $0.001520>   <$0.000072>   <31.85s>s
gpt-4o          10    <$0.029227>   < $0.001392>   < 38.58s>s
```

> gpt-4o cost _<19.2×>_ × more than gpt-4o-mini on the same questions.

## Two-paragraph eyeball reflection

### Paragraph 1 — where the gap mattered

_During my comparison, I found that both GPT-4o-mini and GPT-4o answered most factual questions correctly. The biggest difference appeared on questions that required reasoning or combining multiple concepts. GPT-4o generally provided more detailed explanations with additional context, while GPT-4o-mini gave shorter and more direct answers. For simple definition-based questions such as embeddings, .env files, and async/await, the quality difference was small, but GPT-4o's responses were usually more complete and better structured._

### Paragraph 2 — your rough rule for when to reach for the bigger model

_Based on these results, I would use GPT-4o-mini as my default model because it provides accurate answers for most everyday programming and AI questions at a much lower cost. I would switch to GPT-4o only for tasks that require deeper reasoning, richer explanations, or synthesizing multiple concepts, where the improvement in answer quality justifies the additional API cost._

## Confidence calibration (optional)

The lab pipeline asks the model to return a `confidence` value in `[0, 1]`.
Skim the persisted rows in SQLite:

```bash
sqlite3 data/answers.db \
  "SELECT model, AVG(confidence), AVG(cost_usd) FROM answers GROUP BY model;"
```

Do the two models report similar confidence on the same questions, or do
they disagree on what they know? One sentence is enough.
