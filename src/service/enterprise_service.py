from bson import ObjectId
from fastapi import HTTPException
from ..model.enterprise_model import EnterpriseModel
from ..repository.enterprise_repository import EnterpriseRepository


class EnterpriseService:
    def __init__(self):
        self.repository = EnterpriseRepository()

    async def create_enterprise(self, enterprise: EnterpriseModel):
        if enterprise.name:
            find_enterprise = await self.repository.get_enterprise_by_filter({'name': enterprise.name})

            if find_enterprise:
                return HTTPException(status_code=409, detail='Nome da empresa já cadastrada')
            elif find_enterprise is None:
                await self.repository.create_enterprise(enterprise.name)
                return {
                    'detail': 'Empresa cadastrada com sucesso!',
                    'status_code': 201
                }
        elif enterprise.name == "":
            return HTTPException(status_code=400, detail='Nome da empresa não pode ser vazio')

    async def update_enterprise(self, enterprise: EnterpriseModel, _id: str):
        if enterprise.name:
            find_enterprise = await self.repository.get_enterprise_by_filter({'_id': ObjectId(_id)})
            exist_enterprise = await self.repository.get_enterprise_by_filter({'name': enterprise.name})

            if exist_enterprise:
                return HTTPException(status_code=409, detail='Nome da empresa já existe')
            elif find_enterprise:
                await self.repository.update_enterprise(enterprise.name, {'_id': ObjectId(_id)})
                return {
                    'detail': 'Empresa atualizada com sucesso!',
                    'status_code': 201
                }
            elif find_enterprise is None:
                return HTTPException(status_code=400, detail='Empresa não existe')

        elif enterprise.name == "":
            return HTTPException(status_code=400, detail='Nome da empresa não pode ser vazio')

    async def delete_enterprise(self, enterprise_id: str):
        if enterprise_id:
            await self.repository.delete_enterprise(enterprise_id)
            return {
                'detail': 'Empresa excluida com sucesso!',
                'status_code': 204
            }

    async def list_enterprises(self):
        enterprises = await self.repository.list_enterprises()

        for enterprise in enterprises:
            enterprise['_id'] = str(enterprise['_id'])

        return enterprises
