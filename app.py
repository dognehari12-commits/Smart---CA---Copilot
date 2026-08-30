import streamlit as st

# Page setup
st.set_page_config(
    page_title="Smart CA Copilot",
    page_icon="💼",
    layout="wide"
)

# App Title & Header
st.title("💼 Smart CA Copilot")
st.subheader("Welcome to your AI-powered Financial & Tax Assistant")

st.markdown("---")

# Quick Guidance Banner
st.success("✅ App Successfully Connected!")

st.info("""
👈 **नेविगेशन गाइड:** 
स्क्रीन पर बाईं तरफ दिए गए **Sidebar Menu** से अपना पसंदीदा मॉड्यूल चुनें:
* **📄 Document OCR** - Invoices & Financial Statements एक्सट्रैक्ट करने के लिए।
* **🤖 AI Tax Search** - RAG-powered Tax Queries के लिए।
* **📑 Report Generator** - PDF Financial Reports डाउनलोड करने के लिए।
* **📊 Client Dashboard** - Client Overview & Financial KPIs देखने के लिए।
""")

st.markdown("---")

# Quick Features Breakdown (Visual Cards)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### 📄 Document OCR")
    st.caption("Upload invoices & bank statements for AI extraction.")

with col2:
    st.markdown("### 🤖 AI Tax Search")
    st.caption("Ask complex tax questions with instant RAG citations.")

with col3:
    st.markdown("### 📑 Report Generator")
    st.caption("Generate & export professional PDF financial reports.")

with col4:
    st.markdown("### 📊 Deep Analytics")
    st.caption("Explore interactive financial charts and client KPIs.")
