import json
from datetime import datetime

from enums import BookStatus
from validation import validation_id, validation_year, validation_status


class Book:
    """ Класс книги """
    def __init__(self, title: str, author: str, year: int):
        """
        Конструктор класса книги
        :param title: название книги
        :param author: автор
        :param year: год издания
        :raises ValidationError:  Ошибка при указании года выпуска книги
        """
        self._id = 0
        self._title = title
        self._author = author
        self._year = 0
        self.year = year
        self._status: bool = False

    @property
    def id(self) -> int:
        """ Идентификатор книги """
        return self._id

    @id.setter
    def id(self, val: int):
        """
        Идентификатор книги
        :param val:
        :raises ValidationError: Ошибка проверки корректности идентификатора
        """
        self._id = validation_id(val)

    @property
    def title(self) -> str:
        """ Название книги """
        return self._title

    @title.setter
    def title(self, val: str):
        """ Название книги """
        self._title = val

    @property
    def author(self) -> str:
        """ Автор """
        return self._author

    @author.setter
    def author(self, val: str):
        """ Автор """
        self._author = val

    @property
    def year(self) -> int:
        """ Год издания """
        return self._year

    @year.setter
    def year(self, val: int):
        """
        Год издания
        :param val:
        :raises ValidationError: Ошибка при указании года выпуска книги
        """
        self._year = validation_year(val)

    @property
    def status(self) -> BookStatus:
        """
        Статус книги
        :return: если True, то 'в наличии', иначе 'выдана'
        """
        return BookStatus.get_status(self._status)

    @status.setter
    def status(self, val: BookStatus | bool):
        """
        Статус книги
        :param val: если True, то 'в наличии', иначе 'выдана'
        :raises ValidationError: Статус должен быть логическим значением
        """
        self._status = validation_status(val)

    @property
    def is_available(self) -> bool:
        """ Доступна ли книга """
        return self._status

    def to_dict(self):
        """ Преобразование данных в словарь """
        return self.__dict__

    def to_json(self):
        """ Сериализация данных в JSON """
        return json.dumps(self.__dict__)

    def __str__(self):
        _id = f"id {self._id}, " if self._id > 0 else ""
        return (f"Book {_id}titled '{self._title}' of the author {self._author} {self._year} edition, "
                f"status {self.status.to_str()}")

    def __repr__(self):
        return f"Book('{self._title}', '{self._author}', {self._year})"
