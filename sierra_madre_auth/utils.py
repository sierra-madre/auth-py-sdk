from sierra_madre_auth.models import Users

def get_user_by_email(email):
    user = Users.query.filter_by(email=email).first()
    return user

def get_user_by_id(user_id):
    """Get user by ID"""
    user = Users.query.filter_by(user_id=user_id).first()
    return user
