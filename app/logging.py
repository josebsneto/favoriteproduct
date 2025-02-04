import logging

from app.settings import DEBUG


def setup_logger(logger: logging.Logger) -> logging.Logger:
    level = logging.DEBUG if DEBUG else logging.INFO
    logger.setLevel(level)

    fmt = logging.Formatter(
        "[%(asctime)s " "| %(levelname)s " "| %(name)s " "| %(message)s",
    )

    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    logger.addHandler(sh)
    return logger


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    return setup_logger(logger)
