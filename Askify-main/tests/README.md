
## Testing with Postman

### 1. **Import the Postman Workspace**
   - Import the workspace using this link: [Askify Postman Workspace](https://www.postman.com/flight-geologist-95162013/askify).
   - Alternatively, download the collection JSON and import it manually.

### 2. **Set Up Environment Variables**
   - **`base_url`**: Set to `http://127.0.0.1:8000` (for local testing).
   - **`file`**: Path to your PDF file.

### 3. **Test API Endpoints**

#### **Upload PDF (POST /upload)**
   - Use the **Askify API Collection** in Postman.
   - **Method**: `POST`, **Endpoint**: `/upload`
   - Add `file` in **form-data** to upload the PDF.

   **Response**:
   ```json
   { "filename": "example.pdf", "message": "PDF uploaded", "id": "document_id" }
   ```

#### **Ask Questions (WebSocket /ws/question_answer/{document_id})**
   - Use the **Askify Web Sockets Collection**.
   - **Method**: WebSocket, **Endpoint**: `/ws/question_answer/{document_id}`
   - Send a question like `"What is the main topic?"`.

   **Response**:
   ```json
   { "answer": "This document discusses data science." }
   ```

### 4. **Error Handling**
   - If something goes wrong (e.g., invalid file), the API will return a relevant error message.

---

This is a quick guide to test the Askify service using Postman.