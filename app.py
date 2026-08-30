import streamlit as st

st.set_page_config(page_title="Smart CA Copilot", layout="wide", initial_sidebar_state="expanded")

st.title("💼 Smart CA Copilot")
st.write("नीचे दिए गए किसी भी मॉड्यूल पर जाने के लिए उसके बटन पर क्लिक करें:")

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### 📄 Document OCR")
    st.caption("Upload invoices & bank statements for AI extraction.")
    if st.button("Open Document OCR ➔", key="ocr_btn", use_container_width=True):
        st.switch_page("1_Document_OCR.py")

with col2:
    st.markdown("### 🤖 AI Tax Search")
    st.caption("Ask complex tax questions with instant RAG citations.")
    if st.button("Open AI Tax Search ➔", key="tax_btn", use_container_width=True):
        st.switch_page("2_AI_Tax_Search.py")

with col3:
    st.markdown("### 📑 Report Generator")
    st.caption("Generate & export professional PDF financial reports.")
    if st.button("Open Report Generator ➔", key="rep_btn", use_container_width=True):
        st.switch_page("3_Report_Generator.py")

with col4:
    st.markdown("### 📊 Deep Analytics")
    st.caption("Explore interactive financial charts and client KPIs.")
    if st.button("Open Dashboard ➔", key="dash_btn", use_container_width=True):
        st.switch_page("4_Client_Dashboard.py")
