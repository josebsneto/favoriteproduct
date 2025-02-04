from app.exceptions import BaseAppException


class AuthExpiredTokenError(BaseAppException):
    pass


class AuthTokenExpNotFoundError(BaseAppException):
    pass


class AuthInvalidTokenError(BaseAppException):
    pass
