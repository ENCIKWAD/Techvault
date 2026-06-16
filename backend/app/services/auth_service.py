from ..data_access.user_repository import UserRepository

class AuthService:
    @staticmethod
    def register(username, email, password):
        user_id = UserRepository.create_user(username, email, password, 'customer')
        return user_id is not None

    @staticmethod
    def login(email, password):
        user = UserRepository.get_user_by_email(email)
        if user and user['password'] == password:
            return user
        return None

    @staticmethod
    def get_user_profile(user_id):
        return UserRepository.get_user_by_id(user_id)
