from sierra_madre_core.schemas import BaseModel, EmailStr


class RegisterUserRequestSchema(BaseModel):
    email: EmailStr
    password: str

class LoginUserRequestSchema(BaseModel):
    email: EmailStr
    password: str