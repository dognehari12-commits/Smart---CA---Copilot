"""Smart CA & Financial Advisor Copilot - Main Application."""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

from data.sample_data import CLIENTS, get_financial_summary, get_gst_returns, SAMPLE_INVOICES

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIG & DARK THEME
# ═══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Smart CA Copilot",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom Dark Theme CSS ────────────────────────────────────
st.markdown("""
<style>
    /* Global */
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

    /* Header */
    .main-header {
        background: linear-gradient(135deg, #1E3A5F 0%, #2E86C1 50%, #27AE60 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.4rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #A0AEC0;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%);
        border: 1px solid #2D3748;
        border-radius: 16px;
        padding: 1.3rem 1.5rem;
        text-align: center;
        transition: transform 0.2s, border-color 0.2s;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        border-color: #2E86C1;
    }
    .kpi-icon { font-size: 1.8rem; margin-bottom: 0.3rem; }
    .kpi-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #E2E8F0;
        margin: 0.2rem 0;
    }
    .kpi-label {
        font-size: 0.78rem;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-change {
        font-size: 0.75rem;
        margin-top: 0.3rem;
    }
    .kpi-up { color: #27AE60; }
    .kpi-down { color: #E74C3C; }

    /* Section Headers */
    .section-header {
        color: #E2E8F0;
        font-size: 1.15rem;
        font-weight: 700;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #2E86C1;
        margin: 1.5rem 0 1rem 0;
    }

    /* Feature Cards */
    .feature-card {
        background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%);
        border: 1px solid #2D3748;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s;
        cursor: pointer;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        border-color: #2E86C1;
        box-shadow: 0 8px 25px rgba(46, 134, 193, 0.15);
    }
    .feature-icon { font-size: 2.5rem; margin-bottom: 0.8rem; }
    .feature-title {
        color: #E2E8F0;
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
    }
    .feature-desc {
        color: #718096;
        font-size: 0.82rem;
        line-height: 1.5;
    }

    /* Tables */
    .data-table { width: 100%; border-collapse: collapse; }
    .data-table th {
        background: #1E3A5F;
        color: #E2E8F0;
        padding: 10px 14px;
        text-align: left;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .data-table td {
        padding: 10px 14px;
        border-bottom: 1px solid #2D3748;
        color: #CBD5E0;
        font-size: 0.85rem;
    }
    .data-table tr:hover td { background: rgba(46, 134, 193, 0.05); }

    /* Status badges */
    .badge-paid {
        background: rgba(39, 174, 96, 0.15);
        color: #27AE60;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-pending {
        background: rgba(243, 156, 18, 0.15);
        color: #F39C12;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-overdue {
        background: rgba(231, 76, 60, 0.15);
        color: #E74C3C;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background: #1A1A2E;
        color: #A0AEC0;
        border-radius: 8px 8px 0 0;
        border: 1px solid #2D3748;
        border-bottom: none;
        padding: 10px 24px;
    }
    .stTabs [aria-selected="true"] {
        background: #1E3A5F !important;
        color: #E2E8F0 !important;
        border-color: #2E86C1 !important;
    }

    /* Chat messages */
    .chat-user {
        background: linear-gradient(135deg, #1E3A5F, #2E86C1);
        color: #E2E8F0;
        padding: 12px 16px;
        border-radius: 16px 16px 4px 16px;
        margin: 8px 0;
        max-width: 80%;
        margin-left: auto;
    }
    .chat-ai {
        background: #1A1A2E;
        color: #CBD5E0;
        padding: 12px 16px;
        border-radius: 16px 16px 16px 4px;
        margin: 8px 0;
        max-width: 90%;
        border: 1px solid #2D3748;
    }

    /* Divider */
    hr {
        border: none;
        border-top: 1px solid #2D3748;
        margin: 1rem 0;
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


# ═══════════════════════════════════════════════════════════════
# SESSION STATE INIT
# ═══════════════════════════════════════════════════════════════

if "selected_client" not in st.session_state:
    st.session_state.selected_client = CLIENTS[0]


# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 🏛️ CA Copilot")
    st.markdown("---")

    # Client Selector
    st.markdown("### 👤 Select Client")
    client_names = [c["name"] for c in CLIENTS]
    selected_name = st.selectbox(
        "Active Client",
        client_names,
        index=client_names.index(st.session_state.selected_client["name"]),
        label_visibility="collapsed",
    )
    for c in CLIENTS:
        if c["name"] == selected_name:
            st.session_state.selected_client = c
            break

    st.markdown("---")
    st.markdown("### 🧭 Navigation")

    # Navigation info (actual navigation handled by Streamlit pages)
    st.markdown("""
    | Page | Description |
    |------|-------------|
    | 📊 **Dashboard** | Client overview & KPIs |
    | 📄 **Document OCR** | Upload & extract data |
    | 🤖 **AI Tax Search** | RAG-powered assistant |
    | 📑 **Report Generator** | Export PDF reports |
    """)

    st.markdown("---")

    # Active Client Info
    client = st.session_state.selected_client
    st.markdown("### 📋 Active Client")
    st.markdown(f"**{client['name']}**")
    st.caption(f"{client['type']} • {client['industry']}")
    st.caption(f"PAN: `{client['pan']}`")
    turnover = client['annual_turnover']
    st.metric("Annual Turnover", f"₹{turnover/10000000:.1f} Cr")

    if client["compliance_status"] == "Up to Date":
        st.success("✅ Compliance: Up to Date")
    elif client["compliance_status"] == "Pending Review":
        st.warning("⚠️ Compliance: Pending Review")
    else:
        st.error("🚨 Compliance: Defaulter Notice")

    st.markdown("---")
    st.caption("v2.0 • Smart CA Copilot")


# ═══════════════════════════════════════════════════════════════
# MAIN CONTENT — DASHBOARD LANDING
# ═══════════════════════════════════════════════════════════════

st.markdown('<div class="main-header">📊 Smart CA & Financial Advisor Copilot</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">Welcome back! Here\'s your overview for <b>{st.session_state.selected_client["name"]}</b>  •  FY 2025-26</div>', unsafe_allow_html=True)

# ── KPI Row ──────────────────────────────────────────────────
client_id = st.session_state.selected_client["client_id"]
fin = get_financial_summary(client_id)

total_revenue = sum(fin["revenue"])
total_expenses = sum(fin["total_expenses"])
total_profit = sum(fin["net_profit"])
total_tax = sum(sum(v) for v in fin["taxes"].values())
profit_margin = (total_profit / total_revenue * 100) if total_revenue else 0

c1, c2, c3, c4 = st.columns(4)
kpis = [
    ("💰", "Revenue", f"₹{total_revenue/10000000:.2f} Cr", "+12.3%", "up"),
    ("📉", "Total Expenses", f"₹{total_expenses/10000000:.2f} Cr", "+8.1%", "up"),
    ("📊", "Net Profit", f"₹{total_profit/10000000:.2f} Cr", "+15.7%", "up"),
    ("🏛️", "Tax Liability", f"₹{total_tax/100000:.1f}L", f"{profit_margin:.1f}%", "down" if profit_margin < 15 else "up"),
]
for col, (icon, label, value, change, direction) in zip([c1, c2, c3, c4], kpis):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-change kpi-{direction}">▲ {change}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts Row ───────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.markdown('<div class="section-header">📈 Monthly Revenue vs Expenses</div>', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Revenue", x=fin["months"], y=fin["revenue"],
        marker_color="#2E86C1", opacity=0.9,
    ))
    fig.add_trace(go.Bar(
        name="Expenses", x=fin["months"], y=fin["total_expenses"],
        marker_color="#E74C3C", opacity=0.7,
    ))
    fig.update_layout(
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#A0AEC0"),
        legend=dict(orientation="h", y=1.12),
        margin=dict(l=40, r=20, t=30, b=40),
        height=350,
    )
    fig.update_xaxes(gridcolor="#2D3748")
    fig.update_yaxes(gridcolor="#2D3748")
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.markdown('<div class="section-header">🍩 Expense Breakdown</div>', unsafe_allow_html=True)
    exp_totals = {cat: sum(vals) for cat, vals in fin["expenses"].items()}
    exp_sorted = dict(sorted(exp_totals.items(), key=lambda x: x[1], reverse=True))
    fig2 = px.pie(
        names=list(exp_sorted.keys()),
        values=list(exp_sorted.values()),
        hole=0.5,
        color_discrete_sequence=[
            "#2E86C1", "#27AE60", "#E74C3C", "#F39C12", "#9B59B6",
            "#1ABC9C", "#E67E22", "#34495E", "#16A085",
        ],
    )
    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#A0AEC0"),
        legend=dict(font=dict(size=9)),
        margin=dict(l=20, r=20, t=10, b=10),
        height=350,
        showlegend=True,
    )
    st.plotly_chart(fig2, use_container_width=True)

# ── Second Charts Row ────────────────────────────────────────
col_left2, col_right2 = st.columns(2)

with col_left2:
    st.markdown('<div class="section-header">🏛️ Tax Liability Breakdown</div>', unsafe_allow_html=True)
    tax_totals = {t: sum(v) for t, v in fin["taxes"].items()}
    fig3 = px.pie(
        names=list(tax_totals.keys()),
        values=list(tax_totals.values()),
        hole=0.45,
        color_discrete_sequence=["#E74C3C", "#F39C12", "#2E86C1", "#27AE60", "#9B59B6"],
    )
    fig3.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#A0AEC0"),
        margin=dict(l=20, r=20, t=10, b=10),
        height=350,
    )
    st.plotly_chart(fig3, use_container_width=True)

with col_right2:
    st.markdown('<div class="section-header">💰 Net Profit Trend</div>', unsafe_allow_html=True)
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(
        x=fin["months"], y=fin["net_profit"],
        mode="lines+markers",
        line=dict(color="#27AE60", width=3),
        marker=dict(size=8),
        fill="tozeroy",
        fillcolor="rgba(39,174,96,0.1)",
    ))
    fig4.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#A0AEC0"),
        margin=dict(l=40, r=20, t=10, b=40),
        height=350,
    )
    fig4.update_xaxes(gridcolor="#2D3748")
    fig4.update_yaxes(gridcolor="#2D3748")
    st.plotly_chart(fig4, use_container_width=True)

# ── Recent Invoices ──────────────────────────────────────────
st.markdown('<div class="section-header">📄 Recent Invoices</div>', unsafe_allow_html=True)
inv_df = pd.DataFrame(SAMPLE_INVOICES)
inv_df["amount"] = inv_df["amount"].apply(lambda x: f"₹{x:,.0f}")
inv_df["tax"] = inv_df["tax"].apply(lambda x: f"₹{x:,.0f}")

def status_badge(s):
    cls = {"Paid": "paid", "Pending": "pending", "Overdue": "overdue"}.get(s, "pending")
    return f'<span class="badge-{cls}">{s}</span>'

inv_df["status"] = inv_df["status"].apply(status_badge)
inv_df.columns = ["Invoice No.", "Date", "Vendor", "Amount", "Tax (GST)", "Category", "Status"]

st.markdown(
    inv_df.to_html(escape=False, index=False, classes="data-table"),
    unsafe_allow_html=True,
)

# ── Feature Cards ────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-header">🚀 Quick Actions</div>', unsafe_allow_html=True)

fc1, fc2, fc3, fc4 = st.columns(4)
features = [
    ("📄", "Document OCR", "Upload invoices & statements\nfor AI-powered extraction"),
    ("🤖", "AI Tax Search", "Ask tax questions with\nRAG-powered citations"),
    ("📑", "Report Generator", "Generate professional\nPDF financial reports"),
    ("📊", "Deep Analytics", "Explore detailed financial\ncharts & insights"),
]
for col, (icon, title, desc) in zip([fc1, fc2, fc3, fc4], features):
    with col:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">{icon}</div>
            <div class="feature-title">{title}</div>
            <div class="feature-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.caption("💡 Navigate using the sidebar or the pages dropdown to access each module.")
