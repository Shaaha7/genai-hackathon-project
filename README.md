<<<<<<< HEAD
# genai-hackathon-project
=======
# 🧠 DocuMind AI — Hackathon Edition

🧠 DocuMind AI — Hackathon Edition
DocuMind AI is an advanced document intelligence platform built with Streamlit, Google Gemini, and Groq. It allows users to upload business documents (PDFs) and perform deep analysis, including risk detection, sentiment analysis, and grounded Q&A.

🚀 Features
Grounded Q&A: Ask any question about your document and get answers backed by direct quotes and confidence levels.

6D Document Profiling: Visualizes document metrics across Risk, Financial Impact, Complexity, Compliance, Strategy, and Urgency using Radar charts.

Intelligent Insights: Automatically extracts document types, entities (People, Orgs, Locations), monetary values, and key dates.

Risk Detection: Scans for potential high, medium, and low-level business risks.

Hybrid AI Engine: Dual-model architecture using Gemini 3 Flash as the primary engine with a high-speed Groq (Llama 3) fallback for maximum reliability.

Document Comparison: Side-by-side AI analysis to find similarities and differences between two uploaded files.

🛠️ Tech Stack
Frontend: Streamlit

Primary LLM: Google Gemini 3 Flash

Fallback LLM: Groq (Llama 3.3 70B)

Data Visualization: Plotly

PDF Processing: PyPDF

📋 Prerequisites
Before running the application, ensure you have:

Python 3.10 or higher.

A Google Gemini API Key (from Google AI Studio).

A Groq API Key (from Groq Console).

⚙️ Installation & Setup
Clone the Repository:

Bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
Create a Virtual Environment:

Bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies:

Bash
pip install -r requirements.txt
If you don't have a requirements file yet, install these:
pip install streamlit google-generativeai groq pypdf plotly python-dotenv

Configure Environment Variables:
Create a file named .env in the root directory and add your keys:

Plaintext
GEMINI_API_KEY=your_gemini_key_here
GROQ_API_KEY=your_groq_key_here
Note: Ensure the .env file is saved with UTF-8 encoding.

🏃 Running the App
Start the Streamlit server:

Bash
streamlit run app.py

> GenAI + LLM Module | Powered by Google Gemini + Streamlit

---

## 🚀 Features

| Feature | Description |
|---|---|
| **Multi-PDF Upload** | Analyse up to 3 documents at once |
| **Smart RAG** | Keyword-overlap chunk retrieval — no vector DB needed |
| **Grounded Q&A** | Every answer includes a direct document quote + confidence |
| **6D Radar Profile** | Risk, Financial, Operational, Compliance, Strategic, Urgency |
| **Auto Insights** | Entities, dates, monetary values, risks, action items, clauses |
| **Keyword Frequency** | Top-15 keywords bar chart |
| **Sentiment Gauge** | Document-level sentiment visualisation |
| **Doc Comparison** | AI side-by-side analysis of two documents |
| **Analysis Focus** | General / Legal / Financial / HR / Technical summary modes |
| **Chat Export** | Download full conversation as `.txt` |

---

## 🛠️ Local Setup

```bash
# 1. Clone / copy files
mkdir documind && cd documind
# paste app.py + requirements.txt here

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
echo "GEMINI_API_KEY=your_key_here" > .env

# 4. Run
streamlit run app.py
```

---

## ☁️ Deploy to Streamlit Cloud (Free)

1. Push `app.py` and `requirements.txt` to a **GitHub repo**
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select your repo / branch / `app.py`
4. Click **Advanced settings → Secrets** and add:
   ```toml
   GEMINI_API_KEY = "your_gemini_key_here"
   ```
5. Click **Deploy** — live in ~60 seconds ✅

> Get a free Gemini API key at: https://aistudio.google.com/apikey

---

## 📁 File Structure

```
.
├── app.py            ← main application
├── requirements.txt  ← pip dependencies
└── .env              ← local secrets (never commit this!)
```

---

## 🤖 Model Fallback Chain

The app auto-selects the best available model on your key:

`gemini-1.5-flash` → `gemini-1.5-flash-latest` → `gemini-1.5-pro` → `gemini-pro`

---

*Built for the GenAI + LLM Hackathon Module.*
>>>>>>> a209a93 (Added hackathon project files)
