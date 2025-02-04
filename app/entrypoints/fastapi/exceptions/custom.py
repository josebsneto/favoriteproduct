from app.exceptions import BaseAppException


class AppHttpException(BaseAppException):
    pass


class AppRequestValidationHttpException(BaseAppException):
    pass
