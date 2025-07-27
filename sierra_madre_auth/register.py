from sierra_madre_auth.schemas import RegisterUserRequestSchema
from flask import request, jsonify
from sierra_madre_core.errors import HTTPError
from sierra_madre_auth.utils import get_user_by_email
from sierra_madre_auth.models import Users
from sierra_madre_auth.config import AuthConfig
#Register user, must be used with handle_endpoint decorator from sierra_madre_core
def register_user(auth_config: AuthConfig):
    user = RegisterUserRequestSchema.model_validate(request.json)
    auth_config.password_config.validate_password_security_level(user.password)
    if get_user_by_email(user.email):
        raise HTTPError("Email already exists", 400)
    #Verify if password is valid according to the password config
    auth_config.password_config.validate_password_security_level(user.password)
    user = Users(user.email, user.password)
    user.save()
    return jsonify({"message": "User registered successfully"}), 201