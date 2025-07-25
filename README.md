# HR Resource Query Chatbot

An internal HR tool designed to quickly find employees based on their skills and past project experience.  
It helps HR teams and project managers avoid manual spreadsheet checks by providing fast, conversational queries.

---

## Example Use Cases
- **Find Python developers with 3+ years of experience**
- **Who has worked on healthcare-related projects?**
- **Suggest engineers for a React Native mobile app project**

---

## Why This Project?
Manually searching through HR systems or Excel files is slow and error-prone.  
This chatbot leverages **semantic search** and a **conversational interface** to:
- Find relevant employees based on skills and experience
- Summarize their past work when queries are ambiguous
- Speed up resource allocation decisions

---

## Key Features
- **Skill-based Semantic Search** → Uses FAISS + SentenceTransformers for more accurate matching than keyword search.
- **Context-Aware Answers** → LLM (OpenAI GPT) helps refine unclear queries.
- **Fast Response Time** → Async backend with caching for repeated queries.
- **Simple Interface** → Streamlit web UI for non-technical HR staff.
- **Test Coverage** → Unit tests to ensure stable API performance.

---
## DEMO 

https://docs.google.com/document/d/1dvfYqv9fZ9gLzETJR-yD1ajAppEbiPlxvXPiGJd7bTs/edit?usp=sharing

## System Architecture
```text
[User] → [Streamlit UI] → [FastAPI Backend] → [Semantic Search (FAISS + SBERT)]
                                      ↓
                                  Employee Data (JSON)

Tech Stack:

* Backend: FastAPI, SentenceTransformers, FAISS, OpenAI GPT

* Frontend: Streamlit

* Testing: Pytest

* Python: 3.9+

## PROJECT STRUCTURE

hr-chatbot/
│
├── backend/                  # Backend (FastAPI)
│   ├── main.py               # FastAPI app entry point
│   ├── search.py             # Semantic search logic (FAISS + SentenceTransformers)
│   ├── models.py             # Pydantic models (request & response schemas)
│   ├── employees.json        # Sample employee dataset (25 employees)
│   └── __init__.py           # Makes backend a package
│
├── frontend/                 # Frontend (Streamlit)
│   └── app.py                # Streamlit UI code
│
├── tests/                    # Unit tests
│   └── test_api.py           # Tests for API endpoints
│
├── venv/                     # Virtual environment (ignored in .gitignore)
├── .gitignore                # Git ignore file
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation


GETTING STARTED 

1. CLONE THE REPO 
git clone <repo-url>
cd hr-chatbot
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r backend/requirements.txt

2.RUN THE BACKEND 
uvicorn backend.main:app --reload

3.RUN THE FRONTEND 
streamlit run frontend/app.py

Backend API Docs → http://127.0.0.1:8000/docs
Frontend → http://localhost:8501

RUNNING TEST 
pytest --maxfail=1 --disable-warnings -q

## AI Development Process
This project was primarily designed and implemented manually, with AI tools used as modern productivity aids.

- **Role of AI Tools**:
  - Used ChatGPT for brainstorming architectural approaches, clarifying concepts when stuck, and quick debugging assistance.
  - Used GitHub Copilot for auto-completing repetitive boilerplate code.
  - Used AI tools to revise or refresh forgotten concepts during development (similar to consulting documentation or tutorials).
- **Human-Centric Work**:
  - All core design decisions, semantic search implementation (FAISS + SentenceTransformer), RAG pipeline integration, caching strategy, and final debugging were performed manually.
  - Edge case handling, testing, dataset preparation, and error handling enhancements were entirely hand-written.
- **Benefits of AI Usage**:
  - Helped in faster debugging and learning unfamiliar parts of APIs.
  - Accelerated boilerplate coding (~20-30% faster prototyping).
  - Validated architectural decisions early in the design phase.
- 