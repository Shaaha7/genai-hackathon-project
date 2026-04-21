# 🧠 DocuMind AI

> **AI-powered document intelligence — grounded answers, risk detection, and entity extraction from any PDF.**

🔗 **Live Demo:** [https://genai-hackathon-project-i5dgaxxgdgyfd9eu3jaqxj.streamlit.app/](https://genai-hackathon-project-i5dgaxxgdgyfd9eu3jaqxj.streamlit.app/)

---

## The Problem

Contracts, reports, and policy documents are long, dense, and full of language designed to be hard to read. Analysts, students, and business owners regularly sign or act on documents they haven't fully understood — not because they're careless, but because manual review is slow and error-prone.

DocuMind AI turns a 30-page PDF into a structured, queryable intelligence report in under 15 seconds.

---

## What It Does

Upload any PDF and the system immediately produces:

- **Executive summary** with selectable focus (general, legal, financial, HR, or technical)
- **Risk detection** with severity levels — high 🔴, medium 🟡, low 🟢
- **Entity extraction** — people, organisations, locations, dates, monetary values
- **6-dimension radar chart** scoring Risk, Financial Impact, Operational Complexity, Compliance, Strategic Importance, and Urgency
- **Grounded Q&A** — ask anything in plain English, receive an answer with a direct evidence quote and a confidence rating
- **Document comparison** — upload two documents and get a structured side-by-side AI analysis

Every answer in the Q&A is grounded strictly in the uploaded document. If the information isn't there, the system says so rather than guessing.

---

## How It Works

```
PDF Upload
    │
    ▼
Text Extraction (PyPDF, page-aware)
    │
    ▼
Chunking (700-word chunks, 80-word overlap)
    │
    ▼
Keyword-Overlap Retrieval  ◄── User Question
    │
    ▼
Grounded Prompt → Gemini Flash
    │  (fallback if unavailable)
    └──────────────────► Groq / Llama 3.3 70B
    │
    ▼
Answer + Evidence Quote + Confidence Level
```

The dual-model fallback means the service stays available even if the primary API is down.

---

## Course Concepts Demonstrated

| Concept | Where it appears |
|---|---|
| Retrieval-Augmented Generation (RAG) | Chunk retrieval before every Q&A answer |
| Grounding | Answers sourced only from document context |
| Guardrail behaviour | Refuses to answer outside document scope |
| Structured prompt design | JSON extraction, confidence formatting, focus-mode summaries |
| Fallback / reliability architecture | Gemini → Groq automatic failover |
| Deployment | Live on Streamlit Cloud |
| Evaluation awareness | Confidence scoring + evidence quotes on every response |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend & app | Streamlit |
| Primary LLM | Google Gemini Flash |
| Fallback LLM | Groq (Llama 3.3 70B) |
| PDF parsing | PyPDF |
| Visualisation | Plotly |
| Secrets management | `.env` / Streamlit secrets |

---

## Local Setup

```bash
git clone https://github.com/your-username/documind-ai.git
cd documind-ai
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
```

Run the app:

```bash
streamlit run app.py
```

The `GROQ_API_KEY` is optional — the app runs on Gemini alone, but the fallback will be inactive.

---

## Project Structure

```
documind-ai/
├── app.py            # Full application — extraction, AI, charts, UI
├── requirements.txt  # Python dependencies
├── .env              # API keys (not committed)
├── README.md         # This file
└── GRANDMA.md        # Plain-English explanation for non-technical readers
```

---

## Possible Future Extensions

Vector embedding retrieval (e.g. FAISS) would improve answer quality on large documents. Clause-level page highlighting, multilingual support, and a persistent multi-document workspace are natural next steps.

---

#Working Project Images
<img width="1919" height="827" alt="image" src="https://github.com/user-attachments/assets/f4433bc1-653a-4baa-9c89-017f64007389" />
<img width="1904" height="719" alt="image" src="https://github.com/user-attachments/assets/c0be85d9-3b24-406b-8183-408a46d1deef" />
<img width="1905" height="802" alt="image" src="https://github.com/user-attachments/assets/bfa2eb1d-1683-4f4c-bdbf-d1553d78b271" />
<img width="1531" height="507" alt="image" src="https://github.com/user-attachments/assets/ce4bad39-e8db-4eb4-a4ce-60ce98be8e70" />
<img width="1531" height="559" alt="image" src="https://github.com/user-attachments/assets/ef7b929c-919f-4b6a-a136-37686edecb79" />






## Author

**Shabeer Ahamed Kamal** — M01087870
CST4625 Generative AI — Hackathon Submission
Built with Streamlit · Google Gemini · Groq
