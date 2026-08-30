"""Page: RAG-based AI Tax Search."""

import streamlit as st
from utils.rag_engine import RAGEngine
from data.sample_data import TAX_RULES_KB

st.set_page_config(page_title="AI Tax Search — CA Copilot", page_icon="🤖", layout="wide")

# ── Theme CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0E1117; }
    /* Sidebar: dark, bold, high-contrast text */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1A1A2E 0%, #16213E 100%) !important;
    }
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] .stMarkdown h4,
    section[data-testid="stSidebar"] .stMarkdown h5,
    section[data-testid="stSidebar"] .stMarkdown h6,
    section[data-testid="stSidebar"] .stMarkdown span,
    section[data-testid="stSidebar"] .stMarkdown label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] .stMarkdown h4 {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }
    section[data-testid="stSidebar"] .stMarkdown strong,
    section[data-testid="stSidebar"] .stMarkdown b {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }
    section[data-testid="stSidebar"] .stMarkdown em,
    section[data-testid="stSidebar"] .stMarkdown a {
        color: #90CAF9 !important;
        font-weight: 600 !important;
    }
    section[data-testid="stSidebar"] caption,
    section[data-testid="stSidebar"] .stCaption,
    section[data-testid="stSidebar"] small {
        color: #B0BEC5 !important;
        font-weight: 600 !important;
    }
    section[data-testid="stSidebar"] [data-baseweb="select"] span,
    section[data-testid="stSidebar"] [data-baseweb="select"] div {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    section[data-testid="stSidebar"] [data-baseweb="radio"] span,
    section[data-testid="stSidebar"] [data-baseweb="checkbox"] span {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    section[data-testid="stSidebar"] table th,
    section[data-testid="stSidebar"] table td {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: #3A4A6B !important;
    }
    .page-header {
        background: linear-gradient(135deg, #2E86C1 0%, #27AE60 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 2rem; font-weight: 800; margin-bottom: 0.2rem;
    }
    .page-sub { color: #A0AEC0; font-size: 0.95rem; margin-bottom: 1.5rem; }
    .section-header {
        color: #E2E8F0; font-size: 1.1rem; font-weight: 700;
        border-bottom: 2px solid #2E86C1; padding-bottom: 0.4rem; margin: 1.2rem 0 0.8rem 0;
    }
    .chat-msg {
        padding: 14px 18px; border-radius: 14px; margin: 10px 0; line-height: 1.6;
        font-size: 0.9rem;
    }
    .chat-user {
        background: linear-gradient(135deg, #1E3A5F, #2E86C1);
        color: #E2E8F0; border-radius: 14px 14px 4px 14px;
        max-width: 75%; margin-left: auto;
    }
    .chat-ai {
        background: #1A1A2E; color: #CBD5E0; border: 1px solid #2D3748;
        border-radius: 14px 14px 14px 4px; max-width: 90%;
    }
    .source-card {
        background: linear-gradient(135deg, #1A1A2E, #16213E);
        border: 1px solid #2D3748; border-radius: 10px; padding: 10px 14px;
        margin: 4px 0; font-size: 0.82rem;
    }
    .source-title { color: #2E86C1; font-weight: 700; }
    .source-meta { color: #718096; font-size: 0.75rem; }
    .confidence-pill {
        display: inline-block; padding: 2px 10px; border-radius: 10px;
        font-size: 0.7rem; font-weight: 700; margin-left: 6px;
    }
    .conf-high { background: rgba(39,174,96,0.15); color: #27AE60; }
    .conf-med { background: rgba(243,156,18,0.15); color: #F39C12; }
    .conf-low { background: rgba(231,76,60,0.15); color: #E74C3C; }
    .topic-tag {
        display: inline-block; padding: 3px 10px; border-radius: 10px;
        font-size: 0.72rem; font-weight: 600; margin: 2px;
        background: rgba(46,134,193,0.1); color: #2E86C1; border: 1px solid rgba(46,134,193,0.2);
    }
    /* === Main content: bright widget labels & text === */
    section[data-testid="stMain"] label,
    section[data-testid="stMain"] .stMarkdown p,
    section[data-testid="stMain"] .stMarkdown li,
    section[data-testid="stMain"] .stMarkdown h1,
    section[data-testid="stMain"] .stMarkdown h2,
    section[data-testid="stMain"] .stMarkdown h3,
    section[data-testid="stMain"] .stMarkdown h4,
    section[data-testid="stMain"] .stMarkdown h5,
    section[data-testid="stMain"] .stMarkdown h6,
    section[data-testid="stMain"] .stMarkdown span,
    section[data-testid="stMain"] .stMarkdown td,
    section[data-testid="stMain"] .stMarkdown th,
    section[data-testid="stMain"] p,
    section[data-testid="stMain"] span,
    section[data-testid="stMain"] div,
    section[data-testid="stMain"] li,
    section[data-testid="stMain"] td,
    section[data-testid="stMain"] th {
        color: #E0E0E0 !important;
    }
    /* Widget labels: radio, select, file_uploader, text_area, button labels */
    section[data-testid="stMain"] [data-baseweb="radio"] span,
    section[data-testid="stMain"] [data-baseweb="select"] span,
    section[data-testid="stMain"] [data-baseweb="select"] div,
    section[data-testid="stMain"] [data-baseweb="textarea"] + label,
    section[data-testid="stMain"] [data-baseweb="file-uploader"] + label,
    section[data-testid="stMain"] .stFileUploader label,
    section[data-testid="stMain"] .stTextArea label,
    section[data-testid="stMain"] .stSelectbox label,
    section[data-testid="stMain"] .stRadio label,
    section[data-testid="stMain"] .stMultiSelect label,
    section[data-testid="stMain"] .stSlider label,
    section[data-testid="stMain"] .stNumberInput label,
    section[data-testid="stMain"] .stDateInput label {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    /* Heading labels in main content */
    section[data-testid="stMain"] .stMarkdown h1,
    section[data-testid="stMain"] .stMarkdown h2,
    section[data-testid="stMain"] .stMarkdown h3,
    section[data-testid="stMain"] .stMarkdown h4 {
        color: #FFFFFF !important;
    }
    /* Inline code and bold in main area */
    section[data-testid="stMain"] .stMarkdown code,
    section[data-testid="stMain"] .stMarkdown strong,
    section[data-testid="stMain"] .stMarkdown b {
        color: #FFFFFF !important;
    }
    /* Make .field-label brighter for extracted data cards */
    .field-label {
        color: #B0BEC5 !important;
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600 !important;
    }
    /* Info/warning/error boxes text */
    section[data-testid="stMain"] .stAlert p,
    section[data-testid="stMain"] [data-baseweb="notification"] {
        color: #E0E0E0 !important;
    }
    /* Table text in main content */
    section[data-testid="stMain"] table th {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    section[data-testid="stMain"] table td {
        color: #E0E0E0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────
st.markdown('<div class="page-header">🤖 RAG-Based AI Tax Search</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-sub">Ask any tax question — the AI searches through loaded knowledge base and provides answers with source citations.</div>',
    unsafe_allow_html=True,
)

# ── Init RAG Engine ──────────────────────────────────────────
if "rag_engine" not in st.session_state:
    st.session_state.rag_engine = RAGEngine()

rag = st.session_state.rag_engine

# ── Sidebar: Knowledge Base & Settings ───────────────────────
with st.sidebar:
    st.markdown("### 📚 Knowledge Base")
    st.markdown(f"**{len(TAX_RULES_KB)} documents loaded**")
    st.markdown("---")

    for doc in TAX_RULES_KB:
        tags_html = " ".join([f'<span class="topic-tag">{t}</span>' for t in doc["tags"]])
        st.markdown(f"""
        <div class="source-card">
            <div class="source-title">{doc['title']}</div>
            <div class="source-meta">{doc['source']}</div>
            <div style="margin-top:4px">{tags_html}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    top_k = st.slider("Max sources per answer", 1, 5, 3)
    if st.button("🗑️ Clear Chat History", type="secondary"):
        rag.clear_history()
        st.session_state.pop("chat_messages", None)
        st.rerun()

# ── Chat Messages Init ───────────────────────────────────────
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": (
                "👋 Welcome to the **AI Tax Search Assistant**!\n\n"
                "I can help you with:\n"
                "- 📋 **Income Tax** deductions, regimes, and computation\n"
                "- 🏛️ **GST** rates, filing, ITC rules\n"
                "- 💰 **TDS** rates and provisions\n"
                "- 📊 **Capital Gains** taxation\n"
                "- 🔄 **Transfer Pricing** requirements\n\n"
                "Ask me anything — I'll search through the loaded tax knowledge base and provide answers with citations!"
            ),
            "sources": [],
            "confidence": None,
        }
    ]

# ── Suggested Questions ──────────────────────────────────────
st.markdown('<div class="section-header">💡 Suggested Questions</div>', unsafe_allow_html=True)
sugg_cols = st.columns(4)
suggestions = [
    "What deductions are available under Section 80C?",
    "Compare New vs Old Tax Regime for FY 2025-26",
    "What are the GST rate slabs in India?",
    "Explain TDS rates for contractor payments",
]
for col, q in zip(sugg_cols, suggestions):
    with col:
        if st.button(q, key=f"sugg_{q[:20]}"):
            st.session_state["pending_query"] = q
            st.rerun()

st.markdown("---")

# ── Display Chat History ─────────────────────────────────────
for msg in st.session_state.chat_messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-msg chat-user">🧑 <b>You:</b> {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        # Format answer for display (handle markdown bold etc.)
        answer = msg["content"].replace("\n", "<br>")
        st.markdown(f'<div class="chat-msg chat-ai">🤖 <b>AI Assistant:</b><br><br>{answer}</div>', unsafe_allow_html=True)

        # Show sources
        if msg.get("sources"):
            conf = msg.get("confidence", 0)
            conf_cls = "conf-high" if conf > 0.8 else "conf-med" if conf > 0.5 else "conf-low"
            st.markdown(
                f'<span style="color:#718096;font-size:0.8rem;">📎 Sources '
                f'<span class="confidence-pill {conf_cls}">Confidence: {conf:.0%}</span></span>',
                unsafe_allow_html=True,
            )
            for src in msg["sources"]:
                st.markdown(f"""
                <div class="source-card">
                    <span class="source-title">📖 {src['title']}</span>
                    <span class="source-meta"> — {src['source']}</span>
                    <span class="source-meta" style="margin-left:8px;">Relevance: {src['relevance']:.0%}</span>
                </div>
                """, unsafe_allow_html=True)

# ── Handle Pending Query from Suggestion Button ──────────────
pending = st.session_state.pop("pending_query", None)
if pending:
    # Add user message
    st.session_state.chat_messages.append({"role": "user", "content": pending})
    rag.add_to_history(pending, "")

    with st.spinner("🔍 Searching knowledge base..."):
        response = rag.generate_response(pending)

    assistant_msg = {
        "role": "assistant",
        "content": response["answer"],
        "sources": response["sources"],
        "confidence": response["confidence"],
    }
    st.session_state.chat_messages.append(assistant_msg)
    rag.add_to_history(pending, response["answer"])
    st.rerun()

# ── Chat Input ───────────────────────────────────────────────
st.markdown("---")

with st.form("chat_form", clear_on_submit=True):
    query = st.text_area(
        "Ask a tax question:",
        placeholder="e.g., What are the TDS rates for professional services under Section 194J?",
        height=80,
        label_visibility="collapsed",
    )
    submitted = st.form_submit_button("🚀 Send Question", type="primary", use_container_width=True)

if submitted and query.strip():
    # Add user message
    st.session_state.chat_messages.append({"role": "user", "content": query})
    rag.add_to_history(query, "")

    with st.spinner("🔍 Searching knowledge base & generating response..."):
        response = rag.generate_response(query)

    assistant_msg = {
        "role": "assistant",
        "content": response["answer"],
        "sources": response["sources"],
        "confidence": response["confidence"],
    }
    st.session_state.chat_messages.append(assistant_msg)
    rag.add_to_history(query, response["answer"])
    st.rerun()
