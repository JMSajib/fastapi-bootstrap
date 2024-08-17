from pydantic import BaseModel


class UserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    is_active: bool
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str
