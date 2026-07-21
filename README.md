# PoliWise Ghana

Papa Yaw Dartey  

## Project overview

This project is a manually implemented Retrieval Augmented Generation system for Academic City. It answers questions using:

1. Ghana Election Result CSV
2. Ghana 2025 Budget Statement and Economic Policy PDF

The implementation does not use LangChain, LlamaIndex, or any pre-built RAG pipeline. The core RAG components are built manually, including cleaning, chunking, embeddings, vector storage, retrieval, context selection, prompt construction, logging, evaluation, and feedback.


## How to run locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

On Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
streamlit run app.py
```

## Data setup

The election dataset is already included in:

```text
data/Ghana_Election_Result.csv
```

Download the Ghana 2025 Budget Statement PDF from the Ministry of Finance website and save it as:

```text
data/2025-Budget-Statement-and-Economic-Policy.pdf
```

## Features

- Simple Streamlit interface
- Query input
- Manual data cleaning
- Manual chunking
- Manual embedding pipeline using SentenceTransformers
- Manual FAISS vector storage
- Top-k retrieval
- Similarity scoring
- Hybrid search using vector similarity and keyword overlap
- Feedback loop for retrieval improvement
- Context window management
- Prompt construction with hallucination control
- Display of retrieved chunks
- Display of similarity scores
- Display of final prompt sent to the LLM
- Retrieval and feedback logs
<img width="1920" height="1080" alt="Screenshot 2026-04-24 at 1 33 38 AM" src="https://github.com/user-attachments/assets/f13f2675-f759-44aa-bf8e-d7fc9011317c" />
<img width="1569" height="839" alt="Screenshot 2026-04-24 at 7 24 32 PM" src="https://github.com/user-attachments/assets/22ed5813-2ecd-495d-8c30-6d9828916931" />
<img width="1318" height="583" alt="Screenshot 2026-04-24 at 5 49 02 PM" src="https://github.com/user-attachments/assets/513e45f5-9b34-42f7-9f71-4e29b93bfccb" />


## Architecture

See:

```text
assets/architecture_diagram.png
```

## Manual experiment logs

See:

```text
logs/prompt_experiments.csv
logs/adversarial_tests.csv
```

## Deployment

- Streamlit Community Cloud


