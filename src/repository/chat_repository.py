from ..database.db import execute_query

class ChatRepository:
    def __init__(self):
        pass

    async def save_chat(self, chat_data: dict):
        """
        Salva o histórico do chat no banco de dados.
        """
        return await execute_query("chat", "insert_one", chat_data)
