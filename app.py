import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import warnings
import logging

# Suppress warnings and set logging level
warnings.filterwarnings("ignore")
logging.getLogger("pdfminer").setLevel(logging.ERROR)

# Load environment variables
load_dotenv()

# Initialize LLM
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Initialize session state
def init_session_state():
    if "chat_histories" not in st.session_state:
        st.session_state.chat_histories = {}  # Dictionary to store chat histories for each PDF
    if "input" not in st.session_state:
        st.session_state.input = ""
    if "input_submitted" not in st.session_state:
        st.session_state.input_submitted = False
    if "qa_chains" not in st.session_state:
        st.session_state.qa_chains = {}  # Dictionary to store multiple QA chains
    if "current_pdf" not in st.session_state:
        st.session_state.current_pdf = None
    if "text_input_key" not in st.session_state:
        st.session_state.text_input_key = 0

# Process PDF and create QA chain
def process_pdf(uploaded_file, filename):
    with st.spinner("Processing PDF..."):
        # Save uploaded file temporarily
        temp_path = f"temp_{filename}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())

        # Load and split PDF
        loader = PyPDFLoader(temp_path)
        pages = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = splitter.split_documents(pages)

        # Create vector store and QA chain
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(chunks, embeddings)
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm, 
            retriever=vectorstore.as_retriever()
        )
        
        # Store the QA chain
        st.session_state.qa_chains[filename] = qa_chain
        
        # Clean up temporary file
        try:
            os.remove(temp_path)
        except:
            pass

# Process user question and get answer
def process_question(query):
    with st.spinner("Thinking..."):
        try:
            # Get relevant documents
            docs = st.session_state.qa_chain.retriever.get_relevant_documents(query)
            
            if not docs:
                return "❌ No relevant context found in the document."
            
            # Get answer from QA chain
            result = st.session_state.qa_chain.invoke(query)
            response = result.get('result', '❌ No answer generated.')
            
            if not response.strip():
                return "❌ No relevant info found in the document."
                
            return response

        except Exception as e:
            return f"⚠️ Error: {str(e)}"

# Main UI
st.title("📚 PDF Question Answering Chatbot")

# Initialize session state
init_session_state()

# File uploader
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

# Process PDF if uploaded
if uploaded_file:
    filename = uploaded_file.name
    process_pdf(uploaded_file, filename)
    st.session_state.current_pdf = filename
    st.success(f"✅ Successfully processed {filename}")

# PDF selector if multiple PDFs are loaded
if len(st.session_state.qa_chains) > 0:
    pdf_options = list(st.session_state.qa_chains.keys())
    selected_pdf = st.selectbox(
        "Select a PDF to query:",
        options=pdf_options,
        index=pdf_options.index(st.session_state.current_pdf) if st.session_state.current_pdf in pdf_options else 0
    )
    st.session_state.current_pdf = selected_pdf

# Show input form if PDF is processed
if st.session_state.current_pdf and st.session_state.current_pdf in st.session_state.qa_chains:
    with st.form(key='question_form'):
        user_input = st.text_input("Ask a question about the PDF:", key=f"text_input_{st.session_state.text_input_key}")
        submit_button = st.form_submit_button(label='Submit')
        
        if submit_button and user_input:
            st.session_state.input = user_input
            st.session_state.input_submitted = True
            # Increment the key to force text input to clear
            st.session_state.text_input_key += 1
            # Force a rerun to clear the input
            st.rerun()
else:
    st.info("👆 Upload a PDF to start asking questions.")

# Process question if submitted
if st.session_state.input_submitted and st.session_state.input.strip():
    query = st.session_state.input
    # Use the current PDF's QA chain
    st.session_state.qa_chain = st.session_state.qa_chains[st.session_state.current_pdf]
    response = process_question(query)
    
    # Initialize chat history for this PDF if it doesn't exist
    if st.session_state.current_pdf not in st.session_state.chat_histories:
        st.session_state.chat_histories[st.session_state.current_pdf] = []
    
    # Add to the specific PDF's chat history
    st.session_state.chat_histories[st.session_state.current_pdf].append({
        "question": query, 
        "answer": response
    })
    
    # Reset input state
    st.session_state.input = ""
    st.session_state.input_submitted = False

# Display chat history for current PDF
if st.session_state.current_pdf and st.session_state.current_pdf in st.session_state.chat_histories:
    st.markdown(f"### Chat History for {st.session_state.current_pdf}")
    for chat in st.session_state.chat_histories[st.session_state.current_pdf]:
        st.markdown(f"**You:** {chat['question']}")
        st.markdown(f"**AI:** {chat['answer']}")
        st.markdown("---")
