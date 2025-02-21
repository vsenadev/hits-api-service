from pydantic import BaseModel

class DocumentModel(BaseModel):
    filename: str
    file_content: str
    status: int
    enterprise_id: str
