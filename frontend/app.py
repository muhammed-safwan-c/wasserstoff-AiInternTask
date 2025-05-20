import streamlit as st
import requests



API_BASE = "http://localhost:8000"  # Adjust if running elsewhere

st.set_page_config(page_title="Document Theme Research Bot", page_icon="📄")
st.title("🤖 Document Theme Research Assistant")

# Session state initialization
if "last_answer" not in st.session_state:
    st.session_state.last_answer = ""
if "last_citations" not in st.session_state:
    st.session_state.last_citations = []

# Tab layout
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📄 PDF Theme Extractor",
    "🖼️ Image OCR",
    "💬 LLaMA Chat",
    "🔍 Synthesize Themes",
    "📘 About LLaMA Bot"
])

# ---------------- TAB 1: PDF Upload ----------------
with tab1:
    st.header("📄 Upload PDF for Theme Detection")
    uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"], key="pdf_uploader")

    if uploaded_pdf:
        files = {"file": (uploaded_pdf.name, uploaded_pdf.getvalue())}
        with st.spinner("Processing PDF..."):
            try:
                resp = requests.post(f"{API_BASE}/pdf/upload-pdf/", files=files)
                resp.raise_for_status()
                result = resp.json()
                st.success(f"✅ PDF Uploaded: `{uploaded_pdf.name}`")
                st.info(f"🧠 Detected Theme: **{result.get('theme', 'Unknown')}**")

                extracted_text = result.get("extracted_text")
                if extracted_text:
                    with st.expander("📄 View Extracted Text"):
                        st.text(extracted_text[:3000])
                else:
                    st.info("⚠️ No text extracted from this PDF.")
            except requests.RequestException as e:
                st.error(f"❌ Upload failed: {e}")

# ---------------- TAB 2: Image Upload ----------------
with tab2:
    st.header("🖼️ Upload Image for OCR & Theme Detection")
    uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"], key="image_uploader")

    if uploaded_image:
        files = {"file": (uploaded_image.name, uploaded_image.getvalue())}
        with st.spinner("Processing image..."):
            try:
                resp = requests.post(f"{API_BASE}/ocr/upload-ocr/", files=files)
                resp.raise_for_status()
                result = resp.json()
                st.success(f"✅ Image Uploaded: `{uploaded_image.name}`")
                st.info(f"🧠 Detected Theme: **{result.get('theme', 'Unknown')}**")

                extracted_text = result.get("text")  # FIXED LINE
                if extracted_text:
                    with st.expander("📝 View Extracted Text"):
                        st.text(extracted_text[:3000])
                else:
                    st.info("⚠️ No text extracted from this image.")
            except requests.RequestException as e:
                st.error(f"❌ Upload failed: {e}")


# ---------------- TAB 3: LLaMA Chat ----------------
with tab3:
    st.header("💬 Ask a Question to LLaMA")
    query = st.text_input("Enter your question:")

    if st.button("Ask"):
        if not query.strip():
            st.warning("Please enter a question before asking.")
        else:
            with st.spinner("LLaMA is thinking..."):
                try:
                    response = requests.post(
                        f"http://localhost:11434/api/generate",
                        json={
                            "model": "llama3",  # or your actual model name
                            "prompt": query,
                            "stream": False
                        },
                        timeout=120
                    )
                    response.raise_for_status()
                    answer = response.json().get("response", "_No response returned._")

                    st.markdown("### 🧠 Answer:")
                    st.markdown(answer.strip())

                except requests.RequestException as e:
                    st.error(f"❌ LLaMA request failed: {e}")

# ---------------- TAB 4: Theme Synthesis ----------------
with tab4:
    st.header("🔍 Synthesize Themes Across All Documents")
    synth_query = st.text_input("Enter a topic or keyword to synthesize themes:")

    if st.button("Synthesize Themes"):
        if not synth_query.strip():
            st.warning("Enter a keyword or topic before synthesizing.")
        else:
            with st.spinner("Synthesizing..."):
                try:
                    r = requests.get(f"{API_BASE}/synthesize/", params={"q": synth_query}, timeout=30)
                    r.raise_for_status()
                    response = r.json()
                    themes = response.get("themes", "_No themes returned._")
                    st.markdown("### 🧩 Synthesized Themes")
                    st.markdown(themes)
                except requests.RequestException as e:
                    st.error(f"❌ Theme synthesis failed: {e}")

# ---------------- TAB 5: About ----------------
with tab5:
    st.header("📘 About LLaMA Bot")
    st.markdown("""
    This assistant helps you:
    - 📄 Extract themes from **PDF documents**
    - 🖼️ Perform OCR and theme extraction from **images**
    - 💬 Ask LLaMA-based questions on your uploaded documents
    - 🔍 Synthesize **themes across multiple documents**

    Built using:
    - FastAPI + LangChain + Ollama (LLaMA)
    - Streamlit for the user interface
    - OCR & PDF extraction for document intelligence
    """)
