import os
import re
import json
from collections import Counter

import streamlit as st
import google.generativeai as genai
from groq import Groq  # New Import
from pypdf import PdfReader
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dotenv import load_dotenv

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG  — must be the very first Streamlit call
# ─────────────────────────────────────────────────────────────
load_dotenv()

st.set_page_config(
    page_title="DocuMind AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
[data-testid="stMetric"] {
    background-color: #1e1e2e;
    border: 1px solid #313244;
    border-radius: 10px;
    padding: 12px 16px;
}
[data-testid="stMetricLabel"] { color: #a6adc8 !important; font-size: 0.78em !important; }
[data-testid="stMetricValue"] { color: #cba6f7 !important; }
[data-testid="stSidebar"]     { background-color: #181825; }
.stAlert                      { border-left: 4px solid #cba6f7 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# API KEYS & CLIENTS
# ─────────────────────────────────────────────────────────────
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_API_KEY   = os.getenv("GROQ_API_KEY", "")

if not GEMINI_API_KEY:
    st.error(
        "GEMINI_API_KEY not found.\n\n"
        "Create a `.env` file in the same folder as app.py with:\n\n"
        "```\nGEMINI_API_KEY=your_key_here\n```"
    )
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-3-flash-preview"
GROQ_MODEL = "llama-3.3-70b-versatile" # High-speed reliable fallback

# ─────────────────────────────────────────────────────────────
# AI HELPERS (WITH GROQ FALLBACK)
# ─────────────────────────────────────────────────────────────
def call_ai(prompt, temperature=0.3, max_tokens=2048):
    # 1. Try Gemini
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        cfg = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        )
        return model.generate_content(prompt, generation_config=cfg).text
    
    except Exception as gemini_exc:
        # 2. Try Groq Fallback
        if GROQ_API_KEY:
            try:
                client = Groq(api_key=GROQ_API_KEY)
                completion = client.chat.completions.create(
                    model=GROQ_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                return completion.choices[0].message.content
            except Exception as groq_exc:
                return f"AI Error (Both Gemini & Groq failed): {gemini_exc} | {groq_exc}"
        
        return f"Gemini Error: {gemini_exc}. (No Groq Key found for fallback)"


# ─────────────────────────────────────────────────────────────
# DOCUMENT PROCESSING
# ─────────────────────────────────────────────────────────────
def extract_text(file):
    reader = PdfReader(file)
    pages = []
    for i, page in enumerate(reader.pages, 1):
        t = (page.extract_text() or "").strip()
        if t:
            pages.append(f"[Page {i}]\n{t}")
    return "\n\n".join(pages)


def chunk_text(text, size=700, overlap=80):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i: i + size])
        if chunk.strip():
            chunks.append(chunk)
        i += size - overlap
    return chunks


def retrieve_chunks(query, chunks, top_k=5):
    q_words = set(re.findall(r'\b\w{3,}\b', query.lower()))
    scored = []
    for chunk in chunks:
        c_words = set(re.findall(r'\b\w{3,}\b', chunk.lower()))
        score = len(q_words & c_words) / (len(q_words) + 1)
        scored.append((score, chunk))
    scored.sort(reverse=True)
    return "\n\n---\n\n".join(c for _, c in scored[:top_k])


# ─────────────────────────────────────────────────────────────
# AI ANALYSIS FUNCTIONS
# ─────────────────────────────────────────────────────────────
def ai_extract_insights(text):
    prompt = (
        "Analyze this business document. "
        "Return ONLY a valid JSON object — no markdown fences, no explanation.\n\n"
        '{\n'
        '  "document_type": "Contract or Report or Proposal or Invoice or Agreement or Policy or Other",\n'
        '  "sentiment": "positive or neutral or negative",\n'
        '  "key_topics": ["topic1", "topic2", "topic3"],\n'
        '  "entities": {\n'
        '    "people": ["name1"],\n'
        '    "organizations": ["org1"],\n'
        '    "locations": ["place1"]\n'
        '  },\n'
        '  "monetary_values": ["$1000"],\n'
        '  "key_dates": ["Jan 2024"],\n'
        '  "action_items": ["action 1", "action 2"],\n'
        '  "risks": [\n'
        '    {"level": "high", "description": "risk description"}\n'
        '  ],\n'
        '  "key_clauses": ["clause summary 1"]\n'
        '}\n\n'
        f"Document (first 6000 chars):\n{text[:6000]}"
    )
    raw = call_ai(prompt, temperature=0.1, max_tokens=1800)
    try:
        clean = re.sub(r"```json|```", "", raw).strip()
        return json.loads(clean)
    except Exception:
        return {
            "document_type": "Document",
            "sentiment": "neutral",
            "key_topics": [],
            "entities": {"people": [], "organizations": [], "locations": []},
            "monetary_values": [],
            "key_dates": [],
            "action_items": [],
            "risks": [],
            "key_clauses": [],
        }


def ai_executive_summary(text, focus="general"):
    focus_map = {
        "general":   "Summarize the document's business intent, main findings, and key outcomes in 4-5 sentences.",
        "legal":     "Focus on legal obligations, terms, parties, and liabilities in 4-5 sentences.",
        "financial": "Focus on monetary figures, costs, revenues, and financial obligations in 4-5 sentences.",
        "hr":        "Focus on people, roles, responsibilities, and HR policies in 4-5 sentences.",
        "technical": "Focus on technical specs, systems, and implementation details in 4-5 sentences.",
    }
    instruction = focus_map.get(focus, focus_map["general"])
    prompt = (
        f"You are a senior business analyst. {instruction} "
        "Be precise and professional. No filler phrases.\n\n"
        f"Document:\n{text[:9000]}"
    )
    return call_ai(prompt, temperature=0.3)


def ai_score_dimensions(text):
    prompt = (
        "Rate this document from 1 to 10 on exactly these 6 dimensions:\n"
        "1. Risk Level\n"
        "2. Financial Impact\n"
        "3. Operational Complexity\n"
        "4. Compliance Requirements\n"
        "5. Strategic Importance\n"
        "6. Urgency\n\n"
        "Return ONLY 6 comma-separated integers. Example: 7,5,3,8,6,4\n\n"
        f"Document:\n{text[:3000]}"
    )
    raw = call_ai(prompt, temperature=0.1, max_tokens=30)
    try:
        nums = [min(10, max(1, int(x.strip()))) for x in raw.strip().split(",")]
        return nums if len(nums) == 6 else [5, 5, 5, 5, 5, 5]
    except Exception:
        return [5, 5, 5, 5, 5, 5]


def ai_grounded_answer(query, context):
    prompt = (
        "You are a precise Business Intelligence Agent.\n\n"
        "RULES:\n"
        "1. Answer ONLY from the context below. Do not use outside knowledge.\n"
        "2. Always include a direct quote from the document as evidence.\n"
        "3. If the answer is not in the context, reply: "
        "'This information is not found in the uploaded document.'\n"
        "4. Use this exact format:\n\n"
        "**Answer:**\n[Your concise answer]\n\n"
        "**Evidence:**\n> \"[Direct quote from document]\"\n\n"
        "**Confidence:** [High / Medium / Low] — [One sentence explaining why]\n\n"
        f"CONTEXT:\n{context}\n\n"
        f"QUESTION: {query}"
    )
    return call_ai(prompt, temperature=0.2, max_tokens=1200)


def ai_compare_docs(text1, name1, text2, name2):
    prompt = (
        "Compare these two business documents using this exact structure:\n\n"
        "### Similarities\n- [point]\n\n"
        "### Key Differences\n- [point]\n\n"
        "### Risk & Obligation Comparison\n[Analysis]\n\n"
        "### Recommendation\n[What the reader should do]\n\n"
        f"Document 1 — {name1}:\n{text1[:3500]}\n\n"
        f"Document 2 — {name2}:\n{text2[:3500]}"
    )
    return call_ai(prompt, temperature=0.3)


# ─────────────────────────────────────────────────────────────
# CHARTS
# ─────────────────────────────────────────────────────────────
DIMS = [
    "Risk", "Financial\nImpact", "Operational\nComplexity",
    "Compliance", "Strategic\nImportance", "Urgency",
]
DARK_BG = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")


def chart_radar(scores):
    r = scores + [scores[0]]
    d = DIMS + [DIMS[0]]
    fig = go.Figure(go.Scatterpolar(
        r=r, theta=d, fill="toself",
        fillcolor="rgba(203,166,247,0.18)",
        line=dict(color="#cba6f7", width=2),
        marker=dict(color="#cba6f7", size=7),
    ))
    fig.update_layout(
        **DARK_BG,
        showlegend=False,
        margin=dict(t=30, b=30, l=50, r=50),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True, range=[0, 10],
                gridcolor="#313244", tickfont=dict(color="#a6adc8"),
            ),
            angularaxis=dict(gridcolor="#313244", tickfont=dict(color="#cdd6f4")),
        ),
    )
    return fig


def chart_keywords(text):
    STOPWORDS = {
        "that","this","with","from","have","will","been","were","they",
        "their","them","these","those","when","where","which","while",
        "shall","also","each","such","upon","into","over","under","both",
        "then","than","more","some","your","said","very","what","page",
        "document","section","pursuant","herein","thereof","hereby","party",
    }
    words = [
        w for w in re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        if w not in STOPWORDS
    ]
    top = Counter(words).most_common(15)
    if not top:
        return None
    ws, cs = zip(*top)
    colors = (px.colors.sequential.Purples[::-1] * 3)[:len(ws)]
    fig = go.Figure(go.Bar(
        x=list(cs), y=list(ws), orientation="h",
        marker_color=colors, text=list(cs), textposition="outside",
    ))
    fig.update_layout(
        **DARK_BG,
        xaxis=dict(showgrid=False, color="#a6adc8"),
        yaxis=dict(color="#cdd6f4"),
        margin=dict(t=10, b=10, l=10, r=40),
        height=370,
    )
    return fig


def chart_sentiment(sentiment):
    val   = {"positive": 8.2, "neutral": 5.0, "negative": 1.8}.get(sentiment.lower(), 5.0)
    color = {"positive": "#a6e3a1", "neutral": "#f9e2af", "negative": "#f38ba8"}.get(
        sentiment.lower(), "#f9e2af"
    )
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=val,
        gauge={
            "axis": {
                "range": [0, 10],
                "tickvals": [2, 5, 8],
                "ticktext": ["Neg", "Neutral", "Pos"],
                "tickcolor": "#a6adc8",
            },
            "bar": {"color": color, "thickness": 0.25},
            "bgcolor": "rgba(0,0,0,0)",
            "bordercolor": "#313244",
            "steps": [
                {"range": [0,   3.5], "color": "rgba(243,139,168,0.15)"},
                {"range": [3.5, 6.5], "color": "rgba(249,226,175,0.15)"},
                {"range": [6.5,  10], "color": "rgba(166,227,161,0.15)"},
            ],
        },
        number={"font": {"color": color, "size": 28}},
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        height=210,
        margin=dict(t=40, b=0, l=20, r=20),
    )
    return fig


# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "docs":         {},
        "active_doc":   None,
        "history":      [],
        "summary":      None,
        "focus":        "general",
        "compare_mode": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ─────────────────────────────────────────────────────────────
# CHAT RESPONDER
# ─────────────────────────────────────────────────────────────
def respond(query, chunks):
    st.session_state.history.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)
    with st.chat_message("assistant"):
        with st.spinner("Searching document layers…"):
            ctx  = retrieve_chunks(query, chunks, top_k=5)
            resp = ai_grounded_answer(query, ctx)
        st.markdown(resp)
    st.session_state.history.append({"role": "assistant", "content": resp})


# ─────────────────────────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────────────────────────
def main():
    init_state()

    # ── SIDEBAR ──────────────────────────────────────────────
    with st.sidebar:
        st.markdown("## 🧠 DocuMind AI")
        st.caption("Hackathon Edition • GenAI + LLM")
        st.divider()

        st.markdown("### 📁 Upload Documents")
        uploads = st.file_uploader(
            "PDF files (max 3)",
            type="pdf",
            accept_multiple_files=True,
        )

        if uploads:
            for f in uploads[:3]:
                if f.name not in st.session_state.docs:
                    with st.spinner(f"Processing {f.name}…"):
                        text     = extract_text(f)
                        chunks   = chunk_text(text)
                        insights = ai_extract_insights(text)
                        scores   = ai_score_dimensions(text)
                        st.session_state.docs[f.name] = {
                            "text":     text,
                            "chunks":   chunks,
                            "insights": insights,
                            "scores":   scores,
                        }
                        st.session_state.summary = None
                    st.success(f"✅ {f.name}")

            names = list(st.session_state.docs.keys())
            if names:
                prev = st.session_state.active_doc
                st.session_state.active_doc = st.selectbox("Active Document", names)
                if st.session_state.active_doc != prev:
                    st.session_state.summary = None
                    st.session_state.history  = []

        st.divider()

        st.markdown("### 🎯 Analysis Focus")
        new_focus = st.selectbox(
            "Summary Style",
            ["general", "legal", "financial", "hr", "technical"],
            format_func=str.title,
        )
        if new_focus != st.session_state.focus:
            st.session_state.focus   = new_focus
            st.session_state.summary = None

        if len(st.session_state.docs) >= 2:
            st.divider()
            st.markdown("### 🔀 Compare Mode")
            st.session_state.compare_mode = st.toggle("Enable comparison")

        st.divider()

        col1, col2 = st.columns(2)
        if col1.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.history = []
            st.rerun()

        if st.session_state.history:
            chat_txt = "\n\n".join(
                f"{'YOU' if m['role'] == 'user' else 'AI'}: {m['content']}"
                for m in st.session_state.history
            )
            col2.download_button(
                "📥 Export",
                data=chat_txt,
                file_name="chat.txt",
                mime="text/plain",
                use_container_width=True,
            )

        st.caption(f"Model: `{MODEL_NAME}` (Groq Fallback Active)")

    # ── WELCOME SCREEN ───────────────────────────────────────
    if not st.session_state.docs or not st.session_state.active_doc:
        st.markdown(
            "<div style='text-align:center; padding:60px 20px;'>"
            "<h1>🧠 DocuMind AI</h1>"
            "<p style='color:#a6adc8; font-size:1.1em;'>Advanced Document Intelligence — Hackathon Edition</p>"
            "<p style='color:#a6adc8; max-width:500px; margin:auto;'>"
            "Upload a PDF to unlock AI-powered analysis with grounded Q&amp;A, "
            "risk detection, entity extraction, and executive summaries.</p>"
            "</div>",
            unsafe_allow_html=True,
        )
        c1, c2, c3, c4 = st.columns(4)
        features = [
            (c1, "🔍", "Grounded Q&A",   "Evidence-backed answers with direct quotes"),
            (c2, "📊", "6D Radar Chart", "Risk, Financial, Compliance and more"),
            (c3, "⚠️", "Risk Alerts",    "Auto-detected risks with severity levels"),
            (c4, "🔀", "Doc Comparison", "AI side-by-side analysis of 2 documents"),
        ]
        for col, icon, title, desc in features:
            col.markdown(
                f"<div style='text-align:center; padding:20px; background:#1e1e2e;"
                f"border:1px solid #313244; border-radius:12px;'>"
                f"<div style='font-size:2em;'>{icon}</div>"
                f"<div style='font-weight:bold; margin:8px 0; color:#cdd6f4;'>{title}</div>"
                f"<div style='color:#a6adc8; font-size:0.82em;'>{desc}</div></div>",
                unsafe_allow_html=True,
            )
        return

    # ── LOAD ACTIVE DOC ──────────────────────────────────────
    doc    = st.session_state.docs[st.session_state.active_doc]
    text   = doc["text"]
    chunks = doc["chunks"]
    ins    = doc["insights"]
    scores = doc["scores"]

    # ── HEADER METRICS ───────────────────────────────────────
    st.markdown(f"## 📄 {st.session_state.active_doc}")
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("Type",         ins.get("document_type", "—"))
    m2.metric("Words",        f"{len(text.split()):,}")
    m3.metric("RAG Chunks",   len(chunks))
    m4.metric("Risks Found",  len(ins.get("risks", [])))
    m5.metric("Sentiment",    ins.get("sentiment", "—").title())
    m6.metric("Action Items", len(ins.get("action_items", [])))
    st.divider()

    # ── COMPARE MODE ─────────────────────────────────────────
    if st.session_state.compare_mode and len(st.session_state.docs) >= 2:
        st.subheader("🔀 Document Comparison")
        names = list(st.session_state.docs.keys())
        ca, cb = st.columns(2)
        d1 = ca.selectbox("Document A", names, key="cmpA")
        d2 = cb.selectbox(
            "Document B", [n for n in names if n != d1], key="cmpB"
        )
        if st.button("⚡ Run Comparison", use_container_width=True):
            with st.spinner("Comparing…"):
                result = ai_compare_docs(
                    st.session_state.docs[d1]["text"], d1,
                    st.session_state.docs[d2]["text"], d2,
                )
            st.markdown(result)
        st.divider()

    # ── CHARTS ROW ───────────────────────────────────────────
    col_r, col_k, col_s = st.columns([2, 2, 1])

    with col_r:
        st.subheader("🎯 6D Document Profile")
        st.plotly_chart(chart_radar(scores), use_container_width=True)

    with col_k:
        st.subheader("🔑 Top Keywords")
        kfig = chart_keywords(text)
        if kfig:
            st.plotly_chart(kfig, use_container_width=True)
        else:
            st.info("Not enough text for keyword extraction.")

    with col_s:
        st.subheader("😶 Tone")
        st.plotly_chart(chart_sentiment(ins.get("sentiment", "neutral")), use_container_width=True)
        moneys = ins.get("monetary_values", [])
        if moneys:
            st.markdown("**💰 Values Found**")
            for v in moneys[:4]:
                st.code(v)

    st.divider()

    # ── SUMMARY + INSIGHTS ───────────────────────────────────
    col_l, col_ri = st.columns([3, 2])

    with col_l:
        focus_label = st.session_state.focus.title()
        st.subheader(f"📝 Executive Summary — {focus_label} Focus")
        if st.session_state.summary is None:
            with st.spinner("Generating summary…"):
                st.session_state.summary = ai_executive_summary(
                    text, st.session_state.focus
                )
        st.info(st.session_state.summary)

        actions = ins.get("action_items", [])
        if actions:
            st.markdown("**✅ Action Items**")
            for i, a in enumerate(actions, 1):
                st.markdown(f"{i}. {a}")

        clauses = ins.get("key_clauses", [])
        if clauses:
            st.markdown("**📑 Key Clauses**")
            for c in clauses[:4]:
                st.markdown(f"- {c}")

    with col_ri:
        st.subheader("🔍 Extracted Intelligence")

        risks = ins.get("risks", [])
        if risks:
            st.markdown("**⚠️ Risk Alerts**")
            icons = {"high": "🔴", "medium": "🟡", "low": "🟢"}
            for r in risks[:5]:
                lvl  = r.get("level", "medium").lower()
                icon = icons.get(lvl, "⚪")
                st.markdown(f"{icon} **{lvl.upper()}** — {r.get('description', '')}")

        ents = ins.get("entities", {})
        if ents.get("people"):
            st.markdown("**👤 People**")
            st.markdown(", ".join(ents["people"][:6]))

        if ents.get("organizations"):
            st.markdown("**🏢 Organizations**")
            st.markdown(", ".join(ents["organizations"][:6]))

        dates = ins.get("key_dates", [])
        if dates:
            st.markdown("**📅 Key Dates**")
            st.markdown(", ".join(dates[:6]))

        topics = ins.get("key_topics", [])
        if topics:
            st.markdown("**🏷️ Topics**")
            st.markdown(" • ".join(topics))

    # ── CHAT ─────────────────────────────────────────────────
    st.divider()
    st.subheader("💬 Grounded Q&A")
    st.caption(
        "Every answer is grounded in the document with a direct quote and confidence level."
    )

    # Quick question buttons — show only before first message
    if not st.session_state.history:
        st.markdown("**💡 Try a quick question:**")
        QUICK = [
            "What are the key obligations?",
            "What risks are mentioned?",
            "Who are the parties involved?",
            "What are the financial terms?",
            "What deadlines are mentioned?",
            "Summarize the main conclusions",
        ]
        qc = st.columns(3)
        for i, q in enumerate(QUICK):
            if qc[i % 3].button(q, key=f"qq{i}", use_container_width=True):
                st.session_state["_pending"] = q
                st.rerun()

    # Handle injected quick question
    if "_pending" in st.session_state:
        pending = st.session_state.pop("_pending")
        respond(pending, chunks)

    # Render history
    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Live input
    user_input = st.chat_input("Ask anything about this document…")
    if user_input:
        respond(user_input, chunks)


# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
