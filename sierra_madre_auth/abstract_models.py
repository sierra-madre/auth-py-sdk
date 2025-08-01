from sierra_madre_core.models.abstract_models import db, Model, ModelTimeStamp, ModelTimeStampSoftDelete
from flask import request
from datetime import datetime

class UserModel(Model):
    __abstract__ = True
    
    created_by = db.Column(db.String(255), nullable=True)
    updated_by = db.Column(db.String(255), nullable=True)
    

    def __init__(self):
        super().__init__()

    def save(self, commit=True):
        if hasattr(request, 'user_id') and request.user_id:
            self.created_by = str(request.user_id)
        super().save(commit)

    def update(self, commit=True):
        if hasattr(request, 'user_id') and request.user_id:
            self.updated_by = str(request.user_id)
        
        super().update(commit)

    def delete(self, commit=True):
        super().delete(commit)


class UserModelTimeStamp(ModelTimeStamp):
    __abstract__ = True
    
    created_by = db.Column(db.String(255), nullable=True)
    updated_by = db.Column(db.String(255), nullable=True)
    deleted_by = db.Column(db.String(255), nullable=True)

    def __init__(self):
        super().__init__()

    def save(self, commit=True):
        if hasattr(request, 'user_id') and request.user_id:
            self.created_by = str(request.user_id)
        super().save(commit)

    def update(self, commit=True):
        if hasattr(request, 'user_id') and request.user_id:
            self.updated_by = str(request.user_id)
        
        super().update(commit)

    def delete(self, commit=True):
        super().delete(commit)


class UserModelTimeStampSoftDelete(ModelTimeStampSoftDelete):
    __abstract__ = True
    
    created_by = db.Column(db.String(255), nullable=True)
    updated_by = db.Column(db.String(255), nullable=True)
    deleted_by = db.Column(db.String(255), nullable=True)

    def __init__(self):
        super().__init__()

    def save(self, commit=True):
        if hasattr(request, 'user_id') and request.user_id:
            self.created_by = str(request.user_id)
        
        super().save(commit)

    def update(self, commit=True):
        if hasattr(request, 'user_id') and request.user_id:
            self.updated_by = str(request.user_id)
        
        super().update(commit)

    def delete(self, commit=True):
        if hasattr(request, 'user_id') and request.user_id:
            self.deleted_by = str(request.user_id)
        super().delete(commit)

    def restore(self, commit=True):
        if hasattr(request, 'user_id') and request.user_id:
            self.updated_by = str(request.user_id)
        
        super().restore(commit)
    
    
    
    