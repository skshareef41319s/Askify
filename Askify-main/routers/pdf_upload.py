from pydantic import BaseModel
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, Document
from utils.pdf_processor import load_pdf
import uuid
import os
from typing import Dict
from pathlib import Path
import shutil


# Define response model for better documentation and type safety
class PDFUploadResponse(BaseModel) :
    filename: str
    message: str
    id: str


router = APIRouter()


def get_db() :
    db = SessionLocal()
    try :
        yield db
    finally :
        db.close()


@router.post("/upload_pdf", response_model=PDFUploadResponse)
async def upload_pdf(
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
) -> Dict[str, str] :
    """
    Upload and process a PDF file.

    Args:
        file: The PDF file to upload
        db: Database session dependency

    Returns:
        Dict containing filename, success message, and generated ID

    Raises:
        HTTPException: If file type is invalid or processing fails
    """
    # Validate file type
    if not file.filename.lower().endswith('.pdf') :
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PDF files are allowed."
        )

    try :
        # Generate a random UUID for the PDF
        pdf_id = str(uuid.uuid4())

        # Create upload directory using pathlib
        upload_dir = Path("upload")
        upload_dir.mkdir(exist_ok=True)

        # Construct file path
        pdf_path = upload_dir / f"{pdf_id}.pdf"

        # Save uploaded file
        try :
            with pdf_path.open("wb") as buffer :
                shutil.copyfileobj(file.file, buffer)
        finally :
            file.file.close()  # Ensure file is closed

        # Validate and process PDF
        try :
            pdf_content = load_pdf(str(pdf_path))
            if not pdf_content :
                raise ValueError("No content extracted from PDF")

            extracted_text = pdf_content[0].page_content

            # Create and save document to database
            new_doc = Document(
                filename=file.filename,
                content=extracted_text,
                pdf_id=pdf_id
            )

            db.add(new_doc)
            db.commit()
            db.refresh(new_doc)

            return PDFUploadResponse(
                filename=file.filename,
                message="PDF successfully uploaded and processed",
                id=pdf_id
            )

        except Exception as e :
            # Clean up the file if processing fails
            pdf_path.unlink(missing_ok=True)
            raise HTTPException(
                status_code=500,
                detail=f"Error processing PDF: {str(e)}"
            )

    except Exception as e :
        raise HTTPException(
            status_code=500,
            detail=f"Error handling upload: {str(e)}"
        )


# Optional: Add endpoint to retrieve PDF status or content
@router.get("/pdf/{pdf_id}", response_model=Dict[str, str])
async def get_pdf_status(pdf_id: str, db: Session = Depends(get_db)) :
    """
    Get the status or information about an uploaded PDF.

    Args:
        pdf_id: The UUID of the PDF
        db: Database session dependency

    Returns:
        Dict containing PDF information
    """
    doc = db.query(Document).filter(Document.pdf_id == pdf_id).first()
    if not doc :
        raise HTTPException(
            status_code=404,
            detail="PDF not found"
        )

    return {
        "filename" : doc.filename,
        "status" : "processed",
        "id" : doc.pdf_id
    }