import logging
from app.modules.users import services
from app.modules.common import interfaces, utils

class UserInternalListView(interfaces.APIView):
    def get(self):
        try:
            user_service = services.UserService()
            internal_users = user_service.get_internal_users()
            return utils.Response({"users": internal_users}, status=200)
        except Exception as e:
            logging.error(f"Error processing request: {e}")
            return utils.Response({"message": str(e)}, status=500)


class UserExternalListView(interfaces.APIView):
    def get(self):
        try:
            user_service = services.UserService()
            external_users = user_service.get_external_users()
            return utils.Response({"users": external_users}, status=200)
        except Exception as e:
            logging.error(f"Error processing request: {e}")
            return utils.Response({"message": str(e)}, status=500)