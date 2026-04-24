

import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

from src.data_loader import load_election_data, load_budget_pdf
from src.chunking import build_all_chunks
from src.embeddings import EmbeddingPipeline
from src.vector_store import VectorStore
from src.retrieval import hybrid_retrieve, select_context
from src.prompt_builder import build_prompt, format_context
from src.generator import generate_answer
from src.logger import log_retrieval, log_feedback, read_feedback

load_dotenv()

st.set_page_config(
    page_title="PoliWise Ghana",
    page_icon="🤖",
    layout="wide"
)

DATA_DIR = "data"
LOG_DIR = "logs"
CSV_PATH = os.path.join(DATA_DIR, "Ghana_Election_Result.csv")
BUDGET_PDF_PATH = os.path.join(DATA_DIR, "2025-Budget-Statement-and-Economic-Policy.pdf")
RETRIEVAL_LOG_PATH = os.path.join(LOG_DIR, "retrieval_logs.csv")
FEEDBACK_LOG_PATH = os.path.join(LOG_DIR, "feedback_logs.csv")


@st.cache_resource
def initialise_rag():
    election_df = load_election_data(CSV_PATH)
    budget_pages = load_budget_pdf(BUDGET_PDF_PATH)
    chunks = build_all_chunks(election_df, budget_pages)

    embedder = EmbeddingPipeline()
    texts = [chunk["text"] for chunk in chunks]
    embeddings = embedder.embed_texts(texts)

    store = VectorStore(dimension=embeddings.shape[1])
    store.add(embeddings, chunks)
    return election_df, budget_pages, chunks, embedder, store


st.title("PoliWise Ghana")
st.caption("Manual RAG chatbot")

with st.sidebar:
    
    top_k = st.slider("Top-k retrieved chunks", 3, 10, 5)
    max_words = st.slider("Context window size, words", 300, 2000, 1200, step=100)
    strict_prompt = st.checkbox("Use strict hallucination-control prompt", value=True)

    st.header("Data source status")
    st.write("Election CSV: included")
    st.write("Budget PDF: included" if os.path.exists(BUDGET_PDF_PATH) else "Budget PDF: missing")

try:
    election_df, budget_pages, chunks, embedder, store = initialise_rag()
except Exception as exc:
    st.error(f"Could not initialise the RAG system: {exc}")
    st.stop()

tab_chat, tab_data, tab_logs = st.tabs(["Chat", "Dataset", "Logs"])

with tab_chat:
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "Hi. Ask me about the Ghana election dataset or the 2025 Budget Statement."}
        ]

    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    

    if "last_answer" in st.session_state:
        with st.expander("Retrieved chunks and scores", expanded=False):
            for item in st.session_state["last_retrieved"]:
                st.markdown(f"**{item['chunk_id']} | {item['source']} | final score {item['final_score']:.4f}**")
                st.caption(
                    f"Vector: {item.get('vector_score', 0):.4f} | "
                    f"Keyword: {item.get('keyword_score', 0):.4f} | "
                    f"Feedback: {item.get('feedback_score', 0):.4f} | "
                    f"Domain: {item.get('domain_score', 0):.4f}"
                )
                st.write(item["text"])
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Relevant - {item['chunk_id']}", key=f"rel_{item['chunk_id']}"):
                        log_feedback(FEEDBACK_LOG_PATH, st.session_state["last_query"], item["chunk_id"], "Relevant")
                        st.success("Feedback saved as Relevant")
                with col2:
                    if st.button(f"Not relevant - {item['chunk_id']}", key=f"notrel_{item['chunk_id']}"):
                        log_feedback(FEEDBACK_LOG_PATH, st.session_state["last_query"], item["chunk_id"], "Not relevant")
                        st.success("Feedback saved as Not relevant")
                st.divider()

        with st.expander("Final prompt sent to the LLM"):
            st.code(st.session_state["last_prompt"])

with tab_data:
    
    st.subheader("Cleaned election dataset preview")
    st.dataframe(election_df.head(30), use_container_width=True)

    st.subheader("Knowledge base summary")
    st.write(f"Total chunks: {len(chunks)}")
    st.write(f"Election chunks: {sum(1 for c in chunks if c['source'] == 'Election Dataset')}")
    st.write(f"Budget chunks: {sum(1 for c in chunks if c['source'] == 'Budget Statement')}")

with tab_logs:
    st.subheader("Retrieval logs")
    if os.path.exists(RETRIEVAL_LOG_PATH) and os.path.getsize(RETRIEVAL_LOG_PATH) > 0:
        st.dataframe(pd.read_csv(RETRIEVAL_LOG_PATH), use_container_width=True)
    else:
        st.info("Run the chatbot to create retrieval logs.")

    st.subheader("Feedback logs")
    if os.path.exists(FEEDBACK_LOG_PATH) and os.path.getsize(FEEDBACK_LOG_PATH) > 0:
        st.dataframe(pd.read_csv(FEEDBACK_LOG_PATH), use_container_width=True)
    else:
        st.info("No feedback has been recorded yet.")


query = st.chat_input("Ask a question, for example: Who won the 2020 election?")

if query:
    st.session_state["messages"].append({"role": "user", "content": query})

    with st.spinner("Running manual RAG pipeline..."):
        feedback_records = read_feedback(FEEDBACK_LOG_PATH)
        retrieved = hybrid_retrieve(
            query,
            embedder,
            store,
            top_k=top_k,
            feedback_records=feedback_records
        )

        selected_context = select_context(retrieved, max_words=max_words)
        context_text = format_context(selected_context)
        final_prompt = build_prompt(query, selected_context, strict=strict_prompt)
        answer = generate_answer(final_prompt, context_text)

    st.session_state["messages"].append({"role": "assistant", "content": answer})
    st.session_state["last_query"] = query
    st.session_state["last_retrieved"] = retrieved
    st.session_state["last_prompt"] = final_prompt
    st.session_state["last_answer"] = answer

    log_retrieval(RETRIEVAL_LOG_PATH, query, retrieved, final_prompt, answer)

    st.rerun()