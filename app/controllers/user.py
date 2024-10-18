from app.services.user import UserService
from app.utils.http_response import HttpResponse

class UserController:
    def __init__(self):
        self.service = UserService()

    def get_by_username(self, handler, username):
        try:
            user = self.service.get_by_username(username)
            HttpResponse.success(handler, {"user": user.to_dict()})
        except ValueError as e:
            HttpResponse.not_found(handler, str(e))
        except Exception as e:
            HttpResponse.server_error(handler, str(e))

    def create(self, handler, data):
        try:
            user = self.service.create(data)
            HttpResponse.created(handler, {"user": user.to_dict()})
        except ValueError as e:
            HttpResponse.bad_request(handler, str(e))
        except Exception as e:
            HttpResponse.server_error(handler, str(e))