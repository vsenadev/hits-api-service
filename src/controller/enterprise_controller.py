from fastapi import APIRouter, HTTPException, Path, Body, Depends
from ..model.enterprise_model import EnterpriseModel
from ..service.enterprise_service import EnterpriseService

enterprise_service = EnterpriseService()
router = APIRouter()


@router.post("")
async def create_enterprise(enterprise: EnterpriseModel):
    return await enterprise_service.create_enterprise(enterprise)


@router.put("/{enterprise_id}")
async def update_enterprise(enterprise: EnterpriseModel, enterprise_id: str = Path(..., title="ID da Empresa",
                                                                         description="O ID da empresa a ser atualizado")):
    """
    Atualiza as informações de uma empresa.
    - `_id`: ID da empresa passado como path param.
    - `enterprise`: Corpo da requisição contendo os dados para atualização.
    """
    return await enterprise_service.update_enterprise(enterprise, enterprise_id)
