# PDF Question Answering Chatbot

An intelligent chatbot application that allows users to upload PDF documents and ask questions about their content. Built with Streamlit and powered by OpenAI's GPT-3.5, this application demonstrates advanced natural language processing and document understanding capabilities.

## 🌟 Features

- **Multi-PDF Support**: Upload and manage multiple PDF documents simultaneously
- **Interactive Chat Interface**: Clean and intuitive chat interface for asking questions
- **Separate Chat Histories**: Maintains distinct conversation threads for each PDF
- **Real-time Processing**: Instant responses to questions about document content
- **Context-Aware Responses**: AI-powered answers based on the specific content of each PDF
- **User-Friendly Design**: Simple and intuitive interface for document upload and interaction

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **Language Model**: OpenAI GPT-3.5 Turbo
- **Vector Database**: FAISS (Facebook AI Similarity Search)
- **Document Processing**: LangChain
- **PDF Processing**: PyPDFLoader
- **Environment Management**: Python-dotenv

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/nathannewyen/pdf-qa-chatbot.git
cd pdf-qa-chatbot
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

4. Run the application:
```bash
streamlit run app.py
```

## 💡 Usage

1. Upload a PDF document using the file uploader
2. Wait for the document to be processed
3. Type your question in the text input
4. View the AI's response in the chat history
5. Upload multiple PDFs and switch between them using the dropdown menu
6. Each PDF maintains its own separate chat history

## 🔧 Technical Implementation

- **Document Processing**: PDFs are split into chunks and converted into vector embeddings
- **Vector Storage**: FAISS is used for efficient similarity search
- **Question Answering**: LangChain's RetrievalQA chain combines document retrieval with GPT-3.5
- **State Management**: Streamlit's session state maintains separate chat histories and document contexts
- **Error Handling**: Robust error handling for file processing and API interactions

## 🎯 Project Goals

- Demonstrate practical application of AI and NLP technologies
- Showcase efficient document processing and information retrieval
- Provide a user-friendly interface for document interaction
- Implement scalable architecture for handling multiple documents

## 🔮 Future Enhancements

- Support for more document formats (DOCX, TXT, etc.)
- Enhanced document preprocessing and chunking strategies
- User authentication and document management
- Export chat histories
- Customizable AI parameters
- Batch processing capabilities

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

Your Name - your.email@example.com

Project Link: [https://github.com/nathannewyen/pdf-qa-chatbot](https://github.com/nathannewyen/pdf-qa-chatbot) 