from pydantic import BaseModel, EmailStr, ConfigDict


class UserBaseSchema(BaseModel):
    name: str
    email: EmailStr
    is_active: int = 1
    avatar: str

    model_config = ConfigDict(from_attributes=True)