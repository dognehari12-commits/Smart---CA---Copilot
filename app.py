import streamlit as st
import importlib

st.set_page_config(page_title="Smart CA Copilot", layout="wide", initial_sidebar_state="expanded")

# Sidebar for direct navigation
st.sidebar.title("📌 Navigation Menu")
selected_page = st.sidebar.radio(
    "Select Module:",
    ["Home", "Document OCR", "AI Tax Search", "Report Generator", "Client Dashboard"]
)

# Helper function to dynamically run files
def load_module(file_name):
    module_name = file_name.replace(".py", "")
    module = importlib.import_module(module_name)
    if hasattr(module, "main"):
        module.main()

if selected_page == "Home":
    st.title("💼 Smart CA Copilot")
    st.write("Welcome! Click any option below or use the sidebar menu to navigate:")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("### 📄 Document OCR")
        st.caption("Upload invoices & bank statements for AI extraction.")
        if st.button("Open Document OCR ➔", key="ocr_btn", use_container_width=True):
            st.session_state["nav_choice"] = "Document OCR"
            st.rerun()

    with col2:
        st.markdown("### 🤖 AI Tax Search")
        st.caption("Ask complex tax questions with instant RAG citations.")
        if st.button("Open AI Tax Search ➔", key="tax_btn", use_container_width=True):
            st.session_state["nav_choice"] = "AI Tax Search"
            st.rerun()

    with col3:
        st.markdown("### 📑 Report Generator")
        st.caption("Generate & export professional PDF financial reports.")
        if st.button("Open Report Generator ➔", key="rep_btn", use_container_width=True):
            st.session_state["nav_choice"] = "Report Generator"
            st.rerun()

    with col4:
        st.markdown("### 📊 Deep Analytics")
        st.caption("Explore interactive financial charts and client KPIs.")
        if st.button("Open Dashboard ➔", key="dash_btn", use_container_width=True):
            st.session_state["nav_choice"] = "Client Dashboard"
            st.rerun()

# Check session state for button clicks
if "nav_choice" in st.session_state:
    selected_page = st.session_state.pop("nav_choice")

# Load respective file modules
if selected_page == "Document OCR":
    load_module("1_Document_OCR.py")
elif selected_page == "AI Tax Search":
    load_module("2_AI_Tax_Search.py")
elif selected_page == "Report Generator":
    load_module("3_Report_Generator.py")
elif selected_page == "Client Dashboard":
    load_module("4_Client_Dashboard.py")
