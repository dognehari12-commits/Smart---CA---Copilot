import streamlit as st
import os

st.set_page_config(page_title="Smart CA Copilot", layout="wide", initial_sidebar_state="expanded")

# Get current directory path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Sidebar navigation
st.sidebar.title("📌 Navigation Menu")
selected_page = st.sidebar.radio(
    "Select Module:",
    ["Home", "Document OCR", "AI Tax Search", "Report Generator", "Client Dashboard"]
)

# Helper function to run scripts using dynamic absolute path
def run_script(file_name):
    # Check in root directory first, then in pages/ directory
    path_in_root = os.path.join(BASE_DIR, file_name)
    path_in_pages = os.path.join(BASE_DIR, "pages", file_name)
    
    if os.path.exists(path_in_root):
        file_path = path_in_root
    elif os.path.exists(path_in_pages):
        file_path = path_in_pages
    else:
        st.error(f"❌ Error: File '{file_name}' not found in root or 'pages/' folder.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()
    exec(code, globals())

# Session State sync for home buttons
if "nav_choice" in st.session_state:
    selected_page = st.session_state.pop("nav_choice")

if selected_page == "Home":
    st.title("💼 Smart CA Copilot")
    st.write("नीचे दिए गए किसी भी मॉड्यूल पर जाने के लिए उसके बटन पर क्लिक करें या Sidebar का उपयोग करें:")
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

elif selected_page == "Document OCR":
    run_script("1_Document_OCR.py")
elif selected_page == "AI Tax Search":
    run_script("2_AI_Tax_Search.py")
elif selected_page == "Report Generator":
    run_script("3_Report_Generator.py")
elif selected_page == "Client Dashboard":
    run_script("4_Client_Dashboard.py")
