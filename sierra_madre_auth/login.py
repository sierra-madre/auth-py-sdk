from sierra_madre_auth.schemas import LoginUserRequestSchema
from sierra_madre_auth.utils import get_user_by_email
from sierra_madre_core.errors import HTTPError
from flask import request, jsonify
from sierra_madre_auth.token import generate_jwt
from sierra_madre_auth.config import AuthConfig

def login_user(auth_config: AuthConfig):
    user = LoginUserRequestSchema.model_validate(request.json)
    db_user = get_user_by_email(user.email)
    if not db_user:
        raise HTTPError("User not found", 404)
    if not db_user.check_password(user.password):
        raise HTTPError("Invalid password", 401)
    token = generate_jwt(db_user.user_id, auth_config)
    return jsonify({"message": "User logged in successfully", "token": token}), 200