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
    if not auth_config.autoconfirm_users and not db_user.confirmed:
        raise HTTPError("User not confirmed", 401)
    if not db_user.check_password(user.password):
        raise HTTPError("Invalid password", 401)
    token = generate_jwt(db_user.user_id, auth_config.password_config.password_hash_key, auth_config.password_config.algorithm, auth_config.token_config.token_expiration_time_minutes)
    return jsonify({"message": "User logged in successfully", "token": token}), 200