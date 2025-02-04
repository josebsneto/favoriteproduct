from app.exceptions import BaseAppException


class ProductDatabaseError(BaseAppException):
    pass


class ProductNotFoundError(BaseAppException):
    pass


class HttpProductRequesterError(BaseAppException):
    pass
