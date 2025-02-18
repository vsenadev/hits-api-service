import os
import jwt
import datetime
from dotenv import load_dotenv
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

load_dotenv()

class Auth:
    def __init__(self):
        self.secret_key = os.getenv("SECRET_KEY")
        self.security = HTTPBearer()  # Define o esquema de autenticação

    def generate_token(self, user_id: str) -> str:
        """ Gera um token JWT válido por 1 dia """
        expiration = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        payload = {
            "sub": user_id,
            "exp": expiration
        }
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        return token

    def validate_token(self, token: str) -> dict:
        """ Valida o token JWT e retorna o payload """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expirado")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Token inválido")

    def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        """ Extrai e valida o token a partir do cabeçalho Authorization """
        token = credentials.credentials
        payload = self.validate_token(token)
        return payload["sub"]  # Retorna o user_id extraído do token
