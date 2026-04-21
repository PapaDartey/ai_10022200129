# Video Walkthrough Script, Under 2 Minutes

Student: YOUR NAME  
Index Number: YOUR INDEX NUMBER  

## 0:00 to 0:15 - Introduction

Hello, my name is YOUR NAME and my index number is YOUR INDEX NUMBER. This is my CS4241 Introduction to Artificial Intelligence project. I built a manual RAG chatbot for Academic City using the Ghana Election Result dataset and the Ghana 2025 Budget Statement.

## 0:15 to 0:35 - Design decision

I did not use LangChain, LlamaIndex, or any pre-built RAG pipeline. I manually implemented data cleaning, chunking, embeddings, vector storage, retrieval, prompt construction, response generation, and logging.

## 0:35 to 0:55 - Data preparation

For the election CSV, I used one row as one chunk because each row contains a complete factual result for a candidate, party, region, and year. For the budget PDF, I used 350-word chunks with 60-word overlap to preserve policy context.

## 0:55 to 1:15 - Retrieval

The app uses SentenceTransformers to create embeddings and FAISS to store vectors. I also added hybrid retrieval, which combines vector similarity with keyword overlap. This improves results for exact terms like region names, party names, and years.

## 1:15 to 1:35 - Prompt and hallucination control

The prompt instructs the model to answer only from retrieved context. If the information is not found, it must say it could not find the information instead of inventing an answer.

## 1:35 to 1:50 - Innovation

My innovation is a feedback loop. Users can mark retrieved chunks as Relevant or Not relevant, and the system uses this feedback to adjust future retrieval scores.

## 1:50 to 2:00 - Closing

The app displays retrieved chunks, scores, the final prompt, the final answer, and logs. This makes the full RAG pipeline transparent and testable.
