from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str # The user provides a plain-text password on creation

class UserInDB(UserBase):
    id: str
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True
