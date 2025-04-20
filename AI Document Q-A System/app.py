from PIL import Image
import streamlit as st
import os
from Main_Script import ask_question, load_pdf, load_docx, load_pptx, load_excel, load_csv, load_json, load_txt, load_image, split_text, add_documents

# Disable Streamlit file watcher to avoid torch/classes async issues
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

# Ensure temp directory exists
os.makedirs("temp", exist_ok=True)

st.set_page_config(page_title="📚 QnA Bot", layout="centered")

# Add the logo at the top center
logo_path = "https://raw.githubusercontent.com/retrothruster/AI-Document-Q-A-Website/blob/main/IITM_logo.jpg.png"  # Replace with the path to your logo image
st.image(logo_path, width=200)  # Adjust width as needed to scale the logo

st.title("🤖 Document-Based QnA Bot")
st.write("Upload a document and ask questions based on it! \n This might take a while, Have Patience")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "pptx", "xlsx", "csv", "json", "txt", "png", "jpg", "jpeg"])

if uploaded_file:
    file_path = f"temp/{uploaded_file.name}"

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    ext = file_path.split('.')[-1].lower()

    loader_map = {
        "pdf": load_pdf, "docx": load_docx, "pptx": load_pptx,
        "xlsx": load_excel, "csv": load_csv, "json": load_json,
        "txt": load_txt, "png": load_image, "jpg": load_image, "jpeg": load_image
    }

    if ext in loader_map:
        raw_text = loader_map[ext](file_path)
        chunks = split_text(raw_text)

        if not chunks:
            st.error("No content could be extracted from the document.")
        else:
            add_documents(chunks)
            st.success("✅ Document loaded successfully! Ready to ask questions.")
    else:
        st.error(f"❌ Unsupported file type: {ext}")

if st.session_state.chat_history:
    for idx, (question, answer) in enumerate(st.session_state.chat_history):
        st.write(f"**You:** {question}")
        st.write(f"**Bot:** {answer}")

question = st.text_input("Ask a question based on the document:")

if st.button("Get Answer") and question:
    with st.spinner("Thinking..."):
        try:
            answer = ask_question(question)
            st.session_state.chat_history.append((question, answer))
            st.write(f"**Bot:** {answer}")
        except IndexError:
            st.error("❌ No context found. Please ensure a valid document is uploaded before asking questions.")

# Add footer at the bottom of the page
st.markdown("""
<hr style="border: none; height: 1px; background-color: #ccc;" />
<div style="text-align: center; font-size: 14px; padding-top: 10px;">
    Made By MD24B033 || Team vanilla
</div>
""", unsafe_allow_html=True)
