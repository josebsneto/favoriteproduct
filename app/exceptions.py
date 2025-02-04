from app import logging

logger = logging.get_logger(__name__)


class BaseAppException(Exception):
    def __init__(self, msg: str = ""):
        self.msg = msg
        super().__init__(self.msg)

        logger.error(f"{self.__class__.__name__} | {str(self.msg)}")

    def __str__(self):
        return str(self.msg)
