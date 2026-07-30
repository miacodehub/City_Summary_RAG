# City_Summary_RAG
A RAG pipeline that generates a summary of a city based on user query.


## Introduction

City Summary RAG is a Retrieval-Augmented Generation (RAG) pipeline designed for a collaborative travel planning application. Users can vote on destinations while receiving AI-generated summaries tailored to the type of trip they are looking for (for example, nightlife, food, photography or relaxation). The goal is to help groups make more informed travel decisions without leaving the application.

<img width="1911" height="896" alt="image" src="https://github.com/user-attachments/assets/325a8e0f-f890-444f-82b8-f2ee1914b39d" />


## Problem Statement

Existing travel platforms require users to browse multiple websites before understanding whether a destination matches their interests. Generic city descriptions also fail to adapt to different traveller preferences. The objective of this project is to generate concise, personalised summaries directly within the travel planning workflow.


## Solution

The solution is to have RAG create a short summary of the city user selected. This summary contains two elements:
1. The query: Users, in this case travelers, prefer to look for places with a certain vibe. The query here asks the user's input for the vibe they're looking for and uses that to create summaries of the cities.
2. City Summary : Cities can be summarized in a variety of ways. Once the user enters a vibe, the summary can be modified to show how well it fits the vibe the user entered.

A Retrieval Augmented Generation system works well in this use case because it can provide summaries more accurate to what the user needs by creating embeddings of both the user query and the summary of a prticular city.

## Technology Stack

- Python/FastAPI
- Javascript
- Sentence Transformers
- FAISS
- Ollama

## Architecture
        
<img width="2769" height="1500" alt="arch" src="https://github.com/user-attachments/assets/36c8af7b-9cdf-4050-8459-6b06cc375b83" />


## Project Repository Structure
backend/

├── app/

│   ├── rag/

│   ├── routes/

│   ├── data/

│   ├── indices/

│   └── main.py

frontend/

├── poll.html

├── poll.js

└── poll.css

## Implementation

  - **Data Ingestion:**
      Rather than indexing unrelated cities, neighbouring tourist destinations were selected because travellers commonly visit nearby cities within the same trip. This improves retrieval relevance while keeping the knowledge base compact.
      After having the list of cities, comes the data scraping. I scraped information on the cities from sites like WikiVoyage and stored them in memory. Once enough enough information about cities has been saved, comes the next part - chunking. 
 

- **Chunking:**
      I used recursive character-based chunking with overlap to preserve semantic context while ensuring retrieved passages remained within the language model's context window.

- **Embedding:**
      Each chunk was converted into a dense semantic embedding using BAAI/bge-base-en-v1.5, allowing similarity search based on meaning rather than keyword matching.

- **FAISS Index:**
      I then stored normalized embeddings in a `FAISS IndexFlatIP` vector index for efficient cosine similarity search.

- **Retrieval:**
      User queries are embedded using the same encoder and compared against the FAISS index using cosine similarity. The top three most relevant chunks are retrieved and supplied to the language model as contextual information.

- **Summary:**
      The retrieved context is combined with the traveller's preference using prompt engineering before being passed to a locally hosted LLM via Ollama. The model generates concise, grounded summaries based solely on the retrieved context, reducing hallucinations.


## Output
<img width="1442" height="817" alt="image" src="https://github.com/user-attachments/assets/52149008-ebe5-42d0-be02-90da8be95420" />


## Design Choices

### Chunking Strategy

Large documents often contain multiple topics, making it inefficient to retrieve an entire document for every query. To address this, I employed recursive character-based text chunking with overlapping chunks (~500 characters). This preserves semantic context across chunk boundaries while ensuring that retrieved passages remain concise enough to fit within the language model's context window. The overlap also prevents important information from being split across two unrelated chunks, improving retrieval quality.

---

### Embedding Model

The project uses the **BAAI/bge-base-en-v1.5** sentence transformer to generate dense vector embeddings for both city information and user queries. Unlike keyword-based search, semantic embeddings capture the meaning of the text, allowing the system to retrieve relevant information even when different wording is used. The same embedding model is applied to both documents and user queries to ensure they are represented within the same vector space.

---

### Indexing

Once embeddings are generated, they are normalized and stored in a **FAISS IndexFlatIP** vector index. FAISS provides efficient similarity search over high-dimensional vectors and is well suited for Retrieval-Augmented Generation pipelines. Using a vector index allows the application to quickly retrieve the most relevant pieces of information without scanning every document, making the retrieval process scalable as additional cities are added.

---

### Retrieval Strategy

When a user selects a city and specifies a travel preference (for example, nightlife, food, photography or history), the query is converted into an embedding using the same embedding model. A cosine similarity search is then performed against the FAISS index to retrieve the three most relevant chunks of information. These retrieved passages form the context supplied to the language model, ensuring that generated summaries are grounded in relevant city information rather than relying solely on the model's internal knowledge.

---

### LLM Model and Summary Generation

The retrieved context, together with the user's travel preference, is incorporated into a prompt and passed to a locally hosted Large Language Model using **Ollama**. Rather than generating generic travel descriptions, the model produces concise summaries tailored to the traveller's interests while remaining grounded in the retrieved context. Running the model locally removes dependency on external APIs, reduces operating costs, and enables the entire RAG pipeline to function offline.

## Scaling and Extensibility  
- The product only supports ~60 cities with their summaries now. However, it can be extended to handle more cities.
- Adding cities poses an interesting challenge about how the summary generation aand retrieval will be handled.
- Having the LLM generate summaries on the fly in production creates latency as the multi-step RAG process has several checks and is time consuming.
- However, a solution could be to store the RAG generated summaries of a couple hundred cities in persistent storage or even an in-memory cache like Redis.
- The above is an acceptable solution to scaling the product as the summaries, as can be seen, are only about 100 - 200 words. If they take around 50KB of space, then generating summaries for a million cities would need a 50GB. With modern storage solutions, this is a trivial need of space.










