🤖 Smart CA Copilot
An AI-powered Streamlit app designed to streamline tax research, automate financial document parsing, and generate structured reports for Chartered Accountants, auditors, and tax professionals.

Built using Python, Streamlit, and a RAG (Retrieval-Augmented Generation) architecture, this application reduces hours of manual tax analysis and data entry into a few simple clicks.

🌟 Key Features
🤖 AI Tax Search (RAG Engine): Query complex tax provisions and receive fast, accurate answers backed by real-time citations using advanced LLM retrieval.

📄 Document OCR Extraction: Extract key data seamlessly from invoices, receipts, and bank statements without manual entry.

📑 Automated Report Generator: Swiftly generate structured, exportable financial reports for client deliverables.

📊 Client Analytics Dashboard: View interactive financial insights and track critical metrics in real time.

📁 Repository Structure
Plaintext
smart-ca-copilot/
├── app.py                     # Main application entry point
├── requirements.txt           # Python dependencies
├── __init__.py                # Package initializer
├── data/
│   └── sample_data.py         # Mock tax & client datasets
├── pages/
│   ├── 1_Document_OCR.py      # OCR Document Extractor Page
│   ├── 2_AI_Tax_Search.py     # RAG Tax Search Page
│   ├── 3_Report_Generator.py  # Automated Report Generator Page
│   └── 4_Client_Dashboard.py  # Financial Analytics Dashboard Page
└── utils/
    ├── __init__.py
    ├── ocr_engine.py          # Image & PDF OCR processing module
    ├── rag_engine.py          # RAG pipeline implementation
    └── report_generator.py   # PDF & text report formatting engine
🛠️ Installation & Setup
1. Clone the Repository
Bash
git clone https://github.com/YOUR-USERNAME/smart-ca-copilot.git
cd smart-ca-copilot
2. Create & Activate a Virtual Environment
Bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
Bash
pip install -r requirements.txt
4. Run the Streamlit App
Bash
streamlit run app.py
🚀 Live Demo
Web App: Smart CA Copilot Streamlit App

👨‍💻 Author
Harivansh Dogne



📜 License
This project is licensed under the MIT License — feel free to use, modify, and distribute it for your own applications.
