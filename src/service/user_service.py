from fastapi import HTTPException
from ..auth.auth import Auth
from ..model.user_model import User
from ..utils.cryptography_utils import CryptographyUtils
from ..repository.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.crypto = CryptographyUtils()
        self.repository = UserRepository()
        self.auth = Auth()

    async def validate_user(self, user: User):
        user_information = await self.repository.get_user_information(user.user)

        if user_information:
            decrypted_password = self.crypto.decrypt(user_information['password'])

            if decrypted_password == user.password:
                return { 'token': self.auth.generate_token(str(user_information['_id']))}
            elif decrypted_password != user.password:
                return HTTPException(status_code=401, detail="Credenciais inválidas")

        elif user_information is None:
            return HTTPException(status_code=404, detail="Usuário não encontrado")
