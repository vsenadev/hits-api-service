from ..database.db import execute_query
from bson import ObjectId

class DocumentRepository:
    def __init__(self):
        pass

    async def create_document(self, document_data: dict):
        # Insere o documento no banco de dados
        return await execute_query('document', 'insert_one', document_data)

    async def list_documents(self, enterprise_id: str):
        # Lista os documentos associados a uma empresa
        return await execute_query('document', 'find', {"enterprise_id": ObjectId(enterprise_id)}, {'file_content': 0, 'status': 0})
