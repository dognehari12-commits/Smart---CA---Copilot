"""Page: Smart Document OCR & Parser."""

import streamlit as st
import json
import pandas as pd
from utils.ocr_engine import OCREngine
from data.sample_data import EXTRACTED_DOCUMENTS

st.set_page_config(page_title="Document OCR — CA Copilot", page_icon="📄", layout="wide")

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
        background: linear-gradient(135deg, #F39C12 0%, #E67E22 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 2rem; font-weight: 800; margin-bottom: 0.2rem;
    }
    .page-sub { color: #A0AEC0; font-size: 0.95rem; margin-bottom: 1.5rem; }
    .section-header {
        color: #E2E8F0; font-size: 1.1rem; font-weight: 700;
        border-bottom: 2px solid #F39C12; padding-bottom: 0.4rem; margin: 1.2rem 0 0.8rem 0;
    }
    .extracted-card {
        background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%);
        border: 1px solid #2D3748; border-radius: 14px; padding: 1.2rem 1.5rem;
        margin-bottom: 0.8rem;
    }
    .field-label { color: #718096; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.5px; }
    .field-value { color: #E2E8F0; font-size: 1rem; font-weight: 600; }
    .confidence-badge {
        display: inline-block; padding: 3px 12px; border-radius: 12px;
        font-size: 0.75rem; font-weight: 700;
    }
    .conf-high { background: rgba(39,174,96,0.15); color: #27AE60; }
    .conf-med { background: rgba(243,156,18,0.15); color: #F39C12; }
    .conf-low { background: rgba(231,76,60,0.15); color: #E74C3C; }
    .data-table { width: 100%; border-collapse: collapse; }
    .data-table th {
        background: #1E3A5F; color: #E2E8F0; padding: 8px 12px; text-align: left;
        font-size: 0.8rem; text-transform: uppercase;
    }
    .data-table td {
        padding: 8px 12px; border-bottom: 1px solid #2D3748; color: #CBD5E0; font-size: 0.82rem;
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
st.markdown('<div class="page-header">📄 Smart Document OCR & Parser</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Upload invoices, bank statements, or payroll data — AI extracts structured information automatically.</div>', unsafe_allow_html=True)

# ── Layout ───────────────────────────────────────────────────
col_upload, col_results = st.columns([1, 2])

with col_upload:
    st.markdown('<div class="section-header">📤 Upload Document</div>', unsafe_allow_html=True)

    upload_mode = st.radio(
        "Choose input method:",
        ["📁 Upload File", "📋 Paste Text", "🧪 Use Sample Data"],
        horizontal=True,
    )

    extracted_data = None

    if upload_mode == "📁 Upload File":
        uploaded = st.file_uploader(
            "Upload PDF, Image, or Text file",
            type=["pdf", "png", "jpg", "jpeg", "txt", "csv"],
            help="Supported: PDF, Images (PNG/JPG), Text files, CSV",
        )
        if uploaded:
            with st.spinner("🔍 Analyzing document..."):
                raw_bytes = uploaded.read()
                file_text = ""
                if uploaded.type == "text/plain" or uploaded.name.endswith((".txt", ".csv")):
                    try:
                        file_text = raw_bytes.decode("utf-8", errors="replace")
                    except Exception:
                        file_text = ""
                extracted_data = OCREngine.process_upload(
                    uploaded.name, file_bytes=raw_bytes, file_text=file_text,
                )
                st.success(f"✅ Processed: {uploaded.name}")

    elif upload_mode == "📋 Paste Text":
        text_input = st.text_area(
            "Paste invoice or document text here",
            height=200,
            placeholder="Paste raw text from an invoice, bank statement, or financial document...",
        )
        if st.button("🔍 Extract Data", type="primary"):
            if text_input.strip():
                with st.spinner("🔍 Parsing text..."):
                    extracted_data = OCREngine.process_upload("pasted_text.txt", file_text=text_input)
            else:
                st.warning("Please paste some text to extract.")

    else:  # Sample Data
        st.info("Select a sample document below to see the AI extraction in action.")
        sample_names = [d["filename"] for d in EXTRACTED_DOCUMENTS]
        selected_sample = st.selectbox("Sample documents:", sample_names)
        if st.button("🧠 Extract Sample Data", type="primary"):
            with st.spinner("🔍 Processing sample document..."):
                extracted_data = OCREngine.process_upload(selected_sample)

    # Store in session state
    if extracted_data:
        st.session_state["ocr_result"] = extracted_data

# ── Results Panel ────────────────────────────────────────────
with col_results:
    st.markdown('<div class="section-header">📋 Extraction Results</div>', unsafe_allow_html=True)

    result = st.session_state.get("ocr_result")

    if not result:
        st.info("👆 Upload a document or select a sample to see extracted data here.")
        st.markdown("""
        ### 🔎 Supported Document Types
        | Type | Extracted Fields |
        |------|-----------------|
        | 📄 **Invoices** | Invoice #, Date, Vendor, Amounts, GST, Line Items |
        | 🏦 **Bank Statements** | Account, Period, Balances, Transactions |
        | 👥 **Payroll Register** | Employees, Salary, EPF, ESI, TDS |
        | 🏛️ **GST Returns** | Turnover, Output/Input GST, Net Payable |
        """)
    elif not result.get("success"):
        st.error(f"❌ {result.get('error', 'Extraction failed')}")
    else:
        data = result["extracted_data"]
        conf = result.get("confidence", 0)

        # Header info
        st.markdown(f"""
        <div class="extracted-card" style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span class="field-label">Document Type</span><br>
                <span class="field-value">{result['doc_type']}</span>
            </div>
            <div>
                <span class="field-label">Confidence</span><br>
                <span class="confidence-badge {'conf-high' if conf > 0.9 else 'conf-med' if conf > 0.7 else 'conf-low'}">
                    {conf:.0%}
                </span>
            </div>
            <div>
                <span class="field-label">Source</span><br>
                <span class="field-value">{result.get('source', 'N/A').replace('_', ' ').title()}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Display fields based on document type
        if result["doc_type"] == "Invoice":
            st.markdown("#### Invoice Details")
            inv_cols = st.columns(3)
            fields = [
                ("Invoice No.", data.get("invoice_number", "N/A")),
                ("Date", data.get("date", "N/A")),
                ("Vendor", data.get("vendor_name", "N/A")),
                ("Client", data.get("client_name", "N/A")),
                ("Subtotal", f"₹{data.get('subtotal', 0):,.0f}"),
                ("Total GST", f"₹{data.get('total_gst', 0):,.0f}"),
            ]
            for i, (label, value) in enumerate(fields):
                with inv_cols[i % 3]:
                    st.markdown(f"**{label}**")
                    st.markdown(f"`{value}`")

            st.markdown(f"**💰 Total Amount: ₹{data.get('total_amount', 0):,.0f}**")

            if "line_items" in data:
                st.markdown("##### Line Items")
                items_df = pd.DataFrame(data["line_items"])
                st.dataframe(items_df, use_container_width=True)

        elif result["doc_type"] == "Bank Statement":
            st.markdown("#### Bank Statement Summary")
            bank_cols = st.columns(3)
            bank_fields = [
                ("Bank", data.get("bank", "N/A")),
                ("Account", data.get("account_number", "N/A")),
                ("Period", data.get("statement_period", "N/A")),
                ("Opening Balance", f"₹{data.get('opening_balance', 0):,.0f}"),
                ("Closing Balance", f"₹{data.get('closing_balance', 0):,.0f}"),
                ("Net Movement", f"₹{(data.get('closing_balance', 0) - data.get('opening_balance', 0)):,.0f}"),
            ]
            for i, (label, value) in enumerate(bank_fields):
                with bank_cols[i % 3]:
                    st.markdown(f"**{label}**")
                    st.markdown(f"`{value}`")

            if "key_transactions" in data:
                st.markdown("##### Key Transactions")
                txn_df = pd.DataFrame(data["key_transactions"])
                st.dataframe(txn_df, use_container_width=True)

        elif result["doc_type"] == "Payroll Register":
            st.markdown("#### Payroll Summary")
            pay_cols = st.columns(3)
            pay_fields = [
                ("Period", data.get("period", "N/A")),
                ("Employees", data.get("total_employees", "N/A")),
                ("Gross Salary", f"₹{data.get('gross_salary', 0):,.0f}"),
                ("EPF", f"₹{data.get('epf_contribution', 0):,.0f}"),
                ("ESI", f"₹{data.get('esi_contribution', 0):,.0f}"),
                ("TDS Deducted", f"₹{data.get('tds_deducted', 0):,.0f}"),
                ("Net Paid", f"₹{data.get('net_salary_paid', 0):,.0f}"),
                ("Prof. Tax", f"₹{data.get('professional_tax', 0):,.0f}"),
            ]
            for i, (label, value) in enumerate(pay_fields):
                with pay_cols[i % 3]:
                    st.markdown(f"**{label}**")
                    st.markdown(f"`{value}`")

        elif result["doc_type"] == "GST Return (GSTR-3B)":
            st.markdown("#### GST Return (GSTR-3B)")
            gst_cols = st.columns(3)
            gst_fields = [
                ("Return Period", data.get("return_period", "N/A")),
                ("GSTIN", data.get("gstin", "N/A")),
                ("Total Outward", f"₹{data.get('total_outward_supply', 0):,.0f}"),
                ("Output CGST", f"₹{data.get('output_cgst', 0):,.0f}"),
                ("Output SGST", f"₹{data.get('output_sgst', 0):,.0f}"),
                ("Output IGST", f"₹{data.get('output_igst', 0):,.0f}"),
                ("Input CGST", f"₹{data.get('input_cgst', 0):,.0f}"),
                ("Input SGST", f"₹{data.get('input_sgst', 0):,.0f}"),
                ("Input IGST", f"₹{data.get('input_igst', 0):,.0f}"),
                ("Net CGST", f"₹{data.get('net_cgst_payable', 0):,.0f}"),
                ("Net SGST", f"₹{data.get('net_sgst_payable', 0):,.0f}"),
                ("Net IGST", f"₹{data.get('net_igst_payable', 0):,.0f}"),
                ("Total Tax Payable", f"₹{data.get('total_tax_payable', 0):,.0f}"),
                ("Filing Date", data.get("filing_date", "N/A")),
            ]
            for i, (label, value) in enumerate(gst_fields):
                with gst_cols[i % 3]:
                    st.markdown(f"**{label}**")
                    st.markdown(f"`{value}`")

        else:
            # Generic fallback
            st.markdown("#### Extracted Data")
            st.json(data)

        # JSON Export
        with st.expander("📦 Raw JSON Export"):
            st.json(data)
