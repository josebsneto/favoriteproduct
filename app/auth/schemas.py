from pydantic import BaseModel

from app import settings


class Token(BaseModel):
    access_token: str
    token_type: str = settings.ACCESS_TOKEN_TYPE.lower()
