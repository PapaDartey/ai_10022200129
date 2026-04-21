# Architecture and System Design

Student: Papa Yaw Dartey 
Index Number: 10022200129  

## Architecture flow

```text
User
 ↓
Streamlit Interface
 ↓
Query Processor
 ↓
SentenceTransformer Embedding Model
 ↓
Hybrid Retriever
 ├── FAISS Vector Store
 └── Keyword Overlap Scorer
 ↓
Feedback Score Adjustment
 ↓
Context Selection
 ↓
Prompt Builder
 ↓
LLM Generator
 ↓
Final Answer + Retrieved Chunks + Scores + Logs
```

## Component explanation

### 1. Streamlit interface

The interface accepts the user query and displays the final response, retrieved chunks, similarity scores, final prompt, and logs.

### 2. Data loader

The data loader reads the Ghana Election Result CSV and the Ghana 2025 Budget Statement PDF.

### 3. Cleaning module

The cleaning module removes hidden spaces, standardises text, and converts vote and percentage columns to numerical values.

### 4. Chunking module

The chunking module converts the CSV into row-level factual chunks and the PDF into overlapping word chunks.

### 5. Embedding pipeline

The embedding pipeline manually converts all chunks and user queries into vector embeddings using SentenceTransformers.

### 6. Vector store

The vector store uses FAISS to store embeddings and retrieve similar chunks.

### 7. Hybrid retriever

The retriever combines semantic similarity with keyword overlap. This is suitable because the data contains exact names, parties, regions, years, and policy terms.

### 8. Feedback loop

The feedback loop adjusts retrieval scores based on user feedback. Chunks marked Relevant are boosted. Chunks marked Not relevant are reduced.

### 9. Context manager

The context manager controls the amount of retrieved text passed to the LLM.

### 10. Prompt builder

The prompt builder injects the selected context into a strict hallucination-control prompt.

### 11. LLM generator

The generator sends the final prompt to an LLM and returns the answer.

### 12. Logger

The logger records the query, retrieved chunks, scores, final prompt, and answer.

## Why this architecture is suitable

The chosen domain combines structured election results and long-form government budget text. Row-level chunks are best for election facts, while overlapping text chunks are better for budget policy explanations. Hybrid retrieval is suitable because users may ask questions using exact entities like NPP, NDC, Ahafo, 2020, inflation, budget, or tax.
