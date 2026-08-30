import streamlit as st

st.set_page_config(page_title="Smart CA Copilot", layout="wide")

# Custom navigation menu
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio(
    "Go to page:",
    ["Dashboard", "Document OCR", "AI Tax Search", "Report Generator"]
)

if page == "Dashboard":
    # Executive / Main Dashboard View
    st.title("💼 Smart CA Copilot - Dashboard")
    
    st.markdown("### 🚀 Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.subheader("Document OCR")
        st.caption("Upload invoices & statements")
        
    with col2:
        st.subheader("AI Tax Search")
        st.caption("Ask tax questions with RAG")
        
    with col3:
        st.subheader("Report Generator")
        st.caption("Generate PDF reports")
        
    with col4:
        st.subheader("Deep Analytics")
        st.caption("Explore financial charts")
        
    st.info("👈 Select any feature from the sidebar menu on the left to get started!")

elif page == "Document OCR":
    st.switch_page("pages/1_📄_Document_OCR.py")

elif page == "AI Tax Search":
    st.switch_page("pages/2_🤖_AI_Tax_Search.py")

elif page == "Report Generator":
    st.switch_page("pages/3_📑_Report_Generator.py")
