# Manual Experiment Logs

Student: Papa Yaw Dartey  
Index Number: 10022200129 

Important: These logs must be completed manually after running the app. Do not submit only AI-generated summaries. Use this document as a template and fill in your own observations.

## Experiment 1: Chunking impact

| Date | Query | Chunking strategy | Top retrieved chunk relevant? | Notes |
|---|---|---|---|---|
|  | Who won in Ahafo Region in 2020? | Election row-level chunks |  |  |
|  | What does the budget say about economic policy? | 150 words, 30 overlap |  |  |
|  | What does the budget say about economic policy? | 350 words, 60 overlap |  |  |
|  | What does the budget say about economic policy? | 700 words, 100 overlap |  |  |

## Experiment 2: Prompt design

| Date | Query | Prompt version | Answer quality | Hallucination observed? | Notes |
|---|---|---|---|---|---|
|  | Who won in Ahafo Region in 2020? | Basic prompt |  |  |  |
|  | Who won in Ahafo Region in 2020? | Strict context-only prompt |  |  |  |
|  | Who won in Ahafo Region in 2020? | Strict prompt with source instruction |  |  |  |

## Experiment 3: Retrieval failure and fix

| Date | Query | Retrieval method | Failure observed | Fix | Result after fix |
|---|---|---|---|---|---|
|  | Who won in Ahafo? | Vector only |  | Hybrid keyword scoring |  |
|  | Compare NPP and NDC in Ashanti Region | Vector only |  | Hybrid keyword scoring |  |

## Experiment 4: Adversarial testing

| Date | Query | Query type | RAG response | Pure LLM response | Evidence-based comparison |
|---|---|---|---|---|---|
|  | Who won in the region? | Ambiguous |  |  |  |
|  | How many votes did the Labour Party get in Ahafo in 2020? | Misleading |  |  |  |

## Experiment 5: Feedback loop

| Date | Query | Chunk marked | Feedback | Effect on later retrieval |
|---|---|---|---|---|
|  |  |  | Relevant |  |
|  |  |  | Not relevant |  |
