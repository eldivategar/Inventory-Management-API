import base64
from app.utils.http_response import HttpResponse
from app.models.user import User

class AuthMiddleware:
    @staticmethod
    def authenticate(handler):
        auth_header = handler.headers.get('Authorization')
        
        if not auth_header:
            HttpResponse.unauthorized(handler)
            return False

        try:
            auth_type, auth_string = auth_header.split(' ')
            if auth_type.lower() != 'basic':
                HttpResponse.unauthorized(handler)
                return False

            credentials = base64.b64decode(auth_string).decode('utf-8')
            username, password = credentials.split(':')

            if User.authenticate(username, password):
                return True
            
            HttpResponse.unauthorized(handler, "Invalid credentials")
            return False

        except Exception:
            HttpResponse.unauthorized(handler)
            return False