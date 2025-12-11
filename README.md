# Askify — PDF Question-Answering Service

Askify is a backend service that lets you upload PDF documents, index their content, and ask natural-language questions about them. It combines document parsing, embeddings, and retrieval-augmented generation (RAG) so queries are answered using the actual content of the uploaded PDFs.

This README explains what Askify does, how to run it locally, and how to use its upload and question-answering features.

## Key capabilities

- Upload PDF documents and extract their text.
- Store extracted text and metadata in SQLite.
- Create embeddings and perform similarity search with ChromaDB.
- Answer user questions about a specific PDF using LangChain-powered LLM calls.
- Real-time Q&A using a WebSocket endpoint.

## Technology overview

- FastAPI — API framework
- SQLite — lightweight storage for extracted text and metadata
- LangChain — orchestration of LLM calls and retrieval logic
- ChromaDB — vector store for embeddings and similarity search
- PyPDF2 — PDF parsing and text extraction
- WebSockets — real-time question/answer transport

## Quick start (local)

1. Clone the repository
```bash
git clone https://github.com/skshareef41319s/Askify.git
cd Askify
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your credentials
Example:
```
GOOGLE_API_KEY=<your_gemini_api_key>
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=<your_langchain_api_key>
```
Adjust the variables to match the providers you use. Keep these secrets out of version control.

4. Run the application
```bash
uvicorn main:app --reload
```
The API will be available at: http://127.0.0.1:8000

## How it works (high level)

1. Upload: a PDF is uploaded to the server. The service extracts text and splits it into chunks suitable for embedding.
2. Index: chunks are embedded and stored in ChromaDB. Metadata and mapping to the original PDF are saved in SQLite.
3. Query: when a user asks a question, related document chunks are retrieved via similarity search and provided to the LLM via LangChain to generate a grounded answer.
4. WebSocket: WebSocket endpoints enable streaming or real-time question/answer interactions.

## Usage

### Upload a PDF
Use curl, Postman, or a similar client to upload a PDF:
```bash
curl -X POST "http://127.0.0.1:8000/upload" -F "file=@/path/to/document.pdf"
```
Example JSON response:
```json
{
  "filename": "document.pdf",
  "message": "PDF uploaded and processed",
  "id": "bb76a347-644e-41ff-b63b-a569a63b45d9"
}
```
Save the returned `id` — it identifies the uploaded document for later queries.

### Ask questions (WebSocket)
Connect to the WebSocket endpoint and send questions tied to a document id:
```js
const ws = new WebSocket("ws://127.0.0.1:8000/ws/question_answer/<document_id>");

ws.onopen = () => {
  ws.send(JSON.stringify({ question: "What is the main topic of this document?" }));
};

ws.onmessage = (event) => {
  console.log("Answer:", event.data);
};
```
The server will return answers composed using the retrieved document context and the configured LLM.

## API endpoints (summary)

- POST /upload — Upload and process a PDF
- GET  /documents — (optional) List uploaded documents / metadata
- WS   /ws/question_answer/{document_id} — WebSocket endpoint for asking questions about a specific document

Check the source routers for exact routes and expected request/response shapes.

## Project structure

```
Askify/
├── chroma_db/                # ChromaDB files and embeddings
├── routers/                  # FastAPI route handlers
│   ├── pdf_upload.py         # PDF upload and processing
│   └── question_answer.py    # WebSocket question-answering logic
├── upload/                   # Stored uploaded PDFs
├── utils/                    # Utility functions (pdf parsing, chunking, helpers)
│   └── pdf_processor.py
├── database.py               # SQLite setup and helper functions
├── pdf_data.db               # SQLite database (generated at runtime)
├── llm.py                    # LangChain/LLM interface and helpers
├── rag.py                    # Retrieval / RAG orchestration logic
├── main.py                   # FastAPI app entrypoint
├── models.py                 # Pydantic models and validation schemas
├── requirements.txt
└── .env                      # Environment variables (not committed)
```

## Development notes & best practices

- Secrets: keep API keys and sensitive configs in environment variables or a secrets manager.
- Production: use a managed vector store or persistent Chroma deployment for reliability; consider a hosted database for SQLite replacement (Postgres, etc.).
- Embeddings: choose the embedding model and chunk size carefully—too small or too large chunks impact retrieval relevance.
- Rate limits & cost: LLM calls can be costly. Add caching, rate limiting, and request batching in production.
- Security: validate uploads, enforce file size limits, and scan for malicious files. Restrict WebSocket origins if exposing publicly.
- Logging and monitoring: add structured logs and health checks for long-running services.

## Troubleshooting

- If embedding or LLM calls fail, verify API keys and provider availability.
- If PDF text is missing or garbled, check the PDF parsing step and try alternate chunking strategies (e.g., overlap size).
- For WebSocket connection issues, confirm the server is running and the correct URL/port are used.

## Contributing

Contributions are welcome. Suggested workflow:
1. Fork the repo
2. Create a branch with a clear name (feature/..., fix/...)
3. Commit changes and open a pull request with a description of the change
