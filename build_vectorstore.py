import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings


# Load .env
load_dotenv()

# Load and chunk the PDF
loader = PyPDFLoader("example.pdf")
pages = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(pages)

# Create vector embeddings
embeddings = OpenAIEmbeddings()

# Build FAISS vector store
vectorstore = FAISS.from_documents(chunks, embeddings)

# Save to disk
vectorstore.save_local("faiss_index")

print("✅ Vector store built and saved to 'faiss_index'")
