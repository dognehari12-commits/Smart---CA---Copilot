"""Page: Client Portal & Dashboard."""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from data.sample_data import CLIENTS, get_financial_summary, get_gst_returns, SAMPLE_INVOICES, TAX_TYPES

st.set_page_config(page_title="Client Dashboard — CA Copilot", page_icon="📊", layout="wide")

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
        background: linear-gradient(135deg, #2E86C1 0%, #9B59B6 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 2rem; font-weight: 800; margin-bottom: 0.2rem;
    }
    .page-sub { color: #A0AEC0; font-size: 0.95rem; margin-bottom: 1.5rem; }
    .section-header {
        color: #E2E8F0; font-size: 1.1rem; font-weight: 700;
        border-bottom: 2px solid #2E86C1; padding-bottom: 0.4rem; margin: 1.2rem 0 0.8rem 0;
    }
    .kpi-card {
        background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%);
        border: 1px solid #2D3748; border-radius: 14px;
        padding: 1.2rem 1.4rem; text-align: center;
        transition: transform 0.2s, border-color 0.2s;
    }
    .kpi-card:hover { transform: translateY(-3px); border-color: #2E86C1; }
    .kpi-icon { font-size: 1.6rem; margin-bottom: 0.2rem; }
    .kpi-value { font-size: 1.5rem; font-weight: 700; color: #E2E8F0; margin: 0.15rem 0; }
    .kpi-label { font-size: 0.75rem; color: #718096; text-transform: uppercase; letter-spacing: 0.5px; }
    .kpi-change { font-size: 0.72rem; margin-top: 0.2rem; }
    .kpi-up { color: #27AE60; }
    .kpi-down { color: #E74C3C; }
    .data-table { width: 100%; border-collapse: collapse; }
    .data-table th {
        background: #1E3A5F; color: #E2E8F0; padding: 9px 12px; text-align: left;
        font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.3px;
    }
    .data-table td {
        padding: 9px 12px; border-bottom: 1px solid #2D3748;
        color: #CBD5E0; font-size: 0.82rem;
    }
    .data-table tr:hover td { background: rgba(46,134,193,0.04); }
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
st.markdown('<div class="page-header">📊 Client Portal & Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Interactive financial analytics, charts, and detailed insights for your clients.</div>', unsafe_allow_html=True)

# ── Client Selector ──────────────────────────────────────────
client_names = [c["name"] for c in CLIENTS]
selected_name = st.selectbox("Select Client for Deep Analytics", client_names)
client = next(c for c in CLIENTS if c["name"] == selected_name)
client_id = client["client_id"]

# ── Load Data ────────────────────────────────────────────────
fin = get_financial_summary(client_id)
gst_data = get_gst_returns(client_id)

total_revenue = sum(fin["revenue"])
total_expenses = sum(fin["total_expenses"])
total_profit_before_tax = sum(fin["profit_before_tax"])
total_tax = sum(sum(v) for v in fin["taxes"].values())
net_profit = sum(fin["net_profit"])
profit_margin = (net_profit / total_revenue * 100) if total_revenue else 0
effective_tax_rate = (total_tax / total_profit_before_tax * 100) if total_profit_before_tax else 0
expense_ratio = (total_expenses / total_revenue * 100) if total_revenue else 0

# ── Top KPIs ─────────────────────────────────────────────────
k1, k2, k3, k4, k5, k6 = st.columns(6)
kpis = [
    ("💰", "Revenue", f"₹{total_revenue/10000000:.2f}Cr", "↑ 12.3%", "up"),
    ("📉", "Expenses", f"₹{total_expenses/10000000:.2f}Cr", f"{expense_ratio:.1f}%", "down"),
    ("📊", "Net Profit", f"₹{net_profit/10000000:.2f}Cr", f"{profit_margin:.1f}%", "up" if profit_margin > 10 else "down"),
    ("🏛️", "Tax Paid", f"₹{total_tax/100000:.1f}L", f"{effective_tax_rate:.1f}%", ""),
    ("📈", "Profit Margin", f"{profit_margin:.1f}%", "Target: 15%", "up" if profit_margin > 15 else "down"),
    ("📋", "GST Filed", f"{sum(1 for g in gst_data if g['filing_status']=='Filed')}/12", "months", "up"),
]
for col, (icon, label, value, change, direction) in zip([k1, k2, k3, k4, k5, k6], kpis):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-change kpi-{direction}">{change}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts Row 1: Revenue / Expenses / Profit ────────────────
st.markdown('<div class="section-header">📈 Monthly Financial Performance</div>', unsafe_allow_html=True)

fig1 = make_subplots(
    rows=1, cols=2,
    subplot_titles=("Revenue vs Expenses vs Profit", "Cumulative Net Profit"),
    specs=[[{"type": "bar"}, {"type": "scatter"}]],
)

# Bar chart
fig1.add_trace(go.Bar(
    name="Revenue", x=fin["months"], y=fin["revenue"],
    marker_color="#2E86C1", opacity=0.9,
), row=1, col=1)
fig1.add_trace(go.Bar(
    name="Expenses", x=fin["months"], y=fin["total_expenses"],
    marker_color="#E74C3C", opacity=0.7,
), row=1, col=1)
fig1.add_trace(go.Scatter(
    name="Profit", x=fin["months"], y=fin["profit_before_tax"],
    mode="lines+markers", line=dict(color="#27AE60", width=2),
), row=1, col=1)

# Cumulative profit
cum_profit = np.cumsum(fin["net_profit"]).tolist()
fig1.add_trace(go.Scatter(
    x=fin["months"], y=cum_profit,
    mode="lines+markers",
    line=dict(color="#27AE60", width=3),
    fill="tozeroy",
    fillcolor="rgba(39,174,96,0.1)",
    name="Cumulative Net Profit",
), row=1, col=2)

fig1.update_layout(
    barmode="group",
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#A0AEC0"),
    legend=dict(orientation="h", y=1.12),
    height=380,
    margin=dict(l=50, r=30, t=50, b=50),
)
fig1.update_xaxes(gridcolor="#2D3748")
fig1.update_yaxes(gridcolor="#2D3748")
st.plotly_chart(fig1, use_container_width=True)

# ── Charts Row 2: Breakdown Pies ─────────────────────────────
st.markdown('<div class="section-header">🍩 Financial Breakdowns</div>', unsafe_allow_html=True)

col_exp, col_tax, col_income = st.columns(3)

with col_exp:
    exp_totals = {cat: sum(vals) for cat, vals in fin["expenses"].items()}
    exp_sorted = dict(sorted(exp_totals.items(), key=lambda x: x[1], reverse=True))
    fig_exp = px.pie(
        names=list(exp_sorted.keys()),
        values=list(exp_sorted.values()),
        hole=0.5,
        color_discrete_sequence=[
            "#2E86C1", "#27AE60", "#E74C3C", "#F39C12", "#9B59B6",
            "#1ABC9C", "#E67E22", "#34495E", "#16A085",
        ],
    )
    fig_exp.update_layout(
        title="Expense Distribution",
        title_font=dict(color="#E2E8F0", size=14),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#A0AEC0", size=10),
        margin=dict(l=10, r=10, t=40, b=10),
        height=320,
        showlegend=True,
        legend=dict(font=dict(size=8)),
    )
    st.plotly_chart(fig_exp, use_container_width=True)

with col_tax:
    tax_totals = {t: sum(v) for t, v in fin["taxes"].items()}
    fig_tax = px.pie(
        names=list(tax_totals.keys()),
        values=list(tax_totals.values()),
        hole=0.45,
        color_discrete_sequence=["#E74C3C", "#F39C12", "#2E86C1", "#27AE60", "#9B59B6"],
    )
    fig_tax.update_layout(
        title="Tax Liability Breakdown",
        title_font=dict(color="#E2E8F0", size=14),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#A0AEC0", size=10),
        margin=dict(l=10, r=10, t=40, b=10),
        height=320,
        showlegend=True,
        legend=dict(font=dict(size=8)),
    )
    st.plotly_chart(fig_tax, use_container_width=True)

with col_income:
    income_data = {
        "Category": ["Revenue", "Total Expenses", "Tax Paid", "Net Profit"],
        "Amount (₹ Cr)": [
            total_revenue / 10000000,
            total_expenses / 10000000,
            total_tax / 10000000,
            net_profit / 10000000,
        ],
        "Color": ["#2E86C1", "#E74C3C", "#F39C12", "#27AE60"],
    }
    fig_inc = go.Figure(go.Bar(
        x=income_data["Amount (₹ Cr)"],
        y=income_data["Category"],
        orientation="h",
        marker_color=income_data["Color"],
        text=[f"₹{v:.2f} Cr" for v in income_data["Amount (₹ Cr)"]],
        textposition="auto",
    ))
    fig_inc.update_layout(
        title="Income Waterfall",
        title_font=dict(color="#E2E8F0", size=14),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#A0AEC0"),
        margin=dict(l=10, r=10, t=40, b=10),
        height=320,
        xaxis=dict(gridcolor="#2D3748"),
    )
    st.plotly_chart(fig_inc, use_container_width=True)

# ── Charts Row 3: GST & Tax Analysis ─────────────────────────
st.markdown('<div class="section-header">🏛️ GST Compliance & Tax Analysis</div>', unsafe_allow_html=True)

col_gst_chart, col_gst_table = st.columns([3, 2])

with col_gst_chart:
    fig_gst = go.Figure()
    fig_gst.add_trace(go.Bar(
        name="Output GST", x=[r["month"] for r in gst_data], y=[r["output_gst"] for r in gst_data],
        marker_color="#E74C3C", opacity=0.8,
    ))
    fig_gst.add_trace(go.Bar(
        name="Input GST (ITC)", x=[r["month"] for r in gst_data], y=[r["input_gst"] for r in gst_data],
        marker_color="#27AE60", opacity=0.8,
    ))
    fig_gst.add_trace(go.Scatter(
        name="Net Payable", x=[r["month"] for r in gst_data], y=[r["net_gst_payable"] for r in gst_data],
        mode="lines+markers",
        line=dict(color="#F39C12", width=2, dash="dot"),
    ))
    fig_gst.update_layout(
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#A0AEC0"),
        legend=dict(orientation="h", y=1.15),
        height=350,
        margin=dict(l=50, r=20, t=40, b=60),
        xaxis=dict(gridcolor="#2D3748"),
        yaxis=dict(gridcolor="#2D3748"),
    )
    st.plotly_chart(fig_gst, use_container_width=True)

with col_gst_table:
    st.markdown("#### GST Filing Status")
    gst_df = pd.DataFrame(gst_data)
    gst_display = gst_df[["month", "net_gst_payable", "filing_status"]].copy()
    gst_display.columns = ["Month", "Net GST (₹)", "Status"]
    gst_display["Net GST (₹)"] = gst_display["Net GST (₹)"].apply(lambda x: f"₹{x:,}")

    def fmt_status(s):
        cls = "badge-paid" if s == "Filed" else "badge-pending"
        return f'<span class="{cls}">{s}</span>'

    gst_display["Status"] = gst_display["Status"].apply(fmt_status)
    st.markdown(gst_display.to_html(escape=False, index=False, classes="data-table"), unsafe_allow_html=True)

# ── Charts Row 4: Monthly Expense Stacked Bar ────────────────
st.markdown('<div class="section-header">📊 Monthly Expense Categories (Stacked)</div>', unsafe_allow_html=True)

fig_stack = go.Figure()
colors = ["#2E86C1", "#27AE60", "#E74C3C", "#F39C12", "#9B59B6",
          "#1ABC9C", "#E67E22", "#34495E", "#16A085"]
for i, (cat, vals) in enumerate(fin["expenses"].items()):
    fig_stack.add_trace(go.Bar(
        name=cat, x=fin["months"], y=vals,
        marker_color=colors[i % len(colors)],
    ))

fig_stack.update_layout(
    barmode="stack",
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#A0AEC0"),
    legend=dict(orientation="h", y=1.25, font=dict(size=9)),
    height=400,
    margin=dict(l=50, r=20, t=40, b=50),
    xaxis=dict(gridcolor="#2D3748"),
    yaxis=dict(gridcolor="#2D3748", title="Amount (₹)"),
)
st.plotly_chart(fig_stack, use_container_width=True)

# ── Detailed Data Tables ─────────────────────────────────────
st.markdown('<div class="section-header">📋 Detailed Monthly Data</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["💰 P&L Summary", "🏛️ Tax Breakdown", "📄 Invoice Tracker"])

with tab1:
    pnl_df = pd.DataFrame({
        "Month": fin["months"],
        "Revenue": [f"₹{r:,.0f}" for r in fin["revenue"]],
        "Expenses": [f"₹{e:,.0f}" for e in fin["total_expenses"]],
        "Profit Before Tax": [f"₹{p:,.0f}" for p in fin["profit_before_tax"]],
        "Net Profit": [f"₹{n:,.0f}" for n in fin["net_profit"]],
        "Margin": [f"{(n/r*100):.1f}%" if r > 0 else "N/A" for n, r in zip(fin["net_profit"], fin["revenue"])],
    })
    st.markdown(pnl_df.to_html(escape=False, index=False, classes="data-table"), unsafe_allow_html=True)

with tab2:
    tax_df = pd.DataFrame({
        "Month": fin["months"],
        **{t: [f"₹{v[i]:,.0f}" for i in range(12)] for t, v in fin["taxes"].items()},
        "Total": [f"₹{sum(fin['taxes'][t][i] for t in fin['taxes']):,.0f}" for i in range(12)],
    })
    st.markdown(tax_df.to_html(escape=False, index=False, classes="data-table"), unsafe_allow_html=True)

with tab3:
    inv_df = pd.DataFrame(SAMPLE_INVOICES)
    inv_df["amount"] = inv_df["amount"].apply(lambda x: f"₹{x:,.0f}")
    inv_df["tax"] = inv_df["tax"].apply(lambda x: f"₹{x:,.0f}")

    def status_badge(s):
        cls = {"Paid": "badge-paid", "Pending": "badge-pending", "Overdue": "badge-overdue"}.get(s, "badge-pending")
        return f'<span class="{cls}">{s}</span>'

    inv_df["status"] = inv_df["status"].apply(status_badge)
    inv_df.columns = ["Invoice No.", "Date", "Vendor", "Amount", "Tax (GST)", "Category", "Status"]
    st.markdown(inv_df.to_html(escape=False, index=False, classes="data-table"), unsafe_allow_html=True)
