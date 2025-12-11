import uvicorn
from fastapi import FastAPI
from routers import pdf_upload, question_answer

# Create an instance of the FastAPI application
app = FastAPI()

# Include routers for handling different functionalities
app.include_router(pdf_upload.router)
app.include_router(question_answer.router)

# Main entry point for the application
if __name__ == "__main__":
    # Only for development, to run directly
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)  # Use "main:app"

