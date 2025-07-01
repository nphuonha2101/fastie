from pydantic import EmailStr, ConfigDict, BaseModel


class UserResponseSchema(BaseModel):
    """
    Schema for user response. Excludes sensitive fields.
    """
    id: int
    name: str
    email: EmailStr
    is_active: int = 1
    avatar: str

    model_config = ConfigDict(from_attributes=True)