from fastapi import APIRouter, HTTPException, Path, UploadFile, File, Form, Depends
from bson import ObjectId
from ..model.document_model import DocumentModel
from ..service.enterprise_service import EnterpriseService
from ..service.document_service import DocumentService

document_service = DocumentService()
router = APIRouter()

@router.post("/{enterprise_id}/documents")
async def create_document(enterprise_id: str, file: UploadFile = File(...), filename: str = Form(...)):
    """
    Cria um novo documento associado a uma empresa.
    - `enterprise_id`: ID da empresa a qual o documento será associado.
    - `file`: Arquivo que será armazenado (pode ser PDF ou DOCX).
    - `filename`: Nome do arquivo.
    """
    return await document_service.create_document(enterprise_id, file, filename)

@router.get("/{enterprise_id}/documents")
async def list_documents(enterprise_id: str):
    """
    Lista os documentos associados a uma empresa.
    - `enterprise_id`: ID da empresa da qual os documentos serão listados.
    """
    return await document_service.list_documents(enterprise_id)
