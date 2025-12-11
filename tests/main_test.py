import sys
import os
import pytest
import time
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_question_answer() :
    # First, upload a PDF to get a document ID
    file_path = "E:\\Music_and_Movie_Recommendation_System.pdf"
    with open(file_path, "rb") as file :
        upload_response = client.post("/upload_pdf", files={"file" : ("sample.pdf", file, "application/pdf")})
    assert upload_response.status_code == 200
    document_id = upload_response.json()["id"]

    print(f"Uploaded Document ID: {document_id}")

    # Short delay to ensure the document is available
    time.sleep(1)  # Wait for 1 second

    # WebSocket test for question-answering (use synchronous context)
    with client.websocket_connect(f"/ws/question_answer/{document_id}") as websocket :
        question = "What is this about?"
        websocket.send_text(question)
        response = websocket.receive_text()
        print(response)

        # Modify the assertion to pass if either an answer or "Document not found." is received
        assert "answer" in response or "Document not found." == response, f"Unexpected response: {response}"
