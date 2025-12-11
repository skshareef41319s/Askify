Here's an updated README with Postman information included:

---

# Askify - PDF Question-Answering Service

Askify is a backend service that allows users to upload PDF documents and ask questions based on the content within these documents. It utilizes LangChain for natural language processing and ChromaDB for document embeddings and retrieval.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [PDF Upload](#pdf-upload)
- [Question Answering](#question-answering)
- [Testing with Postman](#testing-with-postman)
- [License](#license)

## Features

- Upload and store PDF documents.
- Text extraction and storage in SQLite database.
- Real-time question-answering capability using LangChain's language model.
- Retrieval-Augmented Generation (RAG) architecture with ChromaDB for efficient document search and retrieval.

## Technologies Used

- **FastAPI**: Web framework for building APIs.
- **SQLite**: Lightweight relational database to store PDF data.
- **LangChain**: Framework for integrating language models in applications.
- **ChromaDB**: Vector database for document embeddings and similarity search.
- **PyPDF2**: PDF parsing and text extraction.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/theshashank1/Askify.git
   cd Askify
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**

   Create a `.env` file in the root directory and add any required configurations.
    
   ```dotenv
   GOOGLE_API_KEY = <Gemini API_Key>
   LANGCHAIN_TRACING_V2 = true
   LANGCHAIN_API_KEY = <Langchain API_Key>
   ```
   Note: Obtain the LangChain API key from LangSmith.

4. **Run the Application**

   Start the FastAPI application with Uvicorn.

   ```bash
   uvicorn main:app --reload
   ```

## Usage

### 1. Upload a PDF

   Use an HTTP client (like Postman or curl) to upload a PDF document to the `/upload` endpoint.

   ```bash
   curl -X POST "http://127.0.0.1:8000/upload" -F "file=@/path/to/your/file.pdf"
   ```

### 2. Ask Questions

   Connect to the WebSocket endpoint `/ws/question_answer/{document_id}`, where `{document_id}` is the ID of an uploaded PDF document.

   Example:

   ```javascript
   const ws = new WebSocket("ws://localhost:8000/ws/question_answer/883d5e93-d2c7-4ad8-b161-02398d24f138");

   ws.onopen = () => {
     ws.send("What is the main topic of this document?");
   };

   ws.onmessage = (event) => {
     console.log("Answer:", event.data);
   };
   ```

   Note: You can also connect to the WebSocket using Postman.

## Project Structure

```plaintext
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

## API Documentation

### PDF Upload

- **Endpoint**: `/upload`
- **Method**: `POST`
- **Parameters**:
  - `file`: PDF file to upload (as form-data).
- **Response**:
  - JSON object with document ID and success message.

Example Response:
```json
{
    "filename": "example.pdf",
    "message": "PDF uploaded and processed",
    "id": "bb76a347-644e-41ff-b63b-a569a63b45d9"
}
```

### Question Answering

- **Endpoint**: `/ws/question_answer/{document_id}`
- **Method**: WebSocket
- **Parameters**:
  - `document_id`: The ID of the document to query.
- **Response**:
  - Real-time answer from LangChain’s Gemini model based on the content of the specified PDF.

Example Response:
```json
{
  "answer": "This document discusses the basics of data science."
}
```

## Testing with Postman

A Postman workspace has been created for testing Askify's API endpoints and WebSocket functionality. The workspace contains two collections:

1. **Askify API Collection**:
   - **Upload PDF**: `POST /upload` — Uploads a PDF file and returns a `document_id`.
   - **Get Document Metadata** (optional): `GET /document/{document_id}` — Retrieves metadata of a specific PDF.

2. **Askify Web Sockets Collection**:
   - **Question Answer WebSocket**: `/ws/question_answer/{document_id}` — Allows real-time question-answering on the uploaded PDF by sending a question and receiving an answer instantly.

You can access the Postman workspace here: [Askify Postman Workspace](https://www.postman.com/flight-geologist-95162013/askify).

### Setup

- **Environment Variables**: Include `document_id` for easy testing.
- **Usage**: Start with uploading a PDF to get a `document_id`, then use it for WebSocket questions.

## License

This project is licensed under the MIT License.

--- 
