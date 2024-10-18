from app.models.user import User
from app.utils.validator import Validator

class UserService:
    @staticmethod
    @staticmethod
    def get_by_username(username):
        user = User.get_by_username(username)
        if not user:
            raise ValueError(f"User with username {username} not found")
        return user
    
    @staticmethod
    def create(data):
        errors = Validator.validate_user(data)
        if errors:
            raise ValueError(errors)
        
        return User.create(data['username'], data['password'])
