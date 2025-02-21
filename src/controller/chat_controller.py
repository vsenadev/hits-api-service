from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import List
from ..service.chat_service import ChatService

router = APIRouter()
chat_service = ChatService()

# Modelo para validar os dados do frontend
class ChatRequest(BaseModel):
    empresa: str
    question: str
    chat_history: List[dict]

@router.post("")
async def chat(request: ChatRequest = Body(...)):
    """
    Processa a pergunta do usuário e retorna a resposta da IA.

    - `empresa`: Nome da empresa selecionada
    - `question`: Pergunta do usuário
    - `chat_history`: Histórico do chat (lista de mensagens anteriores)
    """
    try:
        response = await chat_service.process_chat(request.empresa, request.question, request.chat_history)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
