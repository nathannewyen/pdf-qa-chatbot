import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load API key
load_dotenv()

# Load your PDF
loader = PyPDFLoader("example.pdf")  # Replace with your PDF file
pages = loader.load()

# Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(pages)

print(f"✅ Loaded {len(chunks)} text chunks.")
print(chunks[0].page_content[:300])  # Preview the first chunk
