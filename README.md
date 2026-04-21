# 🧠 DocuMind AI — Distinction-Level Hackathon Submission

## 📌 Problem Statement

Professionals and students often struggle to quickly extract risks, entities, compliance issues, and strategic insights from long documents. Manual analysis is slow, error‑prone, and difficult to verify.

**DocuMind AI solves this problem by providing grounded document intelligence using retrieval‑based Large Language Model reasoning with confidence‑supported answers.**

---

## 🚀 Solution Overview

DocuMind AI is a Streamlit-based intelligent document analysis assistant that allows users to upload PDFs and:

* Ask grounded questions
* Detect risks automatically
* Extract entities and financial values
* Compare documents side‑by‑side
* Generate structured executive summaries
* Visualize document intelligence metrics

The system ensures responses are generated **only from retrieved document context**, improving reliability and reducing hallucination risk.

---

## 🤖 How the AI System Works (Pipeline)

1. User uploads PDF document(s)
2. Text is extracted using PyPDF
3. Document is split into logical chunks
4. Relevant chunks retrieved using keyword‑overlap retrieval
5. Gemini model generates grounded answers
6. Confidence score calculated
7. Evidence quote returned to the user
8. Groq fallback model activates if Gemini unavailable

This architecture improves reliability, interpretability, and availability.

---

## 🧩 Key Features

### 📄 Grounded Q&A

Ask questions about documents and receive:

* evidence‑supported answers
* confidence score
* source paragraph references

### 📊 6D Document Intelligence Radar

Visualizes:

* Risk
* Financial impact
* Operational complexity
* Compliance exposure
* Strategic importance
* Urgency level

### ⚠️ Risk Detection Engine

Automatically identifies:

* legal risks
* compliance concerns
* financial exposure indicators

### 🧾 Entity Extraction

Detects:

* people
* organisations
* locations
* dates
* monetary values

### 📑 Document Comparison

Side‑by‑side AI comparison showing:

* similarities
* differences
* strategic implications

### 📈 Sentiment Analysis Gauge

Displays overall document tone:

* positive
* neutral
* risk‑sensitive

### 🧠 Executive Decision Summary

Provides quick insights:

* Risk Level
* Financial Exposure
* Compliance Flags
* Recommended Action

Designed for fast decision‑making workflows.

---

## 🏗️ Architecture

Frontend:

* Streamlit

Primary Model:

* Google Gemini Flash

Fallback Model:

* Groq (Llama 3.3 70B)

Processing:

* PyPDF document parsing
* keyword‑overlap retrieval grounding

Visualisation:

* Plotly radar charts

---

## 🛡️ Reliability Strategy

DocuMind AI improves trust using:

* retrieval‑based grounding
* confidence scoring
* evidence quotes
* fallback LLM architecture
* document‑scope guardrail responses

Example guardrail behaviour:

> "This question cannot be answered because it is outside the uploaded document context."

---

## 🌐 Live Deployment

Streamlit App:

(Add your deployed Streamlit link here)

Example:

[https://your-streamlit-link.streamlit.app](https://your-streamlit-link.streamlit.app)

---

## 🧪 Example Workflow

1. Upload contract PDF
2. Ask:

"What are the penalty clauses?"

System returns:

* grounded answer
* confidence score
* supporting paragraph
* detected risk level

---

## ⚙️ Installation (Local Setup)

Clone repository:

```
git clone https://github.com/your-username/documind-ai.git
cd documind-ai
```

Install dependencies:

```
pip install -r requirements.txt
```

Create `.env` file:

```
GEMINI_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
```

Run application:

```
streamlit run app.py
```

---

## 📚 Course Concepts Demonstrated

This project integrates key Generative AI engineering ideas:

* Retrieval‑Augmented Generation (RAG)
* grounded responses
* guardrail behaviour
* fallback model architecture
* deployment pipeline
* structured prompt design
* confidence signalling

---

## 📊 Why This Project Matters

DocuMind AI transforms static documents into interactive decision‑support systems.

It helps:

* analysts
* students
* researchers
* compliance reviewers
* business stakeholders

understand complex documents faster and more reliably.

---

## 🚀 Future Improvements

Possible extensions:

* vector database retrieval
* multi‑document memory workspace
* clause‑level highlighting UI
* multilingual support
* citation ranking system

---

## 👨‍💻 Author

Niranjan

GenAI Hackathon Submission

Built using Streamlit + Gemini + Groq
