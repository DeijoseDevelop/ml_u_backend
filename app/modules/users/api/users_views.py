import logging

import flask
from app.modules.users import controllers, services
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
        
        
class UserDeleteView(interfaces.APIView):
    def delete(self, user_id):
        try:
            user_service = services.UserService()
            
            logging.debug(f"Se recibió user_id: {user_id}")

            if not isinstance(user_id, int):
                logging.error(f"El user_id recibido no es un entero: {user_id}")
                return utils.Response({"message": "ID de usuario inválido"}, status=utils.Status.BAD_REQUEST_400)
            
            user = user_service.get_user_by_id(user_id=user_id)
            if not user:
                return utils.Response({"message": "Usuario no encontrado"}, status=utils.Status.NOT_FOUND_404)
            
            user_service.delete_user(user=user)
            
            return utils.Response({"message": "Usuario eliminado con exitó"}, status=204)

        except Exception as e:
            logging.error(f"Error inesperado en UserDeleteView: {e}")
            return utils.Response({"message": str(e)}, status=500)
        
        

class UserUpdateView(interfaces.APIView):
    def patch(self, user_id):
        try:
            
            user_data = flask.request.form if flask.request.form else flask.request.json
            user_service = services.UserService()
            user_controler = controllers.UserController(user_service)
            logging.debug(f"Se recibió user_id: {user_id}")
            print("id:", user_id)
            
            if not isinstance(user_id, int):
                logging.error(f"El user_id recibido no es un entero: {user_id}")
                return utils.Response({"message": "ID de usuario inválido"}, status=utils.Status.BAD_REQUEST_400)
            
            
            return user_controler.update_user(user_id=user_id, data=user_data)
        
        except Exception as e:
            logging.error(f"Error processing request: {e}")
            return utils.Response({"message": str(e)}, status=500)

        
        