from passlib.context import CryptContext
from pydantic import BaseModel, model_validator

from app.user.exceptions import UserNotAuthenticated

PASSWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    username: str
    password: str

    def authenticate(self, plain_password: str) -> "User":
        if bool(PASSWD_CONTEXT.verify(plain_password, self.password)):
            return self
        raise UserNotAuthenticated()


class UserCreate(BaseModel):
    username: str
    password: str

    @model_validator(mode="before")
    def hash_password(cls, values):  # noqa
        if "password" in values:
            values["password"] = PASSWD_CONTEXT.hash(values["password"])
        return values
