import logging
import sys
from functools import lru_cache
from pathlib import Path

from loguru import logger as loguru_logger

from src.common.context import x_request_content
from src.config import settings


def _filter(record):
    record.update({"traceid": x_request_content.get("_x_request_id")})
    return True


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class CustomizeLogger:
    _logger = loguru_logger
    # 阻止日志向上传播
    _logger.propagate = False

    # 移除默认控制台输出
    _logger.remove()

    _log_format = settings.LOG_FORMAT
    _log_level = settings.LOG_LEVEL

    @classmethod
    def log(cls):
        cls._logger.add(sys.stdout, format=cls._log_format, level=cls._log_level, enqueue=True, filter=_filter)
        loggers = (logging.getLogger(name) for name in logging.root.manager.loggerDict if name.startswith("uvicorn"))

        for uvicorn_logger in loggers:
            uvicorn_logger.handlers = []

        intercept_handler = InterceptHandler()
        logging.getLogger("uvicorn.error").addHandler(intercept_handler)
        logging.getLogger("uvicorn.access").addHandler(intercept_handler)

        return cls._logger.bind()


@lru_cache()
def get_logger():
    return CustomizeLogger.log()


logger = get_logger()
