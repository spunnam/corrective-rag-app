# Corrective RAG Application (LlamaIndex + Groq + Linkup)

This project implements a fully modular, production-ready **Corrective Retrieval-Augmented Generation (RAG)** app using:

- **LlamaIndex** for document ingestion, vector retrieval, and query engines
- **Groq** for fast inference using open-source LLMs like Mixtral
- **Linkup** for fallback deep web search when the documents lack context
- **Qdrant** as the vector store
- **Streamlit** for an interactive chat interface

---

## 🔁 RAG Flow Diagram (Text Description)

1. User enters a query.
2. The app retrieves relevant chunks from Qdrant vector DB.
3. A score-based filter checks if retrieved content is good enough.
4. If relevant → answer from document.
5. If not → the query is rephrased and sent to Linkup web search.
6. Results from the web are combined with any doc content.
7. Final response is generated using Groq LLM and streamed to the user.

---

## 🗂️ Project Structure

```bash
corrective_rag_app/
├── app.py                     # Main Streamlit app
├── workflow.py                # Corrective RAG workflow logic
├── utils.py                   # LLM loader, prompt templates
├── vector_store.py            # Qdrant + FastEmbed setup
├── pdf_ingestion.py           # PDF loader via LlamaIndex
├── requirements.txt
├── .env                       # For API keys (not committed)
├── ui/                        # All Streamlit UI logic
│   ├── sidebar.py
│   ├── header.py
│   ├── utils_ui.py
│   ├── chat_display.py
│   └── chat_input.py
└── assets/                    # Logos, etc.
    └── llamaindex.png
```

---

## 🛠 Tech Stack

- **Frontend**: Streamlit
- **LLM Backend**: Groq API (e.g. Mixtral-8x7b)
- **Embeddings**: FastEmbed (BAAI bge-large-en-v1.5)
- **Vector DB**: Qdrant (local Docker container)
- **Web Search Tool**: Linkup
- **Document Processing**: LlamaIndex readers

---

## 🚀 Getting Started

### 1. Clone and Install

```bash
git clone https://github.com/spunnam/corrective-rag
cd corrective-rag
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Run Qdrant (local vector DB)

```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

### 3. Add Your API Keys

Create a `.env` file with:

```env
LINKUP_API_KEY=your_linkup_key
GROQ_API_KEY=your_groq_key
```

### 4. Start the App

```bash
streamlit run app.py
```

---

## ✅ Features

- Upload PDF documents and create a vector index
- Score-based document relevance filtering
- Fallback to web search using Linkup if document doesn't answer
- Combine context from both sources for final LLM response
- Modular architecture, logs per step, Streamlit-based UI

---

## 🙌 Credits

- [LlamaIndex](https://llamaindex.ai)
- [Groq](https://groq.com)
- [Linkup](https://linkup.so)

---

## 📄 License

MIT License
