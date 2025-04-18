import streamlit as st
from Main_Script import ask_question, load_pdf, load_docx, load_pptx, load_excel, load_csv, load_json, load_txt, load_image, split_text, add_documents


st.set_page_config(page_title="📚 QnA Bot", layout="centered")


st.title("🤖 Document-Based QnA Bot")
st.write("Upload a document and ask questions based on it!")


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
        answer = ask_question(question)
        

        st.session_state.chat_history.append((question, answer))
        

        st.write(f"**Bot:** {answer}")

