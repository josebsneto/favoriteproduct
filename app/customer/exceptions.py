from app.exceptions import BaseAppException


class CustomerAlreadyExistError(BaseAppException):
    pass


class CustomerNotFoundError(BaseAppException):
    pass


class CustomerNotUpdatedError(BaseAppException):
    pass


class CustomerNotDeletedError(BaseAppException):
    pass


class CustomerDatabaseError(BaseAppException):
    pass


class CustomerServiceGetProductsError(BaseAppException):
    pass
