import uuid

from sierra_madre_core.models.abstract_models import db, ModelTimeStamp
from sierra_madre_auth.password import hash_password, verify_password

class Users(ModelTimeStamp):
    __tablename__ = "users"
    user_id = db.Column(db.String(255), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, email, password):
        self.email = email
        self.password = hash_password(password)

    def check_password(self, password):
        return verify_password(password, self.password)

