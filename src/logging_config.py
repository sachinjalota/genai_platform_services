import sys
import logging
from pathlib import Path
from src.config import LOG_PATH, LOG_LEVEL


class Logger:
    _default_logger = None

    @staticmethod
    def create_logger(name: str) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(LOG_LEVEL.upper())

        if logger.hasHandlers():
            logger.handlers.clear()

        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(LOG_LEVEL.upper())
        formatter = logging.Formatter("[{levelname}] [{asctime}] [{name}] [{lineno}] {message}", style="{")
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        log_file_path = Path(LOG_PATH).resolve()
        log_file_path.parent.mkdir(parents=True, exist_ok=True)

        fh = logging.FileHandler(log_file_path)
        fh.setLevel(LOG_LEVEL.upper())
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        return logger

    @classmethod
    def _get_default_logger(cls) -> logging.Logger:
        if cls._default_logger is None:
            cls._default_logger = cls.create_logger("defaultLogger")
        return cls._default_logger

    @classmethod
    def debug(cls, message: str, logger_name: str = None):
        logger = cls.create_logger(logger_name) if logger_name else cls._get_default_logger()
        logger.debug(message)

    @classmethod
    def info(cls, message: str, logger_name: str = None):
        logger = cls.create_logger(logger_name) if logger_name else cls._get_default_logger()
        logger.info(message)

    @classmethod
    def warning(cls, message: str, logger_name: str = None):
        logger = cls.create_logger(logger_name) if logger_name else cls._get_default_logger()
        logger.warning(message)

    @classmethod
    def error(cls, message: str, logger_name: str = None):
        logger = cls.create_logger(logger_name) if logger_name else cls._get_default_logger()
        logger.error(message)

    @classmethod
    def critical(cls, message: str, logger_name: str = None):
        logger = cls.create_logger(logger_name) if logger_name else cls._get_default_logger()
        logger.critical(message)