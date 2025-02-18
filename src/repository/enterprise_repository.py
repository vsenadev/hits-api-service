from ..database.db import execute_query


class EnterpriseRepository():
    def __init__(self):
        pass

    async def get_enterprise_by_filter(self, query: dict):
        return await execute_query('enterprise', 'find_one', query, {'name': 0})

    async def create_enterprise(self, enterprise_name: str):
        return await execute_query('enterprise', 'insert_one', {'name': enterprise_name})

    async def update_enterprise(self, enterprise_name: str, filter):
        return await execute_query('enterprise', 'update_one', filter, {'$set': {'name': enterprise_name}})