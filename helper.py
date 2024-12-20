import logging
import os
from pathlib import Path



def get_root_path():
    """ Возвращает корневой путь модуля """
    return Path(__file__).resolve().parent


class Logger:
    """ Класс логгера """
    LOGGER_FILENAME = get_root_path() / "library.log"

    _loggers = {}
    logger_level = logging.ERROR

    @classmethod
    def get_logger(cls, logger_name, logger_level: int = logger_level):
        """
        Возвращает логгер.
        :param logger_name: Наименование логгера.
        :param logger_level: Уровень отображения информации логеера.
        :return:
        """
        return cls._loggers.setdefault(logger_name, cls._create_logger(logger_name, logger_level))

    @classmethod
    def _create_logger(cls, logger_name, logger_level: int = logger_level):
        """
        Создаёт логгер с указанным именем.
        :param logger_name: Наименование логгера.
        :param logger_level: Уровень отображения информации логгера.
        :return:
        """

        logger = logging.getLogger(logger_name)
        logger_handler = logging.FileHandler(cls.LOGGER_FILENAME, mode='a', encoding='utf-8')
        logger_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
        logger_handler.setFormatter(logger_formatter)
        logger.addHandler(logger_handler)

        logger.setLevel(logger_level)
        return logger


def clear_display():
    """ Очищает дисплей. """
    os.system("cls")


def print_awaiting_message(msg):
    """ Вывод ожидающего сообщения. """
    print(msg)
    input("press any key...")
