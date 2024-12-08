
import logging
from app.config import bcrypt
from app.modules.common.exceptions import UseCaseException
from app.modules.common.enums import UserType
from app.modules.users import repositories
from app.modules.user_recognition.models.user import User


class UserInternalAuth:

    def __init__(self):
        self.repository = repositories.UserRepository()

    def auth_user_internal(self, email: str, password: str) -> User:
        try:
            print(email, password)
            user = self.repository.get_user_by_email(email=email)
            if not user:
                logging.error(f"Usuario no encontrado para el email: {email}")
                raise UseCaseException(message="El email o contraseña son incorrectos")

            password_verifi = bcrypt.check_password_hash(pw_hash=user.password, password=password)
            if not password_verifi:
                logging.error(f"Contraseña incorrecta para el email: {email}")
                raise UseCaseException(message="El email o contraseña son incorrectos")

            if user.user_type.lower() not in [type.value.lower() for type in UserType]:
                raise UseCaseException(message="Tipo de usuario no autorizado")
            return user

        except Exception as e:
            raise UseCaseException(message=str(e))
