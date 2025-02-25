from pydantic import BaseModel


class DocumentUpload(BaseModel) :
    filename: str
    content: str
    pdf_id: str  # Change this to str to store the UUID as a string
