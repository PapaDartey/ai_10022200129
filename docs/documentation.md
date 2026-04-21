# Detailed Documentation

Student: Papa Yaw Dartey 
Index Number: 10022200129 

## 1. Problem statement

The task is to design and implement a RAG chatbot for Academic City. The system must allow a user to ask questions and receive answers grounded in the provided datasets. The two required sources are the Ghana Election Result CSV and the Ghana 2025 Budget Statement and Economic Policy PDF.

## 2. Data engineering and preparation

### 2.1 Election CSV cleaning

The CSV is cleaned by:

- Removing hidden non-breaking spaces
- Removing repeated whitespace
- Converting `Votes` to integer
- Converting `Votes(%)` to float
- Standardising region, candidate, and party text
- Removing duplicate rows

### 2.2 Budget PDF cleaning

The PDF is processed with PyMuPDF. Text is extracted page by page and cleaned by removing repeated spaces and blank fragments.

## 3. Chunking strategy

### Election dataset

The election dataset is structured, so the system uses one row as one chunk. This prevents facts from different candidates, parties, or regions from being mixed.

Example chunk:

```text
In the 2020 Ghana election, in Ahafo Region, Nana Addo Dankwa Akufo-Addo of the NPP received 145,584 votes, representing 55.04% of valid votes.
```

### Budget PDF

The budget document is long-form policy text, so it uses word-based chunks:

```text
Chunk size: 350 words
Overlap: 60 words
```

This provides enough context for economic policy questions while reducing the risk of losing information at chunk boundaries.

## 4. Comparative chunking analysis

Three chunking strategies should be tested manually.

| Strategy | Chunk size | Overlap | Expected impact |
|---|---:|---:|---|
| Small | 150 words | 30 words | Precise retrieval but may miss wider policy context |
| Medium | 350 words | 60 words | Best balance between precision and context |
| Large | 700 words | 100 words | More context but may retrieve irrelevant text |

Recommended conclusion: medium chunks are best for the budget PDF, while row-level chunks are best for the election CSV.

## 5. Embedding pipeline

The project uses SentenceTransformers with `all-MiniLM-L6-v2`. Embeddings are normalised so cosine similarity can be approximated using inner product search in FAISS.

## 6. Vector storage

FAISS `IndexFlatIP` is used as the vector store. The implementation manually adds document embeddings and searches with query embeddings.

## 7. Retrieval design

The system uses hybrid retrieval:

```text
final score = 0.75 * vector similarity + 0.25 * keyword overlap + feedback adjustment
```

This works well because election queries often contain exact words such as region names, party names, and years.

## 8. Failure case and fix

Failure case:

```text
Query: Who won in Ahafo?
```

The query is short. Pure vector search may retrieve chunks from nearby topics or other regions.

Fix:

The hybrid retriever adds keyword overlap so exact region names and party names increase relevance.

## 9. Prompt engineering

The strict prompt tells the model to use only the retrieved context and avoid inventing figures, dates, parties, regions, or policy claims.

## 10. Context window management

Retrieved chunks are ranked by final score. The system includes chunks until the selected word limit is reached. If a chunk would exceed the context window, it is truncated only if enough words remain.

## 11. Logging

The system logs:

- Timestamp
- Query
- Retrieved chunk IDs
- Source
- Vector score
- Keyword score
- Feedback score
- Final score
- Chunk text
- Final prompt
- Final answer

## 12. Evaluation

The system should be compared with a pure LLM answer. The RAG system should perform better because it uses retrieved evidence from the dataset and budget document.

## 13. Innovation component

The innovation is a feedback loop. Users can mark retrieved chunks as Relevant or Not relevant. This feedback is saved and used to boost or reduce future retrieval scores.

## 14. Limitations

- The system depends on the quality of extracted PDF text.
- If the OpenAI API key is missing, answer generation is skipped.
- Retrieval quality may reduce for very vague queries.
