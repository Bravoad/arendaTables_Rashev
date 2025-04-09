import logging
import sys
from logging.handlers import RotatingFileHandler

LOG_LEVEL = logging.DEBUG
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FILE = "app.log"


def setup_logger(name: str = None, log_file: str = None) -> logging.Logger:
    """
    Создает и возвращает настроенный логгер.

    Аргументы:
      name: имя логгера, если None используется корневой логгер.
      log_file: путь до файла лога. Если указан, будет использован обработчик RotatingFileHandler.
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    if logger.hasHandlers():
        return logger

    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(LOG_LEVEL)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if log_file or LOG_FILE:
        file_handler = RotatingFileHandler(log_file or LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=5)
        file_handler.setLevel(LOG_LEVEL)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


logger = setup_logger("app")

if __name__ == "__main__":
    logger.debug("Debug сообщение: тестовая отладочная информация")
    logger.info("Info сообщение: информативное сообщение")
    logger.warning("Warning сообщение: предупреждение")
    logger.error("Error сообщение: ошибка")
    logger.critical("Critical сообщение: критическая ошибка")
