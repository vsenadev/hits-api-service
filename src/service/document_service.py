from fastapi import HTTPException
from bson import ObjectId
from ..repository.document_repository import DocumentRepository
import base64


class DocumentService:
    def __init__(self):
        self.repository = DocumentRepository()

    async def create_document(self, enterprise_id: str, file, filename: str):
        if file.content_type not in ["application/pdf",
                                     "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            raise HTTPException(status_code=400, detail="Tipo de arquivo inválido. Apenas PDF e DOCX são permitidos.")

        # Lê o conteúdo do arquivo e converte para base64
        file_content = await file.read()
        file_base64 = base64.b64encode(file_content).decode('utf-8')  # Converte para base64

        # Insere o documento no banco com o status 0 (a ser processado futuramente)
        document_data = {
            "enterprise_id": ObjectId(enterprise_id),
            "file_content": file_base64,
            "filename": filename,
            "status": 0  # Status de 0 para processamento futuro
        }

        try:
            await self.repository.create_document(document_data)
            return {"detail": "Documento cadastrado com sucesso!", "status_code": 201}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def list_documents(self, enterprise_id: str):
        try:
            documents = await self.repository.list_documents(enterprise_id)
            for doc in documents:
                doc['_id'] = str(doc['_id'])
                doc['enterprise_id'] = str(doc['enterprise_id'])

            return documents
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))