from ..database.db import execute_query

class UserRepository:
    def __init__(self):
        pass

    async def get_user_information(self, user: str):
        return await execute_query('user', 'find_one', {'user': user})
