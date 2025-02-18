import os
import urllib
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

client = None
db = None
load_dotenv()
async def connect_to_mongo():
    global client, db
    raw_uri = os.getenv('DATABASE_URL')

    if "@" in raw_uri:
        scheme, rest = raw_uri.split("://", 1)
        creds, host = rest.split("@", 1)
        user, password = creds.split(":", 1)

        # Escapando usuário e senha corretamente
        user_escaped = urllib.parse.quote_plus(user)
        password_escaped = urllib.parse.quote_plus(password)

        # Montando a URI escapada
        escaped_uri = f"{scheme}://{user_escaped}:{password_escaped}@{host}"
    else:
        escaped_uri = raw_uri

    client = AsyncIOMotorClient(escaped_uri)
    db = client['hits']
    print("Connected to MongoDB")

async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("Disconnected from MongoDB")

async def execute_query(collection_name, operation, *args, projection=None, **kwargs):
    """Executa uma query no MongoDB de forma assíncrona.

    Args:
        collection_name (str): Nome da coleção no banco de dados.
        operation (str): Operação a ser executada (ex: 'find', 'insert_one', 'update_one', etc.).
        *args: Argumentos posicionais para a operação do MongoDB.
        projection (dict, optional): Campos a serem retornados na consulta (ex: {'campo1': 1, 'campo2': 1}).
        **kwargs: Argumentos nomeados para a operação do MongoDB.

    Returns:
        Resultado da operação MongoDB.
    """
    if db is None:
        raise Exception("Database não conectado. Chame connect_to_mongo primeiro.")

    collection = db[collection_name]

    if not hasattr(collection, operation):
        raise ValueError(f"Operação '{operation}' não é suportada.")

    method = getattr(collection, operation)

    if callable(method):
        if operation == "find":
            cursor = method(*args, **kwargs)
            if projection:
                cursor = cursor.project(projection)
            return await cursor.to_list(length=100)
        elif operation == "find_one" and projection:
            return await method(*args, projection=projection, **kwargs)
        else:
            return await method(*args, **kwargs)
    else:
        raise ValueError(f"Operação '{operation}' não é executável.")
