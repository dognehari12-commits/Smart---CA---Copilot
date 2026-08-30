import streamlit as st

st.set_page_config(page_title="Smart CA Copilot", layout="wide")

# 1. Define Page Functions using st.Page
dashboard = st.Page("pages/4_📊_Client_Dashboard.py", title="Dashboard", icon="📊", default=True)
ocr_page = st.Page("pages/1_📄_Document_OCR.py", title="Document OCR", icon="📄")
tax_page = st.Page("pages/2_🤖_AI_Tax_Search.py", title="AI Tax Search", icon="🤖")
report_page = st.Page("pages/3_📑_Report_Generator.py", title="Report Generator", icon="📑")

# 2. Setup Navigation Menu (Shows in Left Sidebar)
pg = st.navigation({
    "Modules": [dashboard, ocr_page, tax_page, report_page]
})

# 3. Add Quick Action Buttons to Home/Dashboard View
# (If current page is Dashboard, show quick navigation cards/buttons)
st.title("💼 Smart CA Copilot")

st.markdown("### 🚀 Quick Actions")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("Document OCR")
    st.write("Upload invoices & statements")
    if st.button("Open OCR", key="btn_ocr"):
        st.switch_page(ocr_page)

with col2:
    st.subheader("AI Tax Search")
    st.write("Ask tax questions with RAG")
    if st.button("Open Tax Search", key="btn_tax"):
        st.switch_page(tax_page)

with col3:
    st.subheader("Report Generator")
    st.write("Generate PDF reports")
    if st.button("Open Generator", key="btn_report"):
        st.switch_page(report_page)

with col4:
    st.subheader("Deep Analytics")
    st.write("Explore financial charts")
    if st.button("Open Analytics", key="btn_dash"):
        st.switch_page(dashboard)

st.markdown("---")

# 4. Run the active page
pg.run()
