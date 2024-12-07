from app.modules.users.repositories import UserRepository
from app.modules.common import exceptions

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def get_all_users(self):
        users = self.repository.get_all_users()
        if users is None:
            raise exceptions.UseCaseException(message="Error al obtener todos los usuarios.")
        return [self._user_to_dict(u) for u in users]

    def get_internal_users(self):
        users = self.repository.get_all_users_by_is_internal(is_internal=True)
        if users is None:
            raise exceptions.UseCaseException(message="Error al obtener usuarios internos.")
        return [self._user_to_dict(u) for u in users]

    def get_external_users(self):
        users = self.repository.get_all_users_by_is_internal(is_internal=False)
        if users is None:
            raise exceptions.UseCaseException(message="Error al obtener usuarios externos.")
        return [self._user_to_dict(u) for u in users]

    def _user_to_dict(self, user):
        return {
            "id": user.id,
            "name": user.name,
            "last_name": user.last_name,
            "document_number": user.document_number,
            "email": user.email,
            "gender": user.gender,
            "user_type": user.user_type,
            "is_internal": user.is_internal,
            "dependency": user.dependency,
            "academic_program": user.academic_program,
            "ingress_records": [record.to_dict() for record in user.ingress_records]
        }
