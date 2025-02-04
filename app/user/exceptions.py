from app.exceptions import BaseAppException


class UserNotFoundError(BaseAppException):
    pass


class UserNotAuthenticated(BaseAppException):
    pass


class UserAlreadyExistError(BaseAppException):
    pass


class UserDatabaseError(BaseAppException):
    pass
