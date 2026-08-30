"""Page: Automated Report Generator."""

import streamlit as st
from datetime import datetime
from data.sample_data import CLIENTS, get_financial_summary, get_gst_returns
from utils.report_generator import ReportGenerator

st.set_page_config(page_title="Report Generator — CA Copilot", page_icon="📑", layout="wide")

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
        background: linear-gradient(135deg, #27AE60 0%, #2E86C1 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 2rem; font-weight: 800; margin-bottom: 0.2rem;
    }
    .page-sub { color: #A0AEC0; font-size: 0.95rem; margin-bottom: 1.5rem; }
    .section-header {
        color: #E2E8F0; font-size: 1.1rem; font-weight: 700;
        border-bottom: 2px solid #27AE60; padding-bottom: 0.4rem; margin: 1.2rem 0 0.8rem 0;
    }
    .preview-card {
        background: linear-gradient(135deg, #1A1A2E, #16213E);
        border: 1px solid #2D3748; border-radius: 14px; padding: 1.5rem;
        text-align: center;
    }
    .preview-icon { font-size: 4rem; margin-bottom: 1rem; }
    .preview-title { color: #E2E8F0; font-size: 1.2rem; font-weight: 700; }
    .preview-sub { color: #718096; font-size: 0.85rem; margin-top: 0.5rem; }
    .checklist-item {
        display: flex; align-items: center; gap: 8px; padding: 6px 0;
        color: #CBD5E0; font-size: 0.88rem;
    }
    .check-yes { color: #27AE60; }
    .check-no { color: #E74C3C; }
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
st.markdown('<div class="page-header">📑 Automated Report Generator</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-sub">Generate professional PDF financial health reports with charts, tables, and recommendations.</div>',
    unsafe_allow_html=True,
)

# ── Configuration ────────────────────────────────────────────
col_config, col_preview = st.columns([1, 1])

with col_config:
    st.markdown('<div class="section-header">⚙️ Report Configuration</div>', unsafe_allow_html=True)

    # Client Selection
    client_names = [c["name"] for c in CLIENTS]
    selected_name = st.selectbox("Select Client", client_names)

    client = next(c for c in CLIENTS if c["name"] == selected_name)

    # Report options
    st.markdown("#### 📋 Report Sections")
    include_kpi = st.checkbox("Executive Summary & KPIs", value=True)
    include_revenue = st.checkbox("Revenue vs Expenses Charts", value=True)
    include_expense = st.checkbox("Expense Breakdown Pie Chart", value=True)
    include_tax = st.checkbox("Tax Liability Analysis", value=True)
    include_gst = st.checkbox("GST Compliance Summary", value=True)
    include_profit = st.checkbox("Profitability Trend", value=True)
    include_recs = st.checkbox("Recommendations & Observations", value=True)

    st.markdown("#### 🏢 Client Details")
    st.markdown(f"""
    | Field | Value |
    |-------|-------|
    | **Client** | {client['name']} |
    | **Type** | {client['type']} |
    | **PAN** | `{client['pan']}` |
    | **Industry** | {client['industry']} |
    | **Turnover** | ₹{client['annual_turnover']/10000000:.1f} Cr |
    | **Tax Regime** | {client['tax_regime']} |
    | **GST** | {'Registered ✅' if client['gst_registered'] else 'Not Registered ❌'} |
    """)

    # Generate button
    generate = st.button("🚀 Generate PDF Report", type="primary", use_container_width=True)

with col_preview:
    st.markdown('<div class="section-header">👁️ Report Preview</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="preview-card">
        <div class="preview-icon">📑</div>
        <div class="preview-title">Financial Health Report</div>
        <div class="preview-sub">A4 Format • Professional Layout • Charts & Tables</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### ✅ Report Contents")
    checklist = [
        ("Cover page with client details", include_kpi),
        ("Executive KPI summary cards", include_kpi),
        ("Monthly revenue vs expenses bar chart", include_revenue),
        ("Annual expense breakdown pie chart", include_expense),
        ("Tax liability breakdown pie chart", include_tax),
        ("GST compliance monthly table", include_gst),
        ("Net profit trend line chart", include_profit),
        ("Key observations & recommendations", include_recs),
        ("Professional disclaimer footer", True),
    ]
    for item, included in checklist:
        cls = "check-yes" if included else "check-no"
        icon = "✅" if included else "❌"
        st.markdown(f'<div class="checklist-item"><span class="{cls}">{icon}</span> {item}</div>', unsafe_allow_html=True)

# ── Generate Report ──────────────────────────────────────────
if generate:
    with st.spinner("📄 Generating PDF report..."):
        # Gather data
        fin_data = get_financial_summary(client["client_id"])
        gst_data = get_gst_returns(client["client_id"])

        generator = ReportGenerator()
        pdf_bytes = generator.generate_report(
            client_info=client,
            financial_data=fin_data,
            gst_returns=gst_data,
        )

    st.success(f"✅ Report generated successfully! ({len(pdf_bytes):,} bytes)")

    # Download button
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Financial_Report_{client['client_id']}_{timestamp}.pdf"

    st.download_button(
        label="📥 Download PDF Report",
        data=pdf_bytes,
        file_name=filename,
        mime="application/pdf",
        type="primary",
        use_container_width=True,
    )

    # Show summary stats
    st.markdown("---")
    st.markdown('<div class="section-header">📊 Report Summary</div>', unsafe_allow_html=True)

    total_rev = sum(fin_data["revenue"])
    total_exp = sum(fin_data["total_expenses"])
    total_tax = sum(sum(v) for v in fin_data["taxes"].values())
    net_p = total_rev - total_exp - total_tax

    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Revenue", f"₹{total_rev/10000000:.2f} Cr")
    s2.metric("Expenses", f"₹{total_exp/10000000:.2f} Cr")
    s3.metric("Tax Paid", f"₹{total_tax/100000:.1f}L")
    s4.metric("Net Profit", f"₹{net_p/10000000:.2f} Cr")
