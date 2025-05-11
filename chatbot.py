import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

# Load environment variables
load_dotenv()

# Load vector store
vectorstore = FAISS.load_local("faiss_index", OpenAIEmbeddings(), allow_dangerous_deserialization=True)

# Load LLM
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Create QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    return_source_documents=False
)

# Interactive loop
print("🤖 Ask me anything about the PDF (type 'exit' to quit):")
while True:
    query = input(">> ")
    if query.lower() in ["exit", "quit"]:
        break
    response = qa_chain.run(query)
    print("\n📘", response, "\n")
