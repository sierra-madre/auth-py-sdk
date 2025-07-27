from sierra_madre_core.errors import HTTPError



class PasswordConfig:
    def __init__(self, password_hash_key, algorithm="HS256",password_security_level=1, password_min_length=8):
        self.password_hash_key = password_hash_key
        self.algorithm = algorithm
        self.password_security_level = password_security_level
        self.password_min_length = password_min_length

    def validate_password_security_level(self, password):
        #Validate password length
        if len(password) < self.password_min_length:
            raise HTTPError(f"Password must be at least {self.password_min_length} characters long", 400)
        
        #Validate password security level
        #Level 1 no minimum requirements
        if self.password_security_level == 1:
            pass  # No additional requirements for level 1

        #Level 2 at least one uppercase letter and one lowercase letter
        elif self.password_security_level == 2:
            if not any(char.isupper() for char in password):
                raise HTTPError("Password must contain at least one uppercase letter", 400)
            if not any(char.islower() for char in password):
                raise HTTPError("Password must contain at least one lowercase letter", 400)

        #Level 3 at least one lowercase letter, one uppercase letter and one number
        elif self.password_security_level == 3:
            if not any(char.islower() for char in password):
                raise HTTPError("Password must contain at least one lowercase letter", 400)
            if not any(char.isupper() for char in password):
                raise HTTPError("Password must contain at least one uppercase letter", 400)
            if not any(char.isdigit() for char in password):
                raise HTTPError("Password must contain at least one number", 400)

        #Level 4 at least one lowercase letter, one uppercase letter, one number and one special character
        elif self.password_security_level == 4:
            if not any(char.islower() for char in password):
                raise HTTPError("Password must contain at least one lowercase letter", 400)
            if not any(char.isupper() for char in password):
                raise HTTPError("Password must contain at least one uppercase letter", 400)
            if not any(char.isdigit() for char in password):
                raise HTTPError("Password must contain at least one number", 400)
            if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>?" for char in password):
                raise HTTPError("Password must contain at least one special character", 400)


class TokenConfig:
    def __init__(self, token_expiration_time_minutes=60):
        self.token_expiration_time_minutes = token_expiration_time_minutes


class AuthConfig:
    def __init__(self, password_hash_key, algorithm="HS256", token_expiration_time_minutes=60, password_security_level=1, password_min_length=8, autoconfirm_users=False):
        self.password_config = PasswordConfig(password_hash_key, algorithm, password_security_level, password_min_length)
        self.token_config = TokenConfig(token_expiration_time_minutes)
        self.autoconfirm_users = autoconfirm_users

    def update_password_security_level(self, password_security_level):
        self.password_config.password_security_level = password_security_level

    def update_password_min_length(self, password_min_length):
        self.password_config.password_min_length = password_min_length

    def update_token_expiration_time_minutes(self, token_expiration_time_minutes):
        self.token_config.token_expiration_time_minutes = token_expiration_time_minutes


def get_auth_config(config_dict: dict) -> AuthConfig:
    return AuthConfig(**config_dict)
