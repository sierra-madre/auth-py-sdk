from sierra_madre_auth.schemas import LoginUserRequestSchema
from sierra_madre_auth.utils import get_user_by_email, get_user_by_id
from sierra_madre_core.errors import HTTPError
from flask import request, jsonify
from sierra_madre_auth.token import generate_jwt, decode_jwt
from sierra_madre_auth.config import AuthConfig
from datetime import datetime, timedelta
import jwt

def login_user(auth_config: AuthConfig):
    """
    POST /auth/login
    Input: { email, password }
    Output: { access_token, user }
    Side-effect: set refresh token cookie
    """
    user = LoginUserRequestSchema.model_validate(request.json)
    db_user = get_user_by_email(user.email)
    
    if not db_user:
        raise HTTPError("User not found", 404)
    
    if not auth_config.autoconfirm_users and not db_user.confirmed:
        raise HTTPError("User not confirmed", 401)
    
    if not db_user.check_password(user.password):
        raise HTTPError("Invalid password", 401)
    
    # Generate access token (short lived)
    access_token = generate_jwt(
        db_user.user_id, 
        auth_config.password_config.password_hash_key, 
        auth_config.password_config.algorithm, 
        auth_config.token_config.token_expiration_time_minutes
    )
    
    # Generate refresh token (long lived)
    refresh_token = generate_refresh_token(
        db_user.user_id,
        auth_config.password_config.password_hash_key,
        auth_config.password_config.algorithm
    )
    
    # Set refresh token as HTTP-only cookie
    response = jsonify({
        "access_token": access_token,
        "user": {
            "user_id": db_user.user_id,
            "email": db_user.email,
            "confirmed": db_user.confirmed
        }
    })
    
    response.set_cookie(
        'refresh_token',
        refresh_token,
        httponly=True,
        secure=True,  # Set to False in development
        samesite='None',
        max_age=7 * 24 * 60 * 60  # 7 days
    )
    
    return response, 200

def refresh_token(auth_config: AuthConfig):
    """
    POST /auth/refresh
    Input: (vacío)
    Output: { access_token }
    """
    refresh_token = request.cookies.get('refresh_token')
    if not refresh_token:
        raise HTTPError("Refresh token not found", 401)
    
    try:
        # Decode refresh token
        payload = decode_jwt(
            refresh_token, 
            auth_config.password_config.password_hash_key, 
            auth_config.password_config.algorithm
        )
        
        user_id = payload.get("id_user")
        if not user_id:
            raise HTTPError("Invalid refresh token", 401)
        
        # Generate new access token
        access_token = generate_jwt(
            user_id,
            auth_config.password_config.password_hash_key,
            auth_config.password_config.algorithm,
            auth_config.token_config.token_expiration_time_minutes
        )
        
        return jsonify({"access_token": access_token}), 200
        
    except HTTPError:
        raise HTTPError("Invalid refresh token", 401)

def get_current_user(auth_config: AuthConfig):
    """
    GET /auth/me
    Output: { user }
    Solo válido si refresh token sigue activo
    """
    refresh_token = request.cookies.get('refresh_token')
    
    if not refresh_token:
        raise HTTPError("Refresh token not found", 401)
    
    try:
        # Decode refresh token
        payload = decode_jwt(
            refresh_token, 
            auth_config.password_config.password_hash_key, 
            auth_config.password_config.algorithm
        )
        
        user_id = payload.get("id_user")
        if not user_id:
            raise HTTPError("Invalid refresh token", 401)
        
        # Get user from database
        db_user = get_user_by_id(user_id)
        if not db_user:
            raise HTTPError("User not found", 404)
        
        return jsonify({
            "user": {
                "user_id": db_user.user_id,
                "email": db_user.email,
                "confirmed": db_user.confirmed
            }
        }), 200
        
    except HTTPError:
        raise HTTPError("Invalid refresh token", 401)

def logout_user():
    """
    POST /auth/logout
    Limpia el refresh token
    """
    response = jsonify({"message": "Logged out successfully"})
    response.delete_cookie('refresh_token')
    return response, 200

def generate_refresh_token(user_id: str, secret_key: str, algorithm: str) -> str:
    """Generate a long-lived refresh token"""
    payload = {
        "id_user": user_id,
        "timestamp": datetime.utcnow().isoformat(),
        "exp": datetime.utcnow() + timedelta(days=7),  # 7 days
        "type": "refresh"
    }
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token

