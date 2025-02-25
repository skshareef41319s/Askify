# Askify - PDF Question-Answering Service

Askify is a powerful backend service that allows users to upload PDF documents and ask questions based on the content within them. It leverages **LangChain** for Natural Language Processing (NLP) and **ChromaDB** for efficient document retrieval.

---

## 🚀 Features
- 📂 **Upload and store PDF documents**
- 🔍 **Extract text from PDFs and store in an SQLite database**
- 🤖 **Ask questions based on document content using LangChain**
- 🛠️ **Real-time Retrieval-Augmented Generation (RAG) using ChromaDB**
- 🔌 **WebSocket-based communication for seamless Q&A**

---

## 📌 Technologies Used
- **FastAPI** - For building the API
- **SQLite** - For storing extracted text
- **LangChain** - For NLP and processing user queries
- **ChromaDB** - For document embeddings and similarity search
- **PyPDF2** - For PDF parsing and text extraction
- **WebSockets** - For real-time Q&A functionality

---

## 🛠 Installation
### 1️⃣ Clone the Repository
```sh
 git clone https://github.com/skshareef41319s/Askify.git
 cd Askify
```

### 2️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 3️⃣ Set Up Environment Variables
Create a **.env** file in the root directory and add the following:
```env
GOOGLE_API_KEY = <Your_Gemini_API_Key>
LANGCHAIN_TRACING_V2 = true
LANGCHAIN_API_KEY = <Your_Langchain_API_Key>
```
📌 **Note:** Obtain your LangChain API key from [LangSmith](https://www.langchain.com/docs).

### 4️⃣ Run the Application
```sh
uvicorn main:app --reload
```
The API will now be running at: **http://127.0.0.1:8000**

---

## 📌 Usage
### 🔹 1. Upload a PDF
Use an HTTP client (like Postman or `curl`) to upload a PDF.
```sh
curl -X POST "http://127.0.0.1:8000/upload" -F "file=@/path/to/your/file.pdf"
```
📌 **Response Example:**
```json
{
    "filename": "example.pdf",
    "message": "PDF uploaded and processed",
    "id": "bb76a347-644e-41ff-b63b-a569a63b45d9"
}
```

### 🔹 2. Ask Questions
Connect to the **WebSocket endpoint** to ask questions in real-time.
```js
const ws = new WebSocket("ws://localhost:8000/ws/question_answer/<document_id>");

ws.onopen = () => {
  ws.send("What is the main topic of this document?");
};

ws.onmessage = (event) => {
  console.log("Answer:", event.data);
};

      (or)


{
question: "What is this PDF about?"
}
```
📌 **Example Response:**
```json
{
  "answer": "This document discusses the basics of data science."
}
```

---

## 📂 Project Structure
```
Askify/
├── chroma_db/                # Directory for ChromaDB files and embeddings
├── routers/                  # API route handlers
│   ├── pdf_upload.py         # Endpoint for uploading PDFs
│   └── question_answer.py    # Endpoint for question answering
├── upload/                   # Directory to store uploaded PDFs
├── utils/                    # Utility functions and helper classes
│   └── pdf_processor.py      # PDF text extraction logic
├── database.py               # SQLite database setup and interaction
├── pdf_data.db               # SQLite database file
├── llm.py                    # Language model integration with LangChain
├── rag.py                    # Retrieval-Augmented Generation (RAG) logic
├── main.py                   # FastAPI app initialization
├── models.py                 # Pydantic models for data validation
├── requirements.txt          # Python dependencies
└── .env                      # Environment variables (not included in repo)
```


